from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import (AsyncEngine, async_sessionmaker,
                                    create_async_engine)

from transbordou.coletar import coletar
from transbordou.domain.domain import Base
from transbordou.domain.repositories.rain_repository import RainRepository

# @pytest.fixture(scope="module")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture
def html_response():
    with open("tests/data/IRAJA.html", "r") as f:
        return f.read()


@pytest.fixture
async def load_database(html_response, chuva_repository):
    dados = coletar(html_response)
    [await chuva_repository.create(dado) for dado in dados]

@pytest.fixture
async def session() -> AsyncEngine:
    Path("test.db").unlink(missing_ok=True)
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield Session()
        Path("test.db").unlink()


@pytest.fixture
async def chuva_repository(session) -> RainRepository:
    return RainRepository(session)
