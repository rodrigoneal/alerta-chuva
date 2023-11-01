import asyncio
import shutil
import tempfile
from itertools import chain
from pathlib import Path

import httpx
from selenium_tools.selenium_driver import SeleniumDriver

from transbordou.coletar import (coletar, extract_name_from_txt,
                                 parser_txt_to_DataFrame, unzip_all_file)
from transbordou.domain.entities.rain import RainCreate
from transbordou.domain.repositories.rain_repository import RainRepository
from transbordou.locais import Local


class Crawler:
    base_url = "http://websempre.rio.rj.gov.br"
    rainfall_history_url = (
        "http://alertario.rio.rj.gov.br/download/dados-pluviometricos/"
    )

    def __init__(self, rain_repository: RainRepository):
        self.rain_repository = rain_repository
        self.endpoint = "/dados/h24/{}/"
        self.rains = []
        self.download_folder = tempfile.mkdtemp()

    def _get_driver(self):
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

    def get_zips(self, path):
        for zip in Path(path).glob("*.txt"):
            yield zip

    async def download_rainfall_history(
        self, func: callable, *args, **kwargs
    ) -> "Crawler":
        try:
            driver = self._get_driver()
            func(driver, *args, **kwargs)
            driver.quit()
            path = unzip_all_file(self.download_folder)
            for zip in self.get_zips(path):
                station_name = extract_name_from_txt(str(zip.name))
                df = parser_txt_to_DataFrame(zip, station_name)
                if df is None or df.empty:
                    continue
                chuvas = df.to_dict("records")
                rains = [RainCreate(**chuva) for chuva in chuvas]
                await self.save_many(rains)

            return self
        finally:
            shutil.rmtree(self.download_folder, ignore_errors=True)

    async def save(self):
        [await self.rain_repository.create(rain) for rain in self.rains]

    async def save_many(self, rains: list[RainCreate]):
        await self.rain_repository.create_many(rains)
