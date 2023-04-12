from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from conf.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.account.models import UserModel
from src.account.utils import authenticate_user, create_access_token
from src.account.schemas import Token, UserLogin

from conf.settings import settings

router = APIRouter()

@router.post('/test/')
async def test(session:AsyncSession = Depends(get_async_session), file: UploadFile = File(...)):
    user_obj = UserModel(first_name="Вася",
                          email='tolikberdyev1@gmail.com')
    await user_obj.set_password('qwe123456')
    session.add(user_obj)
    await session.commit()
    await session.close()

    print('*'*40)
    print(user_obj.email)
    print('*' * 40)

    return {'field': 'hello'}

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: UserLogin, session : Annotated[get_async_session, Depends()]
):
    user = await authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(
        data={"sub": user.id}, expires_min=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "Bearer"}