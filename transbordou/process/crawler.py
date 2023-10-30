import httpx
import asyncio
from transbordou.coletar import coletar

from transbordou.locais import Local


class Crawler:
    base_url = "http://websempre.rio.rj.gov.br"

    def __init__(self):
        self.endpoint = "/dados/h24/{}/"

    async def make_request(self, url: str):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            result = await client.get(url)
            return result
    
    def __montar_url(self, bairro: str):
        return self.endpoint.format(bairro)

    async def get_data(self):
        urls = []
        for local in Local.__members__.values():
            url = self.__montar_url(local.value)
            urls.append(url)
        responses = await asyncio.gather(*map(self.make_request, urls))
        return [coletar(response.text) for response in responses]
