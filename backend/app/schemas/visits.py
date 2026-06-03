
from pydantic import BaseModel


class VisitCreate(BaseModel):
    page_url: str


class VisitStatsResponse(BaseModel):
    page_url: str
    total_visits: int
    user_visits: int | None = 0
