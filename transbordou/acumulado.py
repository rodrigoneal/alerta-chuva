from collections import namedtuple

Acumulado = namedtuple(
    "Chuva",
    [
        "data",
        "estacao",
        "quantidade_15_min",
        "quantidade_1_h",
        "quantidade_4_h",
        "quantidade_24_h",
        "quantidade_96_h",
        "quantidade_mes",
    ],
)
