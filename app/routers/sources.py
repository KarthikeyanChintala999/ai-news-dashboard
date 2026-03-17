from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.source import Source
from app.ingestion.source_runner import run_ingestion

router = APIRouter(prefix="/sources")


@router.post("/seed")
async def seed_sources(db: AsyncSession = Depends(get_db)):

    sources_data = [
        {
            "name": "OpenAI Blog",
            "url": "https://openai.com",
            "feed_url": "https://openai.com/blog/rss",
            "fetch_method": "rss",
        },
        {
            "name": "HackerNews",
            "url": "https://news.ycombinator.com",
            "feed_url": "https://hnrss.org/frontpage",
            "fetch_method": "rss",
        },
        {
            "name": "arXiv AI",
            "url": "https://arxiv.org",
            "feed_url": "https://export.arxiv.org/rss/cs.AI",
            "fetch_method": "rss",
        },
    ]

    added = 0

    for s in sources_data:
        existing = await db.execute(
            select(Source).where(Source.feed_url == s["feed_url"])
        )

        if not existing.scalar():
            db.add(Source(**s))
            added += 1

    await db.commit()

    # 🚀 FORCE ingestion immediately after seeding
    await run_ingestion(db)

    return {
        "status": f"{added} new sources added and ingestion triggered"
    }