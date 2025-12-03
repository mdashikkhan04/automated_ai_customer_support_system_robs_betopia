# File: app/api/chatwoot_webhook.py

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatwootIncomingMessage
from app.services.router_service import handle_message
from app.services.chatwoot_service import chatwoot_service

router = APIRouter()


@router.post("/webhook/chatwoot")
async def chatwoot_webhook(payload: ChatwootIncomingMessage):
    """
    Entry point for Chatwoot bot integration.
    Chatwoot should be configured to send incoming messages to this endpoint.
    """
    # Basic sanity: ignore private or non-incoming messages if needed
    if payload.private:
        # ignore internal notes
        return {"status": "ignored"}

    bot_reply = handle_message(payload)

    sent = chatwoot_service.send_message(
        account_id=payload.conversation.account_id,
        conversation_id=payload.conversation.id,
        content=bot_reply.content,
    )

    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send message to Chatwoot")

    return {
        "status": "ok",
        "intent": bot_reply.detected_intent,
        "handoff": bot_reply.should_handoff,
        "used_kb": bot_reply.used_kb,
    }


# this part of code just for testing purposes in locally
@router.post("/test")
async def test_message(payload: ChatwootIncomingMessage):
    """
    Local testing endpoint without sending to Chatwoot.
    It just returns what the bot WOULD reply.
    """
    bot_reply = handle_message(payload)
    return {
        "reply": bot_reply.content,
        "intent": bot_reply.detected_intent,
        "handoff": bot_reply.should_handoff,
        "debug": bot_reply.debug_info,
    }
