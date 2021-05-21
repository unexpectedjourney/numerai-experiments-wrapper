from bson import json_util
from utils.constants import RESPONSE_QUEUE
from utils.events import RabbitMQEvents
from utils.logger import setup_logger
from utils.rabbitmq.message import RabbitMQMessage
from model_execution import execute_model

log = setup_logger(__name__)


async def _on_message(message, rabbitmq):
    message = json_util.loads(message.body)
    message_obj = RabbitMQMessage.from_json(message)

    message_type = message_obj.message_type
    message_params = message_obj.message_params

    if not message_type or not message_params:
        return

    if message_type == RabbitMQEvents.REQUEST_MODEL_EXECUTION.value:
        log.info(RabbitMQEvents.REQUEST_MODEL_EXECUTION.name)

        filename, task_id, model_id, model_params = await execute_model(message_params)

        message = RabbitMQMessage(
            "core",
            RabbitMQEvents.RESPONSE_MODEL_EXECUTION.value,
            {
                "filename": filename,
                "task_id": task_id,
                "model_id": model_id,
                "model_params": model_params,
            }
        )
        await rabbitmq.publish(
            queue=RESPONSE_QUEUE, body=message.to_json())
        log.info("Message was sent\n")
    else:
        log.warn("Unknown message_type was found")


def rabbitmq_message_handler(rabbitmq):
    async def wrapper(message):
        await _on_message(message, rabbitmq)

    return wrapper
