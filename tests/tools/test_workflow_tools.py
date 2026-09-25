import pytest
from pydantic import ValidationError

from app.models.tool_schemas import WorkflowActionRequest
from app.tools.workflow_tools import request_workflow_action


def test_request_workflow_action_success():
    request = WorkflowActionRequest(
        action="escalate_supplier",
        order_number="ord-10482",
        reason="Supplier reliability is below the required threshold.",
        requested_by="recommendation_agent",
    )

    result = request_workflow_action(request)

    assert result.success is True
    assert result.action == "escalate_supplier"
    assert result.order_number == "ORD-10482"
    assert result.status == "pending_approval"
    assert result.requested_by == "recommendation_agent"
    assert result.error is None


def test_request_workflow_action_replenishment():
    request = WorkflowActionRequest(
        action="initiate_replenishment",
        order_number="ORD-10482",
        reason="Current inventory is below reorder point.",
        requested_by="recommendation_agent",
    )

    result = request_workflow_action(request)

    assert result.success is True
    assert result.action == "initiate_replenishment"
    assert result.status == "pending_approval"


def test_request_workflow_action_delayed_shipment():
    request = WorkflowActionRequest(
        action="escalate_delayed_shipment",
        order_number="ORD-10482",
        reason="Shipment is delayed.",
        requested_by="recommendation_agent",
    )

    result = request_workflow_action(request)

    assert result.success is True
    assert result.action == "escalate_delayed_shipment"
    assert result.status == "pending_approval"


def test_workflow_request_normalizes_order_number():
    request = WorkflowActionRequest(
        action="escalate_supplier",
        order_number="  ord-10482  ",
        reason="Supplier performance requires review.",
        requested_by="recommendation_agent",
    )

    assert request.order_number == "ORD-10482"


def test_workflow_request_rejects_invalid_action():
    with pytest.raises(ValidationError):
        WorkflowActionRequest(
            action="delete_supplier",
            order_number="ORD-10482",
            reason="Invalid action test.",
            requested_by="recommendation_agent",
        )


def test_workflow_request_requires_reason():
    with pytest.raises(ValidationError):
        WorkflowActionRequest(
            action="escalate_supplier",
            order_number="ORD-10482",
            reason="",
            requested_by="recommendation_agent",
        )