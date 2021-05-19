from datetime import datetime

from bson.objectid import ObjectId

from .connector import database

_users_collection = database.users


async def get_all_users():
    cursor = _users_collection.find()
    return [d async for d in cursor]


async def get_user(_id=None, username=None):
    if _id is not None:
        user = await _users_collection.find_one({"_id": ObjectId(_id)})
        if user is not None:
            user["_id"] = str(user["_id"])
        return user
    else:
        return await _users_collection.find_one({"username": username})


async def insert_user_if_not_exist(username, hashed_password, first_name="",
                                   last_name="", email=""):
    timestamp = datetime.now().isoformat()
    return await _users_collection.update_one(
        {
            "username": username
        },
        {
            "$setOnInsert": {
                "username": username,
                "password": hashed_password,
                "created_at": timestamp,
                "updated_at": timestamp,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        },
        upsert=True
    )


async def update_user(username, first_name, last_name, email):
    timestamp = datetime.now().isoformat()
    return await _users_collection.update_one(
        {
            "username": username
        },
        {
            "$set": {
                "updated_at": timestamp,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        }
    )