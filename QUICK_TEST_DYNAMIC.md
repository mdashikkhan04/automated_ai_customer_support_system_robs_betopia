# 🚀 **QUICK TEST GUIDE - Dynamic Responses Ready**

## **ধাপে ধাপে Test করার জন্য কমান্ড:**

### **Step 1: Backend চালু করুন (Terminal 1)**

```powershell
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia
venv\Scripts\activate
uvicorn app.main:app --reload
```

**দেখবেন:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ KB Service loaded 30 items from knowledge base
✅ Embeddings generated for 30 KB items
INFO:     Application startup complete
```

---

### **Step 2: Backend Health Check করুন (Terminal 2)**

```powershell
curl http://localhost:8000/health
```

**সফল হলে দেখবেন:**
```
{"status":"healthy","version":"1.0"}
```

---

### **Step 3: Test Script চালান (Optional - Terminal 2)**

```powershell
# ভার্চুয়াল environment activate করুন
venv\Scripts\activate

# Test script চালান
python test_hybrid_system.py
```

**দেখবেন:**
```
===============================================================================
🧪 HYBRID RESPONSE SYSTEM - TEST RESULTS
===============================================================================

❓ Question: What is HardChews?
   Intent: general
✅ Response:
   HardChews is a premium chewable dietary supplement formulated to support 
   male vitality and performance. Each tablet is scientifically designed with 
   natural ingredients...

❓ Question: How do I use it?
   Intent: usage
✅ Response:
   Recommended Dosage: Take 1-2 tablets 30-60 minutes before use. Place tablet 
   in mouth and chew thoroughly for maximum absorption...

[... আরও অনেক টেস্ট ...]
```

---

### **Step 4: Frontend Test করুন (Browser)**

```
1. Windows Explorer খুলুন
2. Navigate: d:\Asik\robs\automated_ai_customer_support_system_robs_betopia
3. index_v2.html খুঁজুন
4. ডাবল ক্লিক → ব্রাউজার এ খুলবে
```

---

### **Step 5: বিভিন্ন প্রশ্ন পাঠান:**

```
Test Case 1:
━━━━━━━━━━━
ইনপুট:   "What is HardChews?"
আশা:     Product information
দেখবেন:  ✅ Different answer (না যে একই!), debug info with "general" intent

Test Case 2:
━━━━━━━━━━━
ইনপুট:   "How should I take it?"
আশা:     Usage instructions
দেখবেন:  ✅ Different answer, debug info with "usage" intent, dosage details

Test Case 3:
━━━━━━━━━━━
ইনপুট:   "What's your refund policy?"
আশা:     Refund information
দেখবেন:  ✅ Different answer, debug info with "refund" intent, 60-day guarantee

Test Case 4:
━━━━━━━━━━━
ইনপুট:   "How long does shipping take?"
আশা:     Shipping timeline
দেখবেন:  ✅ Different answer, debug info with "shipping" intent, 2-5 days (USA)

Test Case 5:
━━━━━━━━━━━
ইনপুট:   "Is it safe to use with medication?"
আশা:     Safety warning + medical advice
দেখবেন:  ✅ Different answer, debug info with "safety" intent, medical consultation

Test Case 6:
━━━━━━━━━━━
ইনপুট:   "Do you offer subscriptions?"
আশা:     Subscription information
দেখবেন:  ✅ Different answer, debug info with "subscription" intent, 15% off

Test Case 7:
━━━━━━━━━━━
ইনপুট:   "What's the price?"
আশা:     Pricing details
দেখবেন:  ✅ Different answer, debug info with "pricing" intent, $29.97

Test Case 8:
━━━━━━━━━━━
ইনপুট:   "Where is my order?"
আশা:     Order tracking info
দেখবেন:  ✅ Different answer, debug info with "order_status" intent
```

---

## **What to Verify:**

### ✅ **প্রতিটি প্রশ্নে আলাদা উত্তর আসছে?**
- "What is it?" → Product intro
- "How to use?" → Usage instructions (ভিন্ন!)
- "Price?" → Pricing (ভিন্ন!)
- পূর্বের মতো একই উত্তর নয়

### ✅ **Debug Info দেখা যাচ্ছে?**
- Intent type (general, usage, refund, shipping, etc.)
- KB match indicator (✓ বা ✗)
- Timestamp

### ✅ **Connection Status দেখা যাচ্ছে?**
- Green indicator = Connected
- Red indicator = Disconnected

### ✅ **Backend Console এ log দেখা যাচ্ছে?**
```
INFO: POST /api/test 200 OK
INFO: Intent detected: general
INFO: KB found 3 matches
```

### ✅ **কোন Error নেই?**
- Browser console এ red error নেই
- Backend terminal এ exception নেই

---

## **Troubleshooting:**

```
সমস্যা: সব প্রশ্নে একই উত্তর আসছে
সমাধান: Backend restart করুন, hybrid_service import যাচাই করুন

সমস্যা: KB items load হচ্ছে না
সমাধান: complete_kb.json ফাইল আছে কিনা check করুন
        JSON syntax valid আছে কিনা check করুন

সমস্যা: API error দেখা যাচ্ছে
সমাধান: Backend terminal এ log দেখুন
        OPENAI_API_KEY set আছে কিনা check করুন

সমস্যা: Frontend blank দেখা যাচ্ছে
সমাধান: Browser console খুলুন (F12)
        CORS errors আছে কিনা দেখুন
```

---

## **Performance Check:**

```
Response Time: < 3 seconds (ideal)
KB Items Loaded: 30+
Intents Detected: 8 types
Fallback Working: Yes (when OpenAI fails)
```

---

## **Quick Summary:**

| Component | Status | Check Command |
|-----------|--------|---------------|
| Backend API | ✅ | `curl http://localhost:8000/health` |
| Knowledge Base | ✅ | Look for "30 items loaded" in backend |
| Hybrid Service | ✅ | Run `python test_hybrid_system.py` |
| Frontend UI | ✅ | Open `index_v2.html` |
| Different Answers | ✅ | Send 8 different test messages |

---

## **Expected Result:**

```
✅ Backend running without errors
✅ KB Service loaded 30 items
✅ Frontend shows different answers for different questions
✅ Debug info shows correct intents
✅ No more "same answer for everything" problem
✅ Fallback system works when OpenAI fails
```

---

## **প্রস্তুত? এখন Test করুন!** 🚀

```
Terminal 1 (চলমান):  uvicorn app.main:app --reload
Terminal 2 (নতুন):   python test_hybrid_system.py
Browser:             Open index_v2.html
                     Send test messages
```

**সব প্রশ্নে আলাদা উত্তর পাবেন!** 🎉
