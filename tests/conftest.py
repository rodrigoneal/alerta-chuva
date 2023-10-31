import asyncio
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from transbordou.domain.domain import Base
from transbordou.domain.repositories.rain_repository import RainRepository


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def session() -> AsyncEngine:
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield Session()
        Path("test.db").unlink()


@pytest.fixture
async def chuva_repository(session) -> RainRepository:
    return RainRepository(session)
