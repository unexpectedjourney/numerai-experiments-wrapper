import os

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    host=os.environ.get("MONGODB_HOSTNAME", "mongodb"),
    port=int(os.environ.get("MONGODB_PORT", "80")),
    username=os.environ.get("MONGODB_ROOT_USERNAME", ""),
    password=os.environ.get("MONGODB_ROOT_PASSWORD", ""),
)

database = client.colorization
