from user_service.dao.base import BaseDAO
from user_service.users.models import User


class UsersDAO(BaseDAO):
    model = User
