import os
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from app.schemas.transaction import TransactionResponse


class InvoiceService:
    def __init__(self) -> None:
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_html_invoice(
        self, transaction: TransactionResponse, donor_name: str | None = None
    ) -> str:
        template = self.env.get_template("invoice.html")
        return template.render(transaction=transaction, donor_name=donor_name)
