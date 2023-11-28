from datetime import datetime
from typing import Annotated

from dateutil import parser  # type: ignore
from pydantic import BeforeValidator, ConfigDict

from alerta_chuva.utils.text import parser_float

volume_type = Annotated[float | None, BeforeValidator(parser_float)]


class RiverBase:
    model_config = ConfigDict(from_attributes=True)

    hora: Annotated[datetime, BeforeValidator(lambda data: parser.parse(data))]
    quantity_15_min: volume_type
    quantity_1h: volume_type
    quantity_14h: volume_type
    quantity_124h: volume_type
    quantity_196h: volume_type
    quantity_130d: volume_type
    rio: volume_type
