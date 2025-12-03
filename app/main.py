# File: app/main.py

from fastapi import FastAPI

from app.api.chatwoot_webhook import router as chatwoot_router
from app.config import get_settings
from app.logger import logger

settings = get_settings()

app = FastAPI(
    title="HardChews AI Support Backend",
    description="AI-powered chatbot backend for HardChews customer support.",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


app.include_router(chatwoot_router, prefix="/api")
