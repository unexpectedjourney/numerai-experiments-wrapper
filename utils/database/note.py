from datetime import datetime

import pymongo
from bson import ObjectId

from utils.database.connector import database
from utils.database.convertor import str2object_id

_notes_collection = database.notes


async def get_all_notes():
    cursor = _notes_collection.find()
    return [d async for d in cursor]


async def get_note(_id):
    note = await _notes_collection.find_one({"_id": ObjectId(_id)})
    if note:
        note['_id'] = _id
    return note


async def get_notes_by_file_id(file_id):
    cursor = _notes_collection.find({"file_id": file_id}).sort(
        "created_at", pymongo.DESCENDING)
    return [d async for d in cursor]


async def insert_note(owner_id, file_id, text=""):
    timestamp = datetime.now().isoformat()
    return await _notes_collection.insert_one(
        {
            "created_at": timestamp,
            "update_at": timestamp,
            "owner_id": owner_id,
            "file_id": file_id,
            "text": text,
        }
    )


async def delete_note(note_id):
    note_id = str2object_id(note_id)
    return await _notes_collection.delete_one({"_id": note_id})
