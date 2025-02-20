from enum import Enum

from sqlalchemy import (Column, DateTime, Integer, String, Text, func)
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from models.base import Base

class DimNews(Base):
    __tablename__ = "dim_news"

    pk_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    press_veichle = Column(String(255), nullable=False)
    keyword = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    s3_url = Column(String(255), nullable=False)
    dt_published_at = Column(DateTime, nullable=False)
    dt_created_at = Column(DateTime, default=func.now(), nullable=False)
    dt_updated_at = Column(DateTime, default=func.now(), nullable=False)
