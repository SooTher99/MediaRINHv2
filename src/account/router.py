from fastapi import APIRouter, Depends, UploadFile, File
from conf.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.account.models import UserModel

router = APIRouter()

@router.post('/test/')
async def test(session:AsyncSession = Depends(get_async_session), file: UploadFile = File(...)):
    user_obj = UserModel(first_name="Вася",
                          avatar=file.file,
                          email='sdfdfsdfsfd@gmail.com',
                          password='qwe123456')
    session.add(user_obj)
    await session.commit()
    await session.close()

    print('*'*40)
    print(user_obj.email)
    print(user_obj.avatar)
    print('*' * 40)

    return {'field': 'hello'}

