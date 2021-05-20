from http import HTTPStatus

from aiohttp import web
from utils.logger import setup_logger
from utils.model_enums import ModelName

log = setup_logger(__name__)


async def get_all_models(request):
    return web.json_response([
        {"linear_regression": ModelName.LINEAR_REGRESSION.value},
        {"elastic_net": ModelName.ELASTIC_NET.value},
        {"lasso": ModelName.LASSO.value},
        {"ridge": ModelName.RIDGE.value},
    ], status=HTTPStatus.CREATED)


async def execute_model(request):
    if request.method == "POST":
        data = await request.json()
        log.info(data)
        model_id = data.get("model_id", "")
        model_params = data.get("model_params", {})
        action = data.get("action", "")
        # TODO SEND EXECUTION + WRITE DO DB

        return web.json_response(status=HTTPStatus.CREATED)

