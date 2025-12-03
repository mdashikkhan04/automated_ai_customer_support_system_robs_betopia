# 🚀 HardChews Chatbot - Quick Start (30 Seconds)

## **STEP 1: Run Backend** (Terminal)

```bash
cd d:/Asik/robs/automated_ai_customer_support_system_robs_betopia
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

✅ **Wait for:** `INFO: Uvicorn running on http://0.0.0.0:8000`

---

## **STEP 2: Open Frontend** (Browser)

```
Double-click: index.html
```

Or:
```
File → Open → index.html
```

---

## **DONE!** 🎉

Your chatbot is running! Try:
- "What is HardChews?"
- "How do I use it?"
- "What's your refund policy?"
- "Where is my order?"

---

## **📋 Requirements**

✅ `.env` must have: `OPENAI_API_KEY=sk-proj-xxx`
✅ Backend running: `http://localhost:8000`
✅ Browser: Any modern browser (Chrome, Firefox, Safari, Edge)

---

## **🐛 Troubleshooting**

| Problem | Solution |
|---------|----------|
| Connection Error | Restart backend: `Ctrl+C` then run again |
| "No Response" | Check OPENAI_API_KEY in .env |
| Styling broken | Refresh browser: `Ctrl+Shift+R` |
| Port 8000 in use | Change to: `uvicorn app.main:app --reload --port 8001` |

---

**Everything ready? Start testing! 🎉**
