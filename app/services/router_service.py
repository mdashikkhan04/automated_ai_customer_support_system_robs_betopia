# File: app/services/router_service.py

import re
from typing import Optional, Tuple

from app.models.schemas import ChatwootIncomingMessage, BotReply
from app.services.kb_service import kb_service
from app.services.openai_service import generate_reply
from app.services.shopify_service import shopify_service
from app.services.clickbank_service import clickbank_service
from app.services.conversation_manager import get_conversation_manager
from app.services.hybrid_response_service import hybrid_service
from app.logger import logger

ORDER_KEYWORDS = ["where is my order", "order status", "track my order", "tracking"]


def detect_intent(message: str) -> str:
    text = message.lower()
    if any(k in text for k in ORDER_KEYWORDS):
        return "order_status"
    if "receipt" in text or "clickbank" in text:
        return "order_status"
    if "refund" in text or "money back" in text:
        return "refund"
    if "shipping" in text or "delivery" in text:
        return "shipping"
    if "subscription" in text or "auto" in text or "recurring" in text:
        return "subscription"
    if "price" in text or "cost" in text or "how much" in text:
        return "pricing"
    if "side effect" in text or "safety" in text or "safe" in text:
        return "safety"
    if "how to use" in text or "take" in text or "dosage" in text:
        return "usage"
    return "general"


def extract_email_and_order(text: str) -> Tuple[Optional[str], Optional[str]]:
    # very simple heuristic; can be improved later
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = email_match.group(0) if email_match else None

    # ClickBank receipt or numeric order number -> allow alnum
    # common ClickBank receipt looks like: ABC12345-1234
    receipt_match = re.search(r"[A-Z0-9\-]{6,}", text, re.IGNORECASE)
    receipt_or_order = receipt_match.group(0) if receipt_match else None

    return email, receipt_or_order


def handle_message(payload: ChatwootIncomingMessage) -> BotReply:
    user_message = payload.content.strip()
    conversation_id = payload.conversation.id
    account_id = payload.conversation.account_id
    customer_email = payload.contact.email if payload.contact else None

    logger.info(f"Handling incoming message: {user_message}")

    # Get or create conversation session
    conv_manager = get_conversation_manager()
    conversation = conv_manager.create_or_get(conversation_id, account_id, customer_email)

    intent = detect_intent(user_message)
    logger.info(f"Detected intent: {intent}")

    # Build KB context
    context = kb_service.build_context(user_message, top_k=5)

    extra_instructions: Optional[str] = None
    used_kb = True
    handoff = False
    handoff_reason: Optional[str] = None
    debug_info = {
        "intent": intent,
        "conversation_message_count": len(conversation.messages)
    }

    # Special handling for ORDER STATUS
    if intent == "order_status":
        email, receipt_or_order = extract_email_and_order(user_message)
        debug_info["email_extracted"] = email
        debug_info["order_or_receipt_extracted"] = receipt_or_order

        if email:
            # 1) Try Shopify
            shopify_order = shopify_service.find_order_by_email_and_number(
                email=email, order_number=receipt_or_order
            )
            if shopify_order:
                logger.info("Found Shopify order for customer")
                status_msg = shopify_service.format_order_status_message(shopify_order)
                context += (
                    "\n\n[ORDER STATUS - SHOPIFY]\n"
                    + status_msg
                    + "\nUse this info when answering the customer."
                )
            else:
                # 2) Try ClickBank
                logger.info("Shopify order not found, trying ClickBank")
                cb_order = clickbank_service.find_order(
                    email=email, receipt=receipt_or_order or ""
                )
                if cb_order:
                    logger.info("Found ClickBank order for customer")
                    status_msg = clickbank_service.format_status(cb_order)
                    context += (
                        "\n\n[ORDER STATUS - CLICKBANK]\n"
                        + status_msg
                        + "\nUse this info when answering the customer."
                    )
                else:
                    logger.info("No order found in Shopify or ClickBank")
                    extra_instructions = (
                        "You could not find an order in Shopify or ClickBank "
                        "with the given details. Politely ask the customer to confirm "
                        "their email and order/receipt number, and let them know "
                        "that a human support agent may need to review it."
                    )
        else:
            extra_instructions = (
                "The customer asked about order status but did not provide an email. "
                "Ask them politely to share the email used for purchase and, if possible, "
                "their order number or ClickBank receipt number."
            )

    # If KB context is empty, be more cautious
    if not context:
        used_kb = False
        extra_instructions = (
            (extra_instructions or "")
            + "\nYou have no relevant knowledge base entries for this question. "
            "Keep your answer generic and clearly offer to escalate the case "
            "to a human support agent for precise details."
        )

    # Add conversation history awareness
    extra_instructions = (
        (extra_instructions or "")
        + f"\n\nThis is message #{len(conversation.messages) + 1} in the conversation. "
        "Remember context from previous messages and maintain continuity."
    )

    # Try OpenAI first, fallback to Hybrid KB Service
    try:
        reply_text = generate_reply(
            user_message=user_message,
            context=context,
            extra_instructions=extra_instructions,
            debug_meta=debug_info,
            conversation_id=conversation_id,
        )
        logger.info("Successfully generated reply using OpenAI API")
    except Exception as e:
        logger.warning(f"OpenAI API failed ({e}), using Hybrid KB Service instead")
        # Fallback to Hybrid Response Service - KB based answers
        reply_text = hybrid_service.get_response(user_message, intent)
        if context:
            reply_text += f"\n\n[📚 Knowledge Base Match]"

    # Add messages to conversation history
    conversation.add_message("user", user_message, {"intent": intent})
    conversation.add_message("assistant", reply_text, {"debug_info": debug_info})

    # Decide handoff conditions (simple rule-set)
    lower = user_message.lower()
    if any(w in lower for w in ["angry", "upset", "frustrated", "complaint", "scam"]):
        handoff = True
        handoff_reason = "Customer seems upset/frustrated; better handled by a human."

    # Escalate after 5+ back-and-forth without resolution
    if len(conversation.messages) > 10 and not handoff:
        # If still on complex topics and many messages, suggest handoff
        if intent in ["order_status", "refund", "shipping"] and len(conversation.messages) % 6 == 0:
            logger.info("Escalating due to conversation length")
            extra_instructions = (
                "The customer has been in this conversation for a while. "
                "If you haven't resolved the issue, offer to connect them with a specialist."
            )

    return BotReply(
        content=reply_text,
        should_handoff=handoff,
        handoff_reason=handoff_reason,
        detected_intent=intent,
        used_kb=used_kb,
        debug_info=debug_info,
    )

