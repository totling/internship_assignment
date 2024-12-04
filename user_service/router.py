from fastapi import APIRouter, Depends, Response, UploadFile, File

from config import settings
from exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException, UserNotExistException
from kafka import get_producer
from auth import authenticate_user, create_access_token, get_password_hash
from dao import UsersDAO
from dependencies import get_current_user, get_admin
from models import User
from schemas import SUserAuth, SUserCreate, SUser, SUserUpdate

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router_admin_manage = APIRouter(
    prefix="/admin/manage-users",
    tags=["Управление пользователями"],
)


router_doc = APIRouter(
    prefix="/doc",
    tags=["Работа с файлами"]
)


@router_auth.post("/register")
async def register_user(user_data: SUserCreate):
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
    response.set_cookie("user_access_token", access_token, httponly=True)
    return access_token


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")


@router_admin_manage.post("/create")
async def create_user(user_data: SUserCreate, user: User = Depends(get_admin)):
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )


@router_admin_manage.patch("/update/{user_id}", description="Эндпоинт позволяет обновить информацию о пользователе"
                                                            ", все параметры кроме user_id - опциональны")
async def update_user_info(
        user_id: int,
        user_data: SUserUpdate,
        user: User = Depends(get_admin)
):
    updating_user = await UsersDAO.find_by_id(user_id)
    if not updating_user:
        raise UserNotExistException

    user_info = user_data.dict(exclude_unset=True)

    if "password" in user_info:
        user_info["password"] = get_password_hash(user_info["password"])

    await UsersDAO.update(user_id, **user_info)

    return {
        "message": "Информация пользователя успешно обновлена"
    }


@router_admin_manage.get("/read/{user_id}")
async def read_user_info(user_id: int, user: User = Depends(get_admin)) -> SUser:
    return await UsersDAO.find_by_id(user_id)


@router_admin_manage.delete("/delete/{user_id}")
async def delete_user(user_id: int, user: User = Depends(get_admin)):
    await UsersDAO.delete(id=user_id)
    return {
        "message": "Пользователь успешно удалён"
    }


@router_doc.post("/upload")
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    file_content = await file.read()

    message = {
        "user_id": user.id,
        "filename": file.filename,
        "file_content": file_content.decode('latin-1')
    }

    producer = await get_producer()

    await producer.send_and_wait(settings.TOPIC_NAME, message)

    return {"message": f"Файл '{file.filename}' успешно отправлен для пользователя {user.name}"}
