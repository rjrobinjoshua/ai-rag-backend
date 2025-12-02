from pathlib import Path

import pytest

from app.core.doc_loader import clean_text, load_document


def test_clean_text_joins_lines_into_paragraphs():
    raw_text = "Line 1\nLine 2\n\nLine 3\n   Line 4  "
    cleaned_text = clean_text(raw_text)

    assert "Line 1 Line 2" in cleaned_text
    assert "Line 3 Line 4" in cleaned_text
    assert "  " not in cleaned_text

    paragraphs = cleaned_text.split("\n\n")
    assert len(paragraphs) == 2


def test_clean_text_collapses_whitespace():
    raw_text = "  FastAPI    is   \n\n   great   "
    cleaned_text = clean_text(raw_text)

    assert cleaned_text == "FastAPI is\n\ngreat"
    assert "  " not in cleaned_text


def test_load_document_for_txt_file(tmp_path: Path):
    txt_path = tmp_path / "sample.txt"
    txt_path.write_text(
        "This is   a\nsimple   text file.\n\nSecond paragraph.",
        encoding="utf-8",
    )

    loaded_text = load_document(str(txt_path))

    assert "This is a simple text file." in loaded_text
    assert "Second paragraph." in loaded_text
    assert "  " not in loaded_text


def test_load_document_for_pdf_sample_if_present():
    project_tests_dir = Path(__file__).parents[1]  # .../tests
    pdf_path = project_tests_dir / "data" / "test_fastapi_multipage.pdf"

    if not pdf_path.exists():
        pytest.skip("Sample PDF not found at tests/data/test_fastapi_multipage.pdf")

    loaded_text = load_document(str(pdf_path))

    assert isinstance(loaded_text, str)
    assert loaded_text
    assert "FastAPI" in loaded_text
