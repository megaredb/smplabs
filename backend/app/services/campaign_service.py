from typing import TYPE_CHECKING
from app.schemas.campaign import CampaignReportCreate, CampaignReportResponse


if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork
    from app.schemas.campaign import (
        Campaign,
        CampaignCreate,
        CampaignId,
        CampaignUpdate,
    )
    from app.schemas.user import UserId


class CampaignService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def add_campaign(self, campaign: CampaignCreate) -> None:
        await self.uow.campaigns.add_one(campaign)

    async def get_campaign(self, campaign_id: CampaignId) -> Campaign | None:
        return await self.uow.campaigns.get_by_id(campaign_id)

    async def remove_campaign(self, campaign_id: CampaignId) -> None:
        await self.uow.campaigns.remove_by_id(campaign_id)

    async def update_campaign(
        self, campaign_id: CampaignId, data: CampaignUpdate
    ) -> None:
        await self.uow.campaigns.update_one(campaign_id, data)

    async def get_by_organizer(
        self, organizer_id: UserId, limit: int, offset: int
    ) -> list[Campaign]:
        return await self.uow.campaigns.get_by_organizer_id(organizer_id, offset, limit)

    async def get_top_campaigns(
        self, 
        limit: int = 10, 
        category: str | None = None, 
        sort_by: str = "current_amount"
    ) -> list[Campaign]:
        # Передаємо всі параметри далі в репозиторій (базу даних)
        return await self.uow.campaigns.get_top_campaigns(limit, category, sort_by)
    
    async def add_report(self, campaign_id: int, user_id: int, data: CampaignReportCreate) -> None:
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Збір не знайдено")
        if campaign.organizer_id != user_id:
            raise ValueError("Тільки організатор може додавати звіти")
        
        await self.uow.campaigns.add_report(campaign_id, data)
        await self.uow.commit()
        
        await self.uow.campaigns.add_report(campaign_id, data)

    async def get_reports(self, campaign_id: int) -> list[CampaignReportResponse]:
        return await self.uow.campaigns.get_reports(campaign_id)