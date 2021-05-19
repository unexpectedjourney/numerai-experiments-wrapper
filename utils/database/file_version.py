from datetime import datetime

import pymongo

from .connector import database
from .convertor import str2object_id

_file_versions_collection = database.file_versions


async def get_all_file_versions():
    cursor = _file_versions_collection.find()
    return [d async for d in cursor]


async def get_one_file_version(file_version_id):
    return await _file_versions_collection.find({"_id": file_version_id})


async def get_file_versions_by_file_id(file_id):
    cursor = _file_versions_collection.find({"file_id": file_id}).sort(
        "created_at", pymongo.DESCENDING)
    return [d async for d in cursor]


async def insert_file_version(filepath, file_id):
    return await _file_versions_collection.insert_one(
        {
            "filepath": filepath,
            "file_id": str2object_id(file_id),
            "created_at": datetime.now().isoformat(),
        }
    )
