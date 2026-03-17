import asyncio
from app.database import AsyncSessionLocal
from app.newsletter.generator import generate_newsletter
from app.bot.telegram_bot import send_newsletter


async def newsletter_worker():

    while True:

        async with AsyncSessionLocal() as db:

            newsletter = await generate_newsletter(db)

            if not newsletter:
                print("⚠️ No content available for newsletter")
            else:
                print("📤 Sending newsletter...")
                await asyncio.to_thread(send_newsletter, newsletter)

        await asyncio.sleep(60)