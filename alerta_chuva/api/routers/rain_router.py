import asyncio
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from alerta_chuva.domain.entities.rain import RainRead
from alerta_chuva.domain.repositories.repositories import Repository

# from alerta_chuva.infra.db import get_session
# from sqlalchemy.ext.asyncio.session import AsyncSession


from alerta_chuva.services.rain.rain import Rain
from alerta_chuva.domain.usecases import rain_cases


rain_routers = APIRouter()





@rain_routers.get("/rain")
async def get_rain():
    return "Hello, World!"


@rain_routers.post("/rain", status_code=201, response_model=list[RainRead])
async def create_rain(
    repository: Annotated[Repository, Depends(Repository)],
    rain: Annotated[Rain, Depends(Rain)],
):
    results = await rain.get_rain()

    return [await rain_cases.create(repository.rain_repository, rain) for rain in results]
