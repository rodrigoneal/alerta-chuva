from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ChuvaModel(Base):
    __tablename__ = "chuvas"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime]
    estacao: Mapped[str]
    quantidade_15_min: Mapped[float | None]
    quantidade_1_h: Mapped[float | None]
    quantidade_4_h: Mapped[float | None]
    quantidade_24_h: Mapped[float | None]
    quantidade_96_h: Mapped[float | None]
    quantidade_mes: Mapped[float | None]
