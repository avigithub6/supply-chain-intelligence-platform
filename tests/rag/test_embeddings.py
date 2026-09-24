from dataclasses import dataclass

import pytest

from app.rag.chunking import DocumentChunk
from app.rag.embeddings import EmbeddingService


@dataclass
class FakeEmbedding:
    values: list[float]

    def tolist(self) -> list[float]:
        return self.values


class FakeModel:
    def encode(
        self,
        texts,
        normalize_embeddings: bool = False,
    ):
        if isinstance(texts, str):
            return FakeEmbedding(
                values=[0.1, 0.2, 0.3, 0.4]
            )

        return [
            FakeEmbedding(
                values=[0.1, 0.2, 0.3, 0.4]
            )
            for _ in texts
        ]


def test_embed_text() -> None:
    service = EmbeddingService(
        model=FakeModel()
    )

    embedding = service.embed_text(
        "Supplier shipment is delayed."
    )

    assert isinstance(embedding, list)

    assert len(embedding) == 4

    assert embedding == [
        0.1,
        0.2,
        0.3,
        0.4,
    ]


def test_embed_empty_text() -> None:
    service = EmbeddingService(
        model=FakeModel()
    )

    with pytest.raises(ValueError):
        service.embed_text("")


def test_embed_whitespace_text() -> None:
    service = EmbeddingService(
        model=FakeModel()
    )

    with pytest.raises(ValueError):
        service.embed_text("   ")


def test_embed_chunks() -> None:
    service = EmbeddingService(
        model=FakeModel()
    )

    chunks = [
        DocumentChunk(
            content="Supplier shipment is delayed.",
            source="supplier_sla/test.txt",
            category="supplier_sla",
            file_name="test.txt",
            chunk_index=0,
        ),
        DocumentChunk(
            content="Inventory is below reorder point.",
            source="sop/test.txt",
            category="sop",
            file_name="test.txt",
            chunk_index=0,
        ),
    ]

    embeddings = service.embed_chunks(chunks)

    assert len(embeddings) == 2

    assert len(embeddings[0]) == 4

    assert len(embeddings[1]) == 4


def test_empty_chunks() -> None:
    service = EmbeddingService(
        model=FakeModel()
    )

    embeddings = service.embed_chunks([])

    assert embeddings == []