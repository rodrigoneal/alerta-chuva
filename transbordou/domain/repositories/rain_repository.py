from datetime import date, datetime

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from transbordou.domain.domain import ChuvaModel
from transbordou.domain.entities.rain import RainBase, RainUpdate


class RainRepository:
    def __init__(self, session: AsyncEngine):
        self.session = session

    async def create(self, schema: RainBase):
        model = ChuvaModel(**schema.model_dump())
        async with self.session as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

    async def read(self, estacao: str):
        query = select(ChuvaModel).where(ChuvaModel.estacao == estacao)
        async with self.session as session:
            result = await session.execute(query)
            return result.scalars().all()

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

    async def is_raining(self, estacao: str, data: date | datetime):
        param = (
            ChuvaModel.data
            if isinstance(data, datetime)
            else func.date(ChuvaModel.data)
        )
        query = select(ChuvaModel).where(
            (ChuvaModel.estacao == estacao)
            & (param == data)
            & (ChuvaModel.quantidade_1_h > 0)
        )
        async with self.session as session:
            result = await session.execute(query)
            return result.scalars().first()

    async def rain_intensity(
        self, estacao: str, data: date | datetime, intensity: tuple[float]
    ):
        param = (
            ChuvaModel.data
            if isinstance(data, datetime)
            else func.date(ChuvaModel.data)
        )
        query = select(ChuvaModel).where(
            (ChuvaModel.estacao == estacao)
            & (param == data)
        & (ChuvaModel.quantidade_1_h.between(*intensity))
        )

        async with self.session as session:
            result = await session.execute(query)
            return result.scalars().first()
