# File: app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.chatwoot_webhook import router as chatwoot_router
from app.config import get_settings
from app.logger import logger
from app.services.scraping_scheduler import scraping_scheduler
from app.services.priority_response_service import priority_service

settings = get_settings()

app = FastAPI(
    title="HardChews AI Support Backend",
    description="AI-powered chatbot backend for HardChews customer support (3-tier priority system).",
    version="2.0.0",
)

# Request/Response models
class ChatRequest(BaseModel):
    user_message: str
    conversation_id: int | None = None

class ChatResponse(BaseModel):
    reply: str
    tier: int
    confidence: float
    tokens_used: dict | None = None

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on app startup."""
    logger.info("🚀 HardChews AI Support Backend Starting...")
    
    # Start background web scraping scheduler
    # NOTE: Temporarily disabled for testing - scraper issues with invalid URLs
    # scraping_scheduler.start()
    logger.info("✅ Scraping scheduler disabled (testing mode)")
    
    # Display tier stats
    stats = priority_service.get_tier_stats()
    logger.info(f"✅ Priority System Ready:")
    logger.info(f"   • Tier 1 (Dataset): {stats['tier1_dataset_items']} KB items")
    logger.info(f"   • Tier 2 (Scraping): {stats['tier2_scraping_items']} cached items")
    logger.info(f"   • Tier 3 (LLM): {'Ready' if stats['tier3_llm_available'] else 'Not configured'}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown."""
    logger.info("🛑 HardChews AI Support Backend Shutting Down...")
    # scraping_scheduler.stop()  # Commented out since scheduler not running

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "HardChews AI Support Backend",
        "version": "2.0.0",
        "system": "3-tier priority response (Dataset → Scraping → LLM)",
        "docs": "/docs",
        "health": "/health",
        "scheduler": "/scheduler/status"
    }

@app.get("/health")
async def health_check():
    stats = priority_service.get_tier_stats()
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "tier_stats": stats,
        "scheduler": scraping_scheduler.get_status()
    }

@app.get("/scheduler/status")
async def scheduler_status():
    """Get background scraping scheduler status."""
    return {
        "service": "Web Scraping Scheduler",
        "status": scraping_scheduler.get_status()
    }

@app.post("/scheduler/refresh")
async def trigger_scraping_refresh(force: bool = False):
    """Manually trigger web scraping refresh."""
    result = priority_service.refresh_scraping_cache(force=force)
    return {
        "message": "Scraping refresh triggered",
        "result": result
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint: Process customer message through 3-tier priority system."""
    try:
        # get_response() expects: user_message, intent, context, extra_instructions, conversation_id, quick_mode
        # We'll pass basic info for now
        response = priority_service.get_response(
            user_message=request.user_message,
            intent="general_inquiry",  # Could be parsed from message
            conversation_id=request.conversation_id,
            quick_mode=True
        )
        
        # Map the response to our model
        # get_response returns: {response, source, confidence, intent, debug}
        # We need to map "source" to "tier" (dataset=1, scraping=2, llm=3)
        tier_map = {"dataset": 1, "scraping": 2, "llm": 3}
        tier = tier_map.get(response.get("source"), 0)
        
        return ChatResponse(
            reply=response["response"],
            tier=tier,
            confidence=response["confidence"],
            tokens_used=response.get("debug", {}).get("tokens")
        )
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        # Always return the error for now (testing)
        return ChatResponse(
            reply=error_msg,
            tier=0,
            confidence=0.0,
            tokens_used=None
        )

app.include_router(chatwoot_router, prefix="/api")
