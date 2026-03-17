from sqlalchemy import select
from app.models.news_item import NewsItem


async def generate_newsletter(db):

    result = await db.execute(
        select(NewsItem)
        .where(NewsItem.is_primary == True)
        .order_by(NewsItem.created_at.desc())
    )

    stories = result.scalars().all()

    print(f"📰 Found {len(stories)} news items for newsletter")

    if not stories:
        return "⚠️ No news available yet. Please wait..."

    newsletter = "🧠 AI Daily Digest\n\n"

    for s in stories[:10]:

        newsletter += f"""🔥 {s.title}

{s.tldr_quick or s.ai_summary or "No summary available"}

Read more:
{s.url}

"""

    return newsletter