from app.agents.supervisor import (
    extract_order_number,
    supervisor_node,
)


def test_extract_order_number():
    query = "Why is ORD-10482 delayed?"

    result = extract_order_number(query)

    assert result == "ORD-10482"


def test_extract_order_number_is_case_insensitive():
    query = "Why is ord-10482 delayed?"

    result = extract_order_number(query)

    assert result == "ORD-10482"


def test_extract_order_number_returns_none_when_missing():
    query = "Which suppliers have delayed shipments?"

    result = extract_order_number(query)

    assert result is None


def test_supervisor_routes_order_investigation():
    state = {
        "user_query": "Why is ORD-10482 delayed?",
    }

    result = supervisor_node(state)

    assert result["order_number"] == "ORD-10482"

    assert result["required_agents"] == [
        "data_agent",
        "graph_agent",
        "rag_agent",
    ]


def test_supervisor_routes_general_query_to_rag():
    state = {
        "user_query": "What is the supplier delay policy?",
    }

    result = supervisor_node(state)

    assert result["order_number"] is None
    assert result["required_agents"] == ["rag_agent"]