from datetime import datetime

import pymongo

from utils.database.connector import database
from utils.database.convertor import (str2object_id, simplify_objects)

_history_collection = database.history


async def get_all_history_records():
    cursor = _history_collection.find()
    return [d async for d in cursor]


async def get_history_record(_id):
    record = await _history_collection.find_one({"_id": str2object_id(_id)})
    if record:
        record['_id'] = _id
    return record


async def get_history_records_by_owner_id(owner_id):
    cursor = _history_collection.find({"owner_id": owner_id}).sort(
        "created_at", pymongo.DESCENDING)
    return [d async for d in cursor]


async def insert_history_record(owner_id, type_):
    timestamp = datetime.now().isoformat()
    return await _history_collection.insert_one(
        {
            "created_at": timestamp,
            "owner_id": owner_id,
            "type": type_,
        }
    )
