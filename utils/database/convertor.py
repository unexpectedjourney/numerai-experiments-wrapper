from bson import ObjectId


def str2object_id(id_):
    if isinstance(id_, str):
        return ObjectId(id_)
    return id_


def object_id2str(id_):
    if isinstance(id_, str):
        return id_
    return str(id_)


def simplify_objects(obj, fields=("_id",)):
    for field in fields:
        id_ = obj.get(field)
        if id_ is None:
            continue
        obj[field] = object_id2str(id_)
    return obj
