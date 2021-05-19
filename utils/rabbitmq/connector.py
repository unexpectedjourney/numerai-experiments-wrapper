import asyncio
import os
import time

import aio_pika

from utils.logger import setup_logger
from utils.rabbitmq.message import create_rabbitmq_message

log = setup_logger(__name__)


class RabbitMQConnection:
    def __init__(self):
        self.channel = None
        self.loop = asyncio.get_event_loop()
        self._host = os.environ.get("RABBITMQ_HOSTNAME", "rabbitmq")
        self._port = int(os.environ.get("RABBITMQ_PORT", "80"))
        self._username = os.environ.get("RABBITMQ_USER", "")
        self._password = os.environ.get("RABBITMQ_PASSWORD", "")

    async def create_connection(self):
        connection = None
        while connection is None:
            try:
                connection = await aio_pika.connect_robust(
                    host=self._host, port=self._port, login=self._username,
                    password=self._password, loop=self.loop
                )
            except ConnectionError:
                log.info('Connecting to rabbitmq...')
                time.sleep(1)
                continue
            return connection

    async def connect(self):
        log.info("Start connecting to rabbitmq")

        connection = await self.create_connection()
        log.info(connection)
        self.channel = await connection.channel()
        log.info("Finished connecting to rabbitmq")

    async def consume(self, queue, callback):
        consumer_queue = await self.channel.declare_queue(
            queue,
            auto_delete=True
        )
        return await consumer_queue.consume(callback, no_ack=True)

    async def publish(self, queue, body):
        message = create_rabbitmq_message(body)
        return await self.channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=queue
        )
