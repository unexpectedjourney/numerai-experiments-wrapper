from http import HTTPStatus

from aiohttp import web
from utils.logger import setup_logger

log = setup_logger(__name__)


async def get_all_states(request):
    states = await get_all_states()
    for state in states:
        state_id = state.get("_id")
        state["_id"] = str(state_id)
    return web.json_response(states, status=HTTPStatus.OK)


async def get_state(request):
    state_id = ...
    state = await get_state(_id=state_id)
    state["_id"] = str(state_id)
    return web.json_response(state, status=HTTPStatus.OK)
