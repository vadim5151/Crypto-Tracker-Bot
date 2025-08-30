from datetime import datetime, UTC
from typing import Optional

from sqlalchemy import String, BigInteger, ForeignKey, JSON, text, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

import os
import sys


# Добавляем корневую директорию в путь для импорта настроек
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    event_date: Mapped[str] = mapped_column(String(50))
    event_time: Mapped[str] = mapped_column(String(50))
    currency: Mapped[str] = mapped_column(String(10))
    importance: Mapped[int] = mapped_column(Integer)
    event_name: Mapped[str] = mapped_column(String(500))
    actual: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    forecast: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    previous: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    update_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(UTC) 

    )


class Coin(Base):
    __tablename__ = 'coins'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    rank_type: Mapped[str]
    ticker: Mapped[str] 
    name: Mapped[str]
    price: Mapped[str] 
    market_cup: Mapped[str]
    price_change_24hm: Mapped[str]
    update_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(UTC) 

    )
    

async def create_tables():
    """Создает таблицы в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    """Удаляет все таблицы из базы данных"""
    async with engine.begin() as conn:
        # Удаляем все таблицы, связанные с метаданными Base
        await conn.run_sync(Base.metadata.drop_all)
        print("Все таблицы базы данных успешно удалены")

