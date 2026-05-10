from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.api.deps.user import get_user_db
from app.core.config import settings
from app.schemas.user import UserDB, UserId

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from app.core.fastapi_users_db_aiosqlite import AioSqliteUserDatabase


class UserManager(IntegerIDMixin, BaseUserManager[UserDB, UserId]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY


async def get_user_manager(
    user_db: Annotated[AioSqliteUserDatabase, Depends(get_user_db)],
) -> AsyncGenerator[UserManager]:
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="/auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[UserDB, UserId](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
