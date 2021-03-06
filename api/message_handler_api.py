from bson import json_util

from utils.logger import setup_logger
from utils.rabbitmq.message import RabbitMQMessage
from utils.events import RabbitMQEvents
from utils.database.task import complete_task
from utils.database.state import insert_state


log = setup_logger(__name__)


async def _on_message(message, rabbitmq):
    message = json_util.loads(message.body)
    message_obj = RabbitMQMessage.from_json(message)

    message_type = message_obj.message_type
    message_params = message_obj.message_params

    if not message_type or not message_params:
        return

    if message_type == RabbitMQEvents.RESPONSE_MODEL_EXECUTION.value:
        log.info(RabbitMQEvents.RESPONSE_MODEL_EXECUTION.name)
        task_id = message_params.get("task_id")
        model_id = message_params.get("model_id")

        filename = message_params.get("filename")
        model_params = message_params.get("model_params")

        await insert_state(filename, model_id, model_params)
        await complete_task(task_id)

    else:
        log.warn("Unknown message_type was found")


def rabbitmq_message_handler(rabbitmq):
    async def wrapper(message):
        await _on_message(message, rabbitmq)
    return wrapper
