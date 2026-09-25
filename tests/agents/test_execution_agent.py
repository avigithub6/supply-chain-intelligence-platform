from app.agents.execution_agent import execution_agent_node


def test_execution_agent_executes_approved_action():
    state = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        },
        "approval_status": "approved",
        "approved_by": "operations_manager",
        "completed_agents": [
            "workflow_action",
            "human_approval",
        ],
    }

    result = execution_agent_node(state)

    assert result["execution_status"] == "executed"
    assert result["execution_result"]["success"] is True
    assert result["execution_result"]["status"] == "executed"
    assert result["execution_result"]["action"] == "escalate_supplier"

    assert result["completed_agents"] == [
        "workflow_action",
        "human_approval",
        "execution_agent",
    ]


def test_execution_agent_skips_rejected_action():
    state = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        },
        "approval_status": "rejected",
        "approved_by": "operations_manager",
        "completed_agents": [
            "workflow_action",
            "human_approval",
        ],
    }

    result = execution_agent_node(state)

    assert result["execution_status"] == "skipped"
    assert result["execution_result"]["success"] is False
    assert result["execution_result"]["status"] == "skipped"

    assert result["completed_agents"] == [
        "workflow_action",
        "human_approval",
        "execution_agent",
    ]


def test_execution_agent_waits_for_pending_approval():
    state = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        },
        "approval_status": "pending",
        "completed_agents": [
            "workflow_action",
        ],
    }

    result = execution_agent_node(state)

    assert result["execution_status"] == "pending"
    assert result["execution_result"]["success"] is False
    assert result["execution_result"]["status"] == "pending"

    assert result["completed_agents"] == [
        "workflow_action",
        "execution_agent",
    ]


def test_execution_agent_requires_no_action_when_none_pending():
    state = {
        "pending_action": None,
        "approval_status": "not_required",
        "completed_agents": [
            "workflow_action",
        ],
    }

    result = execution_agent_node(state)

    assert result["execution_status"] == "not_required"
    assert result["execution_result"] is None

    assert result["completed_agents"] == [
        "workflow_action",
        "execution_agent",
    ]