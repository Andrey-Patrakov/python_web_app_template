from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from .storage import Storage
from .dao import FileDAO
from .schemas import FileSchema
from app.users import get_current_user


router = APIRouter(prefix='/storage', tags=['Файловое хранилище'])
storage = Storage()


@router.get('/list')
async def get_files_list(
        user=Depends(get_current_user)) -> list[FileSchema]:

    return await FileDAO.find_all(user_id=user.id)


@router.post('/upload')
async def upload(
        file: UploadFile = File(),
        user=Depends(get_current_user)) -> FileSchema:

    storage_id = str(uuid4())
    await FileDAO.add(
        filename=file.filename,
        size=file.size,
        storage_id=storage_id,
        user_id=user.id)

    storage.upload(storage_id, file.file, file.size)

    return {
        'storage_id': storage_id,
        'filename': file.filename,
        'size': file.size}


@router.get('/download/{name}')
async def download(name) -> StreamingResponse:
    response = StreamingResponse(
        storage.download(name),
        media_type='application/octet-stream')

    return response


@router.delete('/{storage_id}')
async def delete_file(
        storage_id: str,
        user=Depends(get_current_user)) -> dict:

    deleted = await FileDAO.delete(user_id=user.id, storage_id=storage_id)
    if deleted:
        storage.delete(storage_id)
        return {'message': 'Файл успешно удалён!'}

    return {'message': 'Не удалось удалить файл!'}
