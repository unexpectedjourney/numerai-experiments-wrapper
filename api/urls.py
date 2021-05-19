from aiohttp import web
from views.health import status


def get_urls():
    return [
        web.get("/api/health/", status, name="status"),
        web.get("/api/model/", ..., name="models"),

    ]


def get_routers(app):
    routers = []
    routers.extend(get_urls())
    app.add_routes(routers)
