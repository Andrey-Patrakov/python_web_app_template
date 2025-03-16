from pydantic import BaseModel, Field, ConfigDict


class FileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    storage_id: str = Field(..., description='Идентификатор файла в хранилище')
    filename: str = Field(..., description='Имя файла')
    size: float = Field(..., description='Размер файла')
