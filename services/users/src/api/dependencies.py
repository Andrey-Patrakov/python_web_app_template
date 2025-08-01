from typing import Annotated
from fastapi import Depends
from src.services.users import UsersService
from src.services.mail import EmailService
from src.services.tokens import TokenService

UsersDep = Annotated[UsersService, Depends(UsersService)]
EmailDep = Annotated[EmailService, Depends(EmailService)]
TokenDep = Annotated[TokenService, Depends(TokenService)]
