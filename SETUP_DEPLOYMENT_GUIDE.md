# HardChews AI Chatbot - Complete Setup & Deployment Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Local Development Setup](#local-development-setup)
3. [Environment Configuration](#environment-configuration)
4. [Running the Chatbot](#running-the-chatbot)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The HardChews AI Chatbot is a FastAPI-based service that:
- Answers customer questions using a knowledge base (KB)
- Integrates with Chatwoot for live chat on hardchews.shop
- Checks order status via Shopify and ClickBank APIs
- Handles multi-turn conversations with context memory
- Escalates complex issues to human agents

### Architecture

```
[HardChews.shop] 
    ↓ (Chatwoot widget)
[Chatwoot Inbox]
    ↓ (webhook)
[AI Bot Service] ← OpenAI API
    ↓ ↓ ↓
[KB Service] [Shopify API] [ClickBank API]
    ↑
[Conversation Memory]
```

---

## Local Development Setup

### Prerequisites

- **Python**: 3.9 or higher
- **Git**: For version control
- **OpenAI API Key**: Get from https://platform.openai.com/account/api-keys
- **Chatwoot Account**: (Optional for local testing)

### Step 1: Clone Repository

```bash
cd /path/to/workspace
git clone https://github.com/mdashikkhan04/automated_ai_customer_support_system_robs_betopia.git
cd automated_ai_customer_support_system_robs_betopia
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected output:
```
Successfully installed fastapi uvicorn openai python-dotenv pydantic requests numpy pydantic-settings beautifulsoup4...
```

### Step 4: Create .env File

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

See [Environment Configuration](#environment-configuration) section below.

---

## Environment Configuration

### Required Variables

Create `.env` file in project root with:

```env
# ==========================================
# OpenAI Configuration (REQUIRED)
# ==========================================
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE

# Get from: https://platform.openai.com/account/api-keys

# ==========================================
# Chatwoot Configuration (OPTIONAL - for chat widget)
# ==========================================
CHATWOOT_BASE_URL=https://app.chatwoot.com
CHATWOOT_API_TOKEN=YOUR_API_TOKEN
CHATWOOT_BOT_NAME=HardChews Assistant

# For self-hosted: CHATWOOT_BASE_URL=https://your-chatwoot-domain.com

# ==========================================
# Shopify Configuration (OPTIONAL - for order lookup)
# ==========================================
SHOPIFY_STORE_DOMAIN=yourstore.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_YOUR_TOKEN

# Get from: Shopify Admin → Settings → Apps and integrations → Develop apps

# ==========================================
# ClickBank Configuration (OPTIONAL - for ClickBank orders)
# ==========================================
CLICKBANK_DEV_KEY=your_dev_key
CLICKBANK_CLERK_KEY=your_clerk_key

# Get from: ClickBank → Settings → Account → API Keys

# ==========================================
# General Configuration
# ==========================================
ENVIRONMENT=development
LOG_LEVEL=info

# In production, change to:
# ENVIRONMENT=production
# LOG_LEVEL=warning
```

### Configuration Guide

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| OPENAI_API_KEY | OpenAI API key | ✓ YES | sk-proj-xxx |
| CHATWOOT_BASE_URL | Chatwoot instance URL | ✗ No | https://app.chatwoot.com |
| CHATWOOT_API_TOKEN | Chatwoot API token | ✗ No (if using chat) | token_xxx |
| SHOPIFY_STORE_DOMAIN | Your Shopify store | ✗ No (if using orders) | store.myshopify.com |
| SHOPIFY_ACCESS_TOKEN | Shopify private app token | ✗ No (if using orders) | shpat_xxx |
| CLICKBANK_DEV_KEY | ClickBank developer key | ✗ No (if using CB) | dev_xxx |
| CLICKBANK_CLERK_KEY | ClickBank clerk key | ✗ No (if using CB) | clerk_xxx |
| ENVIRONMENT | dev/production | ✗ No | development |
| LOG_LEVEL | Logging level | ✗ No | info |

---

## Running the Chatbot

### Local Development

```bash
# Activate venv first (if not already)
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Access the API

- **Main**: http://localhost:8000
- **Health check**: http://localhost:8000/health
- **API docs**: http://localhost:8000/docs (Swagger UI)
- **Test endpoint**: http://localhost:8000/api/test

### Test the Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/test \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is HardChews?",
    "conversation": {"id": 1, "account_id": 1},
    "contact": {"email": "test@example.com"}
  }'
```

Expected response:
```json
{
  "reply": "HardChews is a premium dietary supplement...",
  "intent": "general",
  "handoff": false,
  "used_kb": true
}
```

---

## Testing

### Run Test Suite

```bash
# Make sure venv is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Run all tests (23+ scenarios)
python app/tests/test_conversations.py
```

### Expected Output

```
======================================================================
🧪 RUNNING 23+ HARDCHEWS CHATBOT CONVERSATION TESTS
======================================================================

📌 Section 1: Greeting & General Questions
✓ Test 1 Greeting (Hi): Hi there! I'm here to help...
✓ Test 2 Product Info: HardChews is a premium...
✓ Test 3 How It Works: HardChews works by...
...
✓ Test 23 Typo Handling: I'd be happy to help...

======================================================================
✅ ALL TESTS COMPLETED!
======================================================================
```

### Individual Test

```bash
# Test specific scenario
python -c "
from app.tests.test_conversations import test_greeting_hello
test_greeting_hello()
"
```

---

## Deployment

### Option 1: Deploy to Heroku (Easiest for Beginners)

1. **Create Heroku account**: https://www.heroku.com
2. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
3. **Create Procfile** (already in repo)
4. **Deploy**:

```bash
heroku login
heroku create hardchews-ai-bot
git push heroku main
heroku config:set OPENAI_API_KEY=sk-proj-xxx
heroku logs --tail
```

Your API will be at: `https://hardchews-ai-bot.herokuapp.com`

### Option 2: Deploy to AWS (Scalable)

1. **Create AWS account**
2. **Use Elastic Beanstalk**:

```bash
eb init -p python-3.11 hardchews-bot
eb create hardchews-bot-env
eb setenv OPENAI_API_KEY=sk-proj-xxx
eb deploy
```

API will be at: `https://hardchews-bot-env.elasticbeanstalk.com`

### Option 3: Deploy to DigitalOcean (Recommended)

1. **Create DigitalOcean account**: https://www.digitalocean.com
2. **Create App Platform app**
3. **Connect GitHub repo**
4. **Set environment variables** in dashboard
5. **Deploy** (automatic on git push)

### Option 4: Self-Hosted (Full Control)

```bash
# On your server (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3 python3-pip

# Clone repo
git clone https://github.com/mdashikkhan04/...
cd automated_ai_customer_support_system_robs_betopia

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env

# Run with PM2 (for process management)
npm install -g pm2
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name hardchews-bot
pm2 startup
pm2 save
```

### Get Your Deployment URL

After deployment, you'll have a URL like:
- Heroku: `https://hardchews-ai-bot.herokuapp.com`
- AWS: `https://hardchews-bot-env.elasticbeanstalk.com`
- DigitalOcean: `https://hardchews-bot.ondigitalocean.app`
- Self-hosted: `https://your-domain.com`

**Use this URL in Chatwoot webhook configuration.**

---

## Monitoring & Maintenance

### Health Check

```bash
# Check if bot is running
curl https://your-deployment-url/health

# Expected response
{"status": "ok", "environment": "production"}
```

### View Logs

**Heroku**:
```bash
heroku logs --tail
```

**AWS**:
```bash
eb logs
```

**Self-hosted**:
```bash
pm2 logs hardchews-bot
```

### Monitor Performance

- **Response time**: Aim for < 3 seconds
- **Error rate**: Should be < 1%
- **API calls**: Monitor OpenAI usage in billing

### Update Knowledge Base

```bash
# Scrape website for new content (optional)
python -c "
from app.services.web_scraper import scrape_hardchews_website
scrape_hardchews_website('https://hardchews.shop')
"

# New KB files are saved to: app/kb/data/scraped_website_data.json
# Manually review and integrate as needed
```

---

## Troubleshooting

### Bot not responding

**Check:**
1. Is the service running? `curl https://your-url/health`
2. OpenAI API key valid? Check `.env`
3. Check logs for errors

### Slow responses

**Causes:**
- OpenAI API latency (usually < 1s)
- Network issues
- High KB (many documents)

**Solution:**
- Monitor OpenAI performance
- Consider caching frequent questions
- Scale horizontally (add more instances)

### Widget not showing on hardchews.shop

**Check:**
1. Chatwoot script added to Shopify theme?
2. Website token correct?
3. Chatwoot account active?

**See**: `CHATWOOT_INTEGRATION_GUIDE.md`

### Order lookup not working

**Check:**
1. Shopify/ClickBank credentials valid?
2. Email format correct in message?
3. Order exists in system?

**See**: `SHOPIFY_CLICKBANK_SETUP.md`

### Database errors (future)

When upgrading to PostgreSQL:
```bash
# Migrate conversations
python scripts/migrate_conversations.py
```

---

## Production Checklist

Before going live to customers:

- [ ] All `.env` variables set (no placeholders)
- [ ] OPENAI_API_KEY verified
- [ ] Service deployed and health check passing
- [ ] Chatwoot webhook configured
- [ ] Widget showing on hardchews.shop
- [ ] Test conversation working end-to-end
- [ ] Monitoring/alerts setup
- [ ] Fallback human agent trained
- [ ] Response templates approved by client
- [ ] Security audit completed
- [ ] Rate limiting enabled (if needed)
- [ ] Logging and error handling verified

---

## Version Information

```
Python: 3.9+
FastAPI: 0.95+
OpenAI: 1.0+
Pydantic: 2.0+
```

Check versions:
```bash
pip list
python --version
```

---

## Support & Help

- **API Docs**: Visit `/docs` on your deployment
- **Chatwoot Docs**: https://www.chatwoot.com/docs
- **OpenAI Docs**: https://platform.openai.com/docs
- **GitHub Issues**: Report bugs on repository

---

## Quick Reference

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Start dev server | `uvicorn app.main:app --reload` |
| Run tests | `python app/tests/test_conversations.py` |
| Check health | `curl /health` |
| View docs | Open `http://localhost:8000/docs` |
| Deploy (Heroku) | `git push heroku main` |
| View logs | `heroku logs --tail` |

---

## Architecture Summary

```
Request Flow:
1. Customer sends message via Chatwoot widget
2. Chatwoot sends webhook to bot endpoint
3. Bot extracts intent + email + order number (if any)
4. Bot searches KB using semantic similarity
5. Bot optionally checks Shopify/ClickBank for orders
6. Bot calls OpenAI with context + KB info
7. Bot receives reply and posts to Chatwoot
8. Customer sees reply in chat widget

Context Management:
- Conversation history stored in memory (dev) or file (production)
- Last 10 messages kept for context
- Older messages summarized to save tokens
- Conversation expires after 24 hours

Knowledge Base:
- FAQS: ~12 items (policies, shipping, refunds)
- Products: ~7 items (benefits, ingredients, usage, safety)
- Website scraped content: Optional, manual integration
- Embeddings: Text-embedding-3-small from OpenAI
- Search: Cosine similarity, top-5 results
```

---

## Next Steps

1. ✅ Setup local development environment
2. ✅ Configure `.env` with your credentials
3. ✅ Run tests to verify everything works
4. ✅ Deploy to production
5. ✅ Integrate Chatwoot on hardchews.shop
6. ✅ Test end-to-end conversations
7. ✅ Monitor for issues and optimize

---

**Last Updated**: December 3, 2025
**Maintained by**: HardChews Development Team
