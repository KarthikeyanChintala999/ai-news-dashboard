from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.news_item import NewsItem
from app.search.embeddings import embed_text
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import select

router = APIRouter(prefix="/search")

@router.get("/")
async def semantic_search(query: str, db: AsyncSession = Depends(get_db)):

    query_vector = embed_text(query)

    result = await db.execute(select(NewsItem))
    items = result.scalars().all()

    scores = []

    for item in items:
        if item.embedding:
            sim = cosine_similarity(
                [query_vector],
                [item.embedding]
            )[0][0]

            scores.append((sim, item))

    scores.sort(reverse=True)

    return [item.title for _, item in scores[:10]]