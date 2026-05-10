from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict


def validate_campaign_id(v: int) -> int:
    if v <= 0:
        msg = "ID must be positive"
        raise ValueError(msg)
    return v


def validate_campaign_amount(v: float) -> float:
    if v < 0:
        msg = "Target amount must be positive"
        raise ValueError(msg)
    return v


type CampaignId = Annotated[int, AfterValidator(validate_campaign_id)]
type TargetAmount = Annotated[float, AfterValidator(validate_campaign_amount)]


class CampaignBase(BaseModel):
    organizer_id: int
    title: str
    description: str | None = None
    target_amount: TargetAmount


class CampaignCreate(CampaignBase):
    pass


class Campaign(CampaignBase):
    id: CampaignId
    current_amount: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CampaignResponse(CampaignBase):
    id: CampaignId
    current_amount: float
    created_at: datetime
