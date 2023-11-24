from datetime import date, datetime
from typing import Any, Literal, TypeAlias

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine

from alerta_chuva.domain.entities.rain import RainBase, RainUpdate
from alerta_chuva.domain.model import ChuvaModel

type_query: TypeAlias = Literal["id", "station_id", "data", "station_name, region"]


class RainRepository:
    def __init__(self, session: AsyncEngine):
        self.session = session

    async def create(self, schema: RainBase):
        model = ChuvaModel(**schema.model_dump())
        async with self.session as session:
            session.add(model)
            try:
                await session.commit()
                await session.refresh(model)
                return model
            except IntegrityError:
                await session.rollback()

    async def create_many(self, schema: list[RainBase]):
        models = [ChuvaModel(**model.model_dump()) for model in schema]
        async with self.session as session:
            session.add_all(models)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def _read(self, query):
        async with self.session as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def read(
        self,
        _read: Any,
        type_read: type_query | None = None,
    ) -> list[ChuvaModel]:
        if not type_read:
            query = select(ChuvaModel)
        else:
            chuva_type = getattr(ChuvaModel, type_read)
            query = select(ChuvaModel).where(chuva_type == _read)
        return await self._read(query)

    async def read_rain_by_date(
        self, data: date | datetime, station_id: int
    ) -> list[ChuvaModel]:
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

    async def update(self, schema: RainUpdate, _id: int):
        query = (
            update(ChuvaModel)
            .where(ChuvaModel.id == _id)
            .values(**schema.model_dump(exclude_unset=True))
            .returning(ChuvaModel)
        )
        async with self.session as session:
            model = (await session.execute(query)).scalar_one_or_none()
            return model

    async def delete(self, _id: int):
        query = delete(ChuvaModel).where(ChuvaModel.id == _id).returning(ChuvaModel)
        async with self.session as session:
            model = (await session.execute(query)).scalar_one_or_none()
            return model
