from datetime import date, datetime
from functools import cache
from typing import Optional

from alerta_chuva.check import insentidade_chuva
from alerta_chuva.domain.entities.rain import RainRead
from alerta_chuva.domain.repositories.rain_repository import RainRepository


class Chuva:
    chuva = (0.1, 10000.0)
    chuva_fraca = (0.1, 5.0)
    chuva_moderada = (5.1, 25.0)
    chuva_forte = (25.1, 50.0)
    chuva_muito_forte = (50.1, 1000.0)

    def __init__(self, rain_repository: RainRepository):
        self._chuva: list[RainRead] | None = None
        self.rain_repository = rain_repository

    @cache
    async def get_rains(
        self, date: datetime | date, station_id: int
    ) -> RainRead | None:
        """
        Busca um acumulo de chuva no banco de dados a partir de uma data.

        Args:
            date (datetime | date): Data para buscar o acumulo de chuva.
            station_id (int): ID da estação para buscar o acumulo de chuva.

        Returns:
            RainRead: Acumulo de chuva.
        """
        model = await self.rain_repository.read_rain_by_date(date, station_id)
        if model:
            return RainRead.model_validate(model)
        return None

        return await self.rain_repository.read_rain_by_date(date, station_id)

    @insentidade_chuva(intensidade=chuva)
    async def chuva_detectada(  # type: ignore[empty-body]
        self,
        *,
        station: str | int,
        data: Optional[str] = None,
        hora: Optional[str] = None,
    ) -> bool:
        """Verifica se houve chuva detectada na estação especificada.

        Args:
            station (str | int): ID da estação.
            data (str, optional): Data para buscar o acumulo de chuva. Defaults to None.
            hora (str, optional): Hora para buscar o acumulo de chuva. Defaults to None.

        Returns:
            bool: Se houve chuva.
        """
        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_fraca)
    async def choveu_fraca(  # type: ignore[empty-body]
        self,
        *,
        station: str | int,
        data: Optional[str] = None,
        hora: Optional[str] = None,
    ) -> bool:
        """Verifica se houve chuva fraca na estação especificada.

        Args:
            station (str | int): ID da estação.
            data (str, optional): Data para buscar o acumulo de chuva. Defaults to None.
            hora (str, optional): Hora para buscar o acumulo de chuva. Defaults to None.

        Returns:
            bool: Se houve chuva.
        """
        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_moderada)
    async def choveu_moderado(  # type: ignore[empty-body]
        self,
        *,
        station: str | int,
        data: Optional[str] = None,
        hora: Optional[str] = None,
    ) -> bool:
        """Verifica se houve chuva moderada na estação especificada.

        Args:
            station (str | int): ID da estação.
            data (str, optional): Data para buscar o acumulo de chuva. Defaults to None.
            hora (str, optional): Hora para buscar o acumulo de chuva. Defaults to None.

        Returns:
            bool: Se houve chuva.
        """

        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_forte)
    async def choveu_forte(  # type: ignore[empty-body]
        self,
        *,
        station: str | int,
        data: Optional[str] = None,
        hora: Optional[str] = None,
    ) -> bool:
        """Verifica se houve chuva forte na estação especificada.

        Args:
            station (str | int): ID da estação.
            data (str, optional): Data para buscar o acumulo de chuva. Defaults to None.
            hora (str, optional): Hora para buscar o acumulo de chuva. Defaults to None.

        Returns:
            bool: Se houve chuva.
        """

        ...  # pragma: no cover

    @insentidade_chuva(intensidade=chuva_muito_forte)
    async def choveu_muito_forte(  # type: ignore[empty-body]
        self,
        *,
        station: str | int,
        data: Optional[str] = None,
        hora: Optional[str] = None,
    ) -> bool:
        """Verifica se houve chuva muito forte na estação especificada.

        Args:
            station (str | int): ID da estação.
            data (str, optional): Data para buscar o acumulo de chuva. Defaults to None.
            hora (str, optional): Hora para buscar o acumulo de chuva. Defaults to None.

        Returns:
            bool: Se houve chuva.
        """

        ...  # pragma: no cover
