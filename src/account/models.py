from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import validates
from sqlalchemy import func
from sqlalchemy_file import ImageField

from datetime import datetime

from src.account.types import EmailType
from conf.database import Base

class UserModel(Base):
    __tablename__  = "account_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name : Mapped[str] = mapped_column(String(64))
    last_name : Mapped[Optional[str]] = mapped_column(String(64))
    email : Mapped[str] = mapped_column(EmailType, unique=True)
    password : Mapped[str] = mapped_column(String(128))

    date_joined : Mapped[datetime] = mapped_column(server_default=func.utcnow())
    last_login : Mapped[Optional[datetime]]

    is_active : Mapped[bool] = mapped_column(server_default='f', default=False)

    is_superuser : Mapped[bool] = mapped_column(server_default='f', default=False)
    is_staff : Mapped[bool] = mapped_column(server_default='f', default=False)

    post_agreement : Mapped[bool] = mapped_column(server_default='t', default=True)
    avatar : Mapped[Optional[ImageField]]

    @validates('password')
    def validate_password(self, key, password) -> str:
        if len(password) < 8:
            raise ValueError('Password too short, minimum number of characters 8')
        return password