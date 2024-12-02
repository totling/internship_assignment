from sqlalchemy import Column, Integer, String, Boolean

from user_service.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    def __str__(self):
        return f"User:{self.name}\nEmail:{self.email}"
