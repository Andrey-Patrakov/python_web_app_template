from typing import Annotated
from fastapi import Depends
from src.services.users import UsersService

UsersDep = Annotated[UsersService, Depends(UsersService)]
