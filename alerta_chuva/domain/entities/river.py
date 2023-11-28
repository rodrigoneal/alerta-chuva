from datetime import datetime
from typing import Annotated

from dateutil import parser  # type: ignore
from pydantic import BaseModel, BeforeValidator, ConfigDict

from alerta_chuva.utils.text import parser_float

volume_type = Annotated[float | None, BeforeValidator(parser_float)]


class RiverBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hora: Annotated[datetime, BeforeValidator(lambda data: parser.parse(data))]
    quantity_15_min: volume_type
    quantity_1h: volume_type
    quantity_14h: volume_type
    quantity_24h: volume_type
    quantity_96h: volume_type
    quantity_30d: volume_type
    rio: volume_type


class RiverCreate(RiverBase):
    ...


class RiverRead(RiverBase):
    id: int
