# Modulo para criar tipo de dados.

from typing import Literal, TypeAlias, TypedDict

TypeQuery: TypeAlias = Literal["id", "station_id", "data", "station_name, region"]


class ColorAndGrande(TypedDict):
    tuple[int, int, int]: int


RegionType: TypeAlias = Literal[
    "Columbia", "Campo Grande", "Ilha do Governador", "Norte", "Sul", "Leste", "Oeste"
]

RegionRadar: TypeAlias = tuple[tuple[int, int], int]
