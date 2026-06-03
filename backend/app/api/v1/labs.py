from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.core.lab_patterns import (
    CampaignDatabaseAdapter,
    CampaignFactory,
    DonationCalculator,
    PostgresCampaignAdapter,
    SQLiteCampaignAdapter,
    StandardFeeStrategy,
    ZeroFeeStrategy,
)

lab_router = APIRouter()

sqlite_adapter = SQLiteCampaignAdapter("demo_database.db")
postgres_adapter = PostgresCampaignAdapter(
    "postgresql://neondb_owner:npg_Bn53CoglGspw@ep-wispy-moon-ag5vi2zx-pooler.c-2.eu-central-1.aws.neon.tech/yevhentest?sslmode=require&channel_binding=require"
)


@lab_router.post("/api/lab/demo-adapter", tags=["lab-5-patterns"])
async def demonstrate_db_adapters(
    db_type: Annotated[str, Query(description="Введи 'sqlite' або 'postgres'")] = "sqlite",
):
    campaign = CampaignFactory.create_campaign(
        campaign_type="volunteer",
        data={"title": "Збір на тепловізори", "goal_amount": 150000, "currency": "UAH"},
    )

    adapter: CampaignDatabaseAdapter
    if db_type.lower() == "sqlite":
        adapter = sqlite_adapter
    elif db_type.lower() == "postgres":
        adapter = postgres_adapter
    else:
        raise HTTPException(
            status_code=400,
            detail="Невідомий тип БД. Використовуйте 'sqlite' або 'postgres'",
        )

    try:
        await adapter.save(campaign)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка бази даних: {e!s}")

    return {
        "status": "success",
        "message": "Кампанію успішно збережено!",
        "used_adapter": adapter.__class__.__name__,
        "campaign_data": campaign.data,
    }


class CalculateFeeRequest(BaseModel):
    amount: float
    campaign_type: str


@lab_router.post("/api/lab/calculate-fee", tags=["lab-5-patterns"])
async def calculate_fee(request: CalculateFeeRequest):
    if request.campaign_type.lower() == "volunteer":
        calculator = DonationCalculator(ZeroFeeStrategy())
    elif request.campaign_type.lower() == "private":
        calculator = DonationCalculator(StandardFeeStrategy())
    else:
        raise HTTPException(
            status_code=400,
            detail="Unknown campaign_type. Must be 'volunteer' or 'private'",
        )

    return calculator.process_donation(request.amount)
