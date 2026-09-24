from app.rag.retriever import RetrievedChunk
from app.rag.search_service import KnowledgeSearchService


class FakeRetriever:
    def retrieve(
        self,
        query: str,
        limit: int,
    ) -> list[RetrievedChunk]:
        return [
            RetrievedChunk(
                content="Supplier shipment is delayed.",
                source="supplier_sla/supplier_delay_policy.txt",
                category="supplier_sla",
                file_name="supplier_delay_policy.txt",
                chunk_index=0,
                retrieval_score=0.95,
            ),
            RetrievedChunk(
                content="Inventory should be monitored using reorder point.",
                source="sop/inventory_replenishment_sop.txt",
                category="sop",
                file_name="inventory_replenishment_sop.txt",
                chunk_index=0,
                retrieval_score=0.70,
            ),
        ]


class FakeReranker:
    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        top_k: int,
    ) -> list[RetrievedChunk]:
        return chunks[:top_k]


def create_service() -> KnowledgeSearchService:
    return KnowledgeSearchService(
        retriever=FakeRetriever(),
        reranker=FakeReranker(),
    )


def test_search_returns_reranked_results() -> None:
    service = create_service()

    result = service.search(
        query="supplier shipment delay",
        retrieval_limit=5,
        top_k=1,
    )

    assert result.query == "supplier shipment delay"

    assert len(result.chunks) == 1

    assert (
        result.chunks[0].file_name
        == "supplier_delay_policy.txt"
    )


def test_search_rejects_empty_query() -> None:
    service = create_service()

    try:
        service.search("")
        assert False
    except ValueError as error:
        assert str(error) == "Query cannot be empty."


def test_search_rejects_invalid_retrieval_limit() -> None:
    service = create_service()

    try:
        service.search(
            query="supplier delay",
            retrieval_limit=0,
        )
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "retrieval_limit must be greater than 0."
        )


def test_search_rejects_invalid_top_k() -> None:
    service = create_service()

    try:
        service.search(
            query="supplier delay",
            top_k=0,
        )
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "top_k must be greater than 0."
        )