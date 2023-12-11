from datetime import datetime

from sqlalchemy import delete, func, select, update

from alerta_chuva.domain.entities.radar import RadarCreate, RadarUpdate
from alerta_chuva.domain.model import RadarModel


class RadarRepository:
    """
    Repositorio do radar.
    Para interacão com o banco de dados.
    """

    def __init__(self, session):
        self.session = session

    async def create(self, schema: RadarCreate) -> RadarModel:
        """
        Armazena um novo radar no banco de dados.

        Args:
            schema (Radar): modelos para criar um novo radar.

        Returns:
            RadarModel: radar criado.
        """

        model = RadarModel(**schema.model_dump())
        async with self.session as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    async def read(self, _id: int | None = None) -> list[RadarModel]:
        """
        Executa uma consulta no banco de dados.


        Returns:
            list[RadarModel]: Acumulo de chuvas.
        """
        if _id:
            stmt = select(RadarModel).where(RadarModel.id == _id)
        else:
            stmt = select(RadarModel)
        async with self.session as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update(self, schema: RadarUpdate, _id: int) -> RadarModel:
        """
        Atualiza um radar no banco de dados.

        Args:
            schema (Radar): modelos para atualizar um radar.

        Returns:
            RadarModel: radar atualizado.
        """
        stmt = (
            update(RadarModel)
            .where(RadarModel.id == _id)
            .values(**schema.model_dump(exclude_unset=True))
        ).returning(RadarModel)
        async with self.session as session:
            model = (await session.execute(stmt)).scalar_one_or_none()
            return model

    async def delete(self, _id: int) -> RadarModel:
        """
        Deleta um radar no banco de dados.

        Args:
            _id (int): id do radar a ser deletado.
        """
        stmt = delete(RadarModel).where(RadarModel.id == _id).returning(RadarModel)
        async with self.session as session:
            model = (await session.execute(stmt)).scalar_one_or_none()
            return model

    async def read_by_date(self, date: datetime) -> list[RadarModel]:
        """
        Executa uma consulta no banco de dados.


        Returns:
            list[RadarModel]: Acumulo de chuvas.
        """
        param = func.date(RadarModel.data)
        stmt = select(RadarModel).where(param == date.date())
        async with self.session as session:
            result = await session.execute(stmt)
            return result.scalars().all()
