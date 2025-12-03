# File: app/models/schemas.py

from typing import Any, Dict, Optional, List
from pydantic import BaseModel


class ChatwootContact(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None


class ChatwootConversation(BaseModel):
    id: int
    account_id: int


class ChatwootIncomingMessage(BaseModel):
    # This is a simplified version of Chatwoot webhook payload
    content: str
    message_type: Optional[str] = None
    private: Optional[bool] = None
    sender_type: Optional[str] = None
    content_type: Optional[str] = None
    inbox_id: Optional[int] = None
    conversation: ChatwootConversation
    contact: Optional[ChatwootContact] = None
    additional_attributes: Dict[str, Any] = {}
    meta: Dict[str, Any] = {}


class BotReply(BaseModel):
    content: str
    should_handoff: bool = False
    handoff_reason: Optional[str] = None
    detected_intent: Optional[str] = None
    used_kb: Optional[bool] = True
    debug_info: Optional[Dict[str, Any]] = None


class KBItem(BaseModel):
    id: str
    type: str  # "faq", "product", "policy"
    title: str
    question: Optional[str] = None
    answer: str
    tags: List[str] = []
    source: Optional[str] = None
    url: Optional[str] = None
