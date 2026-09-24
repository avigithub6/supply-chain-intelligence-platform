from app.agents.data_agent import data_agent_node


def test_data_agent_requires_order_number():
    state = {
        "user_query": "Show me order information",
        "completed_agents": [],
        "errors": [],
    }

    result = data_agent_node(state)

    assert result["data_result"] is None
    assert "data_agent" in result["completed_agents"]


def test_data_agent_returns_order_data():
    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "order_number": "ORD-10482",
        "completed_agents": [],
        "errors": [],
    }

    result = data_agent_node(state)

    assert result["data_result"] is not None

    assert (
        result["data_result"]["order"]["order_number"]
        == "ORD-10482"
    )

    assert (
        result["data_result"]["order"]["status"]
        == "delayed"
    )


def test_data_agent_returns_shipment_data():
    state = {
        "user_query": "Why is ORD-10482 delayed?",
        "order_number": "ORD-10482",
        "completed_agents": [],
        "errors": [],
    }

    result = data_agent_node(state)

    shipment = result["data_result"]["shipment"]

    assert shipment is not None
    assert shipment["shipment_number"] == "SHIP-20482"
    assert shipment["supplier_code"] == "SUP-017"
    assert shipment["status"] == "delayed"