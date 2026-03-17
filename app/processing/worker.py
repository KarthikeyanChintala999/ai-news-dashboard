import asyncio
from app.database import AsyncSessionLocal
from app.processing.processor import process_articles


async def start_processor():
    await asyncio.sleep(10)

    while True:
        print("🧠 Processor running...")

        async with AsyncSessionLocal() as db:
            await process_articles(db)

        print("😴 Processor sleeping...")
        await asyncio.sleep(300)