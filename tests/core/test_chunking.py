from app.core.chunking import chunk_text, semantic_chunk_text_with_overlap


def test_semantic_chunk_single_paragraph_under_limit():
    text = "FastAPI makes it easy to build APIs quickly with Python."
    chunks = semantic_chunk_text_with_overlap(
        text=text,
        max_chunk_words=50,
        overlap_words=10,
    )

    assert len(chunks) == 1
    assert chunks[0].split() == text.split()


def test_semantic_chunk_two_paragraphs_no_split_when_total_under_limit():
    para1 = "FastAPI is a modern web framework for building APIs."
    para2 = "It is built on top of Starlette and Pydantic."

    text = f"{para1}\n\n{para2}"

    chunks = semantic_chunk_text_with_overlap(
        text=text,
        max_chunk_words=50,
        overlap_words=10,
    )

    assert len(chunks) == 1
    words = chunks[0].split()
    assert len(words) == len(para1.split()) + len(para2.split())
    for part in (para1, para2):
        for w in part.split():
            assert w in words


def test_semantic_chunk_creates_overlap_between_chunks():
    para1_words = [f"p1w{i}" for i in range(50)]
    para2_words = [f"p2w{i}" for i in range(50)]

    para1 = " ".join(para1_words)
    para2 = " ".join(para2_words)

    text = f"{para1}\n\n{para2}"

    chunks = semantic_chunk_text_with_overlap(
        text=text,
        max_chunk_words=60,
        overlap_words=10,
    )

    assert len(chunks) == 2

    chunk1_words = chunks[0].split()
    chunk2_words = chunks[1].split()

    assert len(chunk1_words) == 50
    assert len(chunk2_words) == 60

    expected_overlap = chunk1_words[-10:]
    assert chunk2_words[:10] == expected_overlap

    assert chunk2_words[-1] == "p2w49"


def test_semantic_chunk_no_overlap_when_overlap_zero():
    para1_words = [f"p1w{i}" for i in range(30)]
    para2_words = [f"p2w{i}" for i in range(30)]

    para1 = " ".join(para1_words)
    para2 = " ".join(para2_words)

    text = f"{para1}\n\n{para2}"

    chunks = semantic_chunk_text_with_overlap(
        text=text,
        max_chunk_words=40,
        overlap_words=0,
    )

    assert len(chunks) == 2

    chunk1_words = chunks[0].split()
    chunk2_words = chunks[1].split()

    assert chunk1_words[-1] != chunk2_words[0]
    assert len(chunk1_words) == 30
    assert len(chunk2_words) == 30


def test_semantic_chunk_empty_text_returns_empty_list():
    chunks = semantic_chunk_text_with_overlap(
        text="   ",
        max_chunk_words=50,
        overlap_words=10,
    )

    assert chunks == []


def test_semantic_chunk_preserves_paragraphs_as_units():
    para1 = "First paragraph about RAG and retrieval."
    para2 = "Second paragraph about FastAPI and the /rag-query endpoint."
    para3 = "Third paragraph suddenly switches to chunking strategies."

    text = f"{para1}\n\n{para2}\n\n{para3}"

    chunks = semantic_chunk_text_with_overlap(
        text=text,
        max_chunk_words=10,  # force multiple chunks
        overlap_words=2,
    )

    joined = " || ".join(chunks)

    assert para1.replace("\n", " ") in joined
    assert para2.replace("\n", " ") in joined
    assert para3.replace("\n", " ") in joined


def test_chunk_text_basic_split():
    text = " ".join([f"word{i}" for i in range(1, 51)])  # 50 words

    chunks = chunk_text(text, chunk_size=20, chunk_overlap=5)

    # 50 words with chunks of 20 and overlap 5:
    # 1st: 1–20
    # 2nd: 16–35
    # 3rd: 31–50  → so 3 chunks
    assert len(chunks) == 3

    # Check first and last words of each chunk
    first_chunk_words = chunks[0].split(" ")
    second_chunk_words = chunks[1].split(" ")
    third_chunk_words = chunks[2].split(" ")

    assert first_chunk_words[0] == "word1"
    assert first_chunk_words[-1] == "word20"

    assert second_chunk_words[0] == "word16"  # overlap starts
    assert second_chunk_words[-1] == "word35"

    assert third_chunk_words[0] == "word31"
    assert third_chunk_words[-1] == "word50"


def test_chunk_text_empty_input():
    assert chunk_text("") == []


def test_chunk_text_invalid_params():
    text = "hello world"
    try:
        chunk_text(text, chunk_size=0)
        assert False, "Expected ValueError for chunk_size <= 0"
    except ValueError:
        pass

    try:
        chunk_text(text, chunk_size=10, chunk_overlap=10)
        assert False, "Expected ValueError for overlap >= chunk_size"
    except ValueError:
        pass
