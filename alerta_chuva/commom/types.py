# Modulo para criar tipo de dados.

from typing import Literal, TypeAlias

TypeQuery: TypeAlias = Literal["id", "station_id", "data", "station_name, region"]


ColorAndGrade: TypeAlias = dict[tuple, int]


RegionType: TypeAlias = Literal[
    "Rio",
    "Columbia",
    "Campo Grande",
    "Ilha do Governador",
    "Norte",
    "Sul",
    "Leste",
    "Oeste",
]

RegionRadar: TypeAlias = tuple[tuple[int, int], int]
