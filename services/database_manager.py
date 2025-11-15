import os

import aiosqlite as aiosql
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DB_PATH")

async def init_db():
    async with aiosql.connect(db_path) as db:
        async with db.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        npo_information TEXT)"""):
            await db.commit()


async def create_profile(user_id):
    async with aiosql.connect(db_path) as db:
        async with db.execute ("SELECT 1 FROM users WHERE user_id == ?", (user_id,)) as cursor:
            if not await cursor.fetchone():
                await db.execute("INSERT INTO users VALUES(?, ?)", (user_id, None,))
            await db.commit()

async def add_npo_information(user_id: int, info: str):
    async with aiosql.connect(db_path) as db:
        async with db.execute(f"UPDATE users SET npo_information = ? WHERE user_id = ?", (info, user_id)):
            await db.commit()

async def get_npo_information(user_id: int):
    async with aiosql.connect(db_path) as db:
        async with db.execute(f"SELECT npo_information FROM users WHERE user_id = ?", (user_id,)) as cursor:
            info = await cursor.fetchone()
            return info[0]