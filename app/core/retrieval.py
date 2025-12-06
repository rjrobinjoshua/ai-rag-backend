from typing import Any, Dict, List, Optional

from app.core import chroma_client
from app.models.chunk import ChunkMetadata, TextChunk
from app.services import openai_service


def _to_chunk_metadata(raw_meta) -> ChunkMetadata:
    if isinstance(raw_meta, ChunkMetadata):
        return raw_meta
    return ChunkMetadata(**raw_meta)


def _build_where(
    filename: Optional[str],
    metadata_filter: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """
    Build a Chroma-compatible 'where' filter.

    - If only one simple condition -> {"field": value}
    - If multiple conditions -> {"$and": [ {...}, {...}, ... ]}
    - If metadata_filter already uses an operator ($and, $or, etc.) and you also
      pass a filename, we wrap both in a top-level $and.
    """
    conditions: List[Dict[str, Any]] = []

    if filename:
        conditions.append({"filename": filename})

    if metadata_filter:
        # If the filter already has a top-level operator, treat it as one condition
        if any(key.startswith("$") for key in metadata_filter.keys()):
            conditions.append(metadata_filter)
        else:
            # Plain dict like {"filename": "resume.pdf", "page": {"$gt": 1}}
            # -> split into separate conditions
            for key, value in metadata_filter.items():
                conditions.append({key: value})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


async def search_chunks(
    query: str,
    collection_name: str = "docs",
    k: int = 3,
    filename: Optional[str] = None,
    metadata_filter: Optional[dict[str, Any]] = None,
) -> List[TextChunk]:
    given_embedding = await openai_service.embed_text(query)

    client = chroma_client.get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    where = _build_where(filename=filename, metadata_filter=metadata_filter)

    results = collection.query(
        query_embeddings=[given_embedding],
        n_results=k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results.get("ids", [[]])[0]

    chunks: List[TextChunk] = []
    for doc, meta, dist, id_ in zip(docs, metas, distances, ids):
        text_chunk = TextChunk(
            id=id_,
            text=doc,
            score=float(dist),
            metadata=_to_chunk_metadata(meta),
        )
        chunks.append(text_chunk)

    return chunks
