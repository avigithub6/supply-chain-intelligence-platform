from langgraph.types import Command

from app.agents.state import AgentState
from app.workflows.supply_chain_graph import (
    route_after_approval,
    route_after_data,
    route_after_execution,
    route_after_graph,
    route_after_rag,
    route_after_recommendation,
    route_after_supervisor,
    route_after_workflow_action,
    supply_chain_graph,
)


def test_route_after_supervisor_with_order():
    state: AgentState = {
        "required_agents": [
            "data_agent",
            "graph_agent",
            "rag_agent",
        ]
    }

    assert route_after_supervisor(state) == "data_agent"


def test_route_after_supervisor_without_agents():
    state: AgentState = {
        "required_agents": []
    }

    assert route_after_supervisor(state) == "recommendation_agent"


def test_route_after_data_to_graph():
    state: AgentState = {
        "required_agents": [
            "data_agent",
            "graph_agent",
            "rag_agent",
        ]
    }

    assert route_after_data(state) == "graph_agent"


def test_route_after_data_to_rag():
    state: AgentState = {
        "required_agents": [
            "data_agent",
            "rag_agent",
        ]
    }

    assert route_after_data(state) == "rag_agent"


def test_route_after_data_to_recommendation():
    state: AgentState = {
        "required_agents": [
            "data_agent",
        ]
    }

    assert route_after_data(state) == "recommendation_agent"


def test_route_after_graph_to_rag():
    state: AgentState = {
        "required_agents": [
            "data_agent",
            "graph_agent",
            "rag_agent",
        ]
    }

    assert route_after_graph(state) == "rag_agent"


def test_route_after_graph_to_recommendation():
    state: AgentState = {
        "required_agents": [
            "data_agent",
            "graph_agent",
        ]
    }

    assert route_after_graph(state) == "recommendation_agent"


def test_route_after_rag():
    state: AgentState = {}

    assert route_after_rag(state) == "recommendation_agent"


def test_route_after_recommendation():
    state: AgentState = {}

    assert route_after_recommendation(state) == "workflow_action"


def test_route_after_workflow_action_with_pending_action():
    state: AgentState = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        }
    }

    assert route_after_workflow_action(state) == "human_approval"


def test_route_after_workflow_action_without_pending_action():
    state: AgentState = {
        "pending_action": None
    }

    assert route_after_workflow_action(state) == "end"


def test_route_after_approval_approved():
    state: AgentState = {
        "approval_status": "approved"
    }

    assert route_after_approval(state) == "execution_agent"


def test_route_after_approval_rejected():
    state: AgentState = {
        "approval_status": "rejected"
    }

    assert route_after_approval(state) == "execution_agent"


def test_route_after_approval_pending():
    state: AgentState = {
        "approval_status": "pending"
    }

    assert route_after_approval(state) == "end"


def test_route_after_execution():
    state: AgentState = {
        "execution_status": "executed"
    }

    assert route_after_execution(state) == "end"


def test_complete_order_investigation_workflow():
    config = {
        "configurable": {
            "thread_id": "test-order-10482-interrupt",
        }
    }

    # ---------------------------------------------------------
    # First invocation
    #
    # The workflow should pause at human approval.
    # ---------------------------------------------------------

    result = supply_chain_graph.invoke(
        {
            "user_query": "Why is order ORD-10482 delayed?",
            "completed_agents": [],
        },
        config=config,
    )

    assert "__interrupt__" in result

    interrupts = result["__interrupt__"]

    assert len(interrupts) == 1

    interrupt_value = interrupts[0].value

    assert interrupt_value["type"] == "human_approval"
    assert interrupt_value["action"] == "escalate_delayed_shipment"
    assert interrupt_value["order_number"] == "ORD-10482"

    assert (
        interrupt_value["requested_by"]
        == "recommendation_agent"
    )

    # ---------------------------------------------------------
    # Resume workflow with human approval
    # ---------------------------------------------------------

    resumed_result = supply_chain_graph.invoke(
        Command(
            resume={
                "decision": "approved",
                "reviewer": "operations_manager",
                "comment": (
                    "Approved delayed shipment escalation."
                ),
            }
        ),
        config=config,
    )

    # ---------------------------------------------------------
    # Verify workflow resumed successfully
    # ---------------------------------------------------------

    assert resumed_result["order_number"] == "ORD-10482"

    assert "data_agent" in resumed_result["completed_agents"]
    assert "graph_agent" in resumed_result["completed_agents"]
    assert "rag_agent" in resumed_result["completed_agents"]
    assert (
        "recommendation_agent"
        in resumed_result["completed_agents"]
    )
    assert (
        "workflow_action"
        in resumed_result["completed_agents"]
    )
    assert (
        "human_approval"
        in resumed_result["completed_agents"]
    )
    assert (
        "execution_agent"
        in resumed_result["completed_agents"]
    )

    # ---------------------------------------------------------
    # Verify human approval
    # ---------------------------------------------------------

    assert resumed_result["approval_status"] == "approved"

    assert (
        resumed_result["approved_by"]
        == "operations_manager"
    )

    assert (
        resumed_result["approval_comment"]
        == "Approved delayed shipment escalation."
    )

    # ---------------------------------------------------------
    # Verify execution
    # ---------------------------------------------------------

    assert resumed_result["execution_status"] == "executed"

    assert (
        resumed_result["execution_result"]["success"]
        is True
    )

    assert (
        resumed_result["execution_result"]["status"]
        == "executed"
    )

    assert (
        resumed_result["execution_result"]["action"]
        == "escalate_delayed_shipment"
    )


def test_general_query_runs_rag_workflow():
    result = supply_chain_graph.invoke(
        {
            "user_query": "What is the supplier delay policy?",
            "completed_agents": [],
        },
        config={
            "configurable": {
                "thread_id": "test-general-query-v2",
            }
        },
    )

    assert result["order_number"] is None

    assert "rag_agent" in result["completed_agents"]
    assert "recommendation_agent" in result["completed_agents"]
    assert "workflow_action" in result["completed_agents"]

    assert result["pending_action"] is None
    assert result["approval_status"] == "not_required"