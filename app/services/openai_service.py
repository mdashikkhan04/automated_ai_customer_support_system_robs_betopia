# File: app/services/openai_service.py

from typing import Dict, Any, List

import openai

from app.config import get_settings
from app.logger import logger

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY


SYSTEM_PROMPT = """
You are the official customer support assistant for HardChews, a dietary supplement brand.

Goals:
- Help customers with questions about products, orders, shipping, refunds, and general support.
- Always be friendly, concise, and professional.
- You must strictly follow HardChews policies and FAQs provided in the knowledge base.

Rules:
- Use ONLY the information from:
  1) Client-provided documents (highest priority)
  2) Website content
  3) General reasoning for basic conversational help.
- If something is not clearly stated in the knowledge base, do NOT invent policies or guarantees.
- Do NOT make medical diagnoses, claim to cure diseases, or give personalized medical advice.
  Instead, tell the customer to consult their doctor.
- For questions about order status:
  - Ask for email, full name, and order number if not provided.
  - If real-time lookup is unavailable, say a human agent will check and follow up.
- When you are unsure, say you will forward the request to a human agent instead of guessing.

Answer in clear, simple English. Keep answers focused and helpful.
"""


def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for text using OpenAI's text-embedding-3-small model.
    Used for Pinecone RAG indexing and retrieval.
    """
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise


def generate_reply(
    user_message: str,
    context: str,
    extra_instructions: str | None = None,
    debug_meta: Dict[str, Any] | None = None,
    conversation_id: int | None = None,
) -> str:
    """
    Safe wrapper around OpenAI ChatCompletion. If the API fails,
    returns a fallback message that asks for human support.
    """
    system = SYSTEM_PROMPT
    if extra_instructions:
        system += "\n\nAdditional instructions:\n" + extra_instructions

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": f"Customer message:\n{user_message}\n\nRelevant knowledge base:\n{context}",
        },
    ]

    try:
        logger.info("Calling OpenAI ChatCompletion")
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            max_tokens=600,
        )
        reply = completion.choices[0].message.content.strip()
        return reply
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        # Do not swallow the exception here — raise so callers can decide how to
        # handle fallbacks (e.g., router_service will use the hybrid KB fallback).
        raise
