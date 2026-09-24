from app.agents.state import AgentState


def test_agent_state_accepts_basic_query():
    state: AgentState = {
        "user_query": "Why is ORD-10482 delayed?"
    }

    assert state["user_query"] == "Why is ORD-10482 delayed?"


def test_agent_state_accepts_agent_results():
    state: AgentState = {
        "user_query": "Why is ORD-10482 delayed?",
        "order_number": "ORD-10482",
        "data_result": {
            "order_status": "delayed",
        },
        "rag_result": [
            {
                "source": "supplier_delay_policy.txt",
            }
        ],
        "graph_result": {
            "supplier": "SUP-017",
        },
        "completed_agents": [
            "data_agent",
            "rag_agent",
            "graph_agent",
        ],
        "errors": [],
    }

    assert state["order_number"] == "ORD-10482"
    assert state["data_result"]["order_status"] == "delayed"
    assert state["graph_result"]["supplier"] == "SUP-017"


def test_agent_state_supports_errors():
    state: AgentState = {
        "user_query": "Why is ORD-10482 delayed?",
        "errors": [
            "Graph Agent: Neo4j unavailable"
        ],
    }

    assert len(state["errors"]) == 1
    assert "Neo4j unavailable" in state["errors"][0]