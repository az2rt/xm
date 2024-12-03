import uuid

def is_valid_uuid(uuid_exp):
    try:
        uuid_obj = uuid.UUID(uuid_exp, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_exp
