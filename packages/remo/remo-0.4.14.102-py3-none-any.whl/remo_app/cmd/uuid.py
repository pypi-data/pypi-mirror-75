import os
import uuid
from functools import lru_cache
from pathlib import Path

UUID_VAR = 'REMO_UUID'
UUID_FILE_PATH = str(Path.home().joinpath('tmp', '.remo', 'uuid'))


@lru_cache()
def get_uuid() -> str:
    value = os.getenv(UUID_VAR)
    if value:
        return value
    value = read_uuid_from_file()
    if value:
        return value

    value = str(uuid.uuid4())
    os.environ[UUID_VAR] = value
    write_uuid_to_file(value)
    return value


def set_uuid(uuid: str):
    os.environ[UUID_VAR] = uuid
    write_uuid_to_file(uuid)


def write_uuid_to_file(uuid: str):
    uuid_dir = os.path.dirname(UUID_FILE_PATH)
    if not os.path.exists(uuid_dir):
        os.makedirs(uuid_dir)
    with open(UUID_FILE_PATH, 'w') as f:
        f.write(uuid)


def read_uuid_from_file() -> str:
    if os.path.exists(UUID_FILE_PATH):
        with open(UUID_FILE_PATH) as f:
            return f.readline()
