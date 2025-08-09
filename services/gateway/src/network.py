import aiohttp
import asyncio

from aiohttp import MultipartWriter
from starlette.datastructures import UploadFile

from .config import settings


def get_file_writer(file: UploadFile, name: str):
    with aiohttp.MultipartWriter('form-data') as writer:
        part = writer.append(file.file)
        part.set_content_disposition(
            'form-data', name=name, filename=file.filename)

        return writer


async def make_request(
        url: str,
        method: str,
        json_data: dict = None,
        data: MultipartWriter = None,
        cookies: dict = None):

    async with asyncio.timeout(settings.GATEWAY_TIMEOUT):
        async with aiohttp.ClientSession() as session:
            request = getattr(session, method)
            async with request(
                    url,
                    cookies=cookies,
                    json=json_data,
                    data=data) as response:

                data = await response.json()
                return data, response
