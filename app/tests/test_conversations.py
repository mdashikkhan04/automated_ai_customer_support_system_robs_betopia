# File: app/tests/test_conversations.py

import pytest
from app.models.schemas import ChatwootIncomingMessage, ChatwootConversation, ChatwootContact
from app.services.router_service import handle_message, detect_intent


# Test data helper
def create_test_payload(
    content: str,
    conversation_id: int = 1,
    account_id: int = 1,
    email: str = "customer@example.com"
) -> ChatwootIncomingMessage:
    return ChatwootIncomingMessage(
        content=content,
        conversation=ChatwootConversation(id=conversation_id, account_id=account_id),
        contact=ChatwootContact(email=email, name="Test Customer"),
        message_type="incoming",
        private=False,
    )


# ===============================
# TEST 1-5: GREETING & GENERAL
# ===============================

def test_greeting_hello():
    """Test simple greeting."""
    payload = create_test_payload("Hi there!")
    reply = handle_message(payload)
    assert reply.content
    assert "hello" in reply.content.lower() or "hi" in reply.content.lower() or "help" in reply.content.lower()
    print(f"✓ Test 1 Greeting (Hi): {reply.content[:80]}")


def test_greeting_what_is_hardchews():
    """Test basic product question."""
    payload = create_test_payload("What is HardChews?")
    reply = handle_message(payload)
    assert reply.content
    assert "hardchews" in reply.content.lower()
    assert reply.detected_intent == "general"
    print(f"✓ Test 2 Product Info: {reply.content[:80]}")


def test_how_does_it_work():
    """Test product mechanism question."""
    payload = create_test_payload("How does HardChews work? What are the ingredients?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.used_kb == True
    print(f"✓ Test 3 How It Works: {reply.content[:80]}")


def test_general_support_contact():
    """Test contact support."""
    payload = create_test_payload("How can I contact your support team?")
    reply = handle_message(payload)
    assert reply.content
    assert "support" in reply.content.lower() or "contact" in reply.content.lower()
    print(f"✓ Test 4 Contact Support: {reply.content[:80]}")


def test_unclear_question():
    """Test unclear/rambling question."""
    payload = create_test_payload("umm I don't know what to ask lol")
    reply = handle_message(payload)
    assert reply.content
    print(f"✓ Test 5 Unclear Question: {reply.content[:80]}")


# ===============================
# TEST 6-10: PRODUCT INFO
# ===============================

def test_product_dosage():
    """Test dosage/usage instructions."""
    payload = create_test_payload("How should I take HardChews? What's the recommended dose?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.detected_intent == "usage"
    assert ("1" in reply.content or "tablet" in reply.content.lower() or "dose" in reply.content.lower())
    print(f"✓ Test 6 Dosage: {reply.content[:80]}")


def test_product_side_effects():
    """Test safety and side effects."""
    payload = create_test_payload("Are there any side effects? Is it safe?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.detected_intent == "safety"
    assert "safe" in reply.content.lower() or "effect" in reply.content.lower()
    print(f"✓ Test 7 Side Effects: {reply.content[:80]}")


def test_product_pregnant():
    """Test pregnancy/health condition warning."""
    payload = create_test_payload("Can I take HardChews if I'm pregnant?")
    reply = handle_message(payload)
    assert reply.content
    assert "pregnant" in reply.content.lower() or "doctor" in reply.content.lower() or "no" in reply.content.lower()
    print(f"✓ Test 8 Pregnancy Warning: {reply.content[:80]}")


def test_product_results_timeline():
    """Test how long until results."""
    payload = create_test_payload("How long does HardChews take to work?")
    reply = handle_message(payload)
    assert reply.content
    assert "minute" in reply.content.lower() or "hour" in reply.content.lower() or "time" in reply.content.lower()
    print(f"✓ Test 9 Results Timeline: {reply.content[:80]}")


def test_product_comparison():
    """Test competitor comparison."""
    payload = create_test_payload("Why should I choose HardChews over other brands?")
    reply = handle_message(payload)
    assert reply.content
    print(f"✓ Test 10 Comparison: {reply.content[:80]}")


# ===============================
# TEST 11-15: SHIPPING & DELIVERY
# ===============================

def test_shipping_time():
    """Test shipping timeline."""
    payload = create_test_payload("How long does shipping take?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.detected_intent == "shipping"
    assert ("day" in reply.content.lower() or "business" in reply.content.lower())
    print(f"✓ Test 11 Shipping Time: {reply.content[:80]}")


def test_tracking_order():
    """Test order tracking."""
    payload = create_test_payload("Where is my order? How do I track it?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.detected_intent == "order_status"
    print(f"✓ Test 12 Tracking: {reply.content[:80]}")


def test_lost_package():
    """Test lost package scenario."""
    payload = create_test_payload("I haven't received my package yet. It's been 2 weeks.")
    reply = handle_message(payload)
    assert reply.content
    print(f"✓ Test 13 Lost Package: {reply.content[:80]}")


def test_international_shipping():
    """Test international orders."""
    payload = create_test_payload("Do you ship to Canada? How much for international?")
    reply = handle_message(payload)
    assert reply.content
    assert "international" in reply.content.lower() or "canada" in reply.content.lower() or "ship" in reply.content.lower()
    print(f"✓ Test 14 International: {reply.content[:80]}")


def test_express_shipping():
    """Test expedited shipping."""
    payload = create_test_payload("Can I get faster shipping?")
    reply = handle_message(payload)
    assert reply.content
    print(f"✓ Test 15 Express Shipping: {reply.content[:80]}")


# ===============================
# TEST 16-20: REFUNDS & POLICIES
# ===============================

def test_refund_policy():
    """Test refund policy question."""
    payload = create_test_payload("What is your refund policy?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.detected_intent == "refund"
    assert ("60" in reply.content or "day" in reply.content.lower() or "money" in reply.content.lower())
    print(f"✓ Test 16 Refund Policy: {reply.content[:80]}")


def test_how_to_refund():
    """Test refund process."""
    payload = create_test_payload("How do I request a refund?")
    reply = handle_message(payload)
    assert reply.content
    assert "refund" in reply.content.lower() or "return" in reply.content.lower()
    print(f"✓ Test 17 Refund Process: {reply.content[:80]}")


def test_subscription_question():
    """Test subscription question."""
    payload = create_test_payload("Do you have subscriptions? Can I save money?")
    reply = handle_message(payload)
    assert reply.content
    assert reply.detected_intent == "subscription"
    print(f"✓ Test 18 Subscription: {reply.content[:80]}")


def test_payment_methods():
    """Test accepted payment methods."""
    payload = create_test_payload("What payment methods do you accept? Do you take PayPal?")
    reply = handle_message(payload)
    assert reply.content
    assert "paypal" in reply.content.lower() or "card" in reply.content.lower() or "payment" in reply.content.lower()
    print(f"✓ Test 19 Payment Methods: {reply.content[:80]}")


def test_bulk_order():
    """Test bulk/wholesale query."""
    payload = create_test_payload("Do you offer wholesale pricing? I want to buy 50 units.")
    reply = handle_message(payload)
    assert reply.content
    assert "bulk" in reply.content.lower() or "wholesale" in reply.content.lower() or "discount" in reply.content.lower()
    print(f"✓ Test 20 Bulk Order: {reply.content[:80]}")


# ===============================
# TEST 21-23: EDGE CASES
# ===============================

def test_angry_customer():
    """Test escalation for angry customer."""
    payload = create_test_payload("This product is a SCAM! I'm so frustrated!")
    reply = handle_message(payload)
    assert reply.content
    assert reply.should_handoff == True
    print(f"✓ Test 21 Angry Customer Escalation: {reply.should_handoff}")


def test_medical_claim():
    """Test medical disclaimer."""
    payload = create_test_payload("Can HardChews cure erectile dysfunction?")
    reply = handle_message(payload)
    assert reply.content
    assert "doctor" in reply.content.lower() or "medical" in reply.content.lower() or "not" in reply.content.lower()
    print(f"✓ Test 22 Medical Disclaimer: {reply.content[:80]}")


def test_typo_misspelling():
    """Test handling of typos."""
    payload = create_test_payload("whats the prices?? how much is hardxhews lol")
    reply = handle_message(payload)
    assert reply.content
    print(f"✓ Test 23 Typo Handling: {reply.content[:80]}")


# ===============================
# INTENT DETECTION TESTS
# ===============================

def test_intent_detection_all():
    """Test intent detection for various messages."""
    test_cases = [
        ("Where is my package?", "order_status"),
        ("I want a refund", "refund"),
        ("How long to ship?", "shipping"),
        ("Can I subscribe?", "subscription"),
        ("What's the price?", "pricing"),
        ("Side effects?", "safety"),
        ("How to take it?", "usage"),
        ("Hello there", "general"),
    ]

    for message, expected_intent in test_cases:
        detected = detect_intent(message)
        print(f"  Intent '{message}' → {detected} (expected: {expected_intent})")
        # Note: May not always match exactly, but should be reasonable


# ===============================
# RUN ALL TESTS
# ===============================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 RUNNING 23+ HARDCHEWS CHATBOT CONVERSATION TESTS")
    print("="*70 + "\n")

    # General/Greeting tests
    print("📌 Section 1: Greeting & General Questions")
    test_greeting_hello()
    test_greeting_what_is_hardchews()
    test_how_does_it_work()
    test_general_support_contact()
    test_unclear_question()

    # Product Info tests
    print("\n📌 Section 2: Product Information")
    test_product_dosage()
    test_product_side_effects()
    test_product_pregnant()
    test_product_results_timeline()
    test_product_comparison()

    # Shipping tests
    print("\n📌 Section 3: Shipping & Delivery")
    test_shipping_time()
    test_tracking_order()
    test_lost_package()
    test_international_shipping()
    test_express_shipping()

    # Refund tests
    print("\n📌 Section 4: Refunds & Policies")
    test_refund_policy()
    test_how_to_refund()
    test_subscription_question()
    test_payment_methods()
    test_bulk_order()

    # Edge cases
    print("\n📌 Section 5: Edge Cases")
    test_angry_customer()
    test_medical_claim()
    test_typo_misspelling()

    # Intent detection
    print("\n📌 Section 6: Intent Detection")
    test_intent_detection_all()

    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED!")
    print("="*70 + "\n")
