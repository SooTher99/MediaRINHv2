from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends, HTTPException, status

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Annotated

from conf.database import get_async_session
from conf.settings import settings
from src.account.models import UserModel

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(session:AsyncSession, **kwargs) -> UserModel:
    smtp = select(UserModel).filter_by(**kwargs)
    user = await session.scalars(smtp)
    return user.first()

async def authenticate_user(session:AsyncSession, email: str, raw_password: str) -> UserModel | None:
    user = await get_user(session, email=email)
    if not user:
        return None
    if not await user.check_password(raw_password):
        return None
    return user

async def create_access_token(data: dict, expires_min: int | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session:AsyncSession = Depends(get_async_session)) -> UserModel | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(session=session, id=id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> UserModel | None:
    if current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user