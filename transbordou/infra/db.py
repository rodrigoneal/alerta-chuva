import os
from functools import lru_cache

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from transbordou.domain.domain import Base

connection_pool_size = min(32, os.cpu_count() + 4)


class Settings:
    asyncpg_url: str = os.getenv("SQL_URL") or "sqlite+aiosqlite:///:memory:"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


engine = create_async_engine(
    settings.asyncpg_url, pool_size=connection_pool_size, max_overflow=0
)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
