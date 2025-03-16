from app.database import BaseDAO
from .models import File


class FileDAO(BaseDAO):
    model = File
