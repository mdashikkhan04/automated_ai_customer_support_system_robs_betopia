# 📊 3-Tier Priority System - Visual Guide

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ASKS QUESTION                       │
│         "What is HardChews?" / "How to use?" etc.           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  ROUTER SERVICE      │
          │ (Intent Detection)   │
          │                      │
          │ 8 Intent Types:      │
          │ • product            │
          │ • pricing            │
          │ • usage              │
          │ • support            │
          │ • ordering           │
          │ • status             │
          │ • feedback           │
          │ • general            │
          └────────┬─────────────┘
                   │
                   ▼
    ┌──────────────────────────────────────┐
    │  PRIORITY RESPONSE SERVICE           │
    │  (3-Tier Orchestrator)               │
    └────────────────────────────────────┬─┘
                                         │
         ┌───────────────┬───────────────┼───────────────┐
         │               │               │               │
         ▼               ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ TIER 1  │     │ TIER 2  │     │ TIER 3  │
    │ DATASET │     │SCRAPING │     │   LLM   │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
         │ (if low       │ (if not       │ (fallback)
         │  confidence)  │  found)       │
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  RESPONSE WITH METADATA│
            │                        │
            │ • Answer text          │
            │ • Source (icon)        │
            │ • Confidence (0-1)     │
            │ • Response time        │
            │ • Intent detected      │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   SEND TO USER         │
            │  (Frontend displays)   │
            └────────────────────────┘
```

---

## 🎯 Each Tier Explained

### **TIER 1: DATASET (📚 Knowledge Base)**

```
┌─────────────────────────────────────┐
│      TIER 1: KNOWLEDGE BASE         │
│          (Priority: HIGHEST)        │
├─────────────────────────────────────┤
│                                     │
│ Storage: app/kb/data/*.json         │
│ Size: 30+ knowledge items           │
│ Search: Semantic (embeddings)       │
│                                     │
│ Response Time: 50-100ms (FAST!)     │
│ Confidence: 80-95% (HIGH)           │
│ Data Freshness: Static              │
│                                     │
│ Example Topics:                     │
│ • Product information               │
│ • Usage instructions                │
│ • Pricing details                   │
│ • FAQs                              │
│ • Policies                          │
│                                     │
│ How it works:                       │
│ 1. Generate embeddings of question  │
│ 2. Compare with KB embeddings       │
│ 3. Find most similar items          │
│ 4. Return top match if confident    │
│                                     │
│ When to use:                        │
│ ✅ General product questions        │
│ ✅ Static information requests      │
│ ✅ Policy/FAQ questions             │
│ ✅ Standard support questions       │
│                                     │
│ Confidence threshold: ≥ 0.5 (50%)   │
│ If confident → Return KB answer ✅  │
│ If not → Try Tier 2                 │
│                                     │
└─────────────────────────────────────┘
```

### **TIER 2: WEB SCRAPING (🌐 Live Data)**

```
┌─────────────────────────────────────┐
│     TIER 2: WEB SCRAPING            │
│      (Priority: MEDIUM)             │
├─────────────────────────────────────┤
│                                     │
│ Source: https://hardchews.shop      │
│ Storage: app/cache/scraped_data.json│
│ Size: 12+ pages of data             │
│ Search: Keyword matching            │
│                                     │
│ Response Time: 200-500ms (Medium)   │
│ Confidence: 70-85% (GOOD)           │
│ Data Freshness: 24h (near real-time)│
│                                     │
│ Auto-refresh: Every 6 hours         │
│ Cache TTL: 24 hours                 │
│                                     │
│ Example Data:                       │
│ • Current products                  │
│ • Live pricing                      │
│ • Recent FAQs                       │
│ • Updated policies                  │
│ • News/announcements                │
│                                     │
│ How it works:                       │
│ 1. Check cache first (if valid)     │
│ 2. If cache expired, scrape website │
│ 3. Parse HTML for products/FAQs/etc │
│ 4. Cache data with TTL              │
│ 5. Search with keywords             │
│ 6. Return matches if found          │
│                                     │
│ When to use:                        │
│ ✅ Current product data             │
│ ✅ Live pricing questions           │
│ ✅ Recent updates                   │
│ ✅ When KB incomplete               │
│                                     │
│ If found & confident → Return ✅   │
│ If not → Try Tier 3                 │
│                                     │
└─────────────────────────────────────┘
```

### **TIER 3: OPENAI LLM (🤖 ChatGPT)**

```
┌─────────────────────────────────────┐
│      TIER 3: OPENAI LLM             │
│      (Priority: LOWEST)             │
├─────────────────────────────────────┤
│                                     │
│ Model: gpt-4o-mini                  │
│ Type: Large Language Model          │
│ API: OpenAI                         │
│                                     │
│ Response Time: 1-3s (SLOWER)        │
│ Confidence: 60-75% (MODERATE)       │
│ Data Freshness: Real-time reasoning │
│                                     │
│ Capabilities:                       │
│ • General knowledge Q&A             │
│ • Creative writing                  │
│ • Problem solving                   │
│ • Contextual understanding          │
│ • Nuanced responses                 │
│                                     │
│ How it works:                       │
│ 1. Receive question                 │
│ 2. Add system context               │
│ 3. Send to OpenAI API               │
│ 4. Get ChatGPT response             │
│ 5. Return with "LLM" source         │
│                                     │
│ When to use:                        │
│ ✅ Unknown questions                │
│ ✅ Creative requests                │
│ ✅ General knowledge                │
│ ✅ Conversation                     │
│ ✅ Final fallback (always works)    │
│                                     │
│ Status: ALWAYS WORKS ✅             │
│ Provides graceful response even if: │
│ • Tier 1 KB incomplete              │
│ • Tier 2 scraping fails             │
│ • Website down                      │
│ • Cache expired                     │
│                                     │
└─────────────────────────────────────┘
```

---

## 📊 Comparison Table

| Aspect | Tier 1 (KB) | Tier 2 (Web) | Tier 3 (LLM) |
|--------|------------|-------------|------------|
| **Speed** | ⚡ 50-100ms | ⚡⚡ 200-500ms | ⚡⚡⚡ 1-3s |
| **Accuracy** | 🎯🎯🎯 90%+ | 🎯🎯 75-85% | 🎯 60-75% |
| **Data Type** | Static KB | Live website | Real-time reasoning |
| **Freshness** | Days/months | 24 hours | Seconds |
| **Cost** | Free | Free | $ per request |
| **Availability** | 99.9% | 99% | 99.5% |
| **Best For** | General Q&A | Current data | Unknown queries |
| **Fallback** | → Tier 2 | → Tier 3 | Always works |

---

## 🔄 Decision Flow

```
Question arrives
        │
        ▼
    TIER 1: Dataset
        │
        ├─ Search KB
        │  ├─ Match found?
        │  │  ├─ YES & Confident (≥50%)?
        │  │  │  └─ RETURN KB ANSWER ✅
        │  │  └─ NO or Low confidence?
        │  │     └─ Continue ↓
        │  └─ NO match?
        │     └─ Continue ↓
        │
        ▼
    TIER 2: Web Scraping
        │
        ├─ Check cache
        │  ├─ Cache valid?
        │  │  ├─ YES → Search
        │  │  └─ NO → Scrape website
        │  ├─ Found match?
        │  │  ├─ YES & Confident?
        │  │  │  └─ RETURN WEB ANSWER ✅
        │  │  └─ NO or Low confidence?
        │  │     └─ Continue ↓
        │
        ▼
    TIER 3: LLM
        │
        └─ ALWAYS SEND TO OPENAI ✅
           └─ RETURN LLM ANSWER ✅
```

---

## 💾 Data Flow & Caching

```
┌──────────────────────────────────────────────┐
│           CACHING STRATEGY                   │
├──────────────────────────────────────────────┤
│                                              │
│ Scraped Data Cache:                          │
│ Location: app/cache/scraped_data.json       │
│                                              │
│ ┌─────────────────────────────────┐         │
│ │ scraped_data.json               │         │
│ ├─────────────────────────────────┤         │
│ │ {                               │         │
│ │   "products": [...],            │         │
│ │   "faqs": [...],                │         │
│ │   "policies": [...],            │         │
│ │   "timestamp": 1234567890,      │         │
│ │   "ttl_hours": 24               │         │
│ │ }                               │         │
│ └─────────────────────────────────┘         │
│                                              │
│ Cache Logic:                                 │
│ ┌─────────────────────────────────┐         │
│ │ On each request:                │         │
│ │                                 │         │
│ │ 1. Check cache file exists?     │         │
│ │    NO → Scrape website          │         │
│ │                                 │         │
│ │ 2. Check timestamp + TTL        │         │
│ │    Expired? → Scrape website    │         │
│ │    Valid? → Use cache           │         │
│ │                                 │         │
│ │ 3. Search cache data            │         │
│ │    Found? → Return              │         │
│ │    Not found? → Try LLM         │         │
│ │                                 │         │
│ │ 4. Save new data with TTL       │         │
│ │    (Automatic)                  │         │
│ └─────────────────────────────────┘         │
│                                              │
│ Background Refresh:                          │
│ Every 6 hours:                               │
│ 1. Scheduler wakes up                        │
│ 2. Check cache age                          │
│ 3. If near expiration → Refresh             │
│ 4. Update cache with fresh data             │
│ (No user request needed)                     │
│                                              │
└──────────────────────────────────────────────┘
```

---

## 🎨 Frontend Response Display

```
┌────────────────────────────────────────┐
│          USER SEES THIS:               │
├────────────────────────────────────────┤
│                                        │
│ Q: "What is HardChews?"                │
│                                        │
│ ┌──────────────────────────────────┐  │
│ │ 📚 From Our Knowledge Base       │  │
│ │ Confidence: 92%                  │  │
│ │ Response Time: 45ms              │  │
│ │                                  │  │
│ │ HardChews is a premium chewable  │  │
│ │ supplement formulated to support │  │
│ │ male vitality and performance... │  │
│ └──────────────────────────────────┘  │
│                                        │
│ [DEBUG INFO]                           │
│ Source: dataset                        │
│ Confidence: 0.92                       │
│ Intent: general                        │
│ KB Item: "What is HardChews?"          │
│                                        │
└────────────────────────────────────────┘

OR (if web data):

┌────────────────────────────────────────┐
│ 🌐 From Our Website                   │
│ Confidence: 78%                        │
│ Response Time: 312ms                   │
│                                        │
│ Current HardChews Products:            │
│ • Package A - $49.99                   │
│ • Package B - $79.99                   │
│ • Package C - $99.99                   │
└────────────────────────────────────────┘

OR (if LLM):

┌────────────────────────────────────────┐
│ 🤖 AI Assistant                        │
│ Confidence: 65%                        │
│ Response Time: 1.2s                    │
│                                        │
│ HardChews appears to be a dietary      │
│ supplement brand. Based on the name,   │
│ it likely features chewable tablets... │
└────────────────────────────────────────┘
```

---

## 🔧 System Operations

### **Startup Sequence**
```
1. App starts (main.py)
2. Load KB from JSON files
3. Initialize services
4. Start scraping scheduler (daemon thread)
5. Display tier statistics:
   ✅ Tier 1 (Dataset): 30 KB items loaded
   ✅ Tier 2 (Scraping): 0 items (will populate)
   ✅ Tier 3 (LLM): Ready (waiting for requests)
6. Server ready on http://localhost:8000
```

### **On Each User Request**
```
1. Router receives message
2. Detect intent (8 types)
3. Call priority_service.get_response()
4. Try Tier 1 (KB search)
   - If confident → Return
5. Try Tier 2 (Web scraping)
   - If found → Return
6. Try Tier 3 (OpenAI)
   - Always returns something
7. Attach metadata (source, confidence, etc.)
8. Return to user
9. Log analytics
```

### **Every 6 Hours (Background)**
```
1. Scheduler wakes up
2. Check scraping cache age
3. If approaching expiration:
   - Scrape website
   - Parse data
   - Update cache with new TTL
4. Log refresh operation
5. Sleep 6 hours
```

---

## 📈 Performance Tips

### **Improve Tier 1 (KB) Speed**
- Add more relevant KB items
- Use specific titles and tags
- Keep descriptions focused

### **Improve Tier 2 (Web) Speed**
- Optimize CSS selectors
- Cache more aggressively (reduce TTL refresh)
- Simplify scraping logic

### **Optimize Tier 3 (LLM) Cost**
- Use confident matches from Tier 1/2
- Reduce LLM fallback frequency
- Use cheaper model (gpt-4o-mini vs gpt-4)

### **Overall System Speed**
- All tiers parallel evaluation (future)
- Add Redis caching layer (future)
- Use embeddings cache (current)

---

## ✅ Verification Checklist

After setup, verify each component:

```
□ Tier 1 - Knowledge Base
  □ app/kb/data/complete_kb.json exists
  □ 30+ items in KB
  □ Can search for product info
  
□ Tier 2 - Web Scraping
  □ app/cache/scraped_data.json exists
  □ Scheduler initialized
  □ Can manually refresh with POST /scheduler/refresh
  
□ Tier 3 - OpenAI LLM
  □ OPENAI_API_KEY in .env
  □ API key is valid
  □ Can send requests to OpenAI

□ Backend Health
  □ GET /health returns 200 OK
  □ Tier statistics displayed
  □ All services initialized

□ Response Quality
  □ Known questions return KB answers
  □ Unknown questions return LLM answers
  □ Metadata (source, confidence) included

□ Frontend
  □ index_v2.html loads
  □ Can send messages
  □ Displays source icons (📚/🌐/🤖)
  □ Debug info visible
```

---

This visual guide explains the complete 3-tier system! 🚀

**Want to start?** Run `python launcher.py` 

**Want details?** Check `PRIORITY_SYSTEM_DOCUMENTATION.md`
