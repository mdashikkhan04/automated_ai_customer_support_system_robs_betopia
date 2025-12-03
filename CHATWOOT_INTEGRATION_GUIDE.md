# Chatwoot Integration Guide for HardChews Chatbot

## Overview
This guide explains how to integrate the HardChews AI chatbot with Chatwoot live chat, and embed the widget on `hardchews.shop`.

---

## Part 1: Chatwoot Setup (5-10 minutes)

### Step 1A: Create/Access Chatwoot Account

**Option 1: Chatwoot Cloud (Easiest for Getting Started)**
1. Go to https://app.chatwoot.com
2. Sign up or login
3. Create a new account (if first time)
4. Name: "HardChews Support"

**Option 2: Self-Hosted Chatwoot**
- For production, consider self-hosting on your server
- Setup guide: https://www.chatwoot.com/docs/
- Note: Requires Docker, PostgreSQL, Redis

### Step 1B: Create Inbox

1. In Chatwoot dashboard, click **Settings** → **Inboxes**
2. Click **Add Inbox**
3. Choose **Website** channel
4. Name: `HardChews Support`
5. Configure:
   - **Website Name**: HardChews
   - **Website URL**: https://hardchews.shop
   - **Avatar**: (upload your logo)
   - **Greeting Message**: "👋 Hi! Welcome to HardChews Support. How can we help you today?"
   - **Greeting Tagline**: "We typically reply within 2 hours"

6. Click **Create Website Inbox**

### Step 1C: Get Installation Script

After creating inbox:
1. Go to **Settings** → **Inboxes** → Select "HardChews Support"
2. Under "Install on Your Website", you'll see an **Installation Script**
3. Copy the script (looks like this):

```html
<script>
  window.chatwootSettings = {
    position: 'right',
    hideMessageBubble: false,
    displayFormat: 'bubble',
  };
  (function(d,t) {
    var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
    g.src='https://app.chatwoot.com/packs/js/sdk.js';
    g.defer = true;
    g.async = true;
    s.parentNode.insertBefore(g,s);
    window.addEventListener('chatwoot:ready', function(e) {
      window.chatwootSDK.run({
        websiteToken: 'YOUR_WEBSITE_TOKEN_HERE',
        baseUrl: 'https://app.chatwoot.com'
      })
    });
  })(document,"script");
</script>
```

**Save this script** - you'll need it for embedding on your website.

---

## Part 2: Embed Widget on HardChews.shop (5-10 minutes)

### Step 2A: Where to Add the Script

The Chatwoot script needs to be added to your Shopify store. There are two main ways:

#### Option A: Using Shopify Theme Customizer (EASIEST)
1. In Shopify Admin, go to **Online Store** → **Themes**
2. Find your live theme, click **...** → **Edit code**
3. In the left sidebar, find **theme.liquid** or **Layout** section
4. Look for the closing `</head>` or `</body>` tag
5. Paste the Chatwoot script just before `</body>`

Example placement in `theme.liquid`:
```liquid
...
  <!-- HardChews Chatwoot Widget -->
  <script>
    window.chatwootSettings = { ... }
  </script>
</body>
</html>
```

#### Option B: Using Shopify Script Editor
1. Shopify Admin → **Settings** → **Custom Data**
2. Or use **Settings** → **Pixels & Events**
3. Add new script tag and paste the Chatwoot code

#### Option C: Using App (If Available)
- Search for "Chatwoot" or "Live Chat" in Shopify App Store
- Some third-party apps can auto-embed for you

### Step 2B: Verify Embedding

After adding the script:

1. **Clear cache**: Go to your website and do a hard refresh (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac)
2. **Look for chat bubble**: You should see a chat bubble in the bottom-right corner of the page
3. **Test**: Send a test message to verify it appears in Chatwoot

If you don't see it:
- Check browser console for errors (F12 → Console tab)
- Verify website token is correct
- Ensure Chatwoot account/inbox is active

---

## Part 3: Connect AI Bot to Chatwoot (10-15 minutes)

### Step 3A: Get Chatwoot API Credentials

1. In Chatwoot, go to **Settings** → **Account Settings** → **API**
2. Generate a new **Personal API Token** (or use existing)
3. Copy the token

Also note:
- **API URL**: Usually `https://app.chatwoot.com` (or your self-hosted URL)
- **Account ID**: Available in Settings
- **Inbox ID**: Get from Inboxes page

### Step 3B: Configure Backend Environment

In your `.env` file, add/update:

```env
# Chatwoot
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_API_TOKEN=your_generated_api_token_here
CHATWOOT_BOT_NAME=HardChews AI Assistant

# Optional: Store Chatwoot account/inbox IDs for routing
CHATWOOT_ACCOUNT_ID=1
CHATWOOT_INBOX_ID=1
```

### Step 3C: Setup Webhook (Chatwoot → AI Backend)

This allows Chatwoot to send incoming messages to your AI backend.

**In Chatwoot:**
1. **Settings** → **Integrations** → **Webhooks**
2. Click **Add Webhook**
3. Configure:
   - **URL**: `https://your-backend-domain.com/api/webhook/chatwoot`
   - **Events to subscribe to**: `message_created`
   - **Active**: ✓ Check

4. Save

**Your Backend Must:**
- Accept POST requests at `/api/webhook/chatwoot`
- Process the payload and return AI response
- Send reply back via Chatwoot API

---

## Part 4: Auto-Reply Setup (OPTIONAL - For AI Responses)

### Option A: Chatwoot Automation (Simple)

Chatwoot has built-in automation rules:

1. **Settings** → **Automation Rules**
2. Create rule: "When message received, assign to bot"
3. You can set automatic responses, but for dynamic AI:

### Option B: Custom Bot Agent (Recommended for AI)

Chatwoot v2.0+ supports "Bot Agents":

1. **Settings** → **Team Members**
2. Add a new **Bot** user
3. Name: "HardChews AI"
4. This bot will show in conversations

**However**, to make it actually AI-powered, you need:
- Backend service listening to webhooks
- Processing messages through OpenAI
- Posting replies as this bot user

---

## Part 5: Testing the Full Integration

### Test Scenario 1: Simple Message

1. Go to **hardchews.shop**
2. Click the chat bubble
3. Type: "Hi"
4. Expected: You see it in Chatwoot inbox AND AI response appears

### Test Scenario 2: Product Question

1. Chat: "What is HardChews?"
2. Expected: AI bot responds with product info from KB

### Test Scenario 3: Order Status

1. Chat: "Where is my order? My email is test@example.com"
2. Expected: Bot asks for order number or checks Shopify/ClickBank

### Test Scenario 4: Multi-turn

1. Chat 1: "Do you have refunds?"
2. Bot replies with refund policy
3. Chat 2: "What if I'm not satisfied?"
4. Bot should remember context from first message

---

## Part 6: Production Checklist

Before going live:

- [ ] Chatwoot account created and secured
- [ ] Widget embedded on hardchews.shop
- [ ] Widget tested and visible
- [ ] API credentials in `.env` (not hardcoded)
- [ ] Backend webhook endpoint deployed
- [ ] Backend can receive and respond to messages
- [ ] Fallback human agent setup (for escalations)
- [ ] Support team trained on Chatwoot inbox
- [ ] Response time expectations set (e.g., "We reply within 2 hours")
- [ ] Monitoring/alerts setup (message volume, failures)

---

## Part 7: Troubleshooting

### Widget not appearing

- [ ] Script is added to correct location
- [ ] Website token is correct
- [ ] No JavaScript errors in console
- [ ] Chatwoot account is active
- [ ] Try different position: `position: 'left'` or `'right'`

### Messages not arriving in Chatwoot

- [ ] Check Chatwoot account is active
- [ ] Verify website domain matches config
- [ ] Check browser console for errors
- [ ] Verify inbox is set to receive messages

### AI bot not responding

- [ ] Check webhook URL is correct and reachable
- [ ] Verify OpenAI API key is valid
- [ ] Check backend logs for errors
- [ ] Ensure KB files are loaded
- [ ] Test webhook manually with curl/Postman

### Slow responses

- [ ] Check OpenAI API latency
- [ ] Verify network connection
- [ ] Consider caching frequent questions
- [ ] Scale backend if needed

---

## Part 8: Customization Options

### Change Widget Position
```javascript
window.chatwootSettings = {
  position: 'left',  // or 'right'
};
```

### Hide Widget on Specific Pages
```javascript
// Add before Chatwoot script
window.chatwootSettings = {
  hideOnPages: ['/admin', '/checkout'],
};
```

### Custom Greeting Per Page
```javascript
window.chatwootSettings = {
  greeting_message: "Need help with HardChews? Ask us!",
};
```

### Dark Mode / Styling
Chatwoot admin → **Inboxes** → Select inbox → **Settings** → **Style**

---

## Part 9: Analytics & Monitoring

In Chatwoot dashboard:
- **Reports**: Message volume, response time, customer satisfaction
- **Conversations**: View all chats, search by customer
- **Bot Activity**: See which questions AI handled vs. escalated

---

## Support & Next Steps

- **Chatwoot Docs**: https://www.chatwoot.com/docs/
- **API Reference**: https://www.chatwoot.com/api/
- **Community**: https://github.com/chatwoot/chatwoot/discussions

For HardChews-specific issues:
- Check the test suite: `app/tests/test_conversations.py`
- Review logs in backend service
- Contact AI bot team for debugging
