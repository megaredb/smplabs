from pydantic import BaseModel
from typing import Optional


class VisitCreate(BaseModel):
    page_url: str


class VisitStatsResponse(BaseModel):
    page_url: str
    total_visits: int
    user_visits: Optional[int] = 0
