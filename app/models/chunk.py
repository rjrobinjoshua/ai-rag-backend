from pydantic import BaseModel


class ChunkMetadata(BaseModel):
    source: str
    filename: str
    page: int | None = None
    chunk_number: int | None = None


class TextChunk(BaseModel):
    id: str
    text: str
    score: float
    metadata: ChunkMetadata
