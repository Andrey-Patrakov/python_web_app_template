from typing import AsyncGenerator
from src.config import settings
from minio import Minio
from math import ceil


def get_storage(secure: bool = False):
    return Minio(
        endpoint=settings.storage.URL,
        access_key=settings.storage.ACCESS_KEY,
        secret_key=settings.storage.SECRET_KEY,
        secure=secure)


def make_bucket(bucket):
    client = get_storage()
    if client.bucket_exists(bucket):
        return False

    client.make_bucket(bucket, settings.REGION_NAME)
    return True


async def download_from_storage(
        name: str, secure: bool = False) -> AsyncGenerator:

    BUCKET = settings.storage.BUCKET
    CHUNK_SIZE = settings.storage.CHUNK_SIZE

    client = get_storage()
    total_size = client.stat_object(BUCKET, name).size
    chunks = ceil(total_size / CHUNK_SIZE)

    for chunk in range(chunks):
        offset = chunk * CHUNK_SIZE
        response = client.get_object(
            bucket_name=BUCKET,
            object_name=name,
            offset=offset,
            length=CHUNK_SIZE)

        yield response.read()
