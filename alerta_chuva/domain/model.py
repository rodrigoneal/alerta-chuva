from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ChuvaModel(Base):
    __tablename__ = "chuvas"
    id: Mapped[int] = mapped_column(primary_key=True)
    station_id: Mapped[int]
    station_name: Mapped[str]
    region: Mapped[str]
    data: Mapped[datetime]
    quantity_05_min: Mapped[float]
    quantity_10_min: Mapped[float]
    quantity_15_min: Mapped[float]
    quantity_30_min: Mapped[float]
    quantity_1_h: Mapped[float]
    quantity_2_h: Mapped[float]
    quantity_3_h: Mapped[float]
    quantity_4_h: Mapped[float]
    quantity_6_h: Mapped[float]
    quantity_12_h: Mapped[float]
    quantity_24_h: Mapped[float]
    quantity_96_h: Mapped[float]
    quantity_month: Mapped[float]
    tx_15: Mapped[float]

    __table_args__ = (
        UniqueConstraint("station_name", "data", name="unique_station_data"),
    )
