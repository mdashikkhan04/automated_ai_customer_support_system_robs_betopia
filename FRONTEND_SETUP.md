# 🚀 HardChews Chatbot - Frontend + Backend Running Guide

## Quick Start (2 Steps - 2 Minutes!)

### Step 1: Start the Backend Server

**Open Terminal 1:**
```bash
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia

# Activate virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Backend is running at:** http://localhost:8000

---

### Step 2: Open the Frontend

**Simply open in any browser:**
```
File → Open → index.html
```

Or directly:
```
Double-click: d:\Asik\robs\automated_ai_customer_support_system_robs_betopia\index.html
```

✅ **Frontend is running in your browser!**

---

## 🎉 Now You Have Full Chatbot!

### What You Can Test:

1. **Product Questions** 
   - "What is HardChews?"
   - "How should I take it?"
   - "Any side effects?"

2. **Shipping & Delivery**
   - "How long does shipping take?"
   - "Where is my order?"
   - "Do you ship internationally?"

3. **Refunds & Policies**
   - "What is your refund policy?"
   - "Can I get a refund?"
   - "Do you have subscriptions?"

4. **Order Status** (if you add email)
   - "Where is my order? My email is john@example.com"

5. **Angry Customer Escalation**
   - "This product is a SCAM!"
   - "I'm so frustrated!"

---

## 🏗️ Frontend Features

✨ **Beautiful Modern UI**
- Purple gradient theme (matching brand)
- Smooth animations
- Responsive design (mobile/desktop)
- Typing indicator animation
- Auto-scrolling chat

🎯 **User Experience**
- Quick question buttons for first-time users
- Message timestamps
- Intent detection display
- Debug info (KB used, escalation, etc.)
- Keyboard support (Shift+Enter for new line)

🔧 **Smart Features**
- Auto-resize text input
- Connection error detection
- Graceful fallback messages
- Real-time typing indicators
- Message formatting (bold, italics, newlines)

---

## 🔗 API Connection Details

### Frontend connects to Backend:
```
Frontend (index.html) 
    ↓ POST to
Backend (http://localhost:8000/api/test)
    ↓ Processes through
OpenAI GPT-4 API
    ↓ Returns to
Frontend displays response
```

### The flow:
1. User types message in UI
2. Frontend sends to `http://localhost:8000/api/test`
3. Backend processes with AI
4. Backend returns response with intent + metadata
5. Frontend displays in chat

---

## ⚙️ Required Configuration

**Make sure `.env` has OPENAI_API_KEY:**

```bash
# Edit .env
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

Without this, you'll get an error!

---

## 🧪 Testing the Chatbot

### Test Scenario 1: Product Question
```
You: "What is HardChews?"
Bot: [AI response with product info from KB]
```

### Test Scenario 2: Multi-turn Conversation
```
You: "How long does it take?"
Bot: [Response about results timing]

You: "Any side effects?"
Bot: [Response remembering previous context]
```

### Test Scenario 3: Order Status
```
You: "Where is my order? My email is test@example.com"
Bot: [Tries to lookup in Shopify/ClickBank, shows status]
```

### Test Scenario 4: Escalation
```
You: "I'm so angry about this!"
Bot: [Detects sentiment, offers escalation]
```

---

## 📊 Debug Information

Each bot message shows:
- **Intent**: What the bot detected (product_info, order_status, etc.)
- **KB**: Whether knowledge base was used (✓ or ✗)
- **Escalation**: If human handoff was triggered (⚠️)

Example:
```
Intent: order_status | KB: ✓ | Escalated: ✗
```

---

## 🐛 Troubleshooting

### Issue: "Connection Error: Cannot connect to backend"

**Solution:**
1. Make sure you ran: `uvicorn app.main:app --reload`
2. Backend should be running on `http://localhost:8000`
3. Check terminal for error messages
4. Try refreshing the browser

### Issue: Bot not responding / Long delay

**Causes:**
1. OpenAI API key invalid → Check `.env`
2. OpenAI API is slow → Wait or check https://status.openai.com
3. KB not loaded → Check backend startup logs

**Solution:**
- Restart backend: `Ctrl+C` then run again
- Check logs for error messages
- Verify API key is correct

### Issue: Frontend looks broken / styling missing

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try a different browser
3. Check browser console (F12) for errors
4. Make sure you're opening `index.html` directly

### Issue: Quick buttons not working

**Solution:**
- Reload the page
- Check browser console (F12) for JavaScript errors
- Try typing manually instead

---

## 🚀 Production Deployment

When ready for production:

### Option 1: Serve Frontend from Backend

Move `index.html` to:
```
app/static/index.html
```

Add to `app/main.py`:
```python
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
```

Then visit: `http://your-domain.com/`

### Option 2: Host Separately

- Frontend: Netlify, Vercel, AWS S3
- Backend: Heroku, AWS, DigitalOcean

Update API_URL in index.html:
```javascript
const API_URL = 'https://your-backend-domain.com';
```

### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📁 File Structure

```
project/
├── index.html              ← Frontend (open in browser)
├── app/
│   ├── main.py            ← Backend (with CORS enabled)
│   ├── services/
│   │   ├── openai_service.py
│   │   ├── kb_service.py
│   │   └── ...
│   └── api/
│       └── chatwoot_webhook.py
├── requirements.txt
└── .env
```

---

## 🎯 Next Steps

1. ✅ **Start Backend** - `uvicorn app.main:app --reload`
2. ✅ **Open Frontend** - Open `index.html` in browser
3. ✅ **Test Chatbot** - Ask questions in the UI
4. ✅ **Review Responses** - Check intent detection & KB usage
5. 🔄 **Configure Chatwoot** - Follow CHATWOOT_INTEGRATION_GUIDE.md
6. 🔄 **Deploy** - Follow SETUP_DEPLOYMENT_GUIDE.md

---

## 📞 Support

- **Backend logs**: Check terminal running uvicorn
- **Frontend errors**: Check browser console (F12)
- **API issues**: Visit http://localhost:8000/docs for Swagger docs

---

## ⚡ Quick Commands

```bash
# Start backend
uvicorn app.main:app --reload

# Run tests
python app/tests/test_conversations.py

# Health check
python manage.py health

# Run management commands
python manage.py test-kb
python manage.py test-openai
```

---

**🎉 Congratulations! You now have a FULL AI CHATBOT with Frontend + Backend!**

Enjoy testing! 🚀
