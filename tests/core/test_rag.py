# tests/core/test_rag.py

from app.core import rag
from app.models.chunk import ChunkMetadata, TextChunk


def test_build_context_single_chunk():
    chunks = [
        TextChunk(
            id="c1",
            text="  FastAPI is awesome.  ",
            score=0.1,
            metadata=ChunkMetadata(
                source="docs.md",
                filename="docs.md",
            ),
        )
    ]

    context = rag.build_context(chunks)

    # Should strip whitespace from the text
    assert "FastAPI is awesome." in context

    # Context should start with index [0] and metadata header
    lines = context.split("\n")
    assert lines[0].startswith("[0] [source=docs.md")
    assert "FastAPI is awesome." == lines[1]


def test_build_context_multiple_chunks():
    chunks = [
        TextChunk(
            id="c1",
            text="First chunk",
            score=0.1,
            metadata=ChunkMetadata(
                source="docs.md",
                filename="docs.md",
            ),
        ),
        TextChunk(
            id="c2",
            text="Second chunk",
            score=0.2,
            metadata=ChunkMetadata(
                source="docs.md",
                filename="docs.md",
            ),
        ),
    ]

    context = rag.build_context(chunks)

    # Two chunks, each should become a separate "block"
    parts = context.split("\n\n")
    assert len(parts) == 2

    header0, body0 = parts[0].split("\n", 1)
    header1, body1 = parts[1].split("\n", 1)

    assert header0.startswith("[0] [source=docs.md")
    assert body0 == "First chunk"

    assert header1.startswith("[1] [source=docs.md")
    assert body1 == "Second chunk"


def test_build_rag_prompt_structure():
    context = "[0] [source=docs.md]\nSome context\n\n[1] [source=docs.md]\nMore context"
    question = "What is this about?"

    prompt = rag.build_rag_prompt(context=context, question=question)

    # Basic structure checks
    assert "You are a precise assistant" in prompt
    assert "Context:" in prompt
    assert context in prompt
    assert "Question:" in prompt
    assert question in prompt
    assert "Instructions:" in prompt
    assert "Use ONLY the information in the context" in prompt
    assert "If the answer is not in the context" in prompt
    assert "add citations like [0], [1], [2]" in prompt
    assert "First write an 'ANSWER:' section" in prompt
    assert "Then write a 'SUMMARY:' section" in prompt

    # Format markers
    assert "ANSWER:" in prompt
    assert "SUMMARY:" in prompt
