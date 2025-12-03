# File: app/services/router_service.py

import re
from typing import Optional, Tuple

from app.models.schemas import ChatwootIncomingMessage, BotReply
from app.services.kb_service import kb_service
from app.services.openai_service import generate_reply
from app.services.shopify_service import shopify_service
from app.services.clickbank_service import clickbank_service
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
    logger.info(f"Handling incoming message: {user_message}")

    intent = detect_intent(user_message)
    logger.info(f"Detected intent: {intent}")

    # Build KB context
    context = kb_service.build_context(user_message, top_k=5)

    extra_instructions: Optional[str] = None
    used_kb = True
    handoff = False
    handoff_reason: Optional[str] = None
    debug_info = {"intent": intent}

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
            + "\nYou have no relevant knowledge base entries. "
            "Keep your answer generic and clearly offer to escalate the case "
            "to a human support agent for precise details."
        )

    reply_text = generate_reply(
        user_message=user_message,
        context=context,
        extra_instructions=extra_instructions,
        debug_meta=debug_info,
    )

    # Decide handoff conditions (simple rule-set)
    lower = user_message.lower()
    if any(w in lower for w in ["angry", "upset", "frustrated", "complaint", "scam"]):
        handoff = True
        handoff_reason = "Customer seems upset/frustrated; better handled by a human."

    return BotReply(
        content=reply_text,
        should_handoff=handoff,
        handoff_reason=handoff_reason,
        detected_intent=intent,
        used_kb=used_kb,
        debug_info=debug_info,
    )
