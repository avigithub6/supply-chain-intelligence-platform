from app.agents.recommendation_agent import recommendation_agent_node


def test_recommendation_agent_requires_investigation_results():
    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "completed_agents": [],
        "errors": [],
    }

    result = recommendation_agent_node(state)

    assert result["recommendation"] is None

    assert any(
        "no investigation results" in error
        for error in result["errors"]
    )


def test_recommendation_agent_detects_delayed_order():
    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "order_number": "ORD-10482",
        "data_result": {
            "order": {
                "order_number": "ORD-10482",
                "customer_name": "Customer 0482",
                "product_sku": "SKU-0077",
                "quantity": 445,
                "status": "delayed",
            },
            "shipment": {
                "shipment_number": "SHIP-20482",
                "order_number": "ORD-10482",
                "supplier_code": "SUP-017",
                "status": "delayed",
                "expected_delivery": "2026-09-16",
            },
        },
        "rag_result": [],
        "graph_result": None,
        "completed_agents": [],
        "errors": [],
    }

    result = recommendation_agent_node(state)

    recommendation = result["recommendation"]

    assert recommendation is not None
    assert recommendation["order_number"] == "ORD-10482"

    assert (
        "Escalate the delayed shipment for operational review."
        in recommendation["recommendations"]
    )

    assert "Order or shipment is delayed." in recommendation["risk_factors"]

    assert "recommendation_agent" in result["completed_agents"]


def test_recommendation_agent_detects_low_supplier_reliability():
    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "order_number": "ORD-10482",
        "data_result": None,
        "rag_result": [],
        "graph_result": {
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
        },
        "completed_agents": [],
        "errors": [],
    }

    result = recommendation_agent_node(state)

    recommendation = result["recommendation"]

    assert recommendation is not None
    assert recommendation["risk_level"] == "high"

    assert (
        "Supplier reliability is below the 70% threshold."
        in recommendation["risk_factors"]
    )

    assert any(
        "SUP-017" in item
        for item in recommendation["recommendations"]
    )


def test_recommendation_agent_detects_low_inventory():
    state = {
        "user_query": "Investigate ORD-10482",
        "order_number": "ORD-10482",
        "data_result": None,
        "rag_result": [],
        "graph_result": {
            "order_number": "ORD-10482",
            "product_sku": "SKU-0077",
            "quantity": 445,
            "order_status": "delayed",
            "current_stock": 35,
            "reorder_point": 250,
        },
        "completed_agents": [],
        "errors": [],
    }

    result = recommendation_agent_node(state)

    recommendation = result["recommendation"]

    assert recommendation is not None

    assert (
        "Current inventory is below the reorder point."
        in recommendation["risk_factors"]
    )

    assert any(
        "Initiate replenishment" in item
        for item in recommendation["recommendations"]
    )


def test_recommendation_agent_collects_rag_sources():
    state = {
        "user_query": "What is the supplier delay policy?",
        "data_result": None,
        "graph_result": None,
        "rag_result": [
            {
                "content": "Supplier delay escalation policy...",
                "source": "knowledge_base",
                "category": "supplier_sla",
                "file_name": "supplier_delay_policy.txt",
                "chunk_index": 0,
                "retrieval_score": 0.91,
                "rerank_score": 0.94,
            }
        ],
        "completed_agents": [],
        "errors": [],
    }

    result = recommendation_agent_node(state)

    recommendation = result["recommendation"]

    assert recommendation is not None

    assert (
        "supplier_delay_policy.txt"
        in recommendation["knowledge_sources"]
    )

    assert recommendation["risk_level"] == "low"
    assert "recommendation_agent" in result["completed_agents"]