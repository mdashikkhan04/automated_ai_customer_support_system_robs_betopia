# File: app/services/priority_response_service.py
"""
3-Tier Priority Response System
Priority 1: Dataset (RAG) → Priority 2: Web Scraping → Priority 3: OpenAI LLM
"""

from typing import Dict, Any, Optional, Tuple
from app.services.kb_service import kb_service
from app.services.enhanced_web_scraper import web_scraper
from app.services.openai_service import generate_reply
from app.logger import logger


class PriorityResponseService:
    """
    3-tier fallback system for generating responses:
    1. Dataset (RAG) - cached KB with semantic search (highest priority)
    2. Web Scraping - live website data (fallback if KB insufficient)
    3. OpenAI LLM - general ChatGPT-like responses (lowest priority)
    """

    def __init__(self):
        self.kb_service = kb_service
        self.web_scraper = web_scraper
        self.min_confidence_threshold = 0.5

    def get_response(
        self,
        user_message: str,
        intent: str,
        context: str = "",
        extra_instructions: str = None,
        conversation_id: str = None,
        quick_mode: bool = True  # ⚡ NEW: Quick response mode
    ) -> Dict[str, Any]:
        """
        Main entry point for 3-tier response generation.
        quick_mode=True: Skip LLM if KB/Scraping has good answer (faster)
        Returns: {
            "response": str,
            "source": "dataset" | "scraping" | "llm",
            "confidence": float (0-1),
            "intent": str,
            "debug": {...}
        }
        """
        debug_info = {"message": user_message, "intent": intent}
        
        logger.info(f"🎯 Priority Response: Getting answer for intent={intent}")
        
        # Tier 1: Try Dataset (RAG) - FAST, no API calls
        result = self._try_dataset(user_message, intent)
        if result["source"] == "dataset" and result.get("confidence", 0) >= self.min_confidence_threshold:
            logger.info(f"✅ Tier 1 (Dataset): Found match with confidence {result['confidence']:.2f} [QUICK RETURN]")
            result["debug"] = debug_info
            return result
        
        logger.info(f"⚠️ Tier 1 (Dataset): Confidence too low ({result.get('confidence', 0):.2f}), trying Tier 2")
        
        # Tier 2: Try Web Scraping
        result = self._try_scraping(user_message, intent)
        if result["source"] == "scraping" and result.get("confidence", 0) >= self.min_confidence_threshold:
            logger.info(f"✅ Tier 2 (Scraping): Found match with confidence {result['confidence']:.2f} [QUICK RETURN]")
            result["debug"] = debug_info
            return result
        
        # ⚡ OPTIMIZATION: In quick_mode, if confidence is moderate (>0.3), return scraping result instead of slow LLM
        if quick_mode and result.get("confidence", 0) > 0.3:
            logger.info(f"⚡ Quick Mode: Returning scraping result (confidence {result['confidence']:.2f}) instead of slow LLM")
            result["debug"] = debug_info
            return result
        
        logger.info(f"⚠️ Tier 2 (Scraping): No good match, falling back to Tier 3 (LLM)")
        
        # Tier 3: Use OpenAI LLM - SLOW but comprehensive
        result = self._try_llm(user_message, intent, context, extra_instructions, conversation_id)
        logger.info(f"✅ Tier 3 (LLM): Generated response [SLOW]")
        result["debug"] = debug_info
        return result

    def _try_dataset(self, user_message: str, intent: str) -> Dict[str, Any]:
        """
        Tier 1: Pinecone RAG - semantic search from Pinecone (namespace="kb")
        Uses cached embeddings for instant retrieval (no API calls).
        """
        try:
            from app.services.pinecone_rag import retrieve_context_from_pinecone
            contexts = retrieve_context_from_pinecone(user_message, namespace="kb", top_k=3)
            if not contexts:
                logger.debug("Pinecone KB: No results found")
                return {"source": "dataset", "response": "", "confidence": 0.0}
            content = contexts[0] if contexts else ""
            confidence = 0.9 if content else 0.0  # Pinecone match is usually strong
            response = f"📚 **From Our Knowledge Base:**\n\n{content}"
            return {
                "source": "dataset",
                "response": response,
                "confidence": confidence,
                "kb_item_title": content[:60]  # preview
            }
        except Exception as e:
            logger.warning(f"Pinecone KB search error: {e}")
            return {"source": "dataset", "response": "", "confidence": 0.0}

    def _try_scraping(self, user_message: str, intent: str) -> Dict[str, Any]:
        """
        Tier 2: Pinecone RAG - semantic search from cached website data (namespace="scraping")
        Uses cached embeddings from web scraping for fast retrieval.
        """
        try:
            from app.services.pinecone_rag import retrieve_context_from_pinecone
            contexts = retrieve_context_from_pinecone(user_message, namespace="scraping", top_k=2)
            if not contexts:
                logger.debug("Pinecone scraping: No results found")
                return {"source": "scraping", "response": "", "confidence": 0.0}
            content = contexts[0] if contexts else ""
            confidence = 0.8 if content else 0.0
            response = f"🌐 **From Our Website:**\n\n{content}"
            return {
                "source": "scraping",
                "response": response,
                "confidence": confidence,
                "scraped_item_title": content[:60]
            }
        except Exception as e:
            logger.warning(f"Pinecone scraping search error: {e}")
            return {"source": "scraping", "response": "", "confidence": 0.0}

    def _try_llm(
        self,
        user_message: str,
        intent: str,
        context: str,
        extra_instructions: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Tier 3: Use OpenAI LLM for general conversational responses.
        Falls back to hybrid KB if OpenAI fails.
        """
        try:
            logger.info("LLM: Calling OpenAI API...")
            
            # Build context note
            llm_context = context or ""
            if not llm_context:
                llm_context = "No specific knowledge base information available. "
                llm_context += "Provide a general, helpful response based on your knowledge."
            
            # Call OpenAI
            reply = generate_reply(
                user_message=user_message,
                context=llm_context,
                extra_instructions=extra_instructions,
                conversation_id=conversation_id
            )
            
            response = f"🤖 **AI Assistant Response:**\n\n{reply}"
            logger.info("LLM: OpenAI API call succeeded")
            
            return {
                "source": "llm",
                "response": response,
                "confidence": 0.8,
                "llm_model": "gpt-4o-mini"
            }
        except Exception as e:
            logger.error(f"LLM error: {e}")
            
            # Fallback to polite message
            fallback_response = (
                "🔄 **System Notice:**\n\n"
                "I'm currently unable to process your request through our standard channels. "
                "I've recorded your message and will have our support team follow up with you shortly. "
                "Thank you for your patience!"
            )
            
            return {
                "source": "llm_fallback",
                "response": fallback_response,
                "confidence": 0.5,
                "error": str(e)
            }

    def refresh_scraping_cache(self, force: bool = False) -> Dict[str, Any]:
        """
        Manually trigger web scraping to refresh cached data.
        force=True ignores cache TTL and re-scrapes immediately.
        """
        try:
            logger.info("🔄 Refreshing web scraping cache...")
            data = self.web_scraper.scrape_all(force_refresh=force)
            
            return {
                "status": "success",
                "products": len(data.get("products", [])),
                "faqs": len(data.get("faqs", [])),
                "policies": len(data.get("policies", [])),
                "timestamp": data.get("timestamp")
            }
        except Exception as e:
            logger.error(f"Error refreshing scraping cache: {e}")
            return {"status": "error", "message": str(e)}

    def get_tier_stats(self) -> Dict[str, Any]:
        """Get statistics about each tier's data availability."""
        kb_count = len(self.kb_service.items)
        
        scraped = self.web_scraper.get_cached_data()
        scraped_count = (
            len(scraped.get("products", [])) +
            len(scraped.get("faqs", [])) +
            len(scraped.get("policies", []))
        )
        
        return {
            "tier1_dataset_items": kb_count,
            "tier2_scraping_items": scraped_count,
            "tier3_llm_available": True,
            "total_data_sources": kb_count + scraped_count
        }


# Singleton instance
priority_service = PriorityResponseService()
