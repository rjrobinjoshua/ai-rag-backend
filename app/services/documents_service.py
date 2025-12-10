from collections import defaultdict
from typing import List

from app.core import chroma_client
from app.models.admin import DocumentInfo


def list_documents(collection_name: str = "docs") -> List[DocumentInfo]:
    client = chroma_client.get_chroma_client()
    collection = client.get_or_create_collection(name=collection_name)

    # If this ever gets huge, we can paginate.
    results = collection.get(include=["metadatas"], limit=10000)

    agg = defaultdict(
        lambda: {"source": None, "count": 0, "pages": set()},
    )

    for meta in results.get("metadatas", []):
        if not meta:
            continue
        filename = meta.get("filename")
        source = meta.get("source")
        page = meta.get("page")

        if not filename:
            continue

        key = filename
        if agg[key]["source"] is None:
            agg[key]["source"] = source or ""

        agg[key]["count"] += 1
        if page is not None:
            agg[key]["pages"].add(page)

    docs: List[DocumentInfo] = []
    for filename, info in agg.items():
        docs.append(
            DocumentInfo(
                filename=filename,
                source=info["source"],
                num_chunks=info["count"],
                pages=sorted(info["pages"]),
            )
        )

    return docs
