from sqlalchemy import select
from app.models.source import Source
from app.ingestion.rss_ingestor import ingest_rss_feed


async def run_ingestion(db):

    print("📡 Fetching sources...")

    result = await db.execute(select(Source))
    sources = result.scalars().all()

    print(f"✅ Found {len(sources)} sources")

    for source in sources:

        print(f"➡️ Processing source: {source.name}")

        if source.fetch_method == "rss":
            await ingest_rss_feed(db, source)