from aiohttp import web

from utils.logger import setup_logger

log = setup_logger(__name__)


async def status(request):
    """
        ---
        description: This end-point allow to test that service is up.
        tags:
        - Health check
        produces:
        - text/plain
        responses:
            "200":
                description: successful operation. Return "pong" text
            "405":
                description: invalid HTTP Method
    """
    log.info("Status function has been triggered")
    return web.json_response({
        "status": "ok",
        "database": "ok",
        "api": "ok",
        "core": "ok"
    })
