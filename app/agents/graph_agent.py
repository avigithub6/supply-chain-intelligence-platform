from app.agents.state import AgentState
from app.graph.neo4j_client import neo4j_client
from app.graph.queries import GET_ORDER_GRAPH_CONTEXT_QUERY


def graph_agent_node(state: AgentState) -> AgentState:
    """
    Investigate an order and its related supply-chain entities
    using the Neo4j knowledge graph.
    """

    order_number = state.get("order_number")

    if not order_number:
        return {
            **state,
            "graph_result": None,
            "completed_agents": [
                *state.get("completed_agents", []),
            ],
            "errors": [
                *state.get("errors", []),
                "Graph Agent: order number is missing.",
            ],
        }

    try:
        records = neo4j_client.execute_query(
            GET_ORDER_GRAPH_CONTEXT_QUERY,
            {
                "order_number": order_number,
            },
        )

        if not records:
            return {
                **state,
                "graph_result": None,
                "completed_agents": [
                    *state.get("completed_agents", []),
                    "graph_agent",
                ],
                "errors": [
                    *state.get("errors", []),
                    f"Order not found in graph: {order_number}",
                ],
            }

        graph_result = records[0]

        return {
            **state,
            "graph_result": graph_result,
            "completed_agents": [
                *state.get("completed_agents", []),
                "graph_agent",
            ],
        }

    except Exception as exc:
        return {
            **state,
            "graph_result": None,
            "completed_agents": [
                *state.get("completed_agents", []),
                "graph_agent",
            ],
            "errors": [
                *state.get("errors", []),
                f"Graph Agent error: {exc}",
            ],
        }