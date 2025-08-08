from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from storage import Storage


router = APIRouter(prefix='/api', tags=['Работа с хранилищем'])


@router.get('/download/{name}')
def download(name: str) -> StreamingResponse:
    storage = Storage()
    return StreamingResponse(
        storage.download(name),
        media_type='application/octet-stream')
