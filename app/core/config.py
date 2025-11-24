import os
from functools import lru_cache

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel

# Load variables from .env into environment
load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "default_ai_backend")
    env: str = os.getenv("APP_ENV", "default_local")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    api_key: str = os.getenv("OPENAI_API_KEY")
    chatgpt_model: str = os.getenv("CHATGPT_MODEL", "gpt-4.1-mini")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    logger.info("Settings loaded: env={}, debug={}", settings.env, settings.debug)
    if not settings.api_key:
        raise RuntimeError("OPENAI_API_KEY is not present in the environment")
    return settings
