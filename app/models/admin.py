from pydantic import BaseModel


class DocumentInfo(BaseModel):
    filename: str
    source: str
    num_chunks: int
    pages: list[int]
