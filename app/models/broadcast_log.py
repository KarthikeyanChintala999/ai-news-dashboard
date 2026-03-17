from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.types import TIMESTAMP, JSON
from sqlalchemy.sql import func
from app.database import Base


class BroadcastLog(Base):

    __tablename__ = "broadcast_logs"

    id = Column(Integer, primary_key=True)

    favorite_id = Column(Integer, ForeignKey("favorites.id"))

    platform = Column(Text)

    status = Column(Text)

    platform_response = Column(JSON)

    timestamp = Column(TIMESTAMP, server_default=func.now())