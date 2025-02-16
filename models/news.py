from enum import Enum

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Text, func)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class SourceEnum(Enum):
    NEWS_API = "NEWS_API"
    YAHOO_NEWS = "YAHOO_NEWS"


SourceType: pgEnum = pgEnum(
    SourceEnum,
    name="source_enum",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


class DimNews(Base):
    __tablename__ = "dim_news"

    pk_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    source = Column(SourceType, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    press_veichle = Column(String(255), nullable=False)
    keyword = Column(String(255), nullable=False)
    s3_url = Column(String(255), nullable=False)
    dt_published_at = Column(DateTime, nullable=False)
    dt_created_at = Column(DateTime, default=func.now(), nullable=False)
    dt_updated_at = Column(DateTime, default=func.now(), nullable=False)


class NewsJsonsCatalog(Base):
    __tablename__ = "news_jsons_catalog"

    pk_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    keyword = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    s3_url = Column(String(255), nullable=False)
    dt_created_at = Column(DateTime, default=func.now(), nullable=False)
