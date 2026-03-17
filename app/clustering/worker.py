import asyncio
from app.database import AsyncSessionLocal
from app.clustering.clusterer import cluster_news


async def start_clusterer():

    while True:

        async with AsyncSessionLocal() as db:
            await cluster_news(db)

        # run every 15 minutes
        await asyncio.sleep(900)