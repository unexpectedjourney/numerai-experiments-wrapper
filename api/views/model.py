
import uuid
from http import HTTPStatus

from aiohttp import web
from utils.logger import setup_logger
from utils.model_enums import ModelName
from utils.constants import REQUEST_QUEUE
# from utils.database.convertor import simplify_objects
from utils.database.task import insert_task
from utils.rabbitmq.message import RabbitMQMessage
from utils.events import RabbitMQEvents


log = setup_logger(__name__)


async def get_all_models(request):
    return web.json_response([
        {
            "id": ModelName.LINEAR_REGRESSION.value,
            "model_name": "linear_regression",
        },
        {
            "id": ModelName.ELASTIC_NET.value,
            "model_name": "elastic_net",
        },
        {
            "id": ModelName.LASSO.value,
            "model_name": "lasso",
        },
        {
            "id": ModelName.RIDGE.value,
            "model_name": "ridge",
        }
    ], status=HTTPStatus.OK)


async def execute_model(request):
    log.info("322")
    if request.method == "POST":
        data = await request.json()
        log.info(data)
        model_id = data.get("model_id", "")
        model_params = data.get("model_params", {})
        action = data.get("action", "")
        task_id = uuid.uuid4().hex
        rabbitmq = request.app['rabbitmq']

        await insert_task(1, task_id)

        message = RabbitMQMessage(
            "api", RabbitMQEvents.REQUEST_MODEL_EXECUTION.value, {
                "task_id": task_id,
                "model_id": model_id,
                "model_params": model_params,
                "action": action
            }
        )
        await rabbitmq.publish(queue=REQUEST_QUEUE, body=message.to_json())

        return web.json_response(status=HTTPStatus.CREATED)
