import datetime
import os

import aiosqlite as aiosql
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DB_PATH")

async def init_db():
    async with aiosql.connect(db_path) as db:
        async with db.execute("""CREATE TABLE IF NOT EXISTS history(id INTEGER,
        user_id INTEGER,
        image TEXT,
        text TEXT,
        created_at TEXT)"""):
            await db.commit()

async def create_post(user_id: int, image=None, text=None):
    async with aiosql.connect(db_path) as db:
        await db.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?)", (await get_new_post_id(user_id), user_id, image, text, (datetime.datetime.now(datetime.UTC)).strftime('%d/%m/%y %H:%M:%S')))
        await db.commit()

async def get_new_post_id(user_id: int):
    async with aiosql.connect(db_path) as db:
        async with db.execute("SELECT COUNT(*) FROM history WHERE user_id = ?", (user_id,)) as cursor:
            count = await cursor.fetchone()
            return count[0] + 1

async def get_posts_id(user_id):
    async with aiosql.connect(db_path) as db:
        async with db.execute("SELECT id FROM history WHERE user_id = ?", (user_id,)) as cursor:
            info = await cursor.fetchall()
            return info

async def get_post(user_id, _id):
    async with aiosql.connect(db_path) as db:
        async with db.execute("SELECT image, text FROM history WHERE user_id = ? AND id = ?", (user_id, _id)) as cursor:
            row = await cursor.fetchone()
            image, text = row
            return image, text

async def add_text(user_id: int, info: str):
    async with aiosql.connect(db_path) as db:
        async with db.execute("UPDATE history SET text = ? WHERE user_id = ? AND id = ?", (info, user_id)):
            await db.commit()

async def add_image(user_id: int, info: str):
    async with aiosql.connect(db_path) as db:
        async with db.execute("UPDATE history SET image = ? WHERE user_id = ? AND id = ?", (info, user_id)):
            await db.commit()

async def add_created_at(user_id: int, info: str):
    async with aiosql.connect(db_path) as db:
        async with db.execute("UPDATE history SET created_at = ? WHERE user_id = ? AND id = ?", (info, user_id)):
            await db.commit()