import os
from functools import lru_cache

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from transbordou.domain.domain import Base



class Settings:
    asyncpg_url: str = os.getenv("SQL_URL") or "sqlite+aiosqlite:///:memory:"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


engine = create_async_engine(settings.asyncpg_url)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)