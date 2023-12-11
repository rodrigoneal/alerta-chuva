from contextlib import asynccontextmanager
from fastapi import FastAPI
from alerta_chuva.api.routers import set_routers

from alerta_chuva.infra.db import create_tables



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    
    set_routers(app)
    return app
app = create_app()