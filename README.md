# 🤖 HardChews AI Customer Support Chatbot - V1

Professional-grade AI chatbot for **HardChews** supplement brand. Handles customer support across Chatwoot, email, and future voice/phone channels with a single, unified backend.

---

## ✨ Features

### Core Capabilities
- ✅ **AI-Powered Responses** - Uses OpenAI GPT-4 mini for intelligent, context-aware replies
- ✅ **Knowledge Base Integration** - 19+ pre-loaded KB articles (products, FAQs, policies)
- ✅ **Order Lookup** - Checks Shopify and ClickBank for order status in real-time
- ✅ **Conversation Memory** - Maintains context across multi-turn conversations
- ✅ **Intent Detection** - Classifies customer intent (order_status, refund, shipping, etc.)
- ✅ **Sentiment Analysis** - Detects angry customers and escalates to humans
- ✅ **Webhook Integration** - Seamless Chatwoot integration

### Supported Channels
- 📱 **Chatwoot Live Chat** - Widget on hardchews.shop (V1)
- 💬 **Email** - Auto-reply via ClickBank (V2 ready)
- 🎙️ **Voice/Phone** - Twilio integration (V3 ready)

### Knowledge Base Topics
- Product information (benefits, ingredients, usage, dosage)
- Shipping & delivery timelines
- Refund policy (60-day money-back guarantee)
- Subscription & auto-replenishment
- Payment methods & bulk orders
- International orders
- Safety warnings & contraindications

---

## 🚀 Quick Start (5 minutes)

### 1. Clone & Setup

```bash
git clone https://github.com/mdashikkhan04/automated_ai_customer_support_system_robs_betopia.git
cd automated_ai_customer_support_system_robs_betopia

# Create venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install deps
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env

# Edit .env with:
# - OPENAI_API_KEY (required)
# - CHATWOOT credentials (for chat widget)
# - SHOPIFY credentials (for order lookup)
```

### 3. Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs (Swagger API docs)

### 4. Test

```bash
python app/tests/test_conversations.py
```

Expected: ✅ All 23+ test scenarios pass

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **[SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md)** | Complete setup, configuration, deployment steps |
| **[CHATWOOT_INTEGRATION_GUIDE.md](CHATWOOT_INTEGRATION_GUIDE.md)** | Integrate Chatwoot widget on hardchews.shop |
| **[SHOPIFY_CLICKBANK_SETUP.md](SHOPIFY_CLICKBANK_SETUP.md)** | Configure Shopify & ClickBank for order lookup |

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  HardChews.shop     │
│  (Chatwoot Widget)  │
└──────────┬──────────┘
           │ (webhook)
           ▼
┌─────────────────────────────────────┐
│   AI Bot Service (FastAPI)          │
│  ┌──────────────────────────────┐   │
│  │ - Intent Detection           │   │
│  │ - KB Search (Semantic)       │   │
│  │ - Order Lookup               │   │
│  │ - Conversation Memory        │   │
│  │ - OpenAI Integration         │   │
│  └──────────────────────────────┘   │
└──────┬──────────┬──────────┬────────┘
       │          │          │
       ▼          ▼          ▼
   OpenAI    Shopify    ClickBank
    API       API        API
```

---

## 📁 Project Structure

```
hardchews-chatbot-backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Environment config
│   ├── logger.py               # Logging setup
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── api/
│   │   └── chatwoot_webhook.py # Chatwoot webhook handler
│   ├── services/
│   │   ├── openai_service.py   # OpenAI API calls
│   │   ├── kb_service.py       # Knowledge base + embeddings
│   │   ├── router_service.py   # Intent detection & routing
│   │   ├── conversation_manager.py  # Multi-turn memory
│   │   ├── shopify_service.py  # Shopify order lookup
│   │   ├── clickbank_service.py # ClickBank order lookup
│   │   ├── chatwoot_service.py # Chatwoot API integration
│   │   └── web_scraper.py      # Website content scraper
│   ├── kb/
│   │   └── data/
│   │       ├── faqs_comprehensive.json        # 12 FAQ items
│   │       ├── products_comprehensive.json    # 7 product items
│   │       └── faqs.json, products.json       # Legacy/simple versions
│   └── tests/
│       └── test_conversations.py # 23+ test scenarios
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── SETUP_DEPLOYMENT_GUIDE.md   # How to setup & deploy
├── CHATWOOT_INTEGRATION_GUIDE.md # Chatwoot setup
└── SHOPIFY_CLICKBANK_SETUP.md   # Order lookup setup
```

---

## 🎯 Conversation Examples

### Example 1: Product Question

```
Customer: "What is HardChews? Any side effects?"

Bot: "HardChews is a premium dietary supplement formulated to support 
male performance and vitality. It contains natural ingredients like 
L-Arginine, Ginseng, and Tribulus Terrestris.

Most users report noticeable effects within 20-40 minutes. Some may 
experience mild headaches or digestive sensitivity. 

⚠️ Important: Do NOT use if you have heart conditions, take nitrate 
medications, or are pregnant/nursing. Consult your doctor first.

Can I help with anything else?"
```

### Example 2: Order Status

```
Customer: "Where is my order? My email is john@example.com and 
order number is 12345"

Bot: [Searches Shopify]

Bot: "I found your order #12345!

Payment Status: Paid ✓
Fulfillment Status: Shipped 📦
Tracking: USPS #1234567890
Expected Delivery: Jan 15-17, 2025

Click here for live tracking: [link]

Need anything else?"
```

### Example 3: Refund Request

```
Customer: "I'm not satisfied. Can I get a refund?"

Bot: "Absolutely! We offer a hassle-free 60-day money-back guarantee.

To request a refund:
1. Email support@hardchews.shop with your order number
2. We'll send you a return shipping label
3. Ship the product back to us
4. Once received, we'll process your refund within 3-5 business days

Need help with anything else?"
```

### Example 4: Escalation

```
Customer: "This is SCAM! This product doesn't work and I'm FURIOUS!"

Bot: "I'm truly sorry for the frustration. I'm immediately connecting 
you with a human support specialist who can review your case and find 
a resolution. 

A specialist will respond to you shortly. Thank you for your patience."

[Message flagged for escalation]
```

---

## ⚙️ Configuration

### Required Environment Variables

```env
# Must have for chatbot to work
OPENAI_API_KEY=sk-proj-xxxxx

# Optional: For Chatwoot widget
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_API_TOKEN=xxxx
CHATWOOT_BOT_NAME=HardChews Assistant

# Optional: For order lookup
SHOPIFY_STORE_DOMAIN=yourstore.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxx
CLICKBANK_DEV_KEY=xxxx
CLICKBANK_CLERK_KEY=xxxx

# Optional: Logging
ENVIRONMENT=development
LOG_LEVEL=info
```

See [SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md) for details.

---

## 🧪 Testing

Run the full test suite (23+ scenarios):

```bash
python app/tests/test_conversations.py
```

This tests:
- ✅ Greetings & general questions
- ✅ Product information & dosage
- ✅ Shipping & delivery
- ✅ Refunds & policies
- ✅ Subscription handling
- ✅ Angry customer escalation
- ✅ Medical disclaimers
- ✅ Typo/unclear message handling

---

## 🚢 Deployment

### Quick Deploy to Heroku

```bash
heroku login
heroku create hardchews-ai-bot
git push heroku main
heroku config:set OPENAI_API_KEY=sk-proj-xxxx
heroku open
```

### Other Options
- **AWS Elastic Beanstalk**
- **DigitalOcean App Platform**
- **Render**
- **Self-hosted on VPS**

See [SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md) for detailed steps.

---

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service status |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger API documentation |
| `/api/webhook/chatwoot` | POST | Incoming Chatwoot messages |
| `/api/test` | POST | Local testing (returns bot reply without posting) |

### Test Endpoint Example

```bash
curl -X POST http://localhost:8000/api/test \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is HardChews?",
    "conversation": {"id": 1, "account_id": 1},
    "contact": {"email": "customer@example.com"}
  }'
```

Response:
```json
{
  "reply": "HardChews is a premium dietary supplement...",
  "intent": "general",
  "handoff": false,
  "used_kb": true,
  "debug": {"intent": "general", "conversation_message_count": 0}
}
```

---

## 📊 Knowledge Base

### Current Content
- **7 Product Items**: Details, ingredients, dosage, safety, results
- **12 FAQ Items**: Shipping, refunds, subscriptions, payment, bulk orders

### Updating KB

1. **Add new items** to `app/kb/data/faqs_comprehensive.json` or `products_comprehensive.json`
2. **Scrape website** (optional):
   ```bash
   python -c "from app.services.web_scraper import scrape_hardchews_website; scrape_hardchews_website()"
   ```
3. **Restart service** to reload KB and embeddings

---

## 🔐 Security

⚠️ **Never commit `.env` file to Git!**

- API keys are stored in environment variables
- All API calls over HTTPS
- Customer data (email, order #) processed in memory only
- No data stored permanently (except conversation logs)

For production:
- Use secret management (AWS Secrets Manager, HashiCorp Vault)
- Enable rate limiting
- Add authentication/authorization if needed
- Regular security audits

---

## 📈 Monitoring

### Health Check

```bash
curl https://your-deployment-url/health
```

### View Logs

```bash
# Heroku
heroku logs --tail

# Self-hosted (with PM2)
pm2 logs hardchews-bot
```

### Key Metrics

- **Response Time**: Target < 3s
- **Error Rate**: Target < 1%
- **Uptime**: Target > 99.5%
- **API Calls**: Monitor OpenAI billing

---

## 🛠️ Development

### Adding New Intent

1. Add to `detect_intent()` in `app/services/router_service.py`:
```python
def detect_intent(message: str) -> str:
    text = message.lower()
    if "loyalty" in text or "points" in text:
        return "loyalty"  # New intent
    ...
```

2. Add handling in `handle_message()` if needed

3. Add test in `app/tests/test_conversations.py`

### Adding New KB Items

1. Edit `app/kb/data/faqs_comprehensive.json`:
```json
{
  "id": "faq_new_001",
  "type": "policy",
  "title": "New Question",
  "question": "What is...?",
  "answer": "Answer here...",
  "tags": ["tag1", "tag2"],
  "source": "client_file",
  "url": null
}
```

2. Restart service (KB auto-loads)

3. Test with `/api/test` endpoint

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "OpenAI API key invalid" | Check `.env`, regenerate key |
| "Bot not responding" | Check `/health` endpoint |
| "Slow responses" | Monitor OpenAI latency, consider caching |
| "Widget not showing" | See CHATWOOT_INTEGRATION_GUIDE.md |
| "Order lookup fails" | See SHOPIFY_CLICKBANK_SETUP.md |
| "Tests failing" | Check all dependencies installed: `pip install -r requirements.txt` |

See detailed troubleshooting in [SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md).

---

## 📞 Support

- **Documentation**: See guides in this repo
- **Issues**: Report on GitHub
- **OpenAI Support**: https://help.openai.com
- **Chatwoot Support**: https://www.chatwoot.com/docs

---

## 🗺️ Roadmap

### ✅ V1 (Current)
- Chatwoot widget integration
- AI chat responses
- Order lookup (Shopify + ClickBank)
- Multi-turn conversations
- 19+ KB items

### 🎯 V2 (Next)
- Email auto-reply integration
- ClickBank ticket automation
- Advanced analytics dashboard
- Customer satisfaction surveys

### 🚀 V3 (Future)
- Twilio voice integration
- Phone agent mode
- Advanced NLP (entity extraction)
- Multi-language support
- WhatsApp integration

---

## 📝 License

MIT License - See LICENSE file

---

## 👥 Team

**Created for**: Rob @ Betopia
**By**: HardChews Development Team
**Last Updated**: December 3, 2025

---

## 🎉 Getting Help

1. **Read the docs** - Start with [SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md)
2. **Check troubleshooting** - Section in each guide
3. **Run tests** - `python app/tests/test_conversations.py`
4. **View logs** - Check for error messages
5. **API docs** - Visit `/docs` endpoint

**Ready to deploy?** Follow [SETUP_DEPLOYMENT_GUIDE.md](SETUP_DEPLOYMENT_GUIDE.md) step-by-step.
