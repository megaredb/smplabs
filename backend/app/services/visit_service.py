from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork


class VisitService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def record_visit(
        self, page_url: str, session_id: str, user_id: int | None = None
    ) -> None:
        await self.uow.visits.add_visit(page_url, session_id, user_id)

    async def get_page_stats(self, page_url: str, user_id: int | None = None) -> dict:
        total = await self.uow.visits.get_total_visits(page_url)
        user_total = (
            await self.uow.visits.get_user_visits(page_url, user_id) if user_id else 0
        )

        return {
            "page_url": page_url,
            "total_visits": total,
            "user_visits": user_total,
        }
