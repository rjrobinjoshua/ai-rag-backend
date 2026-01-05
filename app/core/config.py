from functools import lru_cache

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------------------------
    # App
    # -------------------------
    app_name: str = Field(default="default_ai_backend", validation_alias="APP_NAME")
    env: str = Field(default="local", validation_alias="APP_ENV")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    # -------------------------
    # OpenAI
    # -------------------------
    openai_api_key: str = Field(validation_alias="OPENAI_API_KEY")
    chatgpt_model: str = Field(default="gpt-4.1-mini", validation_alias="CHATGPT_MODEL")
    openai_embed_model: str = Field(
        default="text-embedding-3-small",
        validation_alias="OPENAI_EMBED_MODEL",
    )

    # -------------------------
    # RAG Defaults (future-friendly)
    # -------------------------
    default_top_k: int = Field(default=6, validation_alias="DEFAULT_TOP_K")
    max_top_k: int = Field(default=20, validation_alias="MAX_TOP_K")
    max_query_chars: int = Field(default=2000, validation_alias="MAX_QUERY_CHARS")

    # -------------------------
    # Storage (containers / k8s)
    # -------------------------
    chroma_persist_dir: str = Field(
        default="./chroma_db", validation_alias="CHROMA_PERSIST_DIR"
    )
    data_dir: str = Field(default="./data", validation_alias="DATA_DIR")

    # -------------------------
    # Local dev convenience ONLY
    # -------------------------
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.prod"),  # used only when running locally
        extra="ignore",
    )

    # Backward compatibility
    @property
    def api_key(self) -> str:
        return self.openai_api_key


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    logger.info(
        "Settings loaded: env={}, debug={}, log_level={}",
        settings.env,
        settings.debug,
        settings.log_level,
    )

    return settings
