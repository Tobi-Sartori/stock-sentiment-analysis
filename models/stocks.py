from enum import Enum

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Text, func)
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class MarketEnum(Enum):
    US = "US"
    BR = "BR"
    CRYPTO = "CRYPTO"


MarketType: pgEnum = pgEnum(
    MarketEnum,
    name="market_enum",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)


class DimStocks(Base):
    __tablename__ = "dim_stocks"

    pk_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    symbol = Column(String(6), nullable=False)
    name = Column(String(100), nullable=False)
    market = Column(MarketType, nullable=False)
    company_info = Column(Text, nullable=True)
    dt_created_at = Column(DateTime, default=func.now(), nullable=False)
    dt_updated_at = Column(DateTime, default=func.now(), nullable=False)
    dt_last_analyzed = Column(DateTime, nullable=True)
    dt_last_scraped = Column(DateTime, nullable=True)

    prices = relationship("DimStockPrices", back_populates="stock")


class DimStockPrices(Base):
    __tablename__ = "dim_stock_prices"

    pk_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fk_stock_id = Column(Integer, ForeignKey("dim_stocks.pk_id"), nullable=False)
    symbol = Column(String(6), nullable=False)
    no_trades = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    dt_created_at = Column(DateTime, default=func.now(), nullable=False)

    stock = relationship("DimStocks", back_populates="prices")
