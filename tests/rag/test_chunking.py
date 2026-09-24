import pytest

from app.rag.chunking import (
    chunk_document,
    chunk_documents,
)
from app.rag.ingestion import KnowledgeDocument


def create_test_document() -> KnowledgeDocument:
    content = " ".join(
        f"word{i}"
        for i in range(120)
    )

    return KnowledgeDocument(
        content=content,
        source="sop/test_document.txt",
        category="sop",
        file_name="test_document.txt",
    )


def test_chunk_document_creates_chunks() -> None:
    document = create_test_document()

    chunks = chunk_document(
        document=document,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(chunks) > 1

    assert chunks[0].source == (
        "sop/test_document.txt"
    )

    assert chunks[0].category == "sop"

    assert chunks[0].file_name == (
        "test_document.txt"
    )

    assert chunks[0].chunk_index == 0


def test_chunk_overlap() -> None:
    document = create_test_document()

    chunks = chunk_document(
        document=document,
        chunk_size=50,
        chunk_overlap=10,
    )

    first_chunk_words = chunks[0].content.split()
    second_chunk_words = chunks[1].content.split()

    assert first_chunk_words[-10:] == (
        second_chunk_words[:10]
    )


def test_chunk_documents() -> None:
    documents = [
        create_test_document(),
        create_test_document(),
    ]

    chunks = chunk_documents(
        documents=documents,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(chunks) > 2


def test_invalid_chunk_size() -> None:
    document = create_test_document()

    with pytest.raises(ValueError):
        chunk_document(
            document=document,
            chunk_size=0,
        )


def test_invalid_overlap() -> None:
    document = create_test_document()

    with pytest.raises(ValueError):
        chunk_document(
            document=document,
            chunk_size=50,
            chunk_overlap=50,
        )