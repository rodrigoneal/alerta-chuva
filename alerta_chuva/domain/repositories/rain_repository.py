# Modulo para criar repositorio de chuva.

from datetime import date, datetime
from typing import Any

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError

from alerta_chuva.commom.types import TypeQuery
from alerta_chuva.domain.entities.rain import RainCreate, RainUpdate
from alerta_chuva.domain.model import ChuvaModel


class RainRepository:
    """
    Repositorio de chuva.
    Para interacão com o banco de dados.
    """

    def __init__(self, session):
        self.session = session

    async def create(self, schema: RainCreate):
        """
        Armazena um novo acumulo de chuva no banco de dados.

        Args:
            schema (RainCreate): Modelo para criar um novo acumulo de chuva.

        Returns:
            ChuvaModel: acumulo de chuva criado.
        """

        model = ChuvaModel(**schema.model_dump())
        async with self.session as session:
            session.add(model)
            try:
                await session.commit()
                await session.refresh(model)
                return model
            except IntegrityError:
                await session.rollback()

    async def _read(self, query) -> list[ChuvaModel]:
        """
        Executa uma consulta no banco de dados.

        Args:
            query (Any): Consulta a ser executada.

        Returns:
            list[ChuvaModel]: Acumulo de chuvas.
        """
        async with self.session as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def read(
        self,
        _read: Any,
        type_read: TypeQuery | None = None,
    ) -> list[ChuvaModel]:
        """
        Busca um acumulo de chuva no banco de dados.
        Se nenhum argumento for passado, retorna todos os acumulos de chuva.
        Exemplos de uso:

        ```python
        chuva = await RainRepository.read(1)
        chuva = await RainRepository.read(1, "id")
        chuva = await RainRepository.read(1, "station_id")
        chuva = await RainRepository.read("2022-01-01", "data")
        chuva = await RainRepository.read("Vidigal", "station_name")
        ```

        Args:
            _read (Any): Valor que será pesquisado.
            type_read (TypeQuery | None, optional): Tipo de pesquisa. Defaults to None.

        Returns:
            list[ChuvaModel]: Acumulo de chuvas.
        """

        if not type_read:
            query = select(ChuvaModel)
        else:
            chuva_type = getattr(ChuvaModel, type_read)
            query = select(ChuvaModel).where(chuva_type == _read)
        return await self._read(query)

    async def read_rain_by_date(
        self, data: date | datetime, station_id: int
    ) -> ChuvaModel:
        """
        Busca um acumulo de chuva no banco de dados pela data.
        Pode ser pesquisado por date ou datetime do python.

        Args:
            data (date | datetime): Data que será pesquisada.
            station_id (int): ID da estação que será pesquisada.

        Returns:
            ChuvaModel: Acumulo de chuvas.
        """

        param = (
            ChuvaModel.data
            if isinstance(data, datetime)
            else func.date(ChuvaModel.data)
        )
        query = (
            select(ChuvaModel)
            .where((param == data) & (ChuvaModel.station_id == station_id))
            .order_by(ChuvaModel.data)
        )
        async with self.session as session:
            result = await session.execute(query)
            return result.scalars().one()

    async def update(self, schema: RainUpdate, _id: int) -> ChuvaModel | None:
        """Atualiza um acumulo de chuva no banco de dados.

        Args:
            schema (RainUpdate): Modelo para atualizar um acumulo de chuva.
            _id (int): ID do acumulo de chuva que será atualizado.

        Returns:
            ChuvaModel: Acumulo de chuva atualizado.
        """

        query = (
            update(ChuvaModel)
            .where(ChuvaModel.id == _id)
            .values(**schema.model_dump(exclude_unset=True))
            .returning(ChuvaModel)
        )
        async with self.session as session:
            model = (await session.execute(query)).scalar_one_or_none()
            return model

    async def delete(self, _id: int) -> ChuvaModel | None:
        """Deleta um acumulo de chuva no banco de dados.

        Args:
            _id (int): ID do acumulo de chuva que será deletado.

        Returns:
            ChuvaModel: Acumulo de chuva deletado.
        """

        query = delete(ChuvaModel).where(ChuvaModel.id == _id).returning(ChuvaModel)
        async with self.session as session:
            model = (await session.execute(query)).scalar_one_or_none()
            return model
