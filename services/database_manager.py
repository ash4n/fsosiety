import datetime
import os

import aiosqlite as aiosql
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DB_PATH")

async def init_db():
    async with aiosql.connect(db_path) as db:
        async with db.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        type TEXT,
        input_text TEXT,
        output_text TEXT,
        created_at TEXT
        )"""):
            await db.commit()


async def create_profile(user_id):
    async with aiosql.connect(db_path) as db:
        async with db.execute ("SELECT 1 FROM users WHERE user_id == ?", (user_id,)) as cursor:
            if not await cursor.fetchone():
                await db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", (user_id, (datetime.datetime.now(datetime.UTC)).strftime('%d/%m/%y %H:%M:%S'), "NONE", referrer_id, 0, 0))
            await db.commit()