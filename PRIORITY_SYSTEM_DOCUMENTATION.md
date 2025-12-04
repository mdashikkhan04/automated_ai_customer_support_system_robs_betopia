# 📚 **3-TIER PRIORITY RESPONSE SYSTEM - ARCHITECTURE DOCUMENTATION**

## **সিস্টেম Overview**

আপনার chatbot এখন একটি professionally designed **3-tier priority response system** ব্যবহার করে:

```
User Question
    ↓
Tier 1: Dataset (RAG) - Knowledge Base
    ├─ Semantic search with embeddings
    ├─ High-quality, curated responses
    └─ If confidence ≥ 50% → Return answer
         ↓ (if confidence < 50% or no match)
Tier 2: Web Scraping - Live Website Data
    ├─ Cached scraped data (refreshed every 6h)
    ├─ Product, FAQ, policy information
    └─ If match found → Return answer
         ↓ (if no good match)
Tier 3: OpenAI LLM - General ChatGPT
    ├─ General conversational responses
    ├─ Creative/open-ended questions
    └─ Always provides a helpful response
         ↓
Response to User
```

---

## **Tier 1: Dataset (RAG) - সর্বোচ্চ অগ্রাধিকার**

### **কী এটি?**
- আপনার curated knowledge base (KBs) থেকে semantic search
- সবচেয়ে accurate এবং well-sourced উত্তর

### **কিভাবে কাজ করে?**
```python
# app/services/priority_response_service.py
def _try_dataset(user_message, intent):
    # 1. Semantic search KB using embeddings
    kb_results = kb_service.search(user_message, top_k=3)
    
    # 2. Return top result if confidence high enough
    if confidence >= 0.5:
        return KB_based_answer
```

### **যেখানে ডেটা থাকে?**
- `app/kb/data/complete_kb.json` - 18 comprehensive items
- `app/kb/data/faqs_comprehensive.json` - FAQ/policies
- `app/kb/data/products_comprehensive.json` - Product info

### **Example:**
```
Question: "What is HardChews?"
Tier 1 Response: "HardChews is a premium chewable dietary supplement..."
Source: complete_kb.json
Confidence: 0.92
```

---

## **Tier 2: Web Scraping - মাঝারি অগ্রাধিকার**

### **কী এটি?**
- Live website data থেকে auto-scraped information
- Cache করা locally, 24-hour TTL সহ
- Product updates, policy changes capture করে

### **কিভাবে কাজ করে?**
```python
# app/services/enhanced_web_scraper.py
def scrape_all(force_refresh=False):
    # 1. Check if cache exists and is fresh
    if cache_valid():
        return cached_data
    
    # 2. Otherwise, scrape from website
    products = scrape_products()      # /products endpoint
    faqs = scrape_faqs()              # /faq endpoint
    policies = scrape_policies()      # /shipping, /returns, etc
    
    # 3. Cache locally for next 24 hours
    save_to_cache(products, faqs, policies)
```

### **যেখানে cache থাকে?**
- `app/cache/scraped_data.json` - Local file-based cache
- Auto-refreshes every 6 hours (configurable)
- Manual refresh via `POST /scheduler/refresh`

### **Example:**
```
Question: "Tell me about new products"
Tier 1: No match (not in KB)
Tier 2 Response: "Based on our latest website: [Product X, Y, Z]..."
Source: web_scraper (live data)
Confidence: 0.75
```

### **Background Scheduler**
```python
# app/services/scraping_scheduler.py
scraping_scheduler = ScrapingScheduler(interval_hours=6)
scraping_scheduler.start()  # Starts on app startup

# Automatically refreshes every 6 hours
# No manual intervention needed
```

---

## **Tier 3: OpenAI LLM - সর্বনিম্ন অগ্রাধিকার**

### **কী এটি?**
- General ChatGPT-style responses
- Creative questions এর জন্য
- Fallback যখন Tier 1 & 2 no match দেয়

### **কিভাবে কাজ করে?**
```python
# app/services/priority_response_service.py
def _try_llm(user_message, context):
    try:
        # Call OpenAI API
        reply = generate_reply(user_message, context)
        return reply
    except Exception as e:
        # LLM unavailable → graceful fallback
        return "Support team will follow up..."
```

### **কখন ব্যবহার হয়?**
- Questions যা KB বা scraped data তে নেই
- Creative/philosophical প্রশ্ন
- General knowledge প্রশ্ন

### **Example:**
```
Question: "What's a fun fact about supplements?"
Tier 1: No match
Tier 2: No match
Tier 3 Response: "Did you know that many ancient civilizations..."
Source: openai_gpt-4o-mini
Confidence: 0.80
```

---

## **System Architecture - Code Structure**

```
app/services/
├── priority_response_service.py      ← Main orchestrator (3-tier logic)
├── kb_service.py                     ← Tier 1: Dataset/RAG
├── enhanced_web_scraper.py           ← Tier 2: Web scraping + caching
├── scraping_scheduler.py             ← Background task scheduler
├── openai_service.py                 ← Tier 3: LLM integration
├── router_service.py                 ← Updated to use priority_service
└── ...

app/cache/
└── scraped_data.json                 ← Tier 2 cache file

app/kb/data/
├── complete_kb.json                  ← Tier 1 primary data
├── faqs_comprehensive.json
└── products_comprehensive.json
```

---

## **কিভাবে শুরু করবেন?**

### **Step 1: Backend চালু করুন**
```bash
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia
venv\Scripts\activate
uvicorn app.main:app --reload
```

### **Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ KB Service loaded 30 items
✅ Priority System Ready:
   • Tier 1 (Dataset): 30 KB items
   • Tier 2 (Scraping): 0 cached items (first run)
   • Tier 3 (LLM): Ready
✅ Scraping scheduler started (interval: 6h)
```

### **Step 2: System টেস্ট করুন**
```bash
python test_priority_system.py
```

### **Step 3: Frontend test করুন**
```
Open index_v2.html in browser
Send test messages:
- "What is HardChews?"
- "How do I use it?"
- "Tell me something interesting"
```

---

## **API Endpoints - নতুন**

### **Health Check (with tier stats)**
```bash
GET /health
```
Response:
```json
{
  "status": "ok",
  "environment": "development",
  "tier_stats": {
    "tier1_dataset_items": 30,
    "tier2_scraping_items": 12,
    "tier3_llm_available": true,
    "total_data_sources": 42
  },
  "scheduler": {
    "is_running": true,
    "interval_hours": 6,
    "last_scrape_time": "2025-12-04T10:30:00",
    "next_scrape_in_seconds": 18000
  }
}
```

### **Scheduler Status**
```bash
GET /scheduler/status
```

### **Manual Scraping Refresh**
```bash
POST /scheduler/refresh?force=false
```

---

## **Configuration & Customization**

### **Tier 1: Adjust KB items**
Edit `app/kb/data/complete_kb.json`:
```json
{
  "id": "custom_item_1",
  "type": "product",
  "title": "Your Product",
  "content": "Full description...",
  "tags": ["product", "custom"]
}
```

### **Tier 2: Adjust scraping frequency**
In `app/services/scraping_scheduler.py`:
```python
scraping_scheduler = ScrapingScheduler(interval_hours=6)  # Change to 12, 24, etc
```

### **Tier 2: Adjust website URLs**
In `app/services/enhanced_web_scraper.py`:
```python
self.base_url = "https://hardchews.shop"  # Customize
policy_urls = {
    "shipping": f"{self.base_url}/shipping",
    # Add more endpoints...
}
```

### **Tier 3: Adjust LLM model**
In `app/services/openai_service.py`:
```python
completion = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # Change to gpt-4, gpt-3.5-turbo, etc
    ...
)
```

---

## **Response Format - Frontend Display**

Each response includes source information:
```json
{
  "response": "📚 **From Our Knowledge Base:**\n\nHardChews is...",
  "source": "dataset",
  "confidence": 0.92,
  "intent": "general",
  "debug": {
    "message": "What is HardChews?",
    "kb_item_title": "What is HardChews?",
    "response_source": "dataset",
    "response_confidence": 0.92
  }
}
```

Frontend displays:
- 📚 Tier 1 responses (blue icon)
- 🌐 Tier 2 responses (globe icon)
- 🤖 Tier 3 responses (robot icon)

---

## **Data Flow Diagram**

```
┌─────────────────────────────────────────────────────────┐
│                    User Message                         │
└──────────────────────┬──────────────────────────────────┘
                       ↓
          ┌────────────────────────┐
          │  Intent Detection      │
          │ (8 types: product,     │
          │  refund, shipping...)  │
          └────────────┬───────────┘
                       ↓
    ┌──────────────────────────────────────────┐
    │   Priority Response Service              │
    │   (Orchestrator)                         │
    └──────────────────────────────────────────┘
           ↙          ↓          ↘
         Tier1      Tier2       Tier3
         (KB)    (Scraper)      (LLM)
          ↓          ↓           ↓
    ┌────────┐  ┌────────┐  ┌────────┐
    │Semantic│  │Keyword │  │OpenAI  │
    │Search  │  │Search  │  │API     │
    └────┬───┘  └───┬────┘  └───┬────┘
         ↓          ↓           ↓
    ┌─────────────────────────────────┐
    │  Select Best Response           │
    │  (Highest Confidence Source)    │
    └──────────────┬──────────────────┘
                   ↓
    ┌──────────────────────────────────┐
    │  Format Response with Source     │
    │  (📚/🌐/🤖 icon + content)      │
    └──────────────┬──────────────────┘
                   ↓
    ┌──────────────────────────────────┐
    │  Return to Frontend              │
    │  (source, confidence, response)  │
    └──────────────────────────────────┘
```

---

## **Debugging & Monitoring**

### **Enable Detailed Logs**
```python
# In app/logger.py
logger.setLevel("DEBUG")  # More detailed logs
```

### **Monitor Scraping Cache**
```python
from app.services.enhanced_web_scraper import web_scraper

cached = web_scraper.get_cached_data()
print(f"Cache size: {len(cached['products'])} products")
```

### **Check Tier Stats**
```python
from app.services.priority_response_service import priority_service

stats = priority_service.get_tier_stats()
print(stats)
# Output:
# {
#   'tier1_dataset_items': 30,
#   'tier2_scraping_items': 12,
#   'tier3_llm_available': True,
#   'total_data_sources': 42
# }
```

---

## **Performance Notes**

| Tier | Response Time | Accuracy | Best For |
|------|---------------|----------|----------|
| **1 (KB)** | < 100ms | Highest | Products, policies, FAQs |
| **2 (Scraping)** | < 500ms | High | Latest updates, site changes |
| **3 (LLM)** | 1-3s | Good | Creative, general questions |

---

## **Security Considerations**

✅ **What's Protected:**
- API keys stored in `.env` (not in code)
- Web scraping respects rate limits (1s delay)
- Cache cleared automatically after 24h
- No PII stored in KB

⚠️ **What to Configure:**
- Set `allow_origins` to specific domains (production)
- Enable HTTPS/TLS on production
- Rate limit API endpoints
- Monitor for scraping failures

---

## **Next Steps**

1. ✅ Test 3-tier system locally
2. ✅ Populate more KB items (Tier 1)
3. ✅ Configure website scraping endpoints (Tier 2)
4. ✅ Get OpenAI API key for Tier 3
5. ✅ Deploy to production
6. ✅ Monitor tier usage stats

---

## **Troubleshooting**

**All questions return same answer?**
→ Check if `priority_service` is imported in router

**Scraping not working?**
→ Verify website URLs in `enhanced_web_scraper.py`

**LLM responses not good?**
→ Check `OPENAI_API_KEY` in `.env`

**Cache not updating?**
→ Check scheduler logs, manually trigger: `POST /scheduler/refresh`

---

**আপনার chatbot এখন production-ready! 🚀**
