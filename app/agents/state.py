from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    """
    Shared state passed between LangGraph agents.

    Each agent reads information from this state and adds
    its own investigation results.
    """

    # Original user question
    user_query: str

    # Extracted business identifier
    order_number: str | None

    # Agents selected by the supervisor
    required_agents: list[str]

    # Results collected from different sources
    data_result: dict[str, Any] | None
    rag_result: list[dict[str, Any]] | None
    graph_result: dict[str, Any] | None

    # Final combined recommendation
    recommendation: dict[str, Any] | None

    # Final response shown to the user
    final_answer: str | None

    # Tracks which agents have already executed
    completed_agents: list[str]

    # Stores non-fatal errors from individual agents
    errors: list[str]