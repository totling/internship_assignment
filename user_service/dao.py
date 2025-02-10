from user_service.base import BaseDAO
from user_service.models import User


class UsersDAO(BaseDAO):
    model = User
