from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
