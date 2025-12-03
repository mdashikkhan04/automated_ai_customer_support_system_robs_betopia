# File: app/services/chatwoot_service.py

from typing import Optional

import requests

from app.config import get_settings

settings = get_settings()


class ChatwootService:
    def __init__(self):
        self.base_url = settings.CHATWOOT_BASE_URL.rstrip("/")
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
            # In production: log error
            return False


chatwoot_service = ChatwootService()
