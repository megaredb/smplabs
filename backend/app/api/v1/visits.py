import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Request, Response, status

from app.api.deps.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.visits import VisitCreate, VisitStatsResponse
from app.services.visit_service import VisitService
from app.schemas.user import UserDB
from app.core.users import possible_user

visits_router = APIRouter(prefix="/visits", tags=["visits"])


@visits_router.post("/")
async def create_visit(
    visit: VisitCreate,
    request: Request,
    response: Response,
    uow: IUnitOfWork = Depends(get_uow),
    possible_user: Annotated[UserDB, Depends(possible_user)] = None,
) -> Response:
    # Отримуємо session_id з куків. Якщо немає (новий унікальний відвідувач) — генеруємо
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,  # Захист від XSS (JS на фронтенді не матиме доступу до куки)
            max_age=60 * 60 * 24 * 365,  # Живе 1 рік
            samesite="lax",
        )

    # Викликаємо сервіс для збереження візиту в БД
    service = VisitService(uow)
    await service.record_visit(
        visit.page_url,
        session_id,
        user_id=possible_user.id if possible_user else None,
    )

    # Встановлюємо статус 201 та повертаємо модифікований Response
    response.status_code = status.HTTP_201_CREATED
    return response


@visits_router.get("/stats", response_model=VisitStatsResponse)
async def get_visit_stats(
    page_url: str,
    possible_user: Annotated[UserDB, Depends(possible_user)],
    uow: IUnitOfWork = Depends(get_uow),
):
    service = VisitService(uow)
    stats = await service.get_page_stats(
        page_url, user_id=possible_user.id if possible_user else None
    )
    return stats
