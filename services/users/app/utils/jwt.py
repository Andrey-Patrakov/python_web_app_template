from fastapi import Request, Response
from datetime import datetime, timedelta
from app.config import settings
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JOSEError


class TokenMissingError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class TokenCorruptedError(Exception):
    pass


class JWTToken:
    algorithm: str
    key: str
    secret: str
    expires_delta: timedelta | None = None
    secure: bool = True

    def __init__(self, request: Request, response: Response):
        self._request = request
        self._response = response

    def generate_and_save(self, data: dict):
        token = self.generate(data)
        self.save(token)
        return token

    def read_and_decode(self):
        token = self.read()
        return self.decode(token)

    def generate(self, data: dict) -> str:
        expires_at = None
        if self.expires_delta is not None:
            expires_at = datetime.now() + self.expires_delta

        to_encode = data.copy()
        to_encode.update({'exp': expires_at, 'iat': datetime.now()})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def read(self) -> str:
        token = self._request.cookies.get(self.key)
        if not token:
            raise TokenMissingError('Token is missing in headers.')

        return token

    def decode(self, token: str) -> dict:
        try:
            token = jwt.decode(token, self.secret, algorithms=self.algorithm)

        except ExpiredSignatureError:
            raise TokenExpiredError('Token is expired.')

        except JOSEError:
            raise TokenCorruptedError('Token is corrupted.')

        return token

    def save(self, token: str):
        self._response.set_cookie(
            key=self.key,
            value=token,
            httponly=self.secure,
            secure=self.secure,
            max_age=self.expires_delta.total_seconds())

    def delete(self) -> str:
        try:
            token = self.read_and_decode()
        except (TokenMissingError, TokenExpiredError, TokenCorruptedError):
            pass

        self._response.delete_cookie(self.key)
        return token


class AccessToken(JWTToken):
    algorithm = settings.ALGORITHM
    key = 'acctok'
    secret = settings.SECRET_KEY
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    secure = settings.SECURE


class RefreshToken(JWTToken):
    algorithm = settings.ALGORITHM
    key = 'rfstok'
    secret = settings.SECRET_KEY
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    secure = settings.SECURE
