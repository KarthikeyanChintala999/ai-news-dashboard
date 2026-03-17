from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)

    user_id = Column(Text, ForeignKey("users.id"))

    news_item_id = Column(Integer, ForeignKey("news_items.id"))

    created_at = Column(TIMESTAMP, server_default=func.now())