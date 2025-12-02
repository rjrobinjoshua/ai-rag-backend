import os
import re
from typing import Literal

from pypdf import PdfReader


def _load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)

    # Join all pages with a page separator to avoid accidental word merging
    return "\n\n".join(pages_text)


def clean_text(raw_text: str) -> str:
    """
    Very simple text cleaner:
    - Normalizes newlines
    - Removes excessive blank lines
    - Collapses multiple spaces
    - Joins broken lines into paragraphs
    """
    if not raw_text:
        return ""

    # Normalize Windows/Mac newlines
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # Split into paragraphs based on blank lines
    blocks = re.split(r"\n\s*\n", text)

    cleaned_blocks: list[str] = []
    for block in blocks:
        # Remove leading/trailing whitespace per line and filters out empty lines
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        paragraph = " ".join(lines)
        # Collapse multiple spaces inside the paragraph
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if paragraph:
            cleaned_blocks.append(paragraph)

    # Join paragraphs with a single blank line
    cleaned_text = "\n\n".join(cleaned_blocks)
    return cleaned_text


def load_document(
    file_path: str, *, file_type: Literal["auto", "txt", "pdf"] = "auto"
) -> str:
    """
    Load a document from disk and return cleaned text.

    - Supports .txt and .pdf
    - If file_type == 'auto', infers from file extension
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if file_type == "auto":
        if ext == ".txt":
            file_type = "txt"
        elif ext == ".pdf":
            file_type = "pdf"
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    if file_type == "txt":
        raw = _load_txt(file_path)
    elif file_type == "pdf":
        raw = _load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file_type: {file_type}")

    return clean_text(raw)
