from datetime import datetime

import jwt
from fastapi import Depends, Request

from user_service.config import settings
from user_service.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserNotExistException, UserNotAdminException,
)
from user_service.dao import UsersDAO
from user_service.models import User


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.PyJWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserNotExistException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserNotExistException

    return user


def get_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise UserNotAdminException
    return user
