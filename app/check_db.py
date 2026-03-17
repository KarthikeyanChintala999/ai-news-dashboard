import asyncio
from app.database import AsyncSessionLocal
from sqlalchemy import text

async def check():
    async with AsyncSessionLocal() as db:
        result1 = await db.execute(
            text("SELECT COUNT(*) FROM raw_articles WHERE processed = false")
        )
        result2 = await db.execute(
            text("SELECT COUNT(*) FROM raw_articles WHERE processed IS NULL")
        )

        print("processed = false:", result1.scalar())
        print("processed IS NULL:", result2.scalar())

asyncio.run(check())