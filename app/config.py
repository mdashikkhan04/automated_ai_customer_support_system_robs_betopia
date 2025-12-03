# File: app/config.py

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str

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

    # General
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
