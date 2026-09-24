from unittest.mock import patch

from app.agents.graph_agent import graph_agent_node


def test_graph_agent_requires_order_number():
    state = {
        "user_query": "Investigate the supply chain",
        "completed_agents": [],
        "errors": [],
    }

    result = graph_agent_node(state)

    assert result["graph_result"] is None
    assert "graph_agent" not in result["completed_agents"]

    assert any(
        "order number is missing" in error
        for error in result["errors"]
    )


def test_graph_agent_returns_graph_context():
    fake_record = {
        "order_number": "ORD-10482",
        "customer_name": "Customer 0482",
        "product_sku": "SKU-0077",
        "quantity": 445,
        "order_status": "delayed",
        "graph_product_sku": "SKU-0077",
        "warehouse": "Mumbai",
        "current_stock": 35,
        "reorder_point": 250,
        "shipment_number": "SHIP-20482",
        "shipment_status": "delayed",
        "expected_delivery": "2026-09-16",
        "supplier_code": "SUP-017",
        "supplier_name": "Supplier 017 Industries",
        "supplier_location": "Pune",
        "supplier_reliability": 62.5,
    }

    with patch(
        "app.agents.graph_agent.neo4j_client.execute_query",
        return_value=[fake_record],
    ):
        state = {
            "user_query": "Why is ORD-10482 delayed?",
            "order_number": "ORD-10482",
            "completed_agents": [],
            "errors": [],
        }

        result = graph_agent_node(state)

    assert result["graph_result"] is not None

    graph_result = result["graph_result"]

    assert graph_result["order_number"] == "ORD-10482"
    assert graph_result["product_sku"] == "SKU-0077"
    assert graph_result["warehouse"] == "Mumbai"
    assert graph_result["shipment_number"] == "SHIP-20482"
    assert graph_result["supplier_code"] == "SUP-017"
    assert graph_result["supplier_reliability"] == 62.5

    assert "graph_agent" in result["completed_agents"]


def test_graph_agent_handles_missing_graph_record():
    with patch(
        "app.agents.graph_agent.neo4j_client.execute_query",
        return_value=[],
    ):
        state = {
            "user_query": "Why is ORD-99999 delayed?",
            "order_number": "ORD-99999",
            "completed_agents": [],
            "errors": [],
        }

        result = graph_agent_node(state)

    assert result["graph_result"] is None
    assert "graph_agent" in result["completed_agents"]

    assert any(
        "Order not found in graph" in error
        for error in result["errors"]
    )


def test_graph_agent_handles_neo4j_failure():
    with patch(
        "app.agents.graph_agent.neo4j_client.execute_query",
        side_effect=RuntimeError("Neo4j unavailable"),
    ):
        state = {
            "user_query": "Why is ORD-10482 delayed?",
            "order_number": "ORD-10482",
            "completed_agents": [],
            "errors": [],
        }

        result = graph_agent_node(state)

    assert result["graph_result"] is None
    assert "graph_agent" in result["completed_agents"]

    assert any(
        "Neo4j unavailable" in error
        for error in result["errors"]
    )