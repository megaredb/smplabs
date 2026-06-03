import functools
import json
import time
from abc import ABC, abstractmethod
from typing import Any

import aiosqlite
import asyncpg


def log_db_operation(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        time.time()
        result = await func(*args, **kwargs)
        time.time()
        return result

    return wrapper


class Campaign(ABC):
    def __init__(self, data: dict) -> None:
        self.data = data


class VolunteerCampaign(Campaign):
    pass


class PrivateCampaign(Campaign):
    pass


class CampaignFactory:
    @staticmethod
    def create_campaign(campaign_type: str, data: dict[str, Any]) -> Campaign:
        if campaign_type == "volunteer":
            return VolunteerCampaign(data)
        if campaign_type == "private":
            return PrivateCampaign(data)
        msg = f"Unknown campaign type: {campaign_type}"
        raise ValueError(msg)


class CampaignDatabaseAdapter(ABC):
    @abstractmethod
    async def save(self, campaign: Campaign) -> None:
        pass


class SQLiteCampaignAdapter(CampaignDatabaseAdapter):
    def __init__(self, db_path: str = "local_campaigns.db") -> None:
        self.db_path = db_path

    async def init_table(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS campaigns (id INTEGER PRIMARY KEY, type TEXT, data TEXT)"
            )
            await db.commit()

    @log_db_operation
    async def save(self, campaign: Campaign) -> None:
        await self.init_table()
        campaign_type = campaign.__class__.__name__
        campaign_data_json = json.dumps(campaign.data)

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO campaigns (type, data) VALUES (?, ?)",
                (campaign_type, campaign_data_json),
            )
            await db.commit()


class PostgresCampaignAdapter(CampaignDatabaseAdapter):
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    async def init_table(self) -> None:
        try:
            conn = await asyncpg.connect(self.dsn)
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS campaigns (id SERIAL PRIMARY KEY, type TEXT, data JSONB)"
            )
            await conn.close()
        except Exception:
            pass

    @log_db_operation
    async def save(self, campaign: Campaign) -> None:
        await self.init_table()
        campaign_type = campaign.__class__.__name__
        campaign_data_json = json.dumps(campaign.data)

        try:
            conn = await asyncpg.connect(self.dsn)
            await conn.execute(
                "INSERT INTO campaigns (type, data) VALUES ($1, $2)",
                campaign_type,
                campaign_data_json,
            )
            await conn.close()
        except Exception:
            raise


class XMLCampaignAdapter(CampaignDatabaseAdapter):
    def __init__(self, file_path: str = "users_lab.xml") -> None:
        self.file_path = file_path

    def ensure_file_exists(self) -> None:
        import os
        import xml.etree.ElementTree as ET

        if not os.path.exists(self.file_path):
            root = ET.Element("users")
            tree = ET.ElementTree(root)
            tree.write(self.file_path, encoding="utf-8", xml_declaration=True)

    def parse_xml(self) -> dict:
        import xml.etree.ElementTree as ET

        self.ensure_file_exists()
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        def element_to_dict(elem):
            if len(elem) == 0:
                return elem.text.strip() if elem.text else ""
            res = {}
            if elem.attrib:
                res["_attributes"] = elem.attrib
            for child in elem:
                child_data = element_to_dict(child)
                if child.tag in res:
                    if not isinstance(res[child.tag], list):
                        res[child.tag] = [res[child.tag]]
                    res[child.tag].append(child_data)
                else:
                    res[child.tag] = child_data
            return res

        result = {}
        for child in root:
            child_data = element_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [child_data]

        return {"root": root.tag, "data": result}

    @log_db_operation
    async def save(self, campaign: Campaign) -> None:
        import xml.etree.ElementTree as ET

        self.ensure_file_exists()
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        campaign_el = ET.SubElement(root, "campaign", type=campaign.__class__.__name__)
        for key, value in campaign.data.items():
            child = ET.SubElement(campaign_el, key)
            child.text = str(value)

        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)


class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, amount: float) -> float:
        pass


class StandardFeeStrategy(FeeStrategy):
    def calculate_fee(self, amount: float) -> float:
        return amount * 0.01


class ZeroFeeStrategy(FeeStrategy):
    def calculate_fee(self, amount: float) -> float:
        return 0.0


class DonationCalculator:
    def __init__(self, strategy: FeeStrategy) -> None:
        self.strategy = strategy

    def process_donation(self, amount: float) -> dict:
        fee = self.strategy.calculate_fee(amount)
        total = amount + fee
        return {
            "original_amount": amount,
            "fee": fee,
            "total_amount": total,
            "strategy_used": self.strategy.__class__.__name__,
        }
