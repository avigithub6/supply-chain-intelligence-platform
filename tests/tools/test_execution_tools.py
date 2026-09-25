import pytest
from pydantic import ValidationError

from app.models.tool_schemas import ExecuteWorkflowActionRequest
from app.tools.execution_tools import execute_workflow_action


def test_execute_workflow_action_success():
    request = ExecuteWorkflowActionRequest(
        action="escalate_supplier",
        order_number=" ord-10482 ",
        reason="Supplier reliability is below threshold.",
        executed_by="operations_manager",
    )

    result = execute_workflow_action(request)

    assert result.success is True
    assert result.status == "executed"
    assert result.action == "escalate_supplier"
    assert result.order_number == "ORD-10482"
    assert result.executed_by == "operations_manager"


def test_execute_delayed_shipment_action():
    request = ExecuteWorkflowActionRequest(
        action="escalate_delayed_shipment",
        order_number="ORD-10482",
        reason="Shipment is delayed.",
        executed_by="operations_manager",
    )

    result = execute_workflow_action(request)

    assert result.success is True
    assert result.status == "executed"
    assert result.action == "escalate_delayed_shipment"


def test_execute_replenishment_action():
    request = ExecuteWorkflowActionRequest(
        action="initiate_replenishment",
        order_number="ORD-10482",
        reason="Inventory is below reorder point.",
        executed_by="operations_manager",
    )

    result = execute_workflow_action(request)

    assert result.success is True
    assert result.status == "executed"
    assert result.action == "initiate_replenishment"


def test_execution_request_rejects_empty_reason():
    with pytest.raises(ValidationError):
        ExecuteWorkflowActionRequest(
            action="escalate_supplier",
            order_number="ORD-10482",
            reason="   ",
            executed_by="operations_manager",
        )


def test_execution_request_rejects_empty_executor():
    with pytest.raises(ValidationError):
        ExecuteWorkflowActionRequest(
            action="escalate_supplier",
            order_number="ORD-10482",
            reason="Supplier escalation required.",
            executed_by="   ",
        )