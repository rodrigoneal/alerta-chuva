from datetime import datetime
from typing import Annotated

from dateutil import parser
from pydantic import BaseModel, BeforeValidator

from alerta_chuva.utils.text import parser_float

volume_type = Annotated[float | None, BeforeValidator(parser_float)]


class RainBase(BaseModel):
    station_id: int
    station_name: str
    region: str
    data: datetime
    quantity_05_min: float
    quantity_10_min: float
    quantity_15_min: float
    quantity_30_min: float
    quantity_1_h: float
    quantity_2_h: float
    quantity_3_h: float
    quantity_4_h: float
    quantity_6_h: float
    quantity_12_h: float
    quantity_24_h: float
    quantity_96_h: float
    quantity_month: float
    tx_15: float


class RainCreate(RainBase):
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
    id: int


class RainUpdate(BaseModel):
    station_id: int = None
    station_name: str = None
    region: str = None
    data: datetime = None
    quantity_05_min: float = None
    quantity_10_min: float = None
    quantity_15_min: float = None
    quantity_30_min: float = None
    quantity_1_h: float = None
    quantity_2_h: float = None
    quantity_3_h: float = None
    quantity_4_h: float = None
    quantity_6_h: float = None
    quantity_12_h: float = None
    quantity_24_h: float = None
    quantity_96_h: float = None
    quantity_month: float = None
    tx_15: float = None
