from pydantic import BaseModel, Field, ConfigDict


class FileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    storage_id: str = Field(..., description='Идентификатор файла в хранилище')
    filename: str = Field(..., description='Имя файла')
    size: float = Field(..., description='Размер файла')


class StorageSchema(BaseModel):
    used_space: int = Field(..., description='Занятое место на диске')
    available_space: int = Field(..., description='Доступное место на диске')
