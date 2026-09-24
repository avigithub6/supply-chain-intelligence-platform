from fastapi.testclient import TestClient

from app.main import app
from app.rag.dependencies import get_knowledge_search_service
from app.rag.retriever import RetrievedChunk
from app.rag.search_service import KnowledgeSearchResult


class FakeKnowledgeSearchService:
    def search(
        self,
        query: str,
        retrieval_limit: int = 5,
        top_k: int = 3,
    ) -> KnowledgeSearchResult:
        return KnowledgeSearchResult(
            query=query,
            chunks=[
                RetrievedChunk(
                    content="Contact the supplier and request an updated delivery date.",
                    source="supplier_sla/supplier_delay_policy.txt",
                    category="supplier_sla",
                    file_name="supplier_delay_policy.txt",
                    chunk_index=0,
                    retrieval_score=0.91,
                )
            ],
        )


def override_search_service() -> FakeKnowledgeSearchService:
    return FakeKnowledgeSearchService()


app.dependency_overrides[
    get_knowledge_search_service
] = override_search_service


client = TestClient(app)


def teardown_module() -> None:
    app.dependency_overrides.clear()


def test_rag_search_success() -> None:
    response = client.post(
        "/rag/search",
        json={
            "query": "What should we do when a supplier shipment is delayed?",
            "retrieval_limit": 5,
            "top_k": 3,
        },
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]

    data = response.json()

    assert (
        data["query"]
        == "What should we do when a supplier shipment is delayed?"
    )

    assert len(data["chunks"]) == 1

    assert (
        data["chunks"][0]["file_name"]
        == "supplier_delay_policy.txt"
    )


def test_rag_search_rejects_empty_query() -> None:
    response = client.post(
        "/rag/search",
        json={
            "query": "",
        },
    )

    assert response.status_code == 422


def test_rag_search_rejects_invalid_retrieval_limit() -> None:
    response = client.post(
        "/rag/search",
        json={
            "query": "supplier delay",
            "retrieval_limit": 0,
        },
    )

    assert response.status_code == 422


def test_rag_search_rejects_invalid_top_k() -> None:
    response = client.post(
        "/rag/search",
        json={
            "query": "supplier delay",
            "top_k": 0,
        },
    )

    assert response.status_code == 422


def test_rag_search_rejects_excessive_retrieval_limit() -> None:
    response = client.post(
        "/rag/search",
        json={
            "query": "supplier delay",
            "retrieval_limit": 21,
        },
    )

    assert response.status_code == 422