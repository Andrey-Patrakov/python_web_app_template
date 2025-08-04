from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from .utils import download_from_storage


router = APIRouter(prefix='/api', tags=['Работа с хранилищем'])


@router.get('/download/{name}')
def download(name: str) -> StreamingResponse:
    return StreamingResponse(
        download_from_storage(name=name),
        media_type='application/octet-stream')
