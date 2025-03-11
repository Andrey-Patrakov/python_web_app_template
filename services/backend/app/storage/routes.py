from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from .storage import Storage


router = APIRouter(prefix='/storage', tags=['Файловое хранилище'])
storage = Storage()


@router.post('/upload')
async def upload(file: UploadFile = File()):
    print(file.filename)
    storage.upload(file.filename, file.file, file.size)
    return {'message': 'Файл успешно загружен!'}


@router.get('/download/{name}')
async def download(name) -> StreamingResponse:
    response = StreamingResponse(
        storage.download(name),
        media_type='application/octet-stream')

    return response
