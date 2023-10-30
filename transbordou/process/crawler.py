import asyncio
from itertools import chain
from pathlib import Path

import httpx
from selenium_tools.selenium_driver import SeleniumDriver

from transbordou.coletar import coletar, parser_txt_to_DataFrame, unzip_all_file
from transbordou.domain.entities.rain import RainCreate
from transbordou.domain.repositories.rain_repository import RainRepository
from transbordou.locais import Local
from transbordou.process.pages.page import GetHistory


class Crawler:
    base_url = "http://websempre.rio.rj.gov.br"
    rainfall_history_url = (
        "http://alertario.rio.rj.gov.br/download/dados-pluviometricos/"
    )

    def __init__(self, rain_repository: RainRepository):
        self.rain_repository = rain_repository
        self.endpoint = "/dados/h24/{}/"
        self.rains = []
        self.driver = self._get_driver

    def _get_driver(self):
        download_folder = Path("downloads")
        download_folder.mkdir(parents=True, exist_ok=True)
        self.download_folder = str(download_folder.absolute())
        driver = SeleniumDriver(
            download_path=self.download_folder, log=False, headless=True
        ).get_driver()
        driver.get(self.rainfall_history_url)
        return driver

    async def make_request(self, url: str):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            result = await client.get(url)
            return result

    def __montar_url(self, bairro: str):
        return self.endpoint.format(bairro)

    async def scrape(self) -> "Crawler":
        urls = []
        for local in Local.__members__.values():
            url = self.__montar_url(local.value)
            urls.append(url)
        responses = await asyncio.gather(*map(self.make_request, urls))
        rains = [coletar(response.text) for response in responses]
        rains = list(chain.from_iterable(rains))
        self.rains.extend(rains)
        return self

    def get_rainfall_history(self, estacao: str, year: int) -> "Crawler":
        driver = self.driver()
        station = Local[estacao.upper()].value
        get_history = GetHistory(driver)
        get_history.download_history.download_specific_station(year, station)
        driver.quit()
        unzip_all_file(self.download_folder)
        df = parser_txt_to_DataFrame(self.download_folder)
        chuvas = df.to_dict("records")
        [self.rains.append(RainCreate(**chuva)) for chuva in chuvas]
        return self

    def get_rainfall_history_all_stations(self, year: int) -> "Crawler":
        driver = self.driver()
        get_history = GetHistory(driver)
        get_history.download_history.download_history_all_stations(year)
        driver.quit()
        unzip_all_file(self.download_folder)
        df = parser_txt_to_DataFrame(self.download_folder)
        breakpoint()
        return self

    async def save_rain(self):
        [await self.rain_repository.create(rain) for rain in self.rains]
