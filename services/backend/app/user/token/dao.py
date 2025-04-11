from .models import Token
from app.database import BaseDAO


class TokenDAO(BaseDAO):
    model = Token
