from fastapi import HTTPException, status


class BaseUserServiceException(HTTPException):
    status_code = 404
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectEmailOrPasswordException(BaseUserServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class UserAlreadyExistsException(BaseUserServiceException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class TokenExpiredException(BaseUserServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(BaseUserServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BaseUserServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserNotExistException(BaseUserServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotAdminException(BaseUserServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав"
