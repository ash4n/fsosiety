
import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import ClientSession
from dotenv import load_dotenv

from services import init_db
from handlers import register_all_handlers

from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis
import logging

load_dotenv()
TELEGRAM_TOKEN = "8398140480:AAGxkSFUHHw_6XqkEg9O9DzhfTvBbYE3nrg"
session: ClientSession | None = None

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
