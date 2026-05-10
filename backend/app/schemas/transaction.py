from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


def validate_id(v: int) -> int:
    if v <= 0:
        msg = "ID must be a positive integer"
        raise ValueError(msg)
    return v


def validate_optional_id(v: int | None) -> int | None:
    if v is None:
        return None
    return validate_id(v)


type TransactionId = Annotated[int, AfterValidator(validate_id)]
type CampaignId = Annotated[int, AfterValidator(validate_id)]
type DonorId = Annotated[int | None, AfterValidator(validate_optional_id)]
type Amount = Annotated[float, Field(gt=0)]


class TransactionBase(BaseModel):
    campaign_id: CampaignId
    donor_id: DonorId = None
    amount: Amount
    comment: str | None = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: TransactionId
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionResponse(Transaction):
    pass
