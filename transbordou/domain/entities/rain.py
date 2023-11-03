from datetime import datetime
from typing import Annotated

from dateutil import parser
from pydantic import BaseModel, BeforeValidator

from transbordou.utils.text import parser_float, pipeline_text

volume_type = Annotated[float | None, BeforeValidator(parser_float)]


class RainBase(BaseModel):
    data: datetime
    quantidade_15_min: float
    quantidade_1_h: float
    quantidade_4_h: float
    quantidade_24_h: float
    quantidade_96_h: float
    quantidade_mes: float


class RainCreate(RainBase):
    estacao: Annotated[int, BeforeValidator(pipeline_text)]
    data: Annotated[datetime, BeforeValidator(lambda data: parser.parse(data))]
    quantidade_15_min: volume_type
    quantidade_1_h: volume_type
    quantidade_4_h: volume_type
    quantidade_24_h: volume_type
    quantidade_96_h: volume_type
    quantidade_mes: volume_type


class RainRead(RainBase):
    id: int
    estacao: int


class RainUpdate(BaseModel):
    data: datetime | None = None
    estacao: int | None = None
    quantidade_15_min: float | None = None
    quantidade_1_h: float | None = None
    quantidade_4_h: float | None = None
    quantidade_24_h: float | None = None
    quantidade_96_h: float | None = None
    quantidade_mes: float | None = None
