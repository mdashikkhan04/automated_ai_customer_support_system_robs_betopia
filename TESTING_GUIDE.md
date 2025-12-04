# HardChews Chatbot - Step-by-Step Testing Guide

**Last Updated:** 2025-12-04
**Status:** ✅ Ready for Testing

---

## Prerequisites

1. **Server Status**: Check if server is running
   ```powershell
   curl -s http://localhost:8000/health | ConvertFrom-Json | ConvertTo-Json
   ```
   
   Expected: Status 200 with tier stats showing 47 KB items

2. **If server is NOT running**, start it:
   ```powershell
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

---

## STEP 1: Verify Pinecone Data (Run Once)

```powershell
python app/services/pinecone_ingest.py
```

Expected Output:
```
Loading KB items...
Loaded 47 KB items
Upserting KB to Pinecone...
[SUCCESS] Pinecone upsert complete!
Indexed 47 KB items + 0 scraping items
```

---

## STEP 2: Test Chat Endpoint

Run the comprehensive test suite:

```powershell
python test_chat.py
```

This will test:
- ✅ Health endpoint
- ✅ Refund policy question
- ✅ Support center location
- ✅ Shipping policy question
- ✅ Company information

**Expected Behavior:**
- Tier 1 or 3 responses (Pinecone KB or OpenAI LLM)
- Confidence scores between 0.0 and 1.0
- Relevant answers from KB about HardChews policies

---

## STEP 3: Manual Test via cURL (Optional)

```powershell
# Test Question
$body = @{user_message='What is your refund policy?'} | ConvertTo-Json
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d $body
```

---

## STEP 4: View API Documentation

Open in browser:
```
http://localhost:8000/docs
```

This gives you:
- All available endpoints
- Request/response schemas
- Try-it-out functionality

---

## STEP 5: View Server Logs (Optional)

Start server with visible logging:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level debug
```

This shows:
- Tier decisions (1=KB, 2=Scraping, 3=LLM)
- Confidence scores
- Pinecone queries
- OpenAI LLM calls

---

## System Architecture

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Tier 1: Pinecone KB Search  │  (Instant, no API calls)
│   • 47 KB items indexed      │
│   • Semantic similarity      │
│   • Threshold: confidence >0.3
└─────────────────────────────┘
         │
      NO │ MATCH
         ├──────────────────┐
         │                  ▼
         │         ┌──────────────────────┐
         │         │ Tier 2: Web Scraping  │ (Cached)
         │         │   • Current: 0 items  │
         │         │   • From hardchews.me │
         │         │   • Threshold: >0.3   │
         │         └──────────────────────┘
         │                  │
      NO │ MATCH           │
         └──────────────────┤
                           ▼
                  ┌──────────────────────┐
                  │ Tier 3: OpenAI LLM   │ (Fallback)
                  │  • gpt-4o-mini model │
                  │  • Full context      │
                  │  • ~2-3 sec latency  │
                  └──────────────────────┘
                           │
                           ▼
                  ┌──────────────────────┐
                  │ Response to User     │
                  └──────────────────────┘
```

---

## Endpoints Available

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root - API info |
| `/health` | GET | Health check with tier stats |
| `/chat` | POST | Main chat endpoint |
| `/docs` | GET | Swagger UI documentation |
| `/scheduler/status` | GET | Scraping scheduler status |
| `/scheduler/refresh` | POST | Trigger manual refresh |

---

##  Example Chat Request/Response

**Request:**
```json
{
  "user_message": "What is your refund policy?"
}
```

**Response:**
```json
{
  "reply": "60-day money-back guarantee...",
  "tier": 1,
  "confidence": 0.95,
  "tokens_used": null
}
```

---

## Troubleshooting

### Problem: Server won't start
```
Solution: Check if port 8000 is in use
powershell: Get-NetTCPConnection -LocalPort 8000
Kill process: Stop-Process -Id <PID> -Force
```

### Problem: Pinecone API key not found
```
Solution: Ensure .env file exists in project root with:
PINECONE_API_KEY=your_api_key
PINECONE_INDEX=hardchews-support-index
```

### Problem: All responses are Tier 3 (LLM)
```
Solution: This is normal - means Pinecone KB search isn't matching
Check: python app/services/pinecone_ingest.py
Verify: Pinecone index has 47 items
```

### Problem: Slow responses (>5 seconds)
```
Solution: Tier 3 (LLM) is slow (~2-3 sec per call)
Faster: Questions matching Tier 1 KB are instant (<100ms)
```

---

## Next Steps

1. ✅ Test all endpoints with provided questions
2. ✅ Verify Tier 1 (KB) is being used for related questions
3. ⚠️ If Tier 3 (LLM) only: Check Pinecone index populated
4. 🔧 Enable scraper when hardchews.me real URLs confirmed
5. 🚀 Deploy to production

---

## Files & Locations

- **Chatbot API**: `app/main.py`
- **Tier Logic**: `app/services/priority_response_service.py`
- **Pinecone RAG**: `app/services/pinecone_rag.py`
- **KB Data**: `app/kb/data/complete_kb.json` (47 items)
- **Test Script**: `test_chat.py`
- **Configuration**: `.env` (not in repo, local only)

---

**Need Help?** Contact: Your AI Assistant 🤖
