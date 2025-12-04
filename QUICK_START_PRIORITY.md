# ⚡ **QUICK START - 3-TIER PRIORITY SYSTEM**

## **60 সেকেন্ডে Setup করুন**

```bash
# 1. Backend চালু করুন
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal এ দেখবেন:
# ✅ Priority System Ready:
#    • Tier 1 (Dataset): 30 KB items
#    • Tier 2 (Scraping): 0 items (first run)
#    • Tier 3 (LLM): Ready
# ✅ Scraping scheduler started
```

## **Frontend টেস্ট করুন (ব্রাউজার এ)**

```
1. index_v2.html খুলুন
2. এই প্রশ্নগুলো পাঠান:
   - "What is HardChews?" → Tier 1 (KB)
   - "How should I take it?" → Tier 1 (KB)
   - "Tell me something fun" → Tier 3 (LLM)
```

## **System টেস্ট করুন (Terminal এ)**

```bash
python test_priority_system.py
```

Expected output:
```
🧪 TIER 1 TEST - Dataset (RAG) Responses
❓ Query: What is HardChews?
   ✅ Found in Dataset (confidence: 0.92)
   KB Item: What is HardChews?

🌐 TIER 2 TEST - Web Scraping Data
   Products: 0 (first run, cache empty)
   FAQs: 0
   Policies: 0

🤖 TIER 3 TEST - OpenAI LLM Fallback
   Test Query: Tell me something creative about supplements
   ✅ LLM Response Generated
```

---

## **সিস্টেম কিভাবে কাজ করে?**

### **Priority Chain:**
```
Question
  ↓
Tier 1: Dataset (KB) — সর্বোচ্চ অগ্রাধিকার
  ├─ Match found? → Return KB answer
  └─ No match ↓
Tier 2: Web Scraping — মাঝারি অগ্রাধিকার
  ├─ Match found? → Return scraped data
  └─ No match ↓
Tier 3: OpenAI LLM — সর্বনিম্ন অগ্রাধিকার
  └─ Return ChatGPT-style answer
```

### **Response Example:**
```
Question: "What is HardChews?"

Response:
"📚 **From Our Knowledge Base:**

HardChews is a premium chewable dietary supplement formulated 
to support male vitality and performance..."

Debug Info:
- Source: dataset
- Confidence: 0.92
- Intent: general
- KB Item: "What is HardChews?"
```

---

## **API Endpoints**

### **Chat Endpoint**
```bash
curl -X POST http://localhost:8000/api/test \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "What is HardChews?"
  }'
```

### **Health & Stats**
```bash
# Full system status
curl http://localhost:8000/health

# Scheduler status
curl http://localhost:8000/scheduler/status

# Refresh scraping cache
curl -X POST http://localhost:8000/scheduler/refresh
```

---

## **Files যা তৈরি/Update হয়েছে**

| File | Purpose |
|------|---------|
| `app/services/priority_response_service.py` | **NEW** - 3-tier orchestrator |
| `app/services/enhanced_web_scraper.py` | **NEW** - Web scraping + caching |
| `app/services/scraping_scheduler.py` | **NEW** - Background scheduler |
| `app/services/router_service.py` | **UPDATED** - Use priority_service |
| `app/main.py` | **UPDATED** - Start scheduler on startup |
| `app/services/openai_service.py` | **UPDATED** - Better error handling |
| `test_priority_system.py` | **NEW** - Comprehensive test suite |
| `PRIORITY_SYSTEM_DOCUMENTATION.md` | **NEW** - Full documentation |

---

## **Data Sources**

### **Tier 1 (Dataset)**
- Location: `app/kb/data/complete_kb.json` (18 items)
- Plus: `faqs_comprehensive.json`, `products_comprehensive.json`
- Total: 30+ knowledge base items

### **Tier 2 (Scraping)**
- Website: https://hardchews.shop
- Cache: `app/cache/scraped_data.json`
- Auto-refresh: Every 6 hours
- Manual refresh: `POST /scheduler/refresh`

### **Tier 3 (LLM)**
- Model: OpenAI GPT-4o-mini
- Fallback: Graceful message if API unavailable

---

## **Key Features**

✅ **Data-First Approach** — KB data always prioritized
✅ **Live Updates** — Website scraping every 6 hours
✅ **Graceful Fallback** — Always provides helpful response
✅ **Background Processing** — No manual intervention needed
✅ **Comprehensive Logging** — Monitor all operations
✅ **Production Ready** — Professional architecture

---

## **Monitor System Health**

### **Backend Logs (Terminal এ)**
```
✅ KB Service loaded 30 items
✅ Priority System Ready:
   • Tier 1 (Dataset): 30 KB items
   • Tier 2 (Scraping): X items
   • Tier 3 (LLM): Ready
✅ Scraping scheduler started
```

### **Manual Check**
```bash
# Terminal এ
curl http://localhost:8000/health | python -m json.tool

# Output:
# {
#   "status": "ok",
#   "tier_stats": {
#     "tier1_dataset_items": 30,
#     "tier2_scraping_items": 12,
#     "tier3_llm_available": true,
#     "total_data_sources": 42
#   }
# }
```

---

## **Customization**

### **Add more KB items**
Edit `app/kb/data/complete_kb.json`:
```json
{
  "id": "new_item_1",
  "type": "product",
  "title": "Your Product",
  "content": "Detailed description...",
  "tags": ["product", "new"]
}
```

### **Change scraping interval**
In `app/services/scraping_scheduler.py`:
```python
scraping_scheduler = ScrapingScheduler(interval_hours=12)  # Change from 6 to 12
```

### **Change website URL**
In `app/services/enhanced_web_scraper.py`:
```python
def __init__(self, base_url: str = "https://your-site.com"):
```

---

## **Troubleshooting**

| Problem | Solution |
|---------|----------|
| All responses same | Restart backend, verify priority_service imported |
| Scraping not working | Check website URLs in enhanced_web_scraper.py |
| LLM not responding | Verify OPENAI_API_KEY in .env |
| Scheduler not running | Check backend logs for startup errors |

---

## **Next Steps**

1. ✅ Test locally with `test_priority_system.py`
2. ✅ Add more KB items as needed
3. ✅ Configure website endpoints for scraping
4. ✅ Get OpenAI API key
5. ✅ Deploy to production
6. ✅ Monitor tier usage statistics

---

**আপনার 3-tier chatbot প্রস্তুত! 🚀**

**Start:** `uvicorn app.main:app --reload`
**Test:** `python test_priority_system.py`
**Frontend:** Open `index_v2.html`
