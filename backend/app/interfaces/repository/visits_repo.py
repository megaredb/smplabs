from abc import ABC, abstractmethod
from typing import Optional


class IVisitsRepository(ABC):
    @abstractmethod
    async def add_visit(
        self, page_url: str, session_id: str, user_id: Optional[int]
    ) -> None:
        pass

    @abstractmethod
    async def get_total_visits(self, page_url: str) -> int:
        pass

    @abstractmethod
    async def get_user_visits(self, page_url: str, user_id: int) -> int:
        pass
