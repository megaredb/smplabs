from http import HTTPStatus
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.transaction import get_transaction_service
from app.api.deps.user import get_user_service
from app.core.users import current_superuser, current_user
from app.schemas.transaction import TransactionResponse
from app.schemas.user import UserDB, UserId, UserRead
from app.services.transaction_service import TransactionService

if TYPE_CHECKING:
    from app.services.user_service import UserService  # noqa: TC004

users_router = APIRouter()


@users_router.get("/me")
async def get_me(
    _current_user: Annotated[UserDB, Depends(current_user)],
) -> UserRead:
    return UserRead.model_validate(
        _current_user,
        from_attributes=True,
    )


@users_router.get("/{user_id}")
async def get_user(
    user_id: UserId,
    user_service: Annotated[UserService, Depends(get_user_service)],
    _current_superuser: Annotated[UserDB, Depends(current_superuser)],
) -> UserRead:
    user = await user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return UserRead.model_validate(user, from_attributes=True)


@users_router.get("/")
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    _current_superuser: Annotated[UserDB, Depends(current_superuser)],
    offset: int = 0,
    limit: int = 10,
) -> list[UserRead]:
    users = await user_service.get_users(limit=limit, offset=offset)
    return [UserRead.model_validate(user, from_attributes=True) for user in users]


@users_router.delete("/{user_id}")
async def remove_user(
    user_id: UserId,
    user_service: Annotated[UserService, Depends(get_user_service)],
    _current_superuser: Annotated[UserDB, Depends(current_superuser)],
) -> None:
    await user_service.remove_user(user_id)

@users_router.post("/verify", status_code=HTTPStatus.OK)
async def verify_account(
    _current_user: Annotated[UserDB, Depends(current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> dict:
    await user_service.verify_user(_current_user.id)
    return {"message": "Успішно верифіковано"}