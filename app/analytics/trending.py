from collections import Counter
from sqlalchemy import select
from app.models.news_item import NewsItem


async def detect_trends(db):

    result = await db.execute(select(NewsItem))
    items = result.scalars().all()

    tags = []

    for item in items:
        if item.tags:
            tags.extend(item.tags)

    counter = Counter(tags)

    return counter.most_common(10)