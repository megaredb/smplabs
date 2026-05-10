from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork
    from app.schemas.campaign import Campaign, CampaignCreate, CampaignId


class CampaignService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def add_campaign(self, campaign: CampaignCreate) -> None:
        await self.uow.campaigns.add_one(campaign)

    async def get_campaign(self, campaign_id: CampaignId) -> Campaign | None:
        return await self.uow.campaigns.get_by_id(campaign_id)

    async def remove_campaign(self, campaign_id: CampaignId) -> None:
        await self.uow.campaigns.remove_by_id(campaign_id)

    async def get_top_campaigns(self, limit: int = 10) -> list[Campaign]:
        return await self.uow.campaigns.get_top_campaigns(limit)
