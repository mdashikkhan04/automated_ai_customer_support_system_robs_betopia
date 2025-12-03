# ⚡ HardChews Chatbot - Quick Reference Card

## 🎯 One-Minute Setup

```bash
# 1. Install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env → Add OPENAI_API_KEY=sk-proj-xxx

# 3. Check
python manage.py health

# 4. Run
uvicorn app.main:app --reload

# 5. Test
python app/tests/test_conversations.py
```

**Visit**: http://localhost:8000/docs (Swagger UI)

---

## 📚 Documentation Quick Links

| Need Help With... | Read This |
|-------------------|-----------|
| Getting started | README.md |
| Setup & deploy | SETUP_DEPLOYMENT_GUIDE.md |
| Chatwoot widget | CHATWOOT_INTEGRATION_GUIDE.md |
| Shopify/ClickBank orders | SHOPIFY_CLICKBANK_SETUP.md |
| Health check | `python manage.py health` |
| Run tests | `python app/tests/test_conversations.py` |
| What's included | IMPLEMENTATION_COMPLETE.md |

---

## 🔧 Common Commands

```bash
# Development
uvicorn app.main:app --reload                    # Start dev server
python app/tests/test_conversations.py           # Run tests
python manage.py health                          # Check system
python manage.py test-openai                     # Test OpenAI

# Deployment
git push heroku main                             # Deploy to Heroku
heroku logs --tail                               # View logs
heroku config:set OPENAI_API_KEY=sk-proj-xxx    # Set env var

# Maintenance
python manage.py cleanup-convs 7                 # Clean conversations older than 7 days
python manage.py scrape-website                  # Update KB from website
```

---

## 📝 Environment Variables

```env
# REQUIRED
OPENAI_API_KEY=sk-proj-YOUR_KEY

# OPTIONAL
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_API_TOKEN=token_xxx
SHOPIFY_STORE_DOMAIN=store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxx
CLICKBANK_DEV_KEY=dev_xxx
CLICKBANK_CLERK_KEY=clerk_xxx
ENVIRONMENT=development
LOG_LEVEL=info
```

---

## 🧪 Test the Bot

### Via Swagger UI
1. Go to: http://localhost:8000/docs
2. Expand **POST /api/test**
3. Try this payload:
```json
{
  "content": "What is HardChews?",
  "conversation": {"id": 1, "account_id": 1},
  "contact": {"email": "test@example.com"}
}
```

### Via cURL
```bash
curl -X POST http://localhost:8000/api/test \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is HardChews?",
    "conversation": {"id": 1, "account_id": 1},
    "contact": {"email": "test@example.com"}
  }'
```

### Via Full Test Suite
```bash
python app/tests/test_conversations.py
```

---

## 🚀 Deploy to Production

### Heroku (Fastest)
```bash
heroku login
heroku create hardchews-ai-bot
git push heroku main
heroku config:set OPENAI_API_KEY=sk-proj-xxx
heroku open
```

### AWS
```bash
eb init -p python-3.11 hardchews-bot
eb create hardchews-bot-env
eb setenv OPENAI_API_KEY=sk-proj-xxx
eb deploy
```

### DigitalOcean
1. Connect GitHub repo to DigitalOcean App Platform
2. Set env vars in dashboard
3. Deploy (automatic on git push)

See SETUP_DEPLOYMENT_GUIDE.md for full instructions.

---

## 🔐 Credentials Needed

| Service | Credential | Where to Get |
|---------|-----------|-------------|
| OpenAI | API Key | https://platform.openai.com/account/api-keys |
| Chatwoot | API Token | Chatwoot Admin → Settings → Account Settings → API |
| Shopify | Access Token | Shopify Admin → Settings → Apps → Develop apps → Private App |
| ClickBank | Dev + Clerk Key | ClickBank Account → Settings → Account → API Keys |

---

## 📊 File Structure (Important Files)

```
app/
├── main.py                    ← FastAPI app
├── services/
│   ├── openai_service.py      ← OpenAI calls
│   ├── kb_service.py          ← Knowledge base
│   ├── router_service.py      ← Intent detection
│   ├── conversation_manager.py ← Memory
│   └── chatwoot_webhook.py    ← Webhook handler
├── kb/data/
│   ├── products_comprehensive.json    ← 7 product items
│   └── faqs_comprehensive.json        ← 12 FAQ items
└── tests/
    └── test_conversations.py   ← 23+ tests
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| "OpenAI API key invalid" | Check `.env`, get new key from https://platform.openai.com/account/api-keys |
| "Module not found" | `pip install -r requirements.txt` |
| "Bot not responding" | Check `/health` endpoint, verify OpenAI key |
| "Slow responses" | Normal (OpenAI ~1-2s), check internet |
| "Widget not showing" | Follow CHATWOOT_INTEGRATION_GUIDE.md |
| "Order lookup fails" | Check Shopify/ClickBank creds in `.env` |

See full troubleshooting in SETUP_DEPLOYMENT_GUIDE.md

---

## ✅ Production Checklist

- [ ] `.env` configured with all required keys
- [ ] `python manage.py health` returns all ✅
- [ ] `python app/tests/test_conversations.py` passes all tests
- [ ] Service deployed to production
- [ ] `/health` endpoint responds from production URL
- [ ] Chatwoot webhook configured
- [ ] Widget visible on hardchews.shop
- [ ] Test conversation works end-to-end
- [ ] Monitoring setup (optional but recommended)

---

## 📞 Support

1. **Check documentation** - Start with README.md
2. **Run health check** - `python manage.py health`
3. **Run tests** - `python app/tests/test_conversations.py`
4. **Check logs** - `heroku logs --tail` (or deployment's log service)
5. **Review guides** - See Documentation Quick Links above

---

## 🎯 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service status |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI (API documentation) |
| `/api/webhook/chatwoot` | POST | Incoming messages from Chatwoot |
| `/api/test` | POST | Local testing (no Chatwoot needed) |

---

## 🚀 What's Next?

**Immediate (Today)**
- [ ] Setup `.env` with OpenAI key
- [ ] Run `python manage.py health`
- [ ] Run tests: `python app/tests/test_conversations.py`

**This Week**
- [ ] Deploy to production (Heroku/AWS/DigitalOcean)
- [ ] Setup Chatwoot account
- [ ] Embed widget on hardchews.shop

**Next Week**
- [ ] Setup Shopify order lookup
- [ ] Test end-to-end conversations
- [ ] Monitor performance

**Future (V2/V3)**
- Email auto-reply
- Voice/Twilio integration
- Advanced analytics

---

## 📌 Remember

- **Always use `.env`** for credentials (never hardcode)
- **Never commit `.env`** to git
- **Test locally first** before deploying
- **Monitor logs** in production
- **Check `/health`** if something seems wrong

---

## 🎉 You're All Set!

**Status**: ✅ Ready to go
**Next Command**: `python manage.py health`
**Then**: Follow guide matching your need (see table above)

Questions? Check the full guides or run:
```bash
python manage.py help
```

Good luck! 🚀
