import aiohttp
import asyncio
import base64
import json
import time
from typing import Optional

class AsyncFusionBrainAPI:
    def __init__(self, api_key: str, secret_key: str, url: str = 'https://api-key.fusionbrain.ai/'):
        self.URL = url
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self.AUTH_HEADERS)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            raise RuntimeError("Session not initialized. Use async context manager.")
        return self._session

    async def _get_pipeline_id(self) -> str:
        """Get available pipeline ID"""
        async with self.session.get(self.URL + 'key/api/v1/pipelines') as response:
            data = await response.json()
            return data[0]['id']

    async def _start_generation(self, prompt: str, pipeline_id: str, width: int = 1024, height: int = 1024) -> str:
        """Start image generation and return request UUID"""
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        data = aiohttp.FormData()
        data.add_field('pipeline_id', pipeline_id)
        data.add_field('params', json.dumps(params), content_type='application/json')

        async with self.session.post(self.URL + 'key/api/v1/pipeline/run', data=data) as response:
            result = await response.json()
            print(result)
            return result['uuid']

    async def _wait_for_generation(self, request_id: str, attempts: int = 30, delay: int = 5) -> Optional[str]:
        """Wait for generation completion and return base64 image data"""
        for attempt in range(attempts):
            async with self.session.get(self.URL + 'key/api/v1/pipeline/status/' + request_id) as response:
                data = await response.json()
                
                if data['status'] == 'DONE':
                    # Return the first image as base64 string
                    return data['result']['files'][0]
                elif data['status'] == 'FAIL':
                    raise Exception("Image generation failed")
                
            await asyncio.sleep(delay)
        
        raise TimeoutError(f"Generation timeout after {attempts * delay} seconds")

    async def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> str:
        """
        Generate image from prompt and return base64 string
        
        Args:
            prompt: Text description of the image to generate
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            
        Returns:
            Base64 encoded string of the generated image
        """
        pipeline_id = await self._get_pipeline_id()
        request_id = await self._start_generation(prompt, pipeline_id, width, height)
        base64_image = await self._wait_for_generation(request_id)
        
        return base64_image

# Usage example
# async def main():
#     api_key = "EF310F8E5AD822635A24D0D9E083C9BF"
#     secret_key = "E3634B76FB7974D63D7A5BB04B4704E7"
    
#     async with AsyncFusionBrainAPI(api_key, secret_key) as api:
#         try:
#             # Generate image and get base64 string
#             base64_image = await api.generate_image(
#                 "Homeless human with cup of tea at background, negative atmosphere"
#             )
            
#             # You can now use the base64 string as needed
#             print(f"Generated image (base64 length): {len(base64_image)}")
            
#             # Example: Save to file if needed
#             # image_data = base64.b64decode(base64_image)
#             # with open("generated_image.png", "wb") as f:
#             #     f.write(image_data)
            
#         except Exception as e:
#             print(f"Error: {e}")

