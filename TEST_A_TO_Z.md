# 🧪 **COMPLETE A TO Z TEST GUIDE**

## **PART 1: SETUP (প্রথম বার চালানোর সময়)**

```bash
# Step 1: নিজেকে প্রজেক্ট ডিরেক্টরিতে রাখুন
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia

# Step 2: ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন
python -m venv venv

# Step 3: ভার্চুয়াল এনভায়রনমেন্ট চালু করুন (Windows PowerShell এর জন্য)
venv\Scripts\activate

# Step 4: সমস্ত প্যাকেজ ইনস্টল করুন
pip install -r requirements.txt

# Step 5: .env ফাইল তৈরি করুন
echo. > .env

# Step 6: .env তে OpenAI API Key যোগ করুন
# Notepad দিয়ে .env খুলুন এবং এটি লিখুন:
# OPENAI_API_KEY=your_key_here
# CHATWOOT_API_URL=https://your-chatwoot.com
# CHATWOOT_API_TOKEN=your_token_here
# SHOPIFY_API_KEY=your_key_here
# SHOPIFY_API_PASSWORD=your_password_here
# CLICKBANK_VENDOR_NAME=your_vendor_name
# CLICKBANK_API_KEY=your_api_key_here
```

---

## **PART 2: BACKEND টেস্টিং**

### **Test 2.1: Backend সার্ভার চালু করুন (Terminal 1 এ)**

```bash
# ভার্চুয়াল এনভায়রনমেন্ট চালু থাকা সত্ত্বেও চালান
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# আপনি দেখতে পাবেন:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

### **Test 2.2: API স্ট্যাটাস চেক করুন (Terminal 2 এ)**

```bash
# নতুন Terminal খুলুন এবং এই চালান:
curl http://localhost:8000/

# সফল হলে দেখবেন:
# {"message":"Chatbot API is running"}
```

### **Test 2.3: স্বাস্থ্য পরীক্ষা**

```bash
curl http://localhost:8000/health

# সফল হলে:
# {"status":"healthy","version":"1.0"}
```

### **Test 2.4: API ডকুমেন্টেশন (ব্রাউজার এ)**

```
http://localhost:8000/docs

# Swagger UI তে সমস্ত এন্ডপয়েন্ট দেখতে পাবেন
```

### **Test 2.5: প্রথম চ্যাট টেস্ট (PowerShell এ)**

```powershell
# সহজ প্রশ্ন পাঠান
$body = @{
    user_id = "test_user_1"
    message = "What is HardChews?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# সফল হলে দেখবেন:
# {
#   "response": "HardChews is a premium dietary supplement...",
#   "intent": "general",
#   "kb_used": true,
#   "conversation_id": "..."
# }
```

### **Test 2.6: বিভিন্ন Intent টেস্ট করুন**

```powershell
# Test 2.6a: Order Status জিজ্ঞাসা
$body = @{
    user_id = "test_user_1"
    message = "Where is my order? Order ID: #12345"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Test 2.6b: Refund নিয়ে প্রশ্ন
$body = @{
    user_id = "test_user_1"
    message = "Can I get a refund if I'm not satisfied?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Test 2.6c: Shipping সম্পর্কে প্রশ্ন
$body = @{
    user_id = "test_user_1"
    message = "How long does shipping take?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Test 2.6d: Pricing সম্পর্কে প্রশ্ন
$body = @{
    user_id = "test_user_1"
    message = "What's the price of HardChews?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Test 2.6e: Subscription সম্পর্কে প্রশ্ন
$body = @{
    user_id = "test_user_1"
    message = "Do you offer subscriptions?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# Test 2.6f: Safety সম্পর্কে প্রশ্ন
$body = @{
    user_id = "test_user_1"
    message = "Is HardChews safe to use with medication?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

### **Test 2.7: Multi-turn Conversation টেস্ট**

```powershell
# প্রথম বার্তা
$body = @{
    user_id = "multi_user"
    message = "How do I use HardChews?"
} | ConvertTo-Json

$response1 = Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

Write-Host "Response 1: $($response1.response)"

# দ্বিতীয় বার্তা (একই user_id - context থাকবে)
$body = @{
    user_id = "multi_user"
    message = "How long until I see results?"
} | ConvertTo-Json

$response2 = Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

Write-Host "Response 2: $($response2.response)"

# তৃতীয় বার্তা (একই context সাথে)
$body = @{
    user_id = "multi_user"
    message = "What about side effects?"
} | ConvertTo-Json

$response3 = Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

Write-Host "Response 3: $($response3.response)"
```

### **Test 2.8: Escalation টেস্ট (Angry Customer)**

```powershell
# গুস্সানো কাস্টমার সিমুলেট করুন
$body = @{
    user_id = "angry_user"
    message = "THIS IS A SCAM!!! I'M FURIOUS!!! WORST PRODUCT EVER!!!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

# এটা escalation flag সেট করবে এবং বিশেষ response দেবে
```

### **Test 2.9: Knowledge Base পরীক্ষা**

```bash
# Knowledge base files চেক করুন
cat app/kb/data/products_comprehensive.json | head -20

cat app/kb/data/faqs_comprehensive.json | head -20
```

---

## **PART 3: FRONTEND টেস্টিং**

### **Test 3.1: Frontend ওপেন করুন (ব্রাউজার এ)**

```
1. File Explorer খুলুন
2. Navigate: d:\Asik\robs\automated_ai_customer_support_system_robs_betopia
3. index.html এ ডাবল ক্লিক করুন
```

### **Test 3.2: UI উপাদান পরীক্ষা করুন**

```
চেকলিস্ট:
☑ Header: "HardChews AI Support" দেখা যায়
☑ Title: "AI Assistant Ready" দেখা যায়
☑ Quick buttons দেখা যায় (4টি বাটন)
☑ Chat area খালি এবং সাদা
☑ Input field visible
☑ Send button visible
☑ Purple gradient background দেখা যায়
```

### **Test 3.3: Quick Button টেস্ট**

```
করুন:
1. "What is HardChews?" বাটনে ক্লিক করুন
2. ব্রাউজার console চেক করুন (F12)
3. দেখুন বার্তা পাঠানো হয়েছে এবং response আসছে
```

### **Test 3.4: Manual Message টেস্ট**

```
করুন:
1. Input field এ ক্লিক করুন
2. লিখুন: "How long does shipping take?"
3. Enter চাপুন বা Send বাটনে ক্লিক করুন
4. দেখুন:
   - আপনার বার্তা right side এ দেখা যায়
   - Typing indicator দেখা যায়
   - Bot response left side এ দেখা যায়
   - Intent এবং KB info দেখা যায় (Debug section)
```

### **Test 3.5: Multi-line Message টেস্ট**

```
করুন:
1. Input field এ ক্লিক করুন
2. লিখুন: "Hello"
3. Shift+Enter চাপুন (নতুন লাইন)
4. লিখুন: "How are you?"
5. Enter চাপুন
6. দেখুন দুই লাইন একসাথে পাঠানো হয়েছে
```

### **Test 3.6: Angry Message টেস্ট**

```
করুন:
1. Input field এ লিখুন: "THIS IS TERRIBLE! I HATE IT!"
2. Enter চাপুন
3. দেখুন bot বিশেষ response দিয়েছে escalation সহ
```

### **Test 3.7: Browser Console Debug**

```
করুন:
1. F12 দিয়ে Developer Tools খুলুন
2. Console tab এ যান
3. কিছু বার্তা পাঠান
4. দেখুন:
   - No red errors থাকতে হবে
   - API call logs দেখতে হবে
   - Response logs দেখতে হবে
```

### **Test 3.8: Responsive Design টেস্ট**

```
করুন:
1. F12 দিয়ে Developer Tools খুলুন
2. Ctrl+Shift+M দিয়ে Mobile view চালু করুন
3. বিভিন্ন screen size এ চেক করুন:
   - 375px (Mobile)
   - 768px (Tablet)
   - 1024px (Desktop)
4. Layout সঠিক থাকে কিনা দেখুন
```

---

## **PART 4: UNIT TESTING**

### **Test 4.1: Test Suite চালান**

```bash
# ভার্চুয়াল এনভায়রনমেন্ট activate থাকা সত্ত্বেও:
pytest app/tests/test_conversations.py -v

# আপনি দেখবেন সব tests pass করছে
```

### **Test 4.2: Coverage Report**

```bash
# Test coverage দেখুন
pytest app/tests/test_conversations.py --cov=app --cov-report=html

# একটি report generate হবে
```

### **Test 4.3: Specific Test চালান**

```bash
# একটি specific test চালান
pytest app/tests/test_conversations.py::test_greeting_detection -v

# একটি category test চালান
pytest app/tests/test_conversations.py -k "greeting" -v
```

---

## **PART 5: INTEGRATION TESTING**

### **Test 5.1: Frontend-Backend Integration (Full Flow)**

```
করুন:
1. Backend server চালু থাকে (Terminal 1)
2. Frontend browser এ খোলা থাকে
3. Input field এ লিখুন: "Tell me about HardChews products"
4. Enter চাপুন
5. পর্যবেক্ষণ করুন:
   - Message সঠিক ভাবে পাঠানো হয়
   - Backend এ log দেখা যায় (Terminal 1)
   - Response সঠিক ভাবে আসে
   - Frontend এ display হয়
   - Debug info দেখা যায়
```

### **Test 5.2: Error Handling**

```
করুন:
1. Backend বন্ধ করুন (Terminal 1 এ Ctrl+C)
2. Frontend এ বার্তা পাঠান
3. দেখুন error message দেখা যায়: "Failed to connect to server"
4. Backend আবার চালু করুন
5. আবার বার্তা পাঠান
6. এটা কাজ করবে
```

### **Test 5.3: Connection Status**

```
করুন:
1. Backend browser এ API docs খুলুন: http://localhost:8000/docs
2. "Try it out" এ click করুন
3. কোন message পাঠান
4. Response দেখুন সঠিক JSON format এ
```

---

## **PART 6: PERFORMANCE TESTING**

### **Test 6.1: Response Time পরীক্ষা**

```powershell
# এই স্ক্রিপ্ট 10টি consecutive requests পাঠায় এবং সময় মাপে

$times = @()

for ($i = 1; $i -le 10; $i++) {
    $body = @{
        user_id = "perf_test_user"
        message = "What is HardChews? Test $i"
    } | ConvertTo-Json

    $start = Get-Date
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $body
    $end = Get-Date
    
    $duration = ($end - $start).TotalMilliseconds
    $times += $duration
    
    Write-Host "Request $i: ${duration}ms"
}

$avgTime = ($times | Measure-Object -Average).Average
Write-Host "Average Response Time: ${avgTime}ms"
Write-Host "Min: $($times | Measure-Object -Minimum).Minimum ms"
Write-Host "Max: $($times | Measure-Object -Maximum).Maximum ms"
```

### **Test 6.2: Concurrent Users সিমুলেশন**

```powershell
# Multiple users একসাথে message পাঠান

1..5 | ForEach-Object {
    $userId = "user_$_"
    $body = @{
        user_id = $userId
        message = "Hello, I'm user $_. What's HardChews?"
    } | ConvertTo-Json

    Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $body | Write-Host
}
```

---

## **PART 7: KNOWLEDGE BASE TESTING**

### **Test 7.1: KB File Structure চেক করুন**

```bash
# Products KB চেক করুন
cat app/kb/data/products_comprehensive.json

# FAQs KB চেক করুন
cat app/kb/data/faqs_comprehensive.json

# Items count দেখুন
cat app/kb/data/products_comprehensive.json | grep -o '"title"' | wc -l
```

### **Test 7.2: Semantic Search টেস্ট**

```powershell
# এমন কিছু লিখুন যা KB এ আছে

$queries = @(
    "How do I take HardChews?",
    "What are the side effects?",
    "Can I use it with medicine?",
    "What's the refund policy?",
    "How fast is shipping?",
    "Do you have bulk discounts?"
)

foreach ($query in $queries) {
    $body = @{
        user_id = "kb_test"
        message = $query
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/test" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $body
    
    Write-Host "Query: $query"
    Write-Host "KB Used: $($response.kb_used)"
    Write-Host "Response: $($response.response.Substring(0, 100))..."
    Write-Host "---"
}
```

---

## **PART 8: CONFIGURATION TESTING**

### **Test 8.1: Environment Variables চেক করুন**

```bash
# .env file চেক করুন
cat .env

# এগুলো থাকতে হবে:
# OPENAI_API_KEY=xxx
# CHATWOOT_API_URL=xxx (optional)
# SHOPIFY_API_KEY=xxx (optional)
# ইত্যাদি
```

### **Test 8.2: Requirements চেক করুন**

```bash
# সব dependencies installed আছে কিনা দেখুন
pip list

# দেখুন থাকে:
# - fastapi
# - openai
# - pydantic
# - numpy
# - beautifulsoup4
# - python-dotenv
# - requests
# - pytest
```

### **Test 8.3: Config Loading চেক করুন**

```bash
# Python console এ চেক করুন
python -c "from app.config import Config; c = Config(); print(f'OPENAI_API_KEY set: {bool(c.OPENAI_API_KEY)}')"
```

---

## **PART 9: LOGGING & DEBUGGING**

### **Test 9.1: Backend Logs দেখুন**

```
করুন:
1. Backend Terminal এ देखুন সব requests log হচ্ছে
2. প্রতিটি message এর জন্য:
   - Incoming message
   - Intent detected
   - KB search results
   - OpenAI response
   - Outgoing response
```

### **Test 9.2: Frontend Debug Info**

```
করুন:
1. Frontend এ কিছু বার্তা পাঠান
2. Debug section এ দেখুন:
   - User ID
   - Intent type
   - KB match percentage
   - Escalation status
   - Conversation ID
```

### **Test 9.3: Browser Network টেস্ট**

```
করুন:
1. F12 > Network tab খুলুন
2. কিছু বার্তা পাঠান
3. দেখুন:
   - POST request to /api/test
   - Status: 200 OK
   - Response body JSON format এ
   - নো CORS errors
```

---

## **PART 10: FINAL VALIDATION CHECKLIST**

```
☑ Backend চলছে ত্রুটি ছাড়া
☑ Frontend load হয়েছে সুন্দর ভাবে
☑ Quick buttons কাজ করছে
☑ Manual messages কাজ করছে
☑ Multi-turn conversation কাজ করছে
☑ Intent detection কাজ করছে (8 types)
☑ KB search কাজ করছে
☑ Escalation কাজ করছে (angry detection)
☑ Error handling কাজ করছে
☑ Response times acceptable (< 5 seconds)
☑ Browser console এ কোন error নেই
☑ Tests পাস করছে
☑ Responsive design কাজ করছে
☑ Debug info দেখা যাচ্ছে
☑ CORS কাজ করছে
```

---

## **QUICK COMMAND SUMMARY**

```bash
# Setup (প্রথম বার)
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo OPENAI_API_KEY=your_key_here > .env

# Run Backend
uvicorn app.main:app --reload

# Run Tests (new terminal)
pytest app/tests/test_conversations.py -v

# Open Frontend
# Double-click index.html

# Check API
curl http://localhost:8000/health

# Check API Docs
# Open http://localhost:8000/docs in browser
```

---

## **TROUBLESHOOTING**

```
সমস্যা: Port 8000 already in use
সমাধান: lsof -i :8000 (Mac/Linux) বা netstat -ano | findstr :8000 (Windows)
        তারপর kill করুন বা ভিন্ন port use করুন: uvicorn app.main:app --port 8001

সমস্যা: OpenAI API key error
সমাধান: .env এ valid API key আছে কিনা check করুন

সমস্যা: Frontend নির্বাচিত হচ্ছে না
সমাধান: Backend running আছে কিনা check করুন (terminal এ দেখুন)

সমস্যা: CORS error
সমাধান: Backend rerun করুন CORS middleware সহ

সমস্যা: Tests fail হচ্ছে
সমাধান: pytest install আছে কিনা দেখুন: pip install pytest

সমস্যা: KB items load হচ্ছে না
সমাধান: JSON files valid আছে কিনা check করুন: python -m json.tool app/kb/data/products_comprehensive.json
```

---

## **SUCCESS INDICATORS**

যখন সব ঠিক থাকে আপনি দেখবেন:

✅ Backend:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
INFO:     POST /api/test ...200 OK
```

✅ Frontend:
- Beautiful purple gradient background
- Chat messages appear with animations
- No red errors in console
- Response times < 3 seconds

✅ Tests:
```
test_greeting_detection PASSED
test_product_query PASSED
test_multi_turn_conversation PASSED
... (সব PASSED)
```

---

**এখন test করতে থাকুন এবং উপভোগ করুন! 🎉**

