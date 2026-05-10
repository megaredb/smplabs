from fastapi import APIRouter

from app.core.users import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead

api_router = APIRouter()

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
api_router.include_router(
    fastapi_users.get_reset_password_router(),
)
api_router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
