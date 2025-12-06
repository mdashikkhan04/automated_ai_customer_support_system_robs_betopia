"""
File: app/services/clickbank_service.py

ClickBank integration service (orders2/list and orders2/{receipt}).
"""
import requests
import xml.etree.ElementTree as ET
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from app.config import get_settings
from app.logger import logger

settings = get_settings()


class ClickBankService:
    """
    ClickBank integration helper.
    Uses ClickBank REST endpoints (orders2/list and orders2/{receipt}).
    Expects CLICKBANK_API_KEY in .env as plain API string.
    """

    def __init__(self):
        self.api_key = getattr(settings, "CLICKBANK_API_KEY", None)
        if not self.api_key:
            logger.warning("ClickBankService: CLICKBANK_API_KEY not set in environment")
        # Base v1.3 REST endpoint (adjust if your account uses another URL)
        self.base = "https://api.clickbank.com/rest/1.3"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.api_key or "",
            "Accept": "application/xml",
            "User-Agent": "HardChews-Chatbot/1.0"
        }

    def _parse_orders_list_xml(self, xml_text: str) -> List[Dict]:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            logger.error("ClickBankService: XML parse error: %s", e)
            return []

        orders = []
        for od in root.findall('.//orderData'):
            orders.append({
                "receipt": od.findtext("receipt"),
                "email": od.findtext("email"),
                "paymentStatus": od.findtext("paymentStatus"),
                "totalAmount": od.findtext("totalAmount"),
                "vendor": od.findtext("vendor"),
                "orderDate": od.findtext("orderDate"),
            })
        return orders

    def list_orders(self, vendor: str, start_date: str, end_date: str) -> Optional[List[Dict]]:
        url = f"{self.base}/orders2/list"
        params = {"vendor": vendor, "startDate": start_date, "endDate": end_date}
        try:
            resp = requests.get(url, headers=self._headers(), params=params, timeout=20)
            resp.raise_for_status()
            orders = self._parse_orders_list_xml(resp.text)
            logger.info("ClickBankService: found %d orders", len(orders))
            return orders
        except requests.HTTPError as he:
            logger.error("ClickBank list_orders HTTP error: %s ; body: %s", he, resp.text if 'resp' in locals() else "")
            return None
        except Exception as e:
            logger.error("ClickBank list_orders error: %s", e)
            return None

    def find_order(self, receipt: Optional[str] = None, email: Optional[str] = None) -> Optional[Dict]:
        """
        Find a single order by receipt or by email fallback (searches recent orders).
        Returns order dict or None.
        """
        # If receipt provided, try direct lookup
        if receipt:
            receipt_clean = receipt.strip()
            # Sanitize: basic check
            if len(receipt_clean) < 3:
                logger.warning("ClickBankService.find_order: invalid receipt provided: %s", receipt_clean)
            else:
                try:
                    url = f"{self.base}/orders2/{receipt_clean}"
                    resp = requests.get(url, headers=self._headers(), timeout=15)
                    resp.raise_for_status()
                    root = ET.fromstring(resp.text)
                    od = root.find('.//orderData')
                    if od is None:
                        logger.info("ClickBankService.find_order: no orderData in response for %s", receipt_clean)
                    else:
                        return {
                            "receipt": od.findtext("receipt"),
                            "email": od.findtext("email"),
                            "paymentStatus": od.findtext("paymentStatus"),
                            "totalAmount": od.findtext("totalAmount"),
                            "vendor": od.findtext("vendor"),
                            "orderDate": od.findtext("orderDate"),
                        }
                except requests.HTTPError as he:
                    logger.error("ClickBank find_order HTTP error: %s ; body: %s", he, resp.text if 'resp' in locals() else "")
                except Exception as e:
                    logger.error("ClickBank find_order error: %s", e)

        # If no receipt found or not provided, try listing recent orders and match by email
        if email:
            try:
                # default: search last 30 days
                end_date = datetime.utcnow().date()
                start_date = end_date - timedelta(days=30)
                orders = self.list_orders(vendor="hardchews", start_date=start_date.isoformat(), end_date=end_date.isoformat())
                if not orders:
                    return None
                # find best match by email
                for o in orders:
                    if o.get("email") and o.get("email").lower() == email.lower():
                        return o
                # no exact match; return first order that contains the email substring
                for o in orders:
                    if o.get("email") and email.lower() in o.get("email").lower():
                        return o
                return None
            except Exception as e:
                logger.error("ClickBank find_order by email error: %s", e)
                return None

        return None

    def format_status(self, order: Dict) -> str:
        if not order:
            return "No order information available."
        return (
            f"Receipt: {order.get('receipt', 'N/A')} | "
            f"Status: {order.get('paymentStatus', 'N/A')} | "
            f"Amount: {order.get('totalAmount', 'N/A')} | "
            f"Date: {order.get('orderDate', 'N/A')}"
        )


# Singleton instance
clickbank_service = ClickBankService()
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
