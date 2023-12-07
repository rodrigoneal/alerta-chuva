# Esse modulo são as entidades do acumulo de registro da chuva.


from datetime import datetime
from typing import Annotated

from dateutil import parser  # type: ignore
from pydantic import BaseModel, BeforeValidator, ConfigDict

from alerta_chuva.utils.text import parser_float

volume_type = Annotated[float | None, BeforeValidator(parser_float)]


class RainBase(BaseModel):
    """Base que cria um modelo para o acumulo de chuva.

    Args:
        BaseModel (BaseModel): Classe base do Pydantic
    """

    station_id: int
    station_name: str
    region: str
    data: datetime
    quantity_05_min: volume_type
    quantity_10_min: volume_type
    quantity_15_min: volume_type
    quantity_30_min: volume_type
    quantity_1_h: volume_type
    quantity_2_h: volume_type
    quantity_3_h: volume_type
    quantity_4_h: volume_type
    quantity_6_h: volume_type
    quantity_12_h: volume_type
    quantity_24_h: volume_type
    quantity_96_h: volume_type
    quantity_month: volume_type
    tx_15: volume_type

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (tuple, list)):
            return self.quantity_15_min >= other[0] and self.quantity_15_min < other[1]
        return super().__eq__(other)



class RainCreate(RainBase):
    """Modelo para criar um acumulo de chuva.

    Esse modelo será usado para criar um novo acumulo de chuva.

    Exemplo de uso:

    ```python
    from alerta_chuva.domain.entities.rain import RainCreate

    rain = RainCreate(
        station_id=1,
        station_name="Rio de Janeiro",
        region="RJ",
        data=datetime.now(),
        quantity_05_min=0.0,
        quantity_10_min=0.0,
        quantity_15_min=0.0,
        quantity_30_min=0.0,
        quantity_1_h=0.0,
        quantity_2_h=0.0,
        quantity_3_h=0.0,
        quantity_4_h=0.0,
        quantity_6_h=0.0,
        quantity_12_h=0.0,
        quantity_24_h=0.0,
        quantity_96_h=0.0,
        quantity_month=0.0,
        tx_15=0.0    )
    ```

    Args:
        RainBase (BaseModel): Base do acumulo de chuva
    """

    data: Annotated[datetime, BeforeValidator(lambda data: parser.parse(data))]
    quantity_05_min: volume_type
    quantity_10_min: volume_type
    quantity_15_min: volume_type
    quantity_30_min: volume_type
    quantity_1_h: volume_type
    quantity_2_h: volume_type
    quantity_3_h: volume_type
    quantity_4_h: volume_type
    quantity_6_h: volume_type
    quantity_12_h: volume_type
    quantity_24_h: volume_type
    quantity_96_h: volume_type
    quantity_month: volume_type
    tx_15: volume_type


class RainRead(RainBase):
    model_config = ConfigDict(from_attributes=True)
    """Modelo para ler um acumulo de chuva.

    Esse modelo será usado para ler um acumulo de chuva.
    Args:
        RainBase (BaseModel): _description_
    """

    id: int


class RainUpdate(BaseModel):
    """Modelo para atualizar um acumulo de chuva.

    Esse modelo será usado para atualizar um acumulo de chuva.
    Exemplo de uso:

    ```python
    from alerta_chuva.domain.entities.rain import RainUpdate

    rain = RainUpdate(
        station_id=1,
        station_name="Rio de Janeiro",
        region="RJ",
        data=datetime.now(),
        quantity_05_min=0.0,
        quantity_10_min=0.0,
        quantity_15_min=0.0,
        quantity_30_min=0.0,
        quantity_1_h=0.0,
        quantity_2_h=0.0,
        quantity_3_h=0.0,
        quantity_4_h=0.0,
        quantity_6_h=0.0,
        quantity_12_h=0.0,
        quantity_24_h=0.0,
        quantity_96_h=0.0,
        quantity_month=0.0,
        tx_15=0.0    )
    ```

    Args:
        BaseModel (BaseModel): Classe base do Pydantic
    """

    station_id: int | None = None
    station_name: str | None = None
    region: str | None = None
    data: datetime | None = None
    quantity_05_min: float | None = None
    quantity_10_min: float | None = None
    quantity_15_min: float | None = None
    quantity_30_min: float | None = None
    quantity_1_h: float | None = None
    quantity_2_h: float | None = None
    quantity_3_h: float | None = None
    quantity_4_h: float | None = None
    quantity_6_h: float | None = None
    quantity_12_h: float | None = None
    quantity_24_h: float | None = None
    quantity_96_h: float | None = None
    quantity_month: float | None = None
    tx_15: float | None = None
