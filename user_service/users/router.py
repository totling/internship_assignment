from typing import Optional

from fastapi import APIRouter, Depends, Response

from user_service.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException, UserNotExistException
from user_service.users.auth import authenticate_user, create_access_token, get_password_hash
from user_service.users.dao import UsersDAO
from user_service.users.dependencies import get_current_user, get_admin
from user_service.users.models import Users
from user_service.users.schemas import SUserAuth, SUserRegister, SUserCreate, SUser

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router_admin_manage = APIRouter(
    prefix="/admin/manage-users",
    tags=["Управление пользователями"],
)


@router_auth.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(name=user_data.name, email=user_data.email, password=hashed_password)


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router_admin_manage.post("/create")
async def create_user(user_data: SUserCreate, user: Users = Depends(get_admin)):
    hashed_password = user_data.password
    await UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )


@router_admin_manage.patch("/update/{user_id}")
async def update_user_info(
        user_id: int,
        name: Optional[str],
        email: Optional[str],
        password: Optional[str],
        is_admin: Optional[bool],
        user: Users = Depends(get_admin)
):
    updating_user = await UsersDAO.find_by_id(user_id)
    if not updating_user:
        raise UserNotExistException

    if password:
        hashed_password = get_password_hash(password)

    await UsersDAO.update(user_id, name=name, email=email, password=hashed_password, is_admin=is_admin)

    return {
        "message": "Информация пользователя успешно обновлена"
    }


@router_admin_manage.get("/read/{user_id}")
async def read_user_info(user_id: int, user: Users = Depends(get_admin)) -> SUser:
    return await UsersDAO.find_by_id(user_id)


@router_admin_manage.delete("/delete/{user_id}")
async def delete_user(user_id: int, user: Users = Depends(get_admin)):
    await UsersDAO.delete(id=user_id)
