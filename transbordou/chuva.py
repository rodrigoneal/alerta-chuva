from transbordou.acumulado import Acumulado
from dateutil import parser

from transbordou.locais import Local


class Chuva:
    chuva_fraca = 7.6
    chuva_moderada = 30.0
    chuva_forte = 30.1

    def __init__(self):
        self._chuva: list[Acumulado] = None

    def choveu(self, estacao: str | Local | int, data: str, hora: str = None) -> bool:
        if isinstance(estacao, int):
            _estacao = Local(int).name
        elif isinstance(estacao, Local):
            _estacao = estacao.name
        elif isinstance(estacao, str):
            _estacao = estacao.upper()
        if not hora:
            date = parser.parse(data).date()
            return any(
                chuva
                for chuva in self._chuva
                if (chuva.data.date() == date)
                and (chuva.quantidade_1_h >= 0)
                and (chuva.estacao == _estacao)
            )
        else:
            date = parser.parse(data + " " + hora)
            return any(
                chuva
                for chuva in self._chuva
                if chuva.data == date
                and (chuva.quantidade_15_min >= 0)
                and (chuva.estacao == _estacao)
            )

    def choveu_forte(self, data: str, hora: str = None) -> bool:
        if not hora:
            date = parser.parse(data).date()
            return any(
                chuva
                for chuva in self._chuva
                if (chuva.data.date() == date)
                and (chuva.quantidade_1_h >= self.chuva_forte)
            )
        else:
            date = parser.parse(data + " " + hora)
            return any(
                chuva
                for chuva in self._chuva
                if (chuva.data == date)
                and (chuva.quantidade_15_min >= self.chuva_forte)
            )

    def choveu_moderado(self, data: str, hora: str = None) -> bool:
        if not hora:
            date = parser.parse(data).date()
            return any(
                chuva
                for chuva in self._chuva
                if (chuva.data.date() == date)
                and (chuva.quantidade_1_h >= self.chuva_fraca)
                and (chuva.quantidade_1_h < self.chuva_forte)
            )
        else:
            date = parser.parse(data + " " + hora)
            return any(
                chuva
                for chuva in self._chuva
                if chuva.data == date
                and (chuva.quantidade_15_min >= self.chuva_moderada)
                and (chuva.quantidade_15_min < self.chuva_forte)
            )

    def choveu_fraca(self, data: str, hora: str = None) -> bool:
        if not self.choveu:
            return False
        if not hora:
            date = parser.parse(data).date()
            return any(
                chuva
                for chuva in self._chuva
                if (chuva.data.date() == date)
                and (chuva.quantidade_1_h < self.chuva_moderada)
            )
        else:
            date = parser.parse(data + " " + hora)
            return any(
                chuva
                for chuva in self._chuva
                if chuva.data == date
                and (chuva.quantidade_15_min < self.chuva_moderada)
            )

    def maior_acumulado(self, data: str) -> Acumulado:
        date = parser.parse(data).date()
        chuvas = [chuva for chuva in self._chuva if chuva.data.date() == date]
        return max(chuvas, key=lambda chuva: chuva.quantidade_1_h)
