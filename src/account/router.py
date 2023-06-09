from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.account.models import UserModel
from src.account.auth.dependencies import authenticate_user, create_access_token, get_current_active_user
from src.responses import RequestValidationError
from src.account.schemas import (TokenMessage,
                                 UserLogin,
                                 UserRegister,
                                 UserSuccessCreateMessage,
                                 UserPersonArea,
                                 UnauthorizedMessage)

from conf.settings import settings
from conf.database import get_async_session

router = APIRouter()


@router.post("/login", response_model=TokenMessage)
async def login_for_access_token(
        form_data: UserLogin,
        session: Annotated[get_async_session, Depends()]
):
    user = await authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(
        data={"sub": str(user.id)}, expires_min=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return TokenMessage(access_token=access_token)


@router.post("/register", response_model=UserSuccessCreateMessage)
async def register_user(
        form_data: UserRegister,
        session: AsyncSession = Depends(get_async_session)
):
    dict_data = form_data.dict(exclude={'password_repeat'}, exclude_none=True)
    smtp = select(UserModel.email).filter_by(email=dict_data.get('email')).limit(1)
    check_user = await session.scalars(smtp)
    if check_user.first():
        raise RequestValidationError(loc=['body', 'email'], typ='business_logic_error',
                                     msg='Пользователь с данной почтой уже существует')
    password = dict_data.pop('password')
    user = UserModel(**dict_data, is_active=True)
    await user.set_password(password)

    session.add(user)
    await session.commit()

    return UserSuccessCreateMessage()


@router.get("/users/me",
            response_model=UserPersonArea,
            responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnauthorizedMessage)})
async def read_users_me(
        current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
    return current_user
