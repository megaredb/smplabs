from abc import ABC, abstractmethod


class IVisitsRepository(ABC):
    @abstractmethod
    async def add_visit(
        self, page_url: str, session_id: str, user_id: int | None
    ) -> None:
        pass

    @abstractmethod
    async def get_total_visits(self, page_url: str) -> int:
        pass

    @abstractmethod
    async def get_user_visits(self, page_url: str, user_id: int) -> int:
        pass
