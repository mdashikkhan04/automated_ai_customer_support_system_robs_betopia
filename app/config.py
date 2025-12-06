# File: app/config.py

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_REPLY_MODEL: str = "gpt-4o-mini"

    # Chatwoot
    CHATWOOT_BASE_URL: AnyHttpUrl
    CHATWOOT_API_TOKEN: str
    CHATWOOT_BOT_NAME: str = "HardChews Assistant"

    # Shopify
    SHOPIFY_STORE_DOMAIN: str
    SHOPIFY_ACCESS_TOKEN: str

    # USPS (optional)
    USPS_USER_ID: str | None = None

    # ClickBank
    CLICKBANK_DEV_KEY: str
    CLICKBANK_CLERK_KEY: str
    CLICKBANK_API_KEY: str | None = None

    # HardChews Client Config
    WEBSITE_URL: str = "https://www.hardchews.me"
    WEBSITE_DOMAIN: str = "hardchews.shop"
    SUPPORT_URL: str = "https://www.hardchews.me/hc-support"
    FAQ_URL: str = "https://www.hardchews.me/hc-support/faq"
    SHIPPING_URL: str = "https://www.hardchews.me/hc-support/shipping"
    CHATBOT_NAME: str = "Hard Chews Support"

    # Pinecone (RAG vector DB)
    PINECONE_API_KEY: str
    PINECONE_ENV: str = "us-east-1"
    PINECONE_INDEX: str = "hardchews-support-index"
    PINECONE_DIM: int = 1536
    PINECONE_METRIC: str = "cosine"

    # Scheduler & Caching
    SCRAPING_INTERVAL_HOURS: int = 6
    SCRAPING_CACHE_TTL_HOURS: int = 24
    CACHE_PATH: str = "app/cache/scraped_data.json"

    # Database & Redis (optional for future)
    DATABASE_URL: str | None = None
    REDIS_URL: str | None = None

    # Security & Admin
    SECRET_KEY: str = "replace_with_strong_random"
    ADMIN_EMAIL: str = "ops@example.com"

    # General
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
