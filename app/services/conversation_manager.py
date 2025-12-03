# File: app/services/conversation_manager.py

from typing import Dict, List, Optional
import json
import os
from datetime import datetime, timedelta
from pydantic import BaseModel


class ConversationMessage(BaseModel):
    """Single message in conversation history."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    metadata: Dict = {}


class Conversation(BaseModel):
    """Represents a single conversation session."""
    conversation_id: int
    account_id: int
    customer_email: Optional[str] = None
    messages: List[ConversationMessage] = []
    created_at: str = None
    last_updated: str = None
    metadata: Dict = {}

    def __init__(self, **data):
        super().__init__(**data)
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.last_updated:
            self.last_updated = datetime.utcnow().isoformat()

    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add a message to conversation history."""
        msg = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.utcnow().isoformat(),
            metadata=metadata or {}
        )
        self.messages.append(msg)
        self.last_updated = datetime.utcnow().isoformat()

    def get_context_window(self, max_messages: int = 10) -> List[Dict]:
        """
        Get last N messages as OpenAI-compatible message format.
        Older messages are summarized to save tokens.
        """
        if len(self.messages) <= max_messages:
            return [{"role": m.role, "content": m.content} for m in self.messages]

        # Include system context from first message
        result = []

        # Add initial context if available
        if self.messages:
            first_msg = self.messages[0]
            if first_msg.role == "user":
                result.append({
                    "role": "user",
                    "content": f"[Earlier: {first_msg.content[:100]}...]"
                })

        # Add last N messages
        for msg in self.messages[-(max_messages - 1):]:
            result.append({
                "role": msg.role,
                "content": msg.content
            })

        return result

    def is_expired(self, hours: int = 24) -> bool:
        """Check if conversation is older than specified hours."""
        last_update = datetime.fromisoformat(self.last_updated)
        return datetime.utcnow() - last_update > timedelta(hours=hours)


class ConversationManager:
    """
    Manages conversation history and context.
    Supports in-memory storage (dev) or persistent (production).
    """

    def __init__(self, storage_type: str = "memory", storage_path: str = None):
        self.storage_type = storage_type  # "memory" or "file"
        self.storage_path = storage_path or "app/kb/data/conversations"
        self.conversations: Dict[int, Conversation] = {}

        if self.storage_type == "file":
            os.makedirs(self.storage_path, exist_ok=True)

    def create_or_get(
        self,
        conversation_id: int,
        account_id: int,
        customer_email: Optional[str] = None
    ) -> Conversation:
        """Get existing conversation or create new one."""
        key = conversation_id

        if key in self.conversations:
            return self.conversations[key]

        # Load from file if exists
        if self.storage_type == "file":
            filepath = os.path.join(self.storage_path, f"conv_{conversation_id}.json")
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        conv = Conversation(**data)
                        self.conversations[key] = conv
                        return conv
                except Exception as e:
                    print(f"Error loading conversation {conversation_id}: {e}")

        # Create new conversation
        conv = Conversation(
            conversation_id=conversation_id,
            account_id=account_id,
            customer_email=customer_email
        )
        self.conversations[key] = conv
        return conv

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        metadata: Dict = None
    ):
        """Add a message to conversation."""
        # For now, assume conversation already exists
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation(
                conversation_id=conversation_id,
                account_id=0  # Will be set by caller
            )

        self.conversations[conversation_id].add_message(role, content, metadata)

        # Persist if using file storage
        if self.storage_type == "file":
            self._save_conversation(conversation_id)

    def get_context_for_openai(
        self,
        conversation_id: int,
        system_prompt: str,
        max_messages: int = 10
    ) -> List[Dict]:
        """
        Build OpenAI-compatible messages list including system prompt.
        """
        conv = self.conversations.get(conversation_id)
        if not conv:
            return [{"role": "system", "content": system_prompt}]

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conv.get_context_window(max_messages))
        return messages

    def _save_conversation(self, conversation_id: int):
        """Save conversation to file."""
        if conversation_id not in self.conversations:
            return

        conv = self.conversations[conversation_id]
        filepath = os.path.join(self.storage_path, f"conv_{conversation_id}.json")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(conv.dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving conversation {conversation_id}: {e}")

    def cleanup_expired(self, hours: int = 24):
        """Remove conversations older than specified hours."""
        expired = [
            cid for cid, conv in self.conversations.items()
            if conv.is_expired(hours)
        ]

        for cid in expired:
            del self.conversations[cid]
            if self.storage_type == "file":
                filepath = os.path.join(self.storage_path, f"conv_{cid}.json")
                try:
                    os.remove(filepath)
                except:
                    pass

        return len(expired)

    def get_conversation_summary(self, conversation_id: int) -> Optional[Dict]:
        """Get conversation metadata and summary."""
        conv = self.conversations.get(conversation_id)
        if not conv:
            return None

        return {
            "conversation_id": conv.conversation_id,
            "customer_email": conv.customer_email,
            "message_count": len(conv.messages),
            "created_at": conv.created_at,
            "last_updated": conv.last_updated,
            "duration_minutes": (
                (datetime.fromisoformat(conv.last_updated) -
                 datetime.fromisoformat(conv.created_at)).total_seconds() / 60
                if conv.created_at and conv.last_updated
                else 0
            ),
        }


# Global instance
_conversation_manager = None


def get_conversation_manager(
    storage_type: str = "memory",
    storage_path: str = None
) -> ConversationManager:
    """Get or create global conversation manager instance."""
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = ConversationManager(storage_type, storage_path)
    return _conversation_manager
