import asyncio
from app.database import AsyncSessionLocal
from app.newsletter.generator import generate_newsletter
from app.bot.telegram_bot import send_newsletter


async def start_scheduler():

    while True:

        print("⏳ Waiting for processing...")
        await asyncio.sleep(30)

        async with AsyncSessionLocal() as db:

            print("📰 Generating newsletter...")
            newsletter = await generate_newsletter(db)

            await send_newsletter(newsletter)

        await asyncio.sleep(3600)