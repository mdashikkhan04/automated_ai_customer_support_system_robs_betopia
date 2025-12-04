# CHATBOT TESTING GUIDE

**Server is running at: http://localhost:8000**

---

## STEP 1: Check Health (Open in Browser)
```
http://localhost:8000/health
```
Expected: JSON response showing tier stats

---

## STEP 2: Test Chat Endpoint (PowerShell Command)

Run this in a NEW PowerShell terminal:

```powershell
$body = @{user_message='What is your refund policy?'} | ConvertTo-Json
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d $body
```

Expected Response:
```json
{
  "reply": "[Response about refund policy from KB]",
  "tier": 1,
  "confidence": 0.8,
  "tokens_used": null
}
```

---

## STEP 3: Test Another Question

```powershell
$body = @{user_message='Where is your support center?'} | ConvertTo-Json
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d $body
```

Expected: Response with support URL from KB

---

## STEP 4: Test with Complex Question

```powershell
$body = @{user_message='Do you offer free shipping? What is the shipping policy?'} | ConvertTo-Json
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d $body
```

Expected: Response mentioning shipping costs/policy

---

## STEP 5: View API Documentation

Open in Browser:
```
http://localhost:8000/docs
```

This shows all available endpoints with interactive testing!

---

## Tier System Explanation

- **Tier 1 (KB)**: Searches Pinecone for matching knowledge base items (47 items loaded)
- **Tier 2 (Scraping)**: Searches cached website data (fallback)
- **Tier 3 (LLM)**: Uses OpenAI to generate response (last resort)

The system uses Tier 1 if confidence > 0.3, otherwise falls back to Tier 2 or 3.

---

## Server Logs

Watch the server terminal to see:
- Which tier is being used
- Response times
- Confidence scores
