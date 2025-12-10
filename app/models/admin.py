from typing import List, Literal

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    filename: str
    source: str
    num_chunks: int
    pages: list[int]


class ReindexRequest(BaseModel):
    paths: List[str]
    collection: str = "docs"
    chunk_size: int = 200
    chunk_overlap: int = 40
    mode: Literal["fixed", "semantic"] = "fixed"
    reset: bool = True
