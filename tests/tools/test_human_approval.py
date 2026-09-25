from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.agents.approval_agent import human_approval_checkpoint
from app.models.tool_schemas import HumanApprovalRequest
from app.tools.workflow_tools import process_human_approval


def test_human_approval_request_is_approved():
    request = HumanApprovalRequest(
        action="escalate_supplier",
        order_number="ord-10482",
        decision="approved",
        reviewer="operations_manager",
        comment="Approved for supplier escalation.",
    )

    result = process_human_approval(request)

    assert result.success is True
    assert result.decision == "approved"
    assert result.order_number == "ORD-10482"
    assert result.reviewer == "operations_manager"


def test_human_approval_request_is_rejected():
    request = HumanApprovalRequest(
        action="escalate_supplier",
        order_number="ORD-10482",
        decision="rejected",
        reviewer="operations_manager",
        comment="Do not escalate at this time.",
    )

    result = process_human_approval(request)

    assert result.success is True
    assert result.decision == "rejected"
    assert result.order_number == "ORD-10482"


def test_approval_normalizes_order_number():
    request = HumanApprovalRequest(
        action="escalate_supplier",
        order_number=" ord-10482 ",
        decision="approved",
        reviewer=" manager ",
        comment=" approved ",
    )

    assert request.order_number == "ORD-10482"
    assert request.reviewer == "manager"
    assert request.comment == "approved"


def test_invalid_approval_decision_is_rejected():
    with pytest.raises(ValidationError):
        HumanApprovalRequest(
            action="escalate_supplier",
            order_number="ORD-10482",
            decision="invalid",
            reviewer="operations_manager",
        )


def test_checkpoint_without_action():
    state = {
        "pending_action": None,
        "approval_status": "pending",
        "completed_agents": [],
    }

    result = human_approval_checkpoint(state)

    assert result["approval_status"] == "not_required"
    assert result["approved_by"] is None
    assert result["approval_comment"] is None
    assert result["completed_agents"] == [
        "human_approval",
    ]


def test_checkpoint_waits_for_approval():
    state = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        },
        "approval_status": "pending",
        "completed_agents": [],
    }

    with patch(
        "app.agents.approval_agent.interrupt",
        return_value={
            "decision": "approved",
            "reviewer": "operations_manager",
            "comment": "Approved.",
        },
    ) as mocked_interrupt:
        result = human_approval_checkpoint(state)

    mocked_interrupt.assert_called_once()

    approval_request = mocked_interrupt.call_args.args[0]

    assert approval_request["type"] == "human_approval"
    assert approval_request["action"] == "escalate_supplier"
    assert approval_request["order_number"] == "ORD-10482"

    assert result["approval_status"] == "approved"
    assert result["approved_by"] == "operations_manager"
    assert result["approval_comment"] == "Approved."
    assert result["completed_agents"] == [
        "human_approval",
    ]


def test_checkpoint_accepts_approval():
    state = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        },
        "approval_status": "pending",
        "completed_agents": [],
    }

    with patch(
        "app.agents.approval_agent.interrupt",
        return_value={
            "decision": "approved",
            "reviewer": "operations_manager",
            "comment": "Approved for execution.",
        },
    ):
        result = human_approval_checkpoint(state)

    assert result["approval_status"] == "approved"
    assert result["approved_by"] == "operations_manager"
    assert result["approval_comment"] == "Approved for execution."


def test_checkpoint_preserves_rejection():
    state = {
        "pending_action": {
            "action": "escalate_supplier",
            "order_number": "ORD-10482",
            "reason": "Supplier reliability is below threshold.",
            "requested_by": "recommendation_agent",
        },
        "approval_status": "rejected",
        "approved_by": "operations_manager",
        "approval_comment": "Not approved.",
        "completed_agents": [],
    }

    result = human_approval_checkpoint(state)

    assert result["approval_status"] == "rejected"
    assert result["approved_by"] == "operations_manager"
    assert result["approval_comment"] == "Not approved."
    assert result["completed_agents"] == [
        "human_approval",
    ]