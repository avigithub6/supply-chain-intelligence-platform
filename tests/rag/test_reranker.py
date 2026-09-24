import pytest

from app.rag.retriever import RetrievedChunk
from app.rag.reranker import KnowledgeReranker


def create_chunk(
    content: str,
    retrieval_score: float,
    chunk_index: int = 0,
) -> RetrievedChunk:
    return RetrievedChunk(
        content=content,
        source="sop/test.txt",
        category="sop",
        file_name="test.txt",
        chunk_index=chunk_index,
        retrieval_score=retrieval_score,
    )


def test_rerank_returns_top_k() -> None:
    reranker = KnowledgeReranker()

    chunks = [
        create_chunk(
            content="Inventory replenishment process.",
            retrieval_score=0.80,
            chunk_index=0,
        ),
        create_chunk(
            content="Supplier shipment delay policy.",
            retrieval_score=0.90,
            chunk_index=1,
        ),
        create_chunk(
            content="Customer communication policy.",
            retrieval_score=0.70,
            chunk_index=2,
        ),
        create_chunk(
            content="Supplier escalation process.",
            retrieval_score=0.85,
            chunk_index=3,
        ),
    ]

    results = reranker.rerank(
        query="supplier shipment delay",
        chunks=chunks,
        top_k=2,
    )

    assert len(results) == 2


def test_rerank_preserves_chunk_data() -> None:
    reranker = KnowledgeReranker()

    chunk = create_chunk(
        content="Supplier shipment delay policy.",
        retrieval_score=0.90,
    )

    results = reranker.rerank(
        query="supplier shipment delay",
        chunks=[chunk],
        top_k=1,
    )

    assert len(results) == 1

    assert results[0].content == (
        "Supplier shipment delay policy."
    )

    assert results[0].source == (
        "sop/test.txt"
    )

    assert results[0].category == "sop"

    assert results[0].file_name == "test.txt"

    assert results[0].chunk_index == 0

    assert results[0].retrieval_score == 0.90


def test_keyword_relevance_affects_ranking() -> None:
    reranker = KnowledgeReranker()

    chunks = [
        create_chunk(
            content=(
                "Inventory warehouse stock "
                "replenishment process."
            ),
            retrieval_score=0.90,
            chunk_index=0,
        ),
        create_chunk(
            content=(
                "Supplier shipment delay "
                "escalation process."
            ),
            retrieval_score=0.85,
            chunk_index=1,
        ),
    ]

    results = reranker.rerank(
        query="supplier shipment delay",
        chunks=chunks,
        top_k=2,
    )

    assert results[0].chunk_index == 1


def test_empty_chunks() -> None:
    reranker = KnowledgeReranker()

    results = reranker.rerank(
        query="supplier delay",
        chunks=[],
        top_k=3,
    )

    assert results == []


def test_empty_query() -> None:
    reranker = KnowledgeReranker()

    with pytest.raises(ValueError):
        reranker.rerank(
            query="",
            chunks=[],
            top_k=3,
        )


def test_whitespace_query() -> None:
    reranker = KnowledgeReranker()

    with pytest.raises(ValueError):
        reranker.rerank(
            query="   ",
            chunks=[],
            top_k=3,
        )


def test_invalid_top_k() -> None:
    reranker = KnowledgeReranker()

    chunk = create_chunk(
        content="Supplier delay.",
        retrieval_score=0.90,
    )

    with pytest.raises(ValueError):
        reranker.rerank(
            query="supplier delay",
            chunks=[chunk],
            top_k=0,
        )


def test_negative_top_k() -> None:
    reranker = KnowledgeReranker()

    chunk = create_chunk(
        content="Supplier delay.",
        retrieval_score=0.90,
    )

    with pytest.raises(ValueError):
        reranker.rerank(
            query="supplier delay",
            chunks=[chunk],
            top_k=-1,
        )

def test_rerank_sets_rerank_score() -> None:
    reranker = KnowledgeReranker()

    chunk = create_chunk(
        content="Supplier shipment delay requires supplier contact.",
        retrieval_score=0.80,
    )

    results = reranker.rerank(
        query="supplier shipment delay",
        chunks=[chunk],
        top_k=1,
    )

    assert len(results) == 1

    assert results[0].rerank_score is not None

    assert results[0].rerank_score > 0        