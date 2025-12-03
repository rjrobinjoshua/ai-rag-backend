import re
from typing import List


def semantic_chunk_text_with_overlap(
    text: str,
    max_chunk_words: int = 300,
    overlap_words: int = 50,
) -> List[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    chunks: List[str] = []
    current_words: List[str] = []
    current_word_count = 0

    for paragraph in paragraphs:
        words = paragraph.split()
        if not words:
            continue

        if current_word_count + len(words) > max_chunk_words and current_words:
            chunks.append(" ".join(current_words))

            if overlap_words > 0:
                overlap_slice = current_words[-overlap_words:]
                current_words = overlap_slice + words
                current_word_count = len(current_words)
            else:
                current_words = words
                current_word_count = len(words)
        else:
            current_words.extend(words)
            current_word_count += len(words)

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def chunk_text(
    text: str,
    chunk_size: int = 200,  # roughly “words per chunk”
    chunk_overlap: int = 40,  # how many words overlap between chunks
) -> List[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    # Normalize whitespace
    text = " ".join(text.split())

    if not text:
        return []

    words = text.split(" ")
    total_words = len(words)
    chunks: List[str] = []

    start = 0
    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))

        if end == total_words:
            break

        start = end - chunk_overlap

    return chunks
