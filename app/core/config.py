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
    debug: bool = os.getenv("DEBUG", "false").lower == "true"
    

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    logger.info("Settings loaded: env={}, debug={}", settings.env,  settings.debug)
    return settings