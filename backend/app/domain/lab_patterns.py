import time
from abc import ABC, abstractmethod
from typing import Dict, Any


# 1. Decorator: @log_db_operation
def log_db_operation(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"[DB Operation Start] {func.__name__} at {start_time}")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"[DB Operation End] {func.__name__} took {end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper


# 2. Strategy: FeeStrategy
class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, amount: float) -> float:
        pass


class StandardFeeStrategy(FeeStrategy):
    def calculate_fee(self, amount: float) -> float:
        return amount * 0.01  # 1% fee


class ZeroFeeStrategy(FeeStrategy):
    def calculate_fee(self, amount: float) -> float:
        return 0.0  # 0% fee


# 3. Factory: CampaignFactory
class Campaign(ABC):
    def __init__(self, data: dict):
        self.data = data


class VolunteerCampaign(Campaign):
    pass


class PrivateCampaign(Campaign):
    pass


class CampaignFactory:
    @staticmethod
    def create_campaign(campaign_type: str, data: Dict[str, Any]) -> Campaign:
        if campaign_type == "volunteer":
            return VolunteerCampaign(data)
        elif campaign_type == "private":
            return PrivateCampaign(data)
        else:
            raise ValueError(f"Unknown campaign type: {campaign_type}")


# 4. Adapter: CampaignDatabaseAdapter
class CampaignDatabaseAdapter(ABC):
    @abstractmethod
    def save(self, campaign: Campaign) -> None:
        pass


class PostgresCampaignAdapter(CampaignDatabaseAdapter):
    @log_db_operation
    def save(self, campaign: Campaign) -> None:
        print(f"Saving campaign to Postgres: {campaign.data}")


class XMLCampaignAdapter(CampaignDatabaseAdapter):
    def __init__(self, file_path: str = "users_lab.xml"):
        self.file_path = file_path

    def ensure_file_exists(self):
        import os
        import xml.etree.ElementTree as ET

        if not os.path.exists(self.file_path):
            root = ET.Element("users")
            tree = ET.ElementTree(root)
            tree.write(self.file_path, encoding="utf-8", xml_declaration=True)
            print(f"File {self.file_path} created with root <users>.")

    def parse_xml(self) -> dict:
        import os
        import xml.etree.ElementTree as ET

        self.ensure_file_exists()

        tree = ET.parse(self.file_path)
        root = tree.getroot()

        def element_to_dict(elem):
            # Якщо немає дочірніх елементів, повертаємо текст
            if len(elem) == 0:
                return elem.text.strip() if elem.text else ""

            res = {}
            # Якщо є атрибути, можемо додати їх
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

        # Збираємо список усіх елементів у кореневому тегу
        result = {}
        for child in root:
            child_data = element_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [
                    child_data
                ]  # Завжди робимо список для однотипних елементів, наприклад <user>

        print(f"Parsed XML data: {result}")
        return {"root": root.tag, "data": result}

    @log_db_operation
    def save(self, campaign: Campaign) -> None:
        import xml.etree.ElementTree as ET

        self.ensure_file_exists()

        tree = ET.parse(self.file_path)
        root = tree.getroot()

        # Create a new element based on campaign data
        campaign_el = ET.SubElement(root, "campaign")
        for key, value in campaign.data.items():
            child = ET.SubElement(campaign_el, key)
            child.text = str(value)

        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)
        print(f"Saving campaign to XML file: {campaign.data}")
