# tests/core/test_rag.py

from app.core import rag
from app.models.chunk import ChunkMetadata, TextChunk


def test_build_context_single_chunk():
    chunks = [
        TextChunk(
            id="c1",
            text="  FastAPI is awesome.  ",
            score=0.1,
            metadata=ChunkMetadata(source="docs.md", filename="docs.md"),
        )
    ]

    context = rag.build_context(chunks)

    # Should strip whitespace
    assert "FastAPI is awesome." in context
    # Should contain index [0] because enumerate starts at 0 in current code
    assert context.startswith("[0] FastAPI is awesome.")


def test_build_context_multiple_chunks():
    chunks = [
        TextChunk(
            id="c1",
            text="First chunk",
            score=0.1,
            metadata=ChunkMetadata(source="docs.md", filename="docs.md"),
        ),
        TextChunk(
            id="c2",
            text="Second chunk",
            score=0.2,
            metadata=ChunkMetadata(source="docs.md", filename="docs.md"),
        ),
    ]

    context = rag.build_context(chunks)
    # Two chunks, each on their own "paragraph"
    parts = context.split("\n\n")
    assert len(parts) == 2
    assert parts[0] == "[0] First chunk"
    assert parts[1] == "[1] Second chunk"


def test_build_rag_prompt_structure():
    context = "[0] Some context\n\n[1] More context"
    question = "What is this about?"

    prompt = rag.build_rag_prompt(context=context, question=question)

    # Basic structure checks
    assert "You are a precise assistant" in prompt
    assert "Context:" in prompt
    assert context in prompt
    assert "Question:" in prompt
    assert question in prompt
    assert "Instructions:" in prompt
    assert "If the answer is in the context" in prompt
    assert "Answer:" in prompt
