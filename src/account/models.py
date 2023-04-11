from typing import Optional, AnyStr

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import validates
from sqlalchemy import event

import os
from PIL import Image
from datetime import datetime
from pathlib import Path

import shutil
import uuid

from src.account.types import EmailType
from conf.database import Base
from conf.settings import settings

class UserModel(Base):
    __tablename__  = "account_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name : Mapped[str] = mapped_column(String(64))
    last_name : Mapped[Optional[str]] = mapped_column(String(64))
    email : Mapped[str] = mapped_column(EmailType, unique=True, index=True)
    password : Mapped[str] = mapped_column(String(128))

    date_joined : Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login : Mapped[Optional[datetime]]

    is_active : Mapped[bool] = mapped_column(server_default='f', default=False)

    is_superuser : Mapped[bool] = mapped_column(server_default='f', default=False)
    is_staff : Mapped[bool] = mapped_column(server_default='f', default=False)

    post_agreement : Mapped[bool] = mapped_column(server_default='t', default=True)
    avatar : Mapped[Optional[str]] = mapped_column(String(256))

    @validates('password')
    def validate_password(self, key, password) -> str:
        if len(password) < 8:
            raise ValueError('Password too short, minimum number of characters 8')
        return password

def convert_to_webp(source):
    """Convert image to webp.

    Args:
        source (pathlib.Path): Path to source image

    Returns:
        pathlib.Path: path to new image
    """

    image = Image.open(source)  # Open image
    image.save(source, format="webp")  # Convert image to webp

    return source

def upload_to(prefix:str):
    now = datetime.utcnow()
    return f'{now.year}/{now.month}/{prefix}'

@event.listens_for(UserModel, 'before_insert')
def save_avatar(mapper, connect, target):
    path_avatar = upload_to('avatar')
    file_name = Path(str(uuid.uuid4())).with_suffix('.webp')
    absolute_path = settings.MEDIA_DIR.joinpath(path_avatar)

    os.makedirs(absolute_path, 0o777, exist_ok=True)
    with open (absolute_path.joinpath(file_name), 'wb') as avatar:
        shutil.copyfileobj(target.avatar, avatar)
        convert_to_webp(absolute_path.joinpath(file_name))

    target.avatar = f'{path_avatar}/{file_name}.webp'

