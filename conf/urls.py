from fastapi import APIRouter
from src.account.router import router as account_router

api_router = APIRouter()
api_router.include_router(account_router, tags=["test"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
