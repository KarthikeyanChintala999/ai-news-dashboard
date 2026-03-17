from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from app.database import Base


class RawArticle(Base):

    __tablename__ = "raw_articles"

    id = Column(Integer, primary_key=True)

    url_hash = Column(Text, unique=True, nullable=False)

    source_id = Column(Integer, ForeignKey("sources.id"))

    title = Column(Text, nullable=False)

    summary = Column(Text)

    full_text = Column(Text)

    author = Column(Text)

    published_at = Column(TIMESTAMP)

    raw_url = Column(Text, nullable=False)

    word_count = Column(Integer)

    fetched_at = Column(TIMESTAMP, server_default=func.now())

    processed = Column(Boolean, default=False, nullable=False)