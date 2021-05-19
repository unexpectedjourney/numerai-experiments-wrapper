from datetime import datetime

from bson import ObjectId

from .connector import database
from .convertor import str2object_id

_files_collection = database.files


async def get_all_files():
    cursor = _files_collection.find()
    return [d async for d in cursor]


async def get_file(_id):
    file = await _files_collection.find_one({"_id": ObjectId(_id)})
    if file:
        file['_id'] = _id
    return file


async def get_files_by_owner_id(owner_id):
    cursor = _files_collection.find({"owner_id": owner_id})
    return [d async for d in cursor]


async def insert_file(owner_id, title="", filename=""):
    timestamp = datetime.now().isoformat()
    return await _files_collection.insert_one(
        {
            "created_at": timestamp,
            "update_at": timestamp,
            "owner_id": owner_id,
            "title": title,
            "filename": filename
        }
    )


async def update_file(file_id, title=""):
    timestamp = datetime.now().isoformat()
    file_id = str2object_id(file_id)
    return await _files_collection.update_one(
        {
            "_id": file_id
        },
        {
            "$set": {
                "update_at": timestamp,
                "title": title
            }
        }
    )
