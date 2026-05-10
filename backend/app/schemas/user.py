from datetime import datetime  # noqa: TC003
from typing import Literal

from fastapi_users import schemas
from pydantic import ConfigDict, Field

UserId = int
UserRole = Literal["donor", "organizer", "admin"]


class UserRead(schemas.BaseUser[UserId]):
    name: str
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    name: str
    role: UserRole = "donor"


class UserUpdate(schemas.BaseUserUpdate):
    name: str | None = None
    role: UserRole | None = None


class UserDB(UserRead):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
