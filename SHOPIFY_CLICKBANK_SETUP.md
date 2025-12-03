# Shopify & ClickBank Integration Guide

## Overview

This guide explains how to fully integrate your AI chatbot with Shopify and ClickBank so customers can check their order status directly through the chat.

---

## Part 1: Shopify Setup (15-20 minutes)

### Step 1A: Create Shopify Private App

Shopify requires authentication via Private App tokens to access order data.

**In Shopify Admin:**
1. Go to **Settings** → **Apps and integrations**
2. Click **Develop apps**
3. Click **Create an app**
4. Name: `HardChews AI Chatbot`
5. Developer contact: (your email)
6. Create app

### Step 1B: Set Admin API Permissions

After creating the app:

1. Click the app you just created
2. Go to **Configuration**
3. Under **Admin API scopes**, enable these permissions:
   - `read_orders`
   - `read_customers`
   - `write_fulfillments` (optional, if you want to update fulfillment status)

4. Save

### Step 1C: Get Access Token

1. Still in your app page, go to **API credentials**
2. You'll see:
   - **Access token** - Copy this!
   - **API version** - Note this (e.g., `2024-01`)

### Step 1D: Get Store Domain

1. Shopify Admin → **Settings** → **General**
2. Find your **Shop name** (e.g., `mystore.myshopify.com`)
3. Copy this

### Step 1E: Update Environment Variables

In your `.env` file:

```env
# Shopify
SHOPIFY_STORE_DOMAIN=mystore.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxx
SHOPIFY_API_VERSION=2024-01
```

### Step 1F: Test Shopify Connection

Run this quick test to verify connection:

```bash
python -c "
from app.services.shopify_service import shopify_service
order = shopify_service.find_order_by_email_and_number('customer@example.com', '1001')
print('✓ Shopify connected!' if order or order is None else '✗ Connection failed')
"
```

---

## Part 2: ClickBank Setup (15-20 minutes)

ClickBank is a payment processor often used for supplement sales. If customers bought through ClickBank, the bot should be able to look up their order.

### Step 2A: Get ClickBank API Keys

**In ClickBank Account:**
1. Log in to https://www.clickbank.com
2. Go to **Settings** → **Account** → **API Keys**
3. You'll see:
   - **Developer Key** - Copy this
   - **Clerk Key** - Copy this (keep secret!)

**If you don't see these options:**
- You may need to enable API access
- Go to **Account Settings** → **API Management**
- Enable "REST API"

### Step 2B: Understanding ClickBank Order Format

ClickBank order numbers typically look like:
- **Receipt**: `ABC123-1234567` or similar
- **Email**: Customer email on file

### Step 2C: Update Environment Variables

In your `.env` file:

```env
# ClickBank
CLICKBANK_DEV_KEY=your_developer_key_here
CLICKBANK_CLERK_KEY=your_clerk_key_here
```

### Step 2D: Test ClickBank Connection

```bash
python -c "
from app.services.clickbank_service import clickbank_service
order = clickbank_service.find_order('customer@example.com', 'ABC123-1234567')
print('✓ ClickBank connected!' if order or order is None else '✗ Connection failed')
"
```

---

## Part 3: Order Lookup Flow in Chatbot

### How the Bot Handles Order Status Queries

When a customer asks "Where is my order?":

1. **Message Detection**
   - Bot detects intent = `order_status`

2. **Email Extraction**
   - Searches message for email pattern (e.g., john@example.com)
   - Also looks for order/receipt number

3. **Order Lookup** (in this order):
   - Try Shopify first (your main sales channel)
   - If not found, try ClickBank
   - If neither found, ask customer for more details

4. **Response**
   - If found: Show order status (payment status, fulfillment, tracking)
   - If not found: Politely ask for email + order number, or offer to escalate

### Example Conversation Flow

```
Customer: "Where is my order? I bought 2 weeks ago"

Bot: "I'd be happy to help! Could you provide the email 
address associated with your order and your order number?"

Customer: "Sure, it's john@example.com, order #12345"

Bot: [Searches Shopify for john@example.com + order 12345]
     → Found! 
     → "I found your order #12345. Payment: Confirmed. 
     Fulfillment: Shipped. Tracking: [link]"
```

---

## Part 4: Testing Order Lookup

### Test Scenario 1: Real Shopify Order

```python
from app.services.shopify_service import shopify_service

# Test with real email + order number
order = shopify_service.find_order_by_email_and_number(
    email="customer@example.com",
    order_number="1001"
)

if order:
    print("✓ Found Shopify order:", order.get('order_number'))
    print("  Status:", order.get('financial_status'))
    print("  Fulfillment:", order.get('fulfillment_status'))
else:
    print("✗ Order not found")
```

### Test Scenario 2: Real ClickBank Order

```python
from app.services.clickbank_service import clickbank_service

# Test with real ClickBank receipt
order = clickbank_service.find_order(
    email="customer@example.com",
    receipt="ABC123-1234567"
)

if order:
    print("✓ Found ClickBank order:", order.get('receipt'))
    print("  Status:", order.get('paymentStatus'))
else:
    print("✗ Order not found")
```

### Test Scenario 3: Chat Integration Test

1. Go to chat widget on hardchews.shop
2. Send: "Where is order from john@example.com? Order number 1001"
3. Bot should search and respond

---

## Part 5: Handling Different Order Scenarios

### Scenario A: Order Found in Shopify

**Bot Response:**
```
I found your Shopify order #12345. 
Payment status: Paid
Fulfillment status: Shipped
Tracking: [USPS tracking link]
Delivery expected: [date range]

If you need detailed info or have other questions, feel free to ask!
```

### Scenario B: Order Found in ClickBank

**Bot Response:**
```
I found your ClickBank receipt (ABC123-1234567).
Payment status: Approved
Amount: $29.99 USD

If you purchased via ClickBank, also check the tracking link 
in your receipt email. For delivery details, I can help further!
```

### Scenario C: Order Not Found

**Bot Response:**
```
I couldn't find an order with that information. 

Could you help me by confirming:
1. Email address (must match purchase)
2. Order number or receipt number
3. Approximate purchase date

If you still can't find it, I'll connect you with a human 
support specialist who can investigate.
```

### Scenario D: Multiple Orders Found

**Bot Response:**
```
I found 2 orders associated with your email. 
Could you tell me which one you're asking about?

1. Order #12345 from Jan 15 - Status: Delivered
2. Order #12346 from Jan 28 - Status: Shipped

Which one would you like to check?
```

---

## Part 6: Advanced Features (Optional)

### Feature 1: Auto-Fulfill Tracking

Some Shopify stores auto-send tracking info via email. To enable:

1. Shopify Admin → **Settings** → **Notifications** → **Shipping confirmation**
2. Ensure tracking link is included in email

### Feature 2: Order History

Currently, bot looks up one order at a time. To show order history:

```python
def get_customer_order_history(email: str, limit: int = 5):
    """Get last 5 orders for a customer."""
    from app.services.shopify_service import shopify_service
    return shopify_service.get_orders_by_email(email, limit=limit)
```

(Would need to implement in `shopify_service.py`)

### Feature 3: Proactive Tracking Updates

Send customers updates when their order ships:

```python
# Webhook from Shopify: order_updated
# Check if fulfillment status changed
# Auto-send message to customer via Chatwoot
```

---

## Part 7: Troubleshooting

### Shopify Issues

| Problem | Solution |
|---------|----------|
| "Invalid access token" | Verify token in `.env`, check expiration date |
| "Order not found" | Email might not match exactly, check spelling |
| "API rate limited" | Wait a few minutes, implement caching |
| "Permission denied" | Add `read_orders` scope in Private App settings |

### ClickBank Issues

| Problem | Solution |
|---------|----------|
| "Invalid credentials" | Double-check Dev Key and Clerk Key |
| "API returns 500" | Receipt format might be wrong |
| "Order not in system" | ClickBank may still be processing |
| "Email doesn't match" | Verify email used during purchase |

### General Debugging

Enable debug logging:

```python
# In app/logger.py
LOG_LEVEL = "debug"  # Instead of "info"
```

Then check logs for detailed error messages.

---

## Part 8: Security Considerations

⚠️ **IMPORTANT: Protect Your Keys**

1. **Never** commit `.env` file to git
2. **Never** log full API keys
3. **Rotate** keys periodically
4. **Limit** scopes to only what's needed
5. **Monitor** API usage for suspicious activity

Example safe logging:

```python
# ✓ SAFE
logger.info(f"Shopify API call for email: {email}")

# ✗ UNSAFE
logger.info(f"Shopify token: {SHOPIFY_ACCESS_TOKEN}")
```

---

## Part 9: Production Checklist

Before going live:

- [ ] Shopify Private App created
- [ ] Shopify API token in `.env` (not hardcoded)
- [ ] Shopify API scopes correct (`read_orders`)
- [ ] ClickBank credentials (if used) in `.env`
- [ ] Test order lookup with real Shopify data
- [ ] Test order lookup with real ClickBank data (if applicable)
- [ ] Error handling for API failures (graceful fallback)
- [ ] Rate limiting implemented
- [ ] Logging configured (debug/error levels)
- [ ] Customer data privacy verified (GDPR, PCI-DSS)
- [ ] API response time monitored

---

## Part 10: Future Enhancements

Potential features to add:

1. **Refund Processing**
   - Bot initiates refund directly through Shopify API

2. **Inventory Sync**
   - Bot tells customers which products are in stock

3. **Order Updates**
   - Bot sends proactive messages when order ships

4. **Partial Refunds**
   - Bot processes partial returns

5. **Analytics**
   - Dashboard of orders checked via bot

---

## Reference Links

- **Shopify API Docs**: https://shopify.dev/api/admin-rest
- **ClickBank API**: https://www.clickbank.com/developers
- **Order Status Codes**: https://help.shopify.com/en/api/admin-rest/2024-01/resources/order#resource_object

---

## Support

For issues:
1. Check logs: `tail -f app.log`
2. Review error messages in Chatwoot inbox
3. Test API manually with Postman/curl
4. Review this guide's troubleshooting section
