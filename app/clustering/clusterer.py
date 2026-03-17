from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import select
from app.models.news_item import NewsItem


SIMILARITY_THRESHOLD = 0.75


async def cluster_news(db):

    result = await db.execute(select(NewsItem))
    articles = result.scalars().all()

    if len(articles) < 2:
        return

    texts = [
        f"{a.title} {a.ai_summary or ''}"
        for a in articles
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(X)

    cluster_id = 0
    visited = set()

    for i in range(len(articles)):

        if i in visited:
            continue

        cluster_id += 1

        articles[i].cluster_id = cluster_id
        articles[i].is_primary = True

        visited.add(i)

        for j in range(i + 1, len(articles)):

            if similarity_matrix[i][j] > SIMILARITY_THRESHOLD:

                articles[j].cluster_id = cluster_id
                articles[j].is_primary = False
                visited.add(j)

    await db.commit()