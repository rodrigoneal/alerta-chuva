import re
from datetime import datetime
from typing import Annotated

from dateutil import parser
from pydantic import BaseModel, BeforeValidator, constr


def parser_float(text: str):
    if isinstance(text, float):
        return text
    if text == "ND":
        return 0.0
    return float(text.strip().replace(",", "."))


def nome_estacão(texto: str):
    padrao = r"ESTACAO\s+(.*)"
    estacao = re.search(padrao, texto)
    if estacao:
        return estacao.group(1).strip()
    else:
        return texto


class RainBase(BaseModel):
    data: datetime
    quantidade_15_min: float
    quantidade_1_h: float
    quantidade_4_h: float
    quantidade_24_h: float
    quantidade_96_h: float
    quantidade_mes: float


class RainCreate(RainBase):
    estacao: Annotated[str, BeforeValidator(nome_estacão)]
    data: Annotated[datetime, BeforeValidator(lambda data: parser.parse(data))]
    quantidade_15_min: Annotated[float, BeforeValidator(parser_float)]
    quantidade_1_h: Annotated[float, BeforeValidator(parser_float)]
    quantidade_4_h: Annotated[float, BeforeValidator(parser_float)]
    quantidade_24_h: Annotated[float, BeforeValidator(parser_float)]
    quantidade_96_h: Annotated[float, BeforeValidator(parser_float)]
    quantidade_mes: Annotated[float, BeforeValidator(parser_float)]


class RainRead(RainBase):
    id: int
    estacao: str


class RainUpdate(BaseModel):
    data: datetime | None = None
    estacao: str | None = None
    quantidade_15_min: float | None = None
    quantidade_1_h: float | None = None
    quantidade_4_h: float | None = None
    quantidade_24_h: float | None = None
    quantidade_96_h: float | None = None
    quantidade_mes: float | None = None
