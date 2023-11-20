import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from alerta_chuva.coletar import coletar
from alerta_chuva.domain.model import Base
from alerta_chuva.domain.repositories.rain_repository import RainRepository

# @pytest.fixture(scope="module")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture
def html_response():
    return """
    <tbody>

               <tr id ="linha-1">
                   <td id="estacao-1" class=" number">1</td>
                   <td id="nome-1" class=" station">Vidigal

                   </td>
                   <td id="bacia-1" class=" location">Zona Sul</td>
                   <td id="horaLeitura-1" class=" text-center leitura"><a id="data-1" href="/estacoes/pluviometricos/24horas/1/" title="Dados das últimas 24 horas">20/11/2023 - 13:50:00</a></td>

                   <td id="m05-1" class=" text-center m05">0,0</td>
                   <td id="m10-1" class=" text-center m10">0,0</td>
                   <td id="m15-1" class=" text-center m15">0,0</td>
                   <td id="m30-1" class=" text-center m30">0,0</td>
                   <td id="h01-1" class=" text-center h01">2,8</td>
                   <td id="h02-1" class=" text-center h02">0,0</td>
                   <td id="h03-1" class=" text-center h03">0,0</td>
                   <td id="h04-1" class=" text-center h04">0,2</td>
                   <td id="h06-1" class=" text-center h06">0,6</td>
                   <td id="h12-1" class=" text-center h12">7,6</td>
                   <td id="h24-1" class=" text-center h24">9,4</td>
                   <td id="h96-1" class=" text-center h96">21,0</td>
                   <td id="mes-1" class=" text-center mes">52,0</td>
                   <td id="taxa-1" class=" text-center taxa">0,0</td>

               </tr>
       </tbody>
    """


@pytest.fixture
async def load_database(html_response, chuva_repository):
    dados = coletar(html_response)
    [await chuva_repository.create(dado) for dado in dados]


@pytest.fixture(scope="function")
async def session() -> AsyncEngine:
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield Session()
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def chuva_repository(session) -> RainRepository:
    return RainRepository(session)
