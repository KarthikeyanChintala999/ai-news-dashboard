import json
import asyncio
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.article import RawArticle
from app.models.news_item import NewsItem

from app.processing.summarizer import summarize_article
from app.search.embeddings import embed_text


async def get_embedding(text):
    return await asyncio.to_thread(embed_text, text)


async def process_articles(db):

    print("🧠 Processor running...")

    result = await db.execute(
        select(RawArticle).where(RawArticle.processed == False)
    )

    articles = result.scalars().all()

    print(f"🔍 Found {len(articles)} unprocessed articles")

    for article in articles:
        try:
            content = article.full_text or article.summary or article.title

            if not content:
                article.processed = True
                continue

            # ✅ Proper summarization with fallback
            try:
                summary = await summarize_article(
                    article.title, article.summary or ""
                )
            except Exception as e:
                print(f"⚠️ Summarization failed: {e}")
                summary = article.summary or article.title or "No summary available"

            # ✅ Use actual summary
            ai_summary = summary or article.title

            # 🔹 Dedup check
            existing = await db.execute(
                select(NewsItem).where(NewsItem.url == article.raw_url)
            )

            if existing.scalar():
                article.processed = True
                continue

            # 🔹 Embedding
            embedding = await get_embedding(ai_summary)

            news = NewsItem(
                raw_article_id=article.id,
                source_id=article.source_id,
                title=article.title,
                url=article.raw_url,
                ai_summary=ai_summary,
                tldr_quick=ai_summary[:200],  # short TLDR
                tldr_technical="",
                tags=[],
                impact_score=0.5,
                embedding=embedding,
                is_primary=True
            )

            db.add(news)

            # ✅ mark processed BEFORE commit
            article.processed = True

        except Exception as e:
            print(f"❌ Processing error: {e}")
            article.processed = True

    # ✅ SINGLE COMMIT (VERY IMPORTANT)
    try:
        await db.commit()
        print("✅ Processing committed")
    except IntegrityError:
        await db.rollback()