
from typing import TYPE_CHECKING

from app.interfaces.repository.visits_repo import IVisitsRepository

if TYPE_CHECKING:
    import aiosqlite


class VisitsRepository(IVisitsRepository):
    def __init__(self, db: aiosqlite.Connection) -> None:
        self.db = db

    async def add_visit(
        self, page_url: str, session_id: str, user_id: int | None = None
    ) -> None:
        await self.db.execute(
            "INSERT INTO visits (page_url, session_id, user_id) VALUES (?, ?, ?)",
            (page_url, session_id, user_id),
        )
        # Коміт буде викликатися на рівні Unit of Work

    async def get_total_visits(self, page_url: str) -> int:
        async with self.db.execute(
            "SELECT COUNT(*) FROM visits WHERE page_url = ?", (page_url,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def get_user_visits(self, page_url: str, user_id: int) -> int:
        async with self.db.execute(
            "SELECT COUNT(*) FROM visits WHERE page_url = ? AND user_id = ?",
            (page_url, user_id),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
