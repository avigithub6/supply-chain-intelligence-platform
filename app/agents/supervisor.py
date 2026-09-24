import re

from app.agents.state import AgentState


ORDER_PATTERN = re.compile(r"\bORD-\d+\b", re.IGNORECASE)


def extract_order_number(user_query: str) -> str | None:
    """
    Extract an order number from the user's query.
    """

    match = ORDER_PATTERN.search(user_query)

    if not match:
        return None

    return match.group(0).upper()


def supervisor_node(state: AgentState) -> AgentState:
    """
    Decide which agents are required for the user's query.

    Current routing is deterministic.
    """

    user_query = state.get("user_query", "").strip()

    order_number = extract_order_number(user_query)

    required_agents: list[str] = []

    if order_number:
        required_agents.extend(
            [
                "data_agent",
                "graph_agent",
                "rag_agent",
            ]
        )
    else:
        required_agents.append("rag_agent")

    return {
        **state,
        "order_number": order_number,
        "required_agents": required_agents,
    }