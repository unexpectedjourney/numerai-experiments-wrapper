from enum import Enum


class RabbitMQEvents(Enum):
    REQUEST_MODEL_EXECUTION = 1
    RESPONSE_MODEL_EXECUTION = 2
