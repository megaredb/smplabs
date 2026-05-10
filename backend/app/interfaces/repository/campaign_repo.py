from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.campaign import Campaign, CampaignCreate, CampaignId


class ICampaignRepository(ABC):
    @abstractmethod
    async def add_one(self, data: CampaignCreate) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, campaign_id: CampaignId) -> Campaign | None:
        raise NotImplementedError

    @abstractmethod
    async def remove_by_id(self, campaign_id: CampaignId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_top_campaigns(self, limit: int = 10) -> list[Campaign]:
        raise NotImplementedError
