from __future__ import annotations

from http import HTTPStatus
from typing import Annotated  # TYPE_CHECKING тут більше не потрібен

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.campaign import get_campaign_service

from app.schemas.campaign import CampaignId, CampaignResponse, CampaignCreate

from app.services.campaign_service import CampaignService

campaigns_router = APIRouter()


@campaigns_router.post("/", status_code=HTTPStatus.CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
) -> None:
    try:
        await campaign_service.add_campaign(campaign_data)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Помилка при створенні збору: {str(e)}",
        )


@campaigns_router.get("/top")
async def get_top_campaigns(
    campaign_service: Annotated[CampaignService, Depends(get_campaign_service)],
    limit: int = 10,
) -> list[CampaignResponse]:
    campaigns = await campaign_service.get_top_campaigns(limit)
    return [CampaignResponse.model_validate(c) for c in campaigns]


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
