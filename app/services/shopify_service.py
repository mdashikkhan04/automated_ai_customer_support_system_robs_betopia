# File: app/services/shopify_service.py

from typing import Optional
import requests

from app.config import get_settings

settings = get_settings()


class ShopifyService:
    def __init__(self):
        self.store_domain = settings.SHOPIFY_STORE_DOMAIN
        self.access_token = settings.SHOPIFY_ACCESS_TOKEN

    def _base_url(self) -> str:
        return f"https://{self.store_domain}/admin/api/2023-10"

    def _headers(self) -> dict:
        return {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
        }

    def find_order_by_email_and_number(
        self, email: str, order_number: Optional[str] = None
    ) -> Optional[dict]:
        """
        Basic example: search orders by email.
        For production: refine with order_number or other filters.
        """
        try:
            url = f"{self._base_url()}/orders.json"
            params = {"email": email, "status": "any", "limit": 5}
            resp = requests.get(url, headers=self._headers(), params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            orders = data.get("orders", [])

            if not orders:
                return None

            if order_number:
                for o in orders:
                    if str(o.get("order_number")) == str(order_number):
                        return o
            # fallback: return the most recent one
            return orders[0]
        except Exception as e:
            # In production: log error
            return None

    def format_order_status_message(self, order: dict) -> str:
        """Build a human-readable status summary for the chatbot."""
        order_number = order.get("order_number")
        financial_status = order.get("financial_status")
        fulfillment_status = order.get("fulfillment_status") or "unfulfilled"

        shipping_address = order.get("shipping_address") or {}
        city = shipping_address.get("city", "")
        country = shipping_address.get("country", "")

        return (
            f"I found your Shopify order #{order_number}. "
            f"Payment status: {financial_status}. "
            f"Fulfillment status: {fulfillment_status}. "
            f"Shipping to {city}, {country}. "
            "If you need detailed tracking info, I can connect you with a human support agent."
        )


shopify_service = ShopifyService()
