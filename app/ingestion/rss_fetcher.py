import feedparser
import hashlib
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.news_item import RawArticle
from datetime import datetime


async def fetch_rss_feed(db: AsyncSession, feed_url: str, source_id: int):

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:

        url = entry.link
        title = entry.title

        url_hash = hashlib.sha256(url.encode()).hexdigest()

        article = RawArticle(
            url_hash=url_hash,
            source_id=source_id,
            title=title,
            summary=entry.get("summary"),
            raw_url=url,
            published_at=datetime(*entry.published_parsed[:6])
            if entry.get("published_parsed")
            else None,
        )

        db.add(article)

    await db.commit()