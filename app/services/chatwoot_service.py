import os
import logging
from typing import Optional, Any, Dict

import requests

logger = logging.getLogger(__name__)


class ChatwootClient:
    """Minimal Chatwoot client wrapper.

    Reads configuration from env vars:
      - CHATWOOT_API_TOKEN (preferred)
      - CHATWOOT_API_KEY (fallback, if token not set)
      - CHATWOOT_ACCOUNT_ID (required)
      - CHATWOOT_URL (optional, default: https://app.chatwoot.com)
      - CHATWOOT_INBOX_ID (optional)

    This client provides two simple helpers:
      - create_conversation(contact_email, contact_name, message)
      - send_message_to_conversation(conversation_id, content)

    Note: Keep the API key out of source control. Put it in `.env` or a secret vault.
    """

    def __init__(self) -> None:
        # Prefer token; fallback to api key for backward compatibility
        self.api_key = (
            os.environ.get("CHATWOOT_API_TOKEN")
            or os.environ.get("CHATWOOT_API_KEY")
        )
        self.account_id = os.environ.get("CHATWOOT_ACCOUNT_ID")
        self.url = os.environ.get("CHATWOOT_URL", "https://app.chatwoot.com").rstrip("/")
        self.inbox_id = os.environ.get("CHATWOOT_INBOX_ID")

        if not self.api_key or not self.account_id:
            logger.warning(
                "CHATWOOT_API_TOKEN/CHATWOOT_API_KEY or CHATWOOT_ACCOUNT_ID not set — Chatwoot disabled"
            )
            self.enabled = False
            self.headers = {}
        else:
            self.enabled = True
            # Use official Chatwoot header: api_access_token
            self.headers = {
                "Content-Type": "application/json",
                "api_access_token": self.api_key,
            }

    def _account_base(self) -> str:
        return f"{self.url}/api/v1/accounts/{self.account_id}"

    def create_conversation(
        self,
        contact_email: Optional[str],
        contact_name: Optional[str],
        message: str,
    ) -> Dict[str, Any]:
        """Create a conversation and send the initial message.

        Returns the parsed JSON response on success. Raises requests.HTTPError on failure.
        """
        if not self.enabled:
            raise RuntimeError("Chatwoot client not configured")

        endpoint = f"{self._account_base()}/conversations"
        payload: Dict[str, Any] = {
            # source_id is an arbitrary string to identify origin of the conversation
            "source_id": f"bot-{contact_email or 'anon'}",
            "contact": {"name": contact_name or "Automated User", "email": contact_email},
            "message": {"content": message},
        }

        if self.inbox_id:
            try:
                payload["inbox_id"] = int(self.inbox_id)
            except Exception:
                payload["inbox_id"] = self.inbox_id

        # remove nulls
        payload = {k: v for k, v in payload.items() if v is not None}

        logger.debug("Creating conversation on Chatwoot: %s", endpoint)
        resp = requests.post(endpoint, headers=self.headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def send_message_to_conversation(
        self,
        conversation_id: int,
        content: str,
        message_type: str = "outgoing",
    ) -> Dict[str, Any]:
        """Send a message to an existing Chatwoot conversation.

        `message_type` is usually "outgoing" for agent/bot messages.
        """
        if not self.enabled:
            raise RuntimeError("Chatwoot client not configured")

        endpoint = f"{self._account_base()}/conversations/{conversation_id}/messages"
        payload = {"content": content, "message_type": message_type}
        logger.debug("Posting message to Chatwoot conversation %s", conversation_id)
        resp = requests.post(endpoint, headers=self.headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()


# Singleton client instance for simple imports
chatwoot_client = ChatwootClient()


# File: app/services/chatwoot_service.py

from typing import Optional  # noqa: E402  (kept if you need Optional later)
import requests  # noqa: E402

from app.config import get_settings  # noqa: E402

settings = get_settings()


class ChatwootService:
    def __init__(self):
        # Convert AnyHttpUrl (Pydantic) to plain string before using string methods
        self.base_url = str(settings.CHATWOOT_BASE_URL).rstrip("/")
        # Prefer CHATWOOT_API_TOKEN from settings
        self.api_token = settings.CHATWOOT_API_TOKEN

    def _headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "api_access_token": self.api_token,
        }

    def send_message(
        self,
        account_id: int,
        conversation_id: int,
        content: str,
        private: bool = False,
    ) -> bool:
        """
        Sends a message into a Chatwoot conversation as the bot.
        """
        url = (
            f"{self.base_url}/api/v1/accounts/{account_id}/"
            f"conversations/{conversation_id}/messages"
        )
        payload = {
            "content": content,
            "message_type": "outgoing",
            "private": private,
        }

        try:
            resp = requests.post(url, json=payload, headers=self._headers(), timeout=10)
            resp.raise_for_status()
            return True
        except Exception:
            # In production: log error here if needed
            return False


chatwoot_service = ChatwootService()
