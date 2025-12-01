from app.core.chunking import chunk_text


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
