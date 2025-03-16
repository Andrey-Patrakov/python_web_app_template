from typing import AsyncGenerator
from typing import BinaryIO
from minio import Minio
from app.config import settings
from math import ceil


class Storage:

    def __init__(self, secure: bool = False):
        self.client = Minio(
            settings.storage.URL,
            access_key=settings.storage.ACCESS_KEY,
            secret_key=settings.storage.SECRET_KEY,
            secure=secure)

        self.bucket = settings.storage.BUCKET
        self.location = settings.REGION_NAME
        self.CHUNK_SIZE = 524288

    def upload(self, name: str, file: BinaryIO, length: int):
        return self.client.put_object(self.bucket, name, file, length=length)

    def stats(self, name: str):
        return self.client.stat_object(self.bucket, name)

    async def download(self, name: str) -> AsyncGenerator:
        total_size = self.stats(name).size
        chunks = ceil(total_size / self.CHUNK_SIZE)
        for chunk in range(chunks):
            offset = chunk * self.CHUNK_SIZE
            response = self.client.get_object(
                self.bucket, name, offset=offset, length=self.CHUNK_SIZE)

            yield response.read()

    def delete(self, name: str):
        self.client.remove_object(self.bucket, name)

    def make_bucket(self, name):
        if self.client.bucket_exists(name):
            return False

        self.client.make_bucket(name, self.location)
        return True
