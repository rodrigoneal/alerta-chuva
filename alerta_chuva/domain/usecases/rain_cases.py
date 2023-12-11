import asyncio
from alerta_chuva.domain.entities.rain import RainCreate, RainRead
from alerta_chuva.domain.repositories.rain_repository import RainRepository


async def create(repository: RainRepository, schema: RainCreate) -> RainRead:
   result = await repository.create(schema)
   try:
      return RainRead.model_validate(result)
   except Exception as e:
      breakpoint()
      print(e)


