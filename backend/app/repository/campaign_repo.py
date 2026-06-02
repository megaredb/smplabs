from typing import TYPE_CHECKING, Any

from app.interfaces.repository.campaign_repo import ICampaignRepository
from app.schemas.campaign import Campaign as CampaignSchema, Campaign
from app.schemas.campaign import CampaignId

from app.schemas.campaign import CampaignReportCreate, CampaignReportResponse

if TYPE_CHECKING:
    import aiosqlite

    from app.schemas.campaign import CampaignCreate, CampaignUpdate


class CampaignRepository(ICampaignRepository):
    def __init__(self, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_one(self, data: CampaignCreate) -> None:
        query = """
            INSERT INTO campaigns (organizer_id, title, description, target_amount, end_date, image_url, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        await self.connection.execute(
            query,
            (data.organizer_id, data.title, data.description, data.target_amount, data.end_date, data.image_url, data.category),
        )

    async def get_by_id(self, campaign_id: CampaignId) -> CampaignSchema | None:
        # Ми робимо LEFT JOIN, щоб підтягнути ім'я (u.name) з таблиці users
        query = """
            SELECT c.id, c.organizer_id, c.title, c.description, c.target_amount, c.current_amount,
                   c.created_at, c.end_date, c.image_url, c.category, u.name
            FROM campaigns c
            LEFT JOIN users u ON c.organizer_id = u.id
            WHERE c.id = ?
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
                end_date=row[7],
                image_url=row[8],
                category=row[9],
                organizer_name=row[10] # ДОДАНО ІМ'Я
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
        if data.end_date is not None:
            fields.append("end_date = ?")
            values.append(data.end_date)
        if data.image_url is not None:
            fields.append("image_url = ?")
            values.append(data.image_url)

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
                       created_at, end_date, image_url, category
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

    async def get_top_campaigns(
        self, 
        limit: int = 50, 
        category: str | None = None, 
        sort_by: str = "current_amount"
    ) -> list[CampaignSchema]:
        # НОВЕ: Змінили SELECT та додали LEFT JOIN, щоб тягнути ім'я
        query = """
            SELECT c.id, c.organizer_id, c.title, c.description, c.target_amount, c.current_amount,
                   c.created_at, c.end_date, c.image_url, c.category, u.name
            FROM campaigns c
            LEFT JOIN users u ON c.organizer_id = u.id
        """
        params = []
        
        # Фільтрація по категорії
        if category:
            query += " WHERE c.category = ?"
            params.append(category)

        # Сортування
        if sort_by == "date":
            query += " ORDER BY c.created_at DESC"
        elif sort_by == "target":
            query += " ORDER BY c.target_amount DESC"
        else:
            query += " ORDER BY c.current_amount DESC"

        query += " LIMIT ?"
        params.append(limit)

        async with self.connection.execute(query, tuple(params)) as cursor:
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
                    end_date=row[7],
                    image_url=row[8],
                    category=row[9],
                    organizer_name=row[10] # ТЕПЕР ІМ'Я Є ТУТ!
                )
                for row in rows
            ]
    
    async def add_report(self, campaign_id: int, data: CampaignReportCreate) -> None:
        query = """
            INSERT INTO campaign_reports (campaign_id, title, description, image_url)
            VALUES (?, ?, ?, ?)
        """
        await self.connection.execute(query, (campaign_id, data.title, data.description, data.image_url))

    async def get_reports(self, campaign_id: int) -> list[CampaignReportResponse]:
        query = """
            SELECT id, campaign_id, title, description, image_url, created_at
            FROM campaign_reports
            WHERE campaign_id = ?
            ORDER BY created_at DESC
        """
        async with self.connection.execute(query, (campaign_id,)) as cursor:
            rows = await cursor.fetchall()
            return [
                CampaignReportResponse(
                    id=row[0],
                    campaign_id=row[1],
                    title=row[2],
                    description=row[3],
                    image_url=row[4],
                    created_at=row[5]
                ) for row in rows
            ]
