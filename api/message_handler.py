from bson import json_util

from utils.logger import setup_logger
from utils.rabbitmq.message import RabbitMQMessage

log = setup_logger(__name__)


async def _on_message(message, rabbitmq):
    message = json_util.loads(message.body)
    message_obj = RabbitMQMessage.from_json(message)


def rabbitmq_message_handler(rabbitmq):
    async def wrapper(message):
        await _on_message(message, rabbitmq)
    return wrapper
