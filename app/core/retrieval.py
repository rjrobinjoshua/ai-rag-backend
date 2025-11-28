from typing import List

from app.core import chroma_client
from app.models.chunk import TextChunk
from app.services import openai_service


async def search_chunks(
    query: str, collection_name: str = "docs", k: int = 3
) -> List[TextChunk]:
    given_embedding = await openai_service.embed_text(query)
    client = chroma_client.get_chroma_client()

    collection = client.get_or_create_collection(name=collection_name)
    results = collection.query(
        query_embeddings=[given_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results.get("ids", [[]])[0]

    chunks = []
    for doc, meta, dist, id_ in zip(docs, metas, distances, ids):
        text_chunk = TextChunk(
            id=id_,
            text=doc,
            score=float(dist),
            metadata=meta or {},
        )
        chunks.append(text_chunk)

    return chunks
