from fastapi import APIRouter

from app.api.v1.campaign import campaigns_router
from app.api.v1.transactions import transactions_router
from app.api.v1.users import users_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(
    transactions_router, prefix="/transactions", tags=["transactions"]
)
