from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.campaign import (
        Campaign,
        CampaignCreate,
        CampaignId,
        CampaignUpdate,
    )


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
    async def update_one(self, campaign_id: CampaignId, data: CampaignUpdate) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_current_amount(
        self, campaign_id: CampaignId, amount_to_add: float
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_top_campaigns(
        self, 
        limit: int = 50, 
        category: str | None = None, 
        sort_by: str = "current_amount"
    ) -> list[CampaignSchema]:
        pass

    @abstractmethod
    async def get_by_organizer_id(
        self, organizer_id: int, offset: int = 0, limit: int = 50
    ) -> list[Campaign]:
        raise NotImplementedError

    @abstractmethod
    async def add_report(self, campaign_id: int, data: "CampaignReportCreate") -> None:
        pass

    @abstractmethod
    async def get_reports(self, campaign_id: int) -> list["CampaignReportResponse"]:
        pass