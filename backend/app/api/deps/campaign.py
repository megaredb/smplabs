from typing import Annotated

from fastapi import Depends

from app.api.deps.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork  # noqa: TC001
from app.services.campaign_service import CampaignService


def get_campaign_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
) -> CampaignService:
    return CampaignService(uow)
