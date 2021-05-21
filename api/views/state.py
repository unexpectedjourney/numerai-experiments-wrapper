from http import HTTPStatus

from aiohttp import web
from utils.logger import setup_logger
from utils.database.state import get_states, get_one_state

log = setup_logger(__name__)


async def get_all_states(request):
    states = await get_states()
    for state in states:
        state_id = state.get("_id")
        state["_id"] = str(state_id)
    return web.json_response(states, status=HTTPStatus.OK)


async def get_state(request):
    state_id = request.match_info.get('state_id')
    state = await get_one_state(state_id=state_id)

    log.info(f"state: {state}")
    if state:
        state["_id"] = str(state_id)
        return web.json_response(state, status=HTTPStatus.OK)
    else:
        return web.json_response(status=HTTPStatus.NOT_FOUND)
