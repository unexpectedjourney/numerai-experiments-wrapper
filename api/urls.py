from aiohttp import web
from views.health import status
from views.state import get_all_states, get_state
from views.model import get_all_models, execute_model


def get_urls():
    return [
        web.get("/api/health/", status, name="status"),
        web.get("/api/model/", get_all_models, name="get_model"),
        web.post("/api/model/", execute_model, name="execute_model"),
        web.get("/api/state/", get_all_states, name="get_states"),
        web.get("/api/state/{state_id}/", get_state, name="get_state"),
    ]


def get_routers(app):
    routers = []
    routers.extend(get_urls())
    app.add_routes(routers)
