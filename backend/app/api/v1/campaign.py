from http import HTTPStatus
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.campaign import get_campaign_service
from app.core.users import current_user
from app.schemas.campaign import (
    CampaignCreate,
    CampaignId,
    CampaignResponse,
    CampaignUpdate,
)

from app.schemas.campaign import (
    CampaignReportCreate,
    CampaignReportResponse,
    ComplaintCreate,
)

if TYPE_CHECKING:
    from app.schemas.user import UserDB
    from app.services.campaign_service import CampaignService

campaigns_router = APIRouter()


@campaigns_router.post("/", status_code=HTTPStatus.CREATED)
async def create_campaign(
    _current_user: Annotated[UserDB, Depends(current_user)],
    campaign_data: CampaignCreate,
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> None:
    campaign_data.organizer_id = _current_user.id
    await campaign_service.add_campaign(campaign_data)


@campaigns_router.get("/top")
async def get_top_campaigns(
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
    limit: int = 10,
    category: str | None = None,  # НОВИЙ ПАРАМЕТР
    sort_by: str = "current_amount",  # НОВИЙ ПАРАМЕТР
) -> list[CampaignResponse]:
    # Передай ці параметри в campaign_service.get_top_campaigns
    campaigns = await campaign_service.get_top_campaigns(limit, category, sort_by)
    return [CampaignResponse.model_validate(c) for c in campaigns]


@campaigns_router.delete("/{campaign_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_campaign(
    campaign_id: CampaignId,
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> None:
    campaign = await campaign_service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Campaign not found"
        )

    await campaign_service.remove_campaign(campaign_id)


@campaigns_router.get("/my")
async def get_my_campaigns(
    _current_user: Annotated[UserDB, Depends(current_user)],
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
    offset: int = 0,
    limit: int = 10,
) -> list[CampaignResponse]:
    campaigns = await campaign_service.get_by_organizer(_current_user.id, limit, offset)
    return [CampaignResponse.model_validate(c) for c in campaigns]


@campaigns_router.patch("/{campaign_id}")
async def update_campaign(
    campaign_id: CampaignId,
    campaign_data: CampaignUpdate,
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> CampaignResponse:
    campaign = await campaign_service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Campaign not found"
        )

    await campaign_service.update_campaign(campaign_id, campaign_data)
    updated_campaign = await campaign_service.get_campaign(campaign_id)
    return CampaignResponse.model_validate(updated_campaign)


@campaigns_router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: CampaignId,
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> CampaignResponse:
    campaign = await campaign_service.get_campaign(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Campaign not found"
        )

    return CampaignResponse.model_validate(campaign)


@campaigns_router.post("/{campaign_id}/reports", status_code=HTTPStatus.CREATED)
async def create_report(
    campaign_id: CampaignId,
    report_data: CampaignReportCreate,
    _current_user: Annotated[UserDB, Depends(current_user)],
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> None:
    try:
        await campaign_service.add_report(campaign_id, _current_user.id, report_data)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(e))


@campaigns_router.get("/{campaign_id}/reports")
async def get_reports(
    campaign_id: CampaignId,
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> list[CampaignReportResponse]:
    return await campaign_service.get_reports(campaign_id)


@campaigns_router.post("/{campaign_id}/complaints", status_code=HTTPStatus.CREATED)
async def create_complaint(
    campaign_id: CampaignId,
    complaint_data: ComplaintCreate,
    _current_user: Annotated[UserDB, Depends(current_user)],
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> None:
    await campaign_service.add_complaint(
        campaign_id, _current_user.id, complaint_data.reason
    )
