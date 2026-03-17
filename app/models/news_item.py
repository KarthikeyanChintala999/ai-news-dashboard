from sqlalchemy import Column, Integer, Text, Boolean, Float, ForeignKey
from sqlalchemy.types import TIMESTAMP, JSON
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base


class NewsItem(Base):

    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True)

    raw_article_id = Column(Integer, ForeignKey("raw_articles.id"))

    source_id = Column(Integer, ForeignKey("sources.id"))

    title = Column(Text, nullable=False)

    ai_summary = Column(Text)

    tldr_quick = Column(Text)

    tldr_technical = Column(Text)

    url = Column(Text, nullable=False)

    published_at = Column(TIMESTAMP)

    impact_score = Column(Float)

    cluster_id = Column(Integer)

    is_primary = Column(Boolean, default=True)

    tags = Column(JSON)

    entities = Column(JSON)

    embedding = Column(JSON)

    created_at = Column(TIMESTAMP, server_default=func.now())