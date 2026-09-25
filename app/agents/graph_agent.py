from typing import Any

from app.agents.state import AgentState
from app.graph.neo4j_client import neo4j_client
from app.graph.queries import GET_ORDER_GRAPH_CONTEXT_QUERY


def _make_json_safe(value: Any) -> Any:
    """
    Convert Neo4j temporal and nested values into
    LangGraph/msgpack-safe Python values.

    Neo4j may return objects such as:
    - neo4j.time.Date
    - neo4j.time.DateTime
    - datetime/date/time

    These objects are not directly serializable by
    LangGraph's checkpoint serializer.
    """

    if isinstance(value, dict):
        return {
            key: _make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            _make_json_safe(item)
            for item in value
        ]

    if isinstance(value, set):
        return [
            _make_json_safe(item)
            for item in value
        ]

    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except (TypeError, ValueError):
            pass

    return value


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

        graph_result = _make_json_safe(records[0])

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