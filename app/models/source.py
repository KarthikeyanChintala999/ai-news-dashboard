from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from app.database import Base


class Source(Base):

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    feed_url = Column(Text)

    fetch_method = Column(Text, default="rss")
    fetch_interval_minutes = Column(Integer, default=120)

    last_etag = Column(Text)
    last_modified = Column(Text)

    is_active = Column(Boolean, default=True)

    authority_score = Column(Float, default=0.5)