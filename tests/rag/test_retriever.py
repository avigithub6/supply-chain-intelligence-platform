from dataclasses import dataclass

import pytest

from app.rag.retriever import KnowledgeRetriever


@dataclass
class FakeResult:
    payload: dict
    score: float


class FakeSearchResponse:
    def __init__(
        self,
        points: list[FakeResult],
    ) -> None:
        self.points = points


class FakeEmbeddingService:
    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return [
            0.1,
            0.2,
            0.3,
            0.4,
        ]


class FakeQdrantStore:
    def __init__(self) -> None:
        self.received_embedding = None
        self.received_limit = None

    def search(
        self,
        query_embedding: list[float],
        limit: int,
    ) -> FakeSearchResponse:
        self.received_embedding = query_embedding
        self.received_limit = limit

        return FakeSearchResponse(
            points=[
                FakeResult(
                    payload={
                        "content": (
                            "Supplier shipment "
                            "is delayed."
                        ),
                        "source": (
                            "supplier_sla/"
                            "supplier_delay_policy.txt"
                        ),
                        "category": "supplier_sla",
                        "file_name": (
                            "supplier_delay_policy.txt"
                        ),
                        "chunk_index": 0,
                    },
                    score=0.92,
                ),
                FakeResult(
                    payload={
                        "content": (
                            "Contact the supplier "
                            "for an updated delivery date."
                        ),
                        "source": (
                            "supplier_sla/"
                            "supplier_delay_policy.txt"
                        ),
                        "category": "supplier_sla",
                        "file_name": (
                            "supplier_delay_policy.txt"
                        ),
                        "chunk_index": 1,
                    },
                    score=0.87,
                ),
            ]
        )


def create_retriever() -> tuple[
    KnowledgeRetriever,
    FakeEmbeddingService,
    FakeQdrantStore,
]:
    embedding_service = FakeEmbeddingService()
    qdrant_store = FakeQdrantStore()

    retriever = KnowledgeRetriever(
        embedding_service=embedding_service,
        qdrant_store=qdrant_store,
    )

    return (
        retriever,
        embedding_service,
        qdrant_store,
    )


def test_retrieve_chunks() -> None:
    retriever, _, _ = create_retriever()

    results = retriever.retrieve(
        query=(
            "What should we do when "
            "a supplier shipment is delayed?"
        ),
        limit=5,
    )

    assert len(results) == 2

    assert results[0].content == (
        "Supplier shipment is delayed."
    )

    assert results[0].source == (
        "supplier_sla/"
        "supplier_delay_policy.txt"
    )

    assert results[0].category == (
        "supplier_sla"
    )

    assert results[0].file_name == (
        "supplier_delay_policy.txt"
    )

    assert results[0].chunk_index == 0

    assert results[0].retrieval_score == 0.92


def test_query_is_embedded() -> None:
    retriever, _, qdrant_store = (
        create_retriever()
    )

    retriever.retrieve(
        query="Supplier shipment delay",
        limit=3,
    )

    assert qdrant_store.received_embedding == [
        0.1,
        0.2,
        0.3,
        0.4,
    ]

    assert qdrant_store.received_limit == 3


def test_empty_query() -> None:
    retriever, _, _ = create_retriever()

    with pytest.raises(ValueError):
        retriever.retrieve(
            query=""
        )


def test_whitespace_query() -> None:
    retriever, _, _ = create_retriever()

    with pytest.raises(ValueError):
        retriever.retrieve(
            query="   "
        )


def test_invalid_limit() -> None:
    retriever, _, _ = create_retriever()

    with pytest.raises(ValueError):
        retriever.retrieve(
            query="Supplier delay",
            limit=0,
        )


def test_negative_limit() -> None:
    retriever, _, _ = create_retriever()

    with pytest.raises(ValueError):
        retriever.retrieve(
            query="Supplier delay",
            limit=-1,
        )