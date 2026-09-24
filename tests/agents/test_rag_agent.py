from types import SimpleNamespace
from unittest.mock import patch

from app.agents.rag_agent import rag_agent_node


def test_rag_agent_handles_empty_query():
    state = {
        "user_query": "",
        "completed_agents": [],
        "errors": [],
    }

    result = rag_agent_node(state)

    assert result["rag_result"] == []
    assert "rag_agent" not in result["completed_agents"]
    assert any(
        "user query is empty" in error
        for error in result["errors"]
    )


def test_rag_agent_returns_retrieved_knowledge():
    fake_chunk = SimpleNamespace(
        content="Supplier delays must be escalated.",
        source="knowledge_base",
        category="policies",
        file_name="supplier_delay_policy.txt",
        chunk_index=0,
        retrieval_score=0.91,
        rerank_score=0.95,
    )

    fake_search_result = SimpleNamespace(
        query="Why is ORD-10482 delayed?",
        chunks=[fake_chunk],
    )

    fake_search_service = SimpleNamespace(
        search=lambda query, retrieval_limit, top_k: fake_search_result
    )

    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "completed_agents": [],
        "errors": [],
    }

    with patch(
        "app.agents.rag_agent.get_knowledge_search_service",
        return_value=fake_search_service,
    ):
        result = rag_agent_node(state)

    assert len(result["rag_result"]) == 1

    chunk = result["rag_result"][0]

    assert (
        chunk["content"]
        == "Supplier delays must be escalated."
    )

    assert (
        chunk["file_name"]
        == "supplier_delay_policy.txt"
    )

    assert chunk["rerank_score"] == 0.95
    assert "rag_agent" in result["completed_agents"]


def test_rag_agent_handles_search_failure():
    fake_search_service = SimpleNamespace(
        search=lambda query, retrieval_limit, top_k: (
            (_ for _ in ()).throw(
                RuntimeError("Qdrant unavailable")
            )
        )
    )

    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "completed_agents": [],
        "errors": [],
    }

    with patch(
        "app.agents.rag_agent.get_knowledge_search_service",
        return_value=fake_search_service,
    ):
        result = rag_agent_node(state)

    assert result["rag_result"] == []
    assert "rag_agent" in result["completed_agents"]

    assert any(
        "Qdrant unavailable" in error
        for error in result["errors"]
    )