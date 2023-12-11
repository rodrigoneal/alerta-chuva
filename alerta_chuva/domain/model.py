# Modulo de domínio.

from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from alerta_chuva.domain import Base


class ChuvaModel(Base):
    """
    Tabela de chuvas.

    Args:
        Base (DeclarativeBase): Classe base do SQLAlchemy

    Returns:
       ChuvaModel : ChuvaModel
    """

    __tablename__ = "rains"
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

    updated_at: Mapped[datetime | None] = mapped_column(onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        """Representacão do objeto.


        Returns:
            str: representação do objeto com os atributos.
        """

        attributos = []
        ignore = ["metadata", "registry"]
        for attr in dir(self):
            if not attr.startswith("_") and attr not in ignore:
                value = getattr(self, attr)
                attributos.append(f"{attr}: {value!r}")

        return f"ChuvaModel({', '.join(attributos)})"


class RadarModel(Base):
    """
    Tabela de radars.

    Args:
        Base (DeclarativeBase): Classe base do SQLAlchemy

    Returns:
       RadarModel : RadarModel
    """

    __tablename__ = "radars"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime | None]
    img: Mapped[str | None]
    grau: Mapped[int]

    def __repr__(self) -> str:
        """Representacão do objeto.


        Returns:
            str: representação do objeto com os atributos.
        """

        attributos = []
        ignore = ["metadata", "registry"]
        for attr in dir(self):
            if not attr.startswith("_") and attr not in ignore:
                value = getattr(self, attr)
                attributos.append(f"{attr}: {value!r}")

        return f"RadarModel({', '.join(attributos)})"


class RiverModel(Base):
    """
    Tabela de rivers.

    Args:
        Base (DeclarativeBase): Classe base do SQLAlchemy

    Returns:
       RiverModel : RiverModel
    """

    __tablename__ = "rivers"
    id: Mapped[int] = mapped_column(primary_key=True)
    hora: Mapped[datetime]
    quantity_15_min: Mapped[float]
    quantity_1h: Mapped[float]
    quantity_14h: Mapped[float]
    quantity_24h: Mapped[float]
    quantity_96h: Mapped[float]
    quantity_30d: Mapped[float]
    rio: Mapped[float]

    def __repr__(self) -> str:
        """Representacão do objeto.


        Returns:
            str: representação do objeto com os atributos.
        """

        attributos = []
        ignore = ["metadata", "registry"]
        for attr in dir(self):
            if not attr.startswith("_") and attr not in ignore:
                value = getattr(self, attr)
                attributos.append(f"{attr}: {value!r}")

        return f"RiverModel({', '.join(attributos)})"
