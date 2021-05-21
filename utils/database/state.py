from datetime import datetime

import pymongo

from .connector import database
from .convertor import str2object_id

_states_collection = database.states


async def get_all_states():
    cursor = _states_collection.find()
    return [d async for d in cursor]


async def get_one_state(state_id):
    return await _states_collection.find({"_id": state_id})


async def get_states_by_models(state_id):
    cursor = _states_collection.find({"state_id": state_id}).sort(
        "created_at", pymongo.DESCENDING)
    return [d async for d in cursor]


async def insert_state(filepath, model_id, model_params):
    return await _states_collection.insert_one(
        {
            "filepath": filepath,
            "model_id": model_id,
            "model_params": model_params,
            "created_at": datetime.now().isoformat(),
        }
    )
