from fastapi import APIRouter, Depends
from conf.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get('/test/')
async def test(session:AsyncSession = Depends(get_async_session)):
    print(session)
    return {'field': 'hello'}

