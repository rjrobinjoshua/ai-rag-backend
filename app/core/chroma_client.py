import os

import chromadb
from chromadb.config import Settings

CHROMA_DB_PATH = "chroma_db"


def get_chroma_client(db_path: str = CHROMA_DB_PATH):
    os.makedirs(db_path, exist_ok=True)
    client = chromadb.PersistentClient(
        path=db_path, settings=Settings(anonymized_telemetry=False)
    )

    return client
