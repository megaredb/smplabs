from fastapi import APIRouter

from .auth import api_router as auth_router
from .v1 import api_router as api_v1_router

api_router = APIRouter()

api_router.include_router(api_v1_router, prefix="/v1", tags=["api"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
