import asyncio
import base64

import aiohttp_cors
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_swagger import setup_swagger
from cryptography import fernet
from message_handler import rabbitmq_message_handler
from middlewares.login import auth_middleware
from urls import get_routers

from utils.constants import RESPONSE_QUEUE
from utils.logger import setup_logger
from utils.rabbitmq.connector import RabbitMQConnection

log = setup_logger(__name__)


async def main():
    log.info("API application setup has started")
    app = web.Application(
        client_max_size=2 ** 50, middlewares=[auth_middleware])
    get_routers(app)

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    setup_swagger(app)

    # Cors
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    # Add all resources to `CorsConfig`.
    for route in list(app.router.routes()):
        log.info(route)
        cors.add(route)

    rabbitmq = RabbitMQConnection()
    await rabbitmq.connect()
    await rabbitmq.consume(RESPONSE_QUEUE, rabbitmq_message_handler(rabbitmq))
    app['rabbitmq'] = rabbitmq

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, port=8080)
    await site.start()

    log.info("API application setup has finished")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
