from app.agents.state import AgentState
from app.rag.dependencies import get_knowledge_search_service


def rag_agent_node(state: AgentState) -> AgentState:
    """
    Retrieve relevant supply-chain knowledge using the
    existing RAG search service.
    """

    user_query = state.get("user_query", "").strip()

    if not user_query:
        return {
            **state,
            "rag_result": [],
            "completed_agents": [
                *state.get("completed_agents", []),
            ],
            "errors": [
                *state.get("errors", []),
                "RAG Agent: user query is empty.",
            ],
        }

    try:
        search_service = get_knowledge_search_service()

        search_result = search_service.search(
            query=user_query,
            retrieval_limit=5,
            top_k=3,
        )

        rag_result = []

        for chunk in search_result.chunks:
            rag_result.append(
                {
                    "content": chunk.content,
                    "source": chunk.source,
                    "category": chunk.category,
                    "file_name": chunk.file_name,
                    "chunk_index": chunk.chunk_index,
                    "retrieval_score": chunk.retrieval_score,
                    "rerank_score": chunk.rerank_score,
                }
            )

        return {
            **state,
            "rag_result": rag_result,
            "completed_agents": [
                *state.get("completed_agents", []),
                "rag_agent",
            ],
        }

    except Exception as exc:
        return {
            **state,
            "rag_result": [],
            "completed_agents": [
                *state.get("completed_agents", []),
                "rag_agent",
            ],
            "errors": [
                *state.get("errors", []),
                f"RAG Agent error: {exc}",
            ],
        }