from unittest.mock import patch

from app.workflows.supply_chain_graph import (
    build_supply_chain_graph,
    route_after_data,
    route_after_graph,
    route_after_supervisor,
)


def test_route_after_supervisor_order_investigation():
    state = {
        "required_agents": [
            "data_agent",
            "graph_agent",
            "rag_agent",
        ]
    }

    route = route_after_supervisor(state)

    assert route == "data_agent"


def test_route_after_supervisor_general_query():
    state = {
        "required_agents": ["rag_agent"]
    }

    route = route_after_supervisor(state)

    assert route == "rag_agent"


def test_route_after_supervisor_empty():
    state = {
        "required_agents": []
    }

    route = route_after_supervisor(state)

    assert route == "recommendation_agent"


def test_route_after_data():
    state = {
        "required_agents": [
            "data_agent",
            "graph_agent",
            "rag_agent",
        ]
    }

    route = route_after_data(state)

    assert route == "graph_agent"


def test_route_after_graph():
    state = {
        "required_agents": [
            "data_agent",
            "graph_agent",
            "rag_agent",
        ]
    }

    route = route_after_graph(state)

    assert route == "rag_agent"


@patch(
    "app.workflows.supply_chain_graph.recommendation_agent_node"
)
@patch(
    "app.workflows.supply_chain_graph.rag_agent_node"
)
@patch(
    "app.workflows.supply_chain_graph.graph_agent_node"
)
@patch(
    "app.workflows.supply_chain_graph.data_agent_node"
)
def test_complete_order_investigation_workflow(
    mock_data_agent,
    mock_graph_agent,
    mock_rag_agent,
    mock_recommendation_agent,
):
    mock_data_agent.side_effect = lambda state: {
        **state,
        "data_result": {
            "order": {
                "order_number": "ORD-10482",
                "status": "delayed",
                "product_sku": "SKU-0077",
                "quantity": 445,
            },
            "shipment": {
                "shipment_number": "SHIP-20482",
                "supplier_code": "SUP-017",
                "status": "delayed",
                "expected_delivery": "2026-09-16",
            },
        },
        "completed_agents": [
            *state.get("completed_agents", []),
            "data_agent",
        ],
    }

    mock_graph_agent.side_effect = lambda state: {
        **state,
        "graph_result": {
            "order_number": "ORD-10482",
            "product_sku": "SKU-0077",
            "warehouse": "Mumbai",
            "current_stock": 35,
            "reorder_point": 250,
            "supplier_code": "SUP-017",
            "supplier_reliability": 62.5,
        },
        "completed_agents": [
            *state.get("completed_agents", []),
            "graph_agent",
        ],
    }

    mock_rag_agent.side_effect = lambda state: {
        **state,
        "rag_result": [
            {
                "content": "Supplier delay policy",
                "source": "knowledge_base",
                "category": "supplier_sla",
                "file_name": "supplier_delay_policy.txt",
                "chunk_index": 0,
                "retrieval_score": 0.90,
                "rerank_score": 0.95,
            }
        ],
        "completed_agents": [
            *state.get("completed_agents", []),
            "rag_agent",
        ],
    }

    mock_recommendation_agent.side_effect = lambda state: {
        **state,
        "recommendation": {
            "order_number": "ORD-10482",
            "risk_level": "high",
            "recommendations": [
                "Escalate delayed shipment.",
                "Review supplier performance.",
                "Initiate replenishment.",
            ],
        },
        "completed_agents": [
            *state.get("completed_agents", []),
            "recommendation_agent",
        ],
    }

    graph = build_supply_chain_graph()

    initial_state = {
        "user_query": "Why is ORD-10482 delayed?",
        "completed_agents": [],
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["order_number"] == "ORD-10482"

    assert result["required_agents"] == [
        "data_agent",
        "graph_agent",
        "rag_agent",
    ]

    assert result["data_result"] is not None
    assert result["graph_result"] is not None
    assert result["rag_result"]

    assert result["recommendation"] is not None

    assert result["recommendation"]["risk_level"] == "high"

    assert result["completed_agents"] == [
        "data_agent",
        "graph_agent",
        "rag_agent",
        "recommendation_agent",
    ]

    mock_data_agent.assert_called_once()
    mock_graph_agent.assert_called_once()
    mock_rag_agent.assert_called_once()
    mock_recommendation_agent.assert_called_once()


@patch(
    "app.workflows.supply_chain_graph.recommendation_agent_node"
)
@patch(
    "app.workflows.supply_chain_graph.rag_agent_node"
)
def test_general_query_runs_rag_workflow(
    mock_rag_agent,
    mock_recommendation_agent,
):
    mock_rag_agent.side_effect = lambda state: {
        **state,
        "rag_result": [
            {
                "content": "Supplier delay policy",
                "source": "knowledge_base",
                "category": "supplier_sla",
                "file_name": "supplier_delay_policy.txt",
                "chunk_index": 0,
                "retrieval_score": 0.90,
                "rerank_score": 0.95,
            }
        ],
        "completed_agents": [
            *state.get("completed_agents", []),
            "rag_agent",
        ],
    }

    mock_recommendation_agent.side_effect = lambda state: {
        **state,
        "recommendation": {
            "risk_level": "low",
            "recommendations": [
                "Continue monitoring.",
            ],
        },
        "completed_agents": [
            *state.get("completed_agents", []),
            "recommendation_agent",
        ],
    }

    graph = build_supply_chain_graph()

    initial_state = {
        "user_query": "What is the supplier delay policy?",
        "completed_agents": [],
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["required_agents"] == ["rag_agent"]

    assert result["rag_result"]

    assert result["recommendation"] is not None

    assert result["recommendation"]["risk_level"] == "low"

    assert result["completed_agents"] == [
        "rag_agent",
        "recommendation_agent",
    ]

    mock_rag_agent.assert_called_once()
    mock_recommendation_agent.assert_called_once()