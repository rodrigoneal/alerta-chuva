import asyncio
from typing import Generator

import httpx
from bs4 import BeautifulSoup

from alerta_chuva.commom.aux import RainRecord
from alerta_chuva.domain.entities.rain import RainCreate
from alerta_chuva.domain.repositories.rain_repository import RainRepository


class Crawler:

    """
    Facilita a coleta de dados de chuva de forma assíncrona.
    """

    def __init__(self, rain_repository: RainRepository | None = None):
        self.rain_repository = rain_repository
        self.endpoint = "/dados/h24/{}/"
        self.link_img_radar = "https://bpyu1frhri.execute-api.us-east-1.amazonaws.com/maparadar/radar0{}.png"
        self.url_data_rain = "https://websempre.rio.rj.gov.br/estacoes/"
        self.url_rivers = "http://alertadecheias.inea.rj.gov.br/alertadecheias/{}.html"

    async def make_request(self, url: str) -> httpx.Response | None:
        """Faz uma requisição HTTP assíncrona.
        Lança uma exceção se demorar mais que 5 segundos.
        Args:
            url (str): url para requisição.

        Returns:
            Response: Objeto Response do HTTPX.
        """
        print("Pegando dados de {} ...".format(url))
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                return await client.get(url)
            except httpx.ReadTimeout:
                return None

    async def get_river_data(self, river: str) -> str | None:
        """Faz uma requisição HTTP assíncrona e coleta os dados do rio.
        Args:
            river (str): Nome do rio.

        Returns:
            str: Pagina HTML.
        """
        response = await self.make_request(self.url_rivers.format(river))
        if not response:
            return None
        return response.text

    def extract_info_river(self, html: str | None) -> dict[str, str]:
        """Pega o valor do acumulo de chuva.
        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup.

        Returns:
            str: Acumulo de chuva.
        """
        # Encontre todas as linhas da tabela
        if not html:
            return {}
        th = (
            "hora",
            "quantity_15_min",
            "quantity_1h",
            "quantity_14h",
            "quantity_24h",
            "quantity_96h",
            "quantity_30d",
            "rio",
        )
        soup = BeautifulSoup(html, "html.parser")
        linhas = soup.find("table", {"id": "Table"}).find_all("tr")  # type: ignore
        primeira_linha_com_td = None
        for linha in linhas:
            if linha.find("td"):
                primeira_linha_com_td = linha
                break
        tds = primeira_linha_com_td.find_all("td")  # type: ignore

        return {key: td.text for key, td in zip(th, tds)}

    async def river_data(self, river: str) -> dict:
        """Faz uma requisição HTTP assíncrona e coleta os dados do rio.
        Args:
            river (str): Nome do rio.

        Returns:
            dict: Dados do rio.
        """
        river_html = await self.get_river_data(river)
        return self.extract_info_river(river_html)
    
    def create_url_img_radar(self, img_index: int) -> str:
        """Cria a url da imagem do radar.
        Args:
            img_index (int): Indice da imagem do radar.

        Returns:
            str: Url da imagem do radar.
        """
        img_index = str(int(img_index))
        img_index = img_index.zfill(2)

        return self.link_img_radar.format(img_index)

    async def get_radar_img(self) -> Generator[bytes, None, None]:
        """Baixa as 20 imagens do radar.

        Returns:
            Generator[bytes]: Imagens do radar.
        """

        tasks = []
        for i in range(1, 20 + 1):
            if i < 10:
                url = self.link_img_radar.format("0" + str(i))
            else:
                url = self.link_img_radar.format(i)
            task = asyncio.create_task(self.make_request(url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return (
            response.content
            for response in responses
            if isinstance(response, httpx.Response) and hasattr(response, "content")
        )

    async def get_rainfall_data(self) -> RainRecord | None:
        """Faz uma requisição HTTP assíncrona e coleta os dados de chuva.
        Returns:
            RainRecord: Acumulo de chuva.
        """
        response = await self.make_request(self.url_data_rain)
        if not response:
            return None
        rain_register = self.extract_info_rain(response.text)
        return RainRecord(rain_register, self.rain_repository)  # type: ignore

    def extract_info_rain(self, html: str) -> list[RainCreate]:
        acumulados = []
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all(
            lambda tag: tag.name == "tr" and tag.get("id", "").startswith("linha")
        )
        for row in rows:
            # Encontre todas as colunas (td) na linha
            columns = row.find_all("td")
            if not columns or len(columns) < 17:
                continue
            # Acesse as informações que você deseja com base na posição das colunas
            _temp = dict(
                station_id=columns[0].text.strip(),
                station_name=columns[1].text.strip(),
                region=columns[2].text.strip(),
                data=columns[3].text.strip(),
                quantity_05_min=columns[4].text.strip(),
                quantity_10_min=columns[5].text.strip(),
                quantity_15_min=columns[6].text.strip(),
                quantity_30_min=columns[7].text.strip(),
                quantity_1_h=columns[8].text.strip(),
                quantity_2_h=columns[9].text.strip(),
                quantity_3_h=columns[10].text.strip(),
                quantity_4_h=columns[11].text.strip(),
                quantity_6_h=columns[12].text.strip(),
                quantity_12_h=columns[13].text.strip(),
                quantity_24_h=columns[14].text.strip(),
                quantity_96_h=columns[15].text.strip(),
                quantity_month=columns[16].text.strip(),
                tx_15=columns[17].text.strip(),
            )

            acumulado = RainCreate(**_temp)
            acumulados.append(acumulado)
        return acumulados
