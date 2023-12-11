from fastapi import Depends
from alerta_chuva.domain.repositories import RepositoryABC

from alerta_chuva.domain.repositories.radar_repository import RadarRepository
from alerta_chuva.domain.repositories.rain_repository import RainRepository

from sqlalchemy.ext.asyncio.session import AsyncSession

from alerta_chuva.infra.db import get_session


class Repository:
    """
    Classe que define os repositórios utilizados pela aplicação.

    Atributos:
        empresa_repository (EmpresaRepository): O repositório para a entidade Empresa.
        filial_repository (FilialRepository): O repositório para a entidade Filial.
        usuario_repository (UsuarioRepository): O repositório para a entidade Usuário.
        xml_repository (RepositoryXML): O repositório para o XML.
        xml_dados_repository (RepositoryXMLDados): O repositório para os dados XML.

    """

    radar_repository = RadarRepository()
    rain_repository = RainRepository()

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session
        self._reflection()

    def _reflection(self):
        """
        Método interno que associa o objeto `AsyncSession` a todos os repositórios presentes na instância da classe.

        Returns:
            None

        """
        for atributo in dir(self):
            if atributo.startswith("_"):
                continue
            atributo_real = getattr(self, atributo)
            try:
                if isinstance(atributo_real, RepositoryABC):
                    atributo_real.session = self.session  # type: ignore
            except TypeError:
                pass
