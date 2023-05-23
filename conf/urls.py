from fastapi import APIRouter
from src.account.router import router as account_router
from src.chat.router import router as chat_router

api_router = APIRouter()
api_router.include_router(account_router, tags=["Account"])

template_router = APIRouter()
template_router.include_router(chat_router, tags=["Chat"])
