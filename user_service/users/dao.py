from user_service.dao.base import BaseDAO
from user_service.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
