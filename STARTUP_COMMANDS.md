# HardChews Chatbot - Startup Commands

এই গাইডটি ব্যবহার করে আপনি যেকোনো সময় chatbot run করতে পারবেন।

---

## সবচেয়ে সহজ উপায় (Recommended)

### **Step 1: Terminal খুলুন**

PowerShell খুলুন এবং project folder-এ যান:

```powershell
cd D:\Asik\robs\automated_ai_customer_support_system_robs_betopia
```

### **Step 2: সরাসরি Server চালু করুন**

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

আপনি এই output দেখবেন:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### **Step 3: Browser এ খুলুন**

নতুন browser tab এ এই URL ভিজিট করুন:

```
http://127.0.0.1:8000/ui/index.html
```

**Done!** 🎉 Chatbot এখন ready। কোনো প্রশ্ন করুন এবং response পান।

---

## প্রথম বার চালানোর সময়

যদি এটি প্রথমবার চালাচ্ছেন বা নতুন URLs থেকে data scrape করতে চান:

### **Step 1: Dependencies ইনস্টল করুন**

```powershell
cd D:\Asik\robs\automated_ai_customer_support_system_robs_betopia
python -m pip install -r requirements.txt
```

### **Step 2: Web Scraping + Pinecone Ingest করুন** (Optional)

যদি নতুন data scrape করতে চান:

```powershell
$env:PYTHONPATH = "."
python .\scripts\scrape_and_ingest.py
```

এটি:
- Hardchews website থেকে সব pages scrape করবে
- OpenAI embeddings generate করবে
- Pinecone database-এ সব data store করবে

### **Step 3: Server চালু করুন**

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### **Step 4: Browser এ খুলুন**

```
http://127.0.0.1:8000/ui/index.html
```

---

## Quick Test (বিনা Browser)

Server চলার সময় নতুন Terminal tab এ এই command দিয়ে test করুন:

```powershell
$env:PYTHONPATH = "."
python .\test_chat.py
```

এটি 4টি sample questions দিয়ে chatbot test করবে এবং responses দেখাবে।

---

## একবার Script দিয়ে সব কিছু চালু করুন

একটি PowerShell script তৈরি করুন `start_chatbot.ps1`:

```powershell
# Navigate to project
cd "D:\Asik\robs\automated_ai_customer_support_system_robs_betopia"

# Start server
$env:PYTHONPATH = "."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

এখন প্রতিবার এই command দিয়ে চালু করুন:

```powershell
cd "D:\Asik\robs\automated_ai_customer_support_system_robs_betopia"
.\start_chatbot.ps1
```

---

## যদি PORT 8000 ব্যস্ত থাকে

অন্য PORT ব্যবহার করুন (যেমন 8080):

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

তারপর এই URL ভিজিট করুন:
```
http://127.0.0.1:8080/ui/index.html
```

---

## সমস্ত Endpoints

চালু হওয়ার পর আপনি এই endpoints ব্যবহার করতে পারবেন:

| Endpoint | Purpose |
|----------|---------|
| `GET http://127.0.0.1:8000/` | Root API info |
| `GET http://127.0.0.1:8000/health` | Backend health check |
| `GET http://127.0.0.1:8000/docs` | Swagger API docs |
| `GET http://127.0.0.1:8000/ui/index.html` | **Main Chatbot UI** |
| `POST http://127.0.0.1:8000/chat` | Chat API (JSON) |

---

## Troubleshooting

### **Problem: "ModuleNotFoundError: No module named 'app'"**

**Solution:**
```powershell
$env:PYTHONPATH = "."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### **Problem: "Connection refused" on browser**

Server এর জন্য 3-5 সেকেন্ড অপেক্ষা করুন, তারপর refresh করুন।

### **Problem: ".env API keys missing"**

নিশ্চিত করুন `.env` ফাইলে এই variables আছে:
- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_INDEX`
- `PINECONE_DIM`

### **Problem: Pinecone connection error**

নিশ্চিত করুন `.env`-এ সঠিক API keys আছে এবং internet connection চালু আছে।

---

## Summary (দ্রুত রেফারেন্স)

সবচেয়ে সহজ:

```powershell
cd D:\Asik\robs\automated_ai_customer_support_system_robs_betopia
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

তারপর browser এ:
```
http://127.0.0.1:8000/ui/index.html
```

**Done!** 🎉
