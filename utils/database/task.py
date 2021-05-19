from datetime import datetime

from .connector import database

_tasks_collection = database.tasks


async def get_all_tasks():
    cursor = _tasks_collection.find()
    return [d async for d in cursor]


async def get_one_task(task_id):
    return await _tasks_collection.find_one({"task_id": task_id})


async def insert_task(type, owner_id, file_version_id):
    timestamp = datetime.now().isoformat()
    return await _tasks_collection.insert_one(
        {
            "type": type,
            "created_at": timestamp,
            "updated_at": timestamp,
            "is_completed": False,
            "owner_id": owner_id,
            "file_version_id": file_version_id,
        }
    )


async def complete_task(task_id):
    return await _tasks_collection.update(
        {"task_id": task_id},
        {
            "$set": {
                "is_completed": True
            }
        }
    )
