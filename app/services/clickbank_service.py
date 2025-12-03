# File: app/services/clickbank_service.py

from typing import Optional
import requests

from app.config import get_settings
from app.logger import logger

settings = get_settings()


class ClickBankService:
    """
    Minimal ClickBank orders API client.
    Used to look up order / receipt info for customers who bought via ClickBank.
    """

    def __init__(self):
        self.dev_key = settings.CLICKBANK_DEV_KEY
        self.clerk_key = settings.CLICKBANK_CLERK_KEY
        self.base_url = "https://api.clickbank.com/rest/1.3/orders"

    def _headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Authorization": f"{self.dev_key}:{self.clerk_key}",
        }

    def find_order(self, email: str = "", receipt: str = "") -> Optional[dict]:
        """
        Search ClickBank order by email or receipt number.
        At least one of email or receipt should be provided.
        """
        params: dict = {}
        if email:
            params["email"] = email
        if receipt:
            params["receipt"] = receipt

        if not params:
            logger.warning("ClickBankService.find_order called without email/receipt")
            return None

        try:
            logger.info(f"Searching ClickBank order with params={params}")
            resp = requests.get(
                f"{self.base_url}/find",
                headers=self._headers(),
                params=params,
                timeout=12,
            )
            resp.raise_for_status()
            data = resp.json()
            orders = data.get("orderData", [])

            if not orders:
                logger.info("No ClickBank orders found for given params")
                return None

            # Latest/first order
            return orders[0]

        except Exception as e:
            logger.error(f"Error calling ClickBank orders API: {e}")
            return None

    def format_status(self, order: dict) -> str:
        """
        Build a human-readable status message for the chatbot from ClickBank order data.
        """
        receipt = order.get("receipt", "N/A")
        status = order.get("paymentStatus", "Unknown")
        amount = order.get("totalAmount", "N/A")
        currency = order.get("currency", "USD")

        return (
            f"I found your ClickBank order (Receipt: {receipt}). "
            f"Payment status: {status}. "
            f"Total amount: {amount} {currency}. "
            "If you need a detailed delivery or tracking update, "
            "a human support agent can review your order further."
        )


clickbank_service = ClickBankService()
