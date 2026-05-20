from typing import TYPE_CHECKING, Any

from app.interfaces.repository.campaign_repo import ICampaignRepository
from app.schemas.campaign import Campaign as CampaignSchema, Campaign
from app.schemas.campaign import CampaignId

if TYPE_CHECKING:
    import aiosqlite

    from app.schemas.campaign import CampaignCreate, CampaignUpdate


class CampaignRepository(ICampaignRepository):
    def __init__(self, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_one(self, data: CampaignCreate) -> None:
        query = """
        INSERT INTO campaigns (organizer_id, title, description, target_amount)
        VALUES (?, ?, ?, ?)
        """
        await self.connection.execute(
            query,
            (data.organizer_id, data.title, data.description, data.target_amount),
        )

    async def get_by_id(self, campaign_id: CampaignId) -> CampaignSchema | None:
        query = """
        SELECT id, organizer_id, title, description, target_amount, current_amount,
               created_at
        FROM campaigns
        WHERE id = ?
        """
        async with self.connection.execute(query, (campaign_id,)) as cursor:
            row = await cursor.fetchone()

            if not row:
                return None

            return CampaignSchema(
                id=row[0],
                organizer_id=row[1],
                title=row[2],
                description=row[3],
                target_amount=row[4],
                current_amount=row[5],
                created_at=row[6],
            )

    async def remove_by_id(self, campaign_id: CampaignId) -> None:
        query = """
        DELETE FROM campaigns
        WHERE id = ?
        """
        await self.connection.execute(query, (campaign_id,))

    async def update_one(self, campaign_id: CampaignId, data: CampaignUpdate) -> None:
        fields = []
        values: list[Any] = []
        if data.title is not None:
            fields.append("title = ?")
            values.append(data.title)
        if data.description is not None:
            fields.append("description = ?")
            values.append(data.description)
        if data.target_amount is not None:
            fields.append("target_amount = ?")
            values.append(data.target_amount)

        if not fields:
            return

        query = f"UPDATE campaigns SET {', '.join(fields)} WHERE id = ?"
        values.append(campaign_id)
        await self.connection.execute(query, tuple(values))

    async def update_current_amount(
        self, campaign_id: CampaignId, amount_to_add: float
    ) -> None:
        query = """
        UPDATE campaigns 
        SET current_amount = current_amount + ? 
        WHERE id = ?
        """
        await self.connection.execute(query, (amount_to_add, campaign_id))

    async def get_by_organizer_id(
        self, organizer_id: int, offset: int = 0, limit: int = 50
    ) -> list[Campaign]:
        query = """
                SELECT id, organizer_id, title, description, target_amount, current_amount,
                       created_at
                FROM campaigns
                WHERE organizer_id = ?
                ORDER BY current_amount DESC
                LIMIT ? OFFSET ? \
                """
        async with self.connection.execute(
            query, (organizer_id, limit, offset)
        ) as cursor:
            rows = await cursor.fetchall()

        return [CampaignSchema(**row) for row in rows]

    async def get_top_campaigns(self, limit: int = 10) -> list[CampaignSchema]:
        query = """
            SELECT id, organizer_id, title, description, target_amount, current_amount, 
            created_at
            FROM Campaigns
            ORDER BY current_amount DESC
            LIMIT ?
        """
        async with self.connection.execute(query, (limit,)) as cursor:
            rows = await cursor.fetchall()

        return [
            CampaignSchema(
                id=row[0],
                organizer_id=row[1],
                title=row[2],
                description=row[3],
                target_amount=row[4],
                current_amount=row[5],
                created_at=row[6],
            )
            for row in rows
        ]
