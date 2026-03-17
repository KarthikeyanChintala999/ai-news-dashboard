from sqlalchemy import Column, Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Text, primary_key=True)

    name = Column(Text)

    email = Column(Text, unique=True)

    role = Column(Text, default="user")

    created_at = Column(TIMESTAMP, server_default=func.now())