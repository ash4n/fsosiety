import asyncio
import logging
from typing import Optional
from gigachat import GigaChat

logger = logging.getLogger(__name__)

class GigaChatAPI:
    
    def __init__(self, api_token: str, verify_ssl: bool = False):
        """
        Init GigaChat API
        
        Args:
            api_token: GigaChat API tokem
            verify_ssl: Check SSL certificates (false for development)
        """
        self.api_token = api_token
        self.verify_ssl = verify_ssl
        
    async def generate_text(self, request: str, system_prompt: Optional[str] = None) -> str:
        """
        Text generation with GigaChat
        
        Args:
            request: User request
            system_prompt: System prompt (optional)
            
        Returns:
            Generated text
            
        Raises:
            Exception: At API errors
        """
        if not self.api_token:
            logger.warning("GigaChat token not set")
            return "GigaChat token not set"
        
        try:
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{request}"
            else:
                full_prompt = request
            
            result = await asyncio.get_event_loop().run_in_executor(
                None, 
                self._call_gigachat_sync, 
                full_prompt
            )
            
            return result
            
        except Exception as e:
            logger.exception("GigaChat API call failed: %s", e)
            return f"GigaChat API call failed: {str(e)}"
    
    def _call_gigachat_sync(self, prompt: str) -> str:
        """
        Synchronous GigaChat API call
        
        Args:
            prompt: full user request
            
        Returns:
            Generated text
        """
        with GigaChat(credentials=self.api_token, verify_ssl_certs=self.verify_ssl) as giga:
            response = giga.chat(prompt)
            return response.choices[0].message.content

#Example
# async def main():
    
#     api = GigaChatAPI(api_token="")
    
#     response = await api.generate_text("Расскажи о себе в двух словах")
