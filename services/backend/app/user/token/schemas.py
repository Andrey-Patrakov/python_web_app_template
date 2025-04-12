from pydantic import BaseModel, Field


class EmailVerificationSchema(BaseModel):
    token: str = Field(..., description='Токен для верификации электронной почты') # noqa
