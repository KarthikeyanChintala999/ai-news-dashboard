import feedparser
import hashlib
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.article import RawArticle


async def ingest_rss_feed(db: AsyncSession, source):

    feed = feedparser.parse(source.feed_url)
    print(f"🌐 Fetching RSS: {source.feed_url}")
    print(f"📰 Entries found: {len(feed.entries)}")

    articles_to_insert = []

    for entry in feed.entries[:50]:

        url = entry.link
        title = entry.title

        url_hash = hashlib.sha256(url.encode()).hexdigest()

        published = None
        if "published_parsed" in entry:
            published = datetime(*entry.published_parsed[:6])

        articles_to_insert.append({
            "url_hash": url_hash,
            "source_id": source.id,
            "title": title,
            "summary": entry.get("summary"),
            "raw_url": url,
            "published_at": published,
            "processed": False  # ✅ KEEP THIS
        })

    if not articles_to_insert:
        return

    stmt = insert(RawArticle).values(articles_to_insert)

    stmt = stmt.on_conflict_do_nothing(
        index_elements=["url_hash"]
    )

    result = await db.execute(stmt)

    # ✅ DEBUG: HOW MANY INSERTED
    print(f"✅ Insert attempted: {len(articles_to_insert)}")

    await db.commit()

    # ✅ FORCE VISIBILITY (CRITICAL FIX)
    await db.flush()