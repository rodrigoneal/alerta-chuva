from alerta_chuva.api.routers.rain_router import rain_routers

def set_routers(app):
    app.include_router(rain_routers)