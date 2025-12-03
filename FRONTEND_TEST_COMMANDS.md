# 🎨 **FRONTEND TEST - সব কমান্ড**

## **Step 1: Backend চালু করুন (Terminal 1)**

```powershell
# প্রজেক্ট ডিরেক্টরিতে যান
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia

# ভার্চুয়াল এনভায়রনমেন্ট চালু করুন
venv\Scripts\activate

# Backend সার্ভার চালু করুন
uvicorn app.main:app --reload

# দেখবেন:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

---

## **Step 2: Backend সার্ভার Test করুন (Terminal 2)**

```powershell
# নতুন PowerShell খুলুন

# Backend running আছে কিনা চেক করুন
curl http://localhost:8000/

# সফল হলে দেখবেন:
# {"message":"Chatbot API is running"}
```

---

## **Step 3: Frontend ওপেন করুন (ব্রাউজার)**

```
ম্যানুয়ালি:
1. File Explorer খুলুন
2. Navigate করুন: d:\Asik\robs\automated_ai_customer_support_system_robs_betopia
3. index.html ফাইল খুঁজুন
4. ডাবল ক্লিক করুন → ব্রাউজার এ খুলবে

অথবা প্রথম ডিরেক্টরি থেকে যান:
cd d:\Asik\robs\automated_ai_customer_support_system_robs_betopia
.\index.html
```

---

## **Step 4: Frontend UI Check করুন**

ব্রাউজার খুলে এই চেকলিস্ট follow করুন:

```
☑ Header দেখা যাচ্ছে কিনা?
   "🤖 HardChews AI Support"

☑ Title দেখা যাচ্ছে কিনা?
   "AI Assistant Ready"

☑ Quick Buttons দেখা যাচ্ছে কিনা?
   - "What is HardChews?"
   - "How to use it?"
   - "Refund policy?"
   - "Shipping time?"

☑ Chat Area খালি আছে কিনা?

☑ Input Field দেখা যাচ্ছে কিনা?
   "Ask me anything..."

☑ Send Button দেখা যাচ্ছে কিনা?
   "→" button

☑ Purple Gradient Background দেখা যাচ্ছে কিনা?

☑ কোন Error দেখা যাচ্ছে কিনা?
   (F12 খুলে Console check করুন)
```

---

## **Step 5: Frontend Functionality Test**

### **Test 5.1: Quick Button Click করুন**

```
1. ব্রাউজার এ "What is HardChews?" বাটনে ক্লিক করুন
2. দেখুন:
   ✓ আপনার বার্তা ডানপাশে দেখা যায় (আপনার message)
   ✓ Typing indicator দেখা যায় (dots animating)
   ✓ Bot এর response বাঁপাশে দেখা যায় (AI message)
   ✓ Response তে product info থাকে
```

### **Test 5.2: Manual Message পাঠান**

```
1. Input field এ ক্লিক করুন
2. লিখুন: "How long does shipping take?"
3. Enter চাপুন
4. দেখুন:
   ✓ বার্তা পাঠানো হয়েছে
   ✓ Bot response আসে
   ✓ Shipping info দেখা যায়
```

### **Test 5.3: বিভিন্ন প্রশ্ন টেস্ট করুন**

```
এই প্রশ্নগুলো পাঠান এবং দেখুন সঠিক response আসছে কিনা:

প্রশ্ন 1: "What is HardChews?"
প্রত্যাশিত: Product information

প্রশ্ন 2: "How do I use it?"
প্রত্যাশিত: Usage instructions

প্রশ্ন 3: "What's the price?"
প্রত্যাশিত: Pricing information

প্রশ্ন 4: "Can I get a refund?"
প্রত্যাশিত: Refund policy

প্রশ্ন 5: "Is it safe to use with medication?"
প্রত্যাশিত: Safety information + escalation warning

প্রশ্ন 6: "How long until results?"
প্রত্যাশিত: Timeline information

প্রশ্ন 7: "THIS IS A SCAM!!! FURIOUS!!!"
প্রত্যাশিত: Escalation message
```

---

## **Step 6: Developer Console Debug (F12)**

```
1. ব্রাউজার এ F12 চাপুন (Developer Tools খুলবে)
2. Console Tab এ যান
3. কিছু বার্তা পাঠান
4. দেখুন এই logs:

কিছু দেখতে পাবেন এমন:
- "Sending message to backend..."
- "Response from backend:"
- JSON response data
- Intent type
- KB match info

5. Errors থাকলে দেখা যাবে লাল রংয়ে (NO ERRORS থাকা উচিত)
```

---

## **Step 7: Network Request Check (F12)**

```
1. F12 চাপুন
2. Network Tab এ যান
3. কিছু বার্তা পাঠান
4. দেখুন:
   ✓ POST request আসছে http://localhost:8000/api/test
   ✓ Status: 200 OK
   ✓ Response body JSON format এ আছে
   ✓ কোন CORS error নেই
```

---

## **Step 8: Multi-turn Conversation Test**

```
1. প্রথম বার্তা: "How do I use HardChews?"
2. Bot এর response পড়ুন
3. দ্বিতীয় বার্তা: "How long until I see results?"
4. উল্লেখ করুন bot আগের context মনে রেখেছে কিনা
5. তৃতীয় বার্তা: "What about side effects?"
6. Bot যদি আগের context use করে response দেয় → ✓ কাজ করছে!
```

---

## **Step 9: Responsive Design Test (Mobile View)**

```
1. F12 চাপুন
2. Ctrl+Shift+M চাপুন (Mobile view mode)
3. বিভিন্ন screen size এ টেস্ট করুন:

   • 375px width (iPhone)
     - Header visible? ✓
     - Chat readable? ✓
     - Input accessible? ✓

   • 768px width (Tablet)
     - Layout correct? ✓
     - Buttons clickable? ✓
     - Text readable? ✓

   • 1024px width (Desktop)
     - Full width used? ✓
     - No overflow? ✓
     - Beautiful display? ✓
```

---

## **Step 10: Error Handling Test**

```
Test 10.1: Backend বন্ধ করুন
1. Terminal 1 এ (Backend চলছে) Ctrl+C চাপুন
2. Frontend এ বার্তা পাঠান
3. দেখুন: "Failed to connect to server" error
4. Backend আবার চালু করুন: uvicorn app.main:app --reload
5. আবার বার্তা পাঠান
6. এটা কাজ করবে ✓

Test 10.2: Invalid Message
1. Input field খালি রেখে Send চাপুন
2. কোন error message দেখা যায় কিনা?

Test 10.3: Very Long Message
1. অনেক লম্বা বার্তা লিখুন (500+ characters)
2. পাঠান
3. সঠিক ভাবে handle হচ্ছে কিনা দেখুন
```

---

## **Step 11: Animation & UX Test**

```
☑ Smooth Message Animation?
   - বার্তা খুব দ্রুত appear হয় নাকি smooth আসে?
   
☑ Typing Indicator Working?
   - Bot responding করার সময় dots animate হয় কিনা?
   
☑ Auto-scroll Working?
   - নতুন message আসলে automatically scroll হয় কিনা?
   
☑ Buttons Responsive?
   - Hover effect আছে কিনা?
   - Click করলে সঠিক কাজ হয় কিনা?
   
☑ Input Field Behavior?
   - Focus effect দেখা যায় কিনা?
   - Placeholder text দেখা যায় কিনা?
```

---

## **Step 12: Debug Information Panel Test**

```
প্রতিটি response এর নিচে Debug Info থাকে:

1. একটি বার্তা পাঠান
2. Response এর নিচে দেখুন:
   - Intent Type (e.g., "general", "order_status", "refund")
   - KB Used (true/false)
   - Confidence Score
   - Conversation ID
   - Escalation Status

এই সব info দেখা যায় কিনা check করুন ✓
```

---

## **COMPLETE TESTING CHECKLIST**

```
FRONTEND UI (Step 5-4):
☑ Header visible
☑ Title visible
☑ Quick buttons visible
☑ Chat area empty initially
☑ Input field visible
☑ Send button visible
☑ Purple gradient background
☑ No errors in console

FUNCTIONALITY (Step 5-6):
☑ Quick buttons work
☑ Manual messages work
☑ Messages sent successfully
☑ Bot responds appropriately
☑ Different intents handled
☑ Multi-turn conversation works

DEVELOPER TOOLS (Step 7-8):
☑ No console errors
☑ API calls successful
☑ POST requests made
☑ 200 OK responses
☑ JSON responses valid
☑ No CORS errors

RESPONSIVE DESIGN (Step 9):
☑ Mobile view (375px) works
☑ Tablet view (768px) works
☑ Desktop view (1024px) works
☑ Layout adjusts properly
☑ All elements visible

ERROR HANDLING (Step 10):
☑ Handles disconnections
☑ Shows error messages
☑ Recovers when online
☑ Validates inputs

ANIMATIONS & UX (Step 11):
☑ Smooth animations
☑ Typing indicators
☑ Auto-scroll works
☑ Buttons have hover effects
☑ Input field responsive

DEBUG INFO (Step 12):
☑ Intent type displayed
☑ KB usage shown
☑ Confidence scores visible
☑ Conversation ID present
☑ Escalation status shown
```

---

## **QUICK COMMAND REFERENCE**

```powershell
# Start Backend
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia
venv\Scripts\activate
uvicorn app.main:app --reload

# Check Backend Running
curl http://localhost:8000/

# Open Frontend
# Double-click index.html in File Explorer

# Open Developer Tools
# F12 in browser

# Mobile View in Developer Tools
# Ctrl+Shift+M

# Backend API Documentation
# http://localhost:8000/docs
```

---

## **TEST RESULTS TEMPLATE**

যখন testing complete হবে, এটা note করুন:

```
FRONTEND TESTING RESULTS
========================
Date: [Today's Date]
Tester: [Your Name]

Backend Status: ✓ Running on http://localhost:8000
Frontend Status: ✓ Loaded and Responsive

UI Components: ✓ All visible and working
Functionality: ✓ All features working
Error Handling: ✓ Graceful failures
Performance: ✓ < 3 second response times
Mobile Responsive: ✓ Works on all screen sizes

Issues Found: [None / List any issues]

Recommendations: [Any improvements needed]

OVERALL STATUS: ✓✓✓ READY FOR PRODUCTION
```

---

## **TROUBLESHOOTING COMMON ISSUES**

```
Issue: Backend not running
Solution: Terminal 1 এ: uvicorn app.main:app --reload

Issue: "Failed to connect to server" message
Solution: Backend running আছে কিনা check করুন, Port 8000 free আছে কিনা

Issue: Messages not appearing
Solution: Browser console (F12) check করুন errors আছে কিনা

Issue: Styling looks broken
Solution: Browser cache clear করুন (Ctrl+Shift+Delete)

Issue: Mobile view broken
Solution: Browser zoom reset করুন (Ctrl+0)

Issue: No API responses
Solution: .env file এ OPENAI_API_KEY set আছে কিনা check করুন

Issue: CORS error
Solution: Backend restart করুন, CORS middleware আছে কিনা verify করুন
```

---

**Ready to test? শুরু করুন Step 1 থেকে!** 🚀
