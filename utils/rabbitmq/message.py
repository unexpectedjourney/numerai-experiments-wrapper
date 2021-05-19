import datetime
import json

from bson import json_util


class RabbitMQMessage:
    def __init__(self, service_name, message_type, message_params=None):
        self.service_name = service_name
        self.message_type = message_type
        self.message_params = {} if message_params is None else message_params

    def to_json(self):
        return {
            'service_name': self.service_name,
            'message_type': self.message_type,
            'message_params': self.message_params,
        }

    @classmethod
    def from_json(cls, json_message: dict):
        return RabbitMQMessage(
            json_message.get("service_name"),
            json_message.get("message_type"),
            json_message.get("message_params"),
        )


def create_rabbitmq_message(body: dict):
    return json.dumps({
        **body,
        "timestamp": datetime.datetime.now().isoformat()
    }, default=json_util.default).encode()
