from typing import Annotated

from catalog.infrastructure.fastapi.user import User
from fastapi import Depends, Request


def get_user(request: Request) -> User:
    return request.user


UserDep = Annotated[User, Depends(get_user)]
