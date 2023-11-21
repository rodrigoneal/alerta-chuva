import asyncio

import httpx

from alerta_chuva.coletar import coletar
from alerta_chuva.domain.repositories.rain_repository import RainRepository
from alerta_chuva.services.acumulado import RainRecord



class Crawler:
    def __init__(self, rain_repository: RainRepository):
        self.rain_repository = rain_repository
        self.endpoint = "/dados/h24/{}/"
        self.rains = []
        self.link_img_radar = "https://bpyu1frhri.execute-api.us-east-1.amazonaws.com/maparadar/radar0{}.png"
        self.url_data_rain = "https://websempre.rio.rj.gov.br/estacoes/"

    async def make_request(self, url: str):
        print("Pegando dados de {} ...".format(url))
        async with httpx.AsyncClient() as client:
            result = await client.get(url)
            return result

    async def get_radar_img(self) -> list[httpx.Response]:
        urls = []
        for i in range(1, 20 + 1):
            if i < 10:
                url = self.link_img_radar.format("0" + str(i))
            else:
                url = self.link_img_radar.format(i)
            urls.append(url)

        tasks = [self.make_request(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses

    async def get_rainfall_data(self) -> RainRecord:
        response = await self.make_request(self.url_data_rain)
        rain_register = coletar(response.text)
        return RainRecord(rain_register, self.rain_repository)
