from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from fastapi.responses import StreamingResponse
from .storage import Storage
from .dao import FileDAO
from .schemas import FileSchema, StorageSchema
from app.user import get_current_user


router = APIRouter(prefix='/storage', tags=['Файловое хранилище'])
storage = Storage()


@router.get('/status')
async def get_storage_status(
        user=Depends(get_current_user)) -> StorageSchema:

    return {
        'used_space': await FileDAO.used_space(user.id),
        'available_space': user.available_space}


@router.get('/list')
async def get_files_list(
        user=Depends(get_current_user)) -> list[FileSchema]:

    return await FileDAO.find_all(user_id=user.id)


@router.post('/upload')
async def upload(
        file: UploadFile = File(),
        user=Depends(get_current_user)) -> FileSchema:

    used_space = await FileDAO.used_space(user.id)
    used_space += file.size / 1024**2
    if used_space > user.available_space:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail='Закончилось доступное пользователю место на диске!')

    storage_id = storage.upload(file.file, file.size)
    await FileDAO.add(
        filename=file.filename,
        size=file.size,
        storage_id=storage_id,
        user_id=user.id)

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
