
import asyncio
import os
import api.gigachat_api,api.kandinsky
from aiogram import Bot, Dispatcher
from aiohttp import ClientSession
from dotenv import load_dotenv

from services import init_db
from handlers import register_all_handlers

from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis
import logging
import handlers.common
load_dotenv()
TELEGRAM_TOKEN = "8512556585:AAFu5gRiT4AGi1vQrBhBLVuZoi3sU0a_b3k"
giga = api.gigachat_api.GigaChatAPI("MDE5YTdkODktZWQzYi03ZGMwLTliZjQtYmJiMjg0YWUzZmRjOmFjNDdkMzkxLWI5YmItNDI1ZC1iZTdjLWQ1OTZiMWYzMGZhOA==")
kandinksy = api.kandinsky.AsyncFusionBrainAPI('EF310F8E5AD822635A24D0D9E083C9BF', 'E3634B76FB7974D63D7A5BB04B4704E7')
session: ClientSession | None = None
handlers.common.kandinsky = kandinksy
handlers.common.giga = kandinksy

redis_conn = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    password=None,
    decode_responses=True
)

storage = RedisStorage(redis=redis_conn)


async def main():
    global session

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=storage)
    bot = Bot(token=TELEGRAM_TOKEN)

    session = ClientSession()

    await register_all_handlers(dp)
    await init_db()

    try:
        await dp.start_polling(bot)
    finally:
        if not session.closed:
            await session.close()
        await redis_conn.aclose()
        await storage.close()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped manually")
