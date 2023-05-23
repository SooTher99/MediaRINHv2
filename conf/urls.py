from fastapi import APIRouter
from src.account.router import router as account_router

api_router = APIRouter()
api_router.include_router(account_router, tags=["Account"])
