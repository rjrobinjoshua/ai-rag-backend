import os

import chromadb
from chromadb.config import Settings

from app.core.config import get_settings


def get_chroma_client(db_path: str | None = None):
    settings = get_settings()
    resolved_path = db_path or settings.chroma_persist_dir
    os.makedirs(resolved_path, exist_ok=True)
    client = chromadb.PersistentClient(
        path=resolved_path, settings=Settings(anonymized_telemetry=False)
    )

    return client
