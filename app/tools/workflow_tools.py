from app.models.tool_schemas import (
    HumanApprovalRequest,
    HumanApprovalResponse,
    WorkflowActionRequest,
    WorkflowActionResponse,
)


def request_workflow_action(
    request: WorkflowActionRequest,
) -> WorkflowActionResponse:
    """
    Request an operational workflow action.

    The action is NOT executed here.

    It remains pending until a human reviewer
    explicitly approves it.
    """

    return WorkflowActionResponse(
        success=True,
        action=request.action,
        order_number=request.order_number,
        status="pending_approval",
        reason=request.reason,
        requested_by=request.requested_by,
        message=(
            f"Workflow action '{request.action}' requested "
            f"for {request.order_number}. "
            "Human approval is required before execution."
        ),
    )


def process_human_approval(
    request: HumanApprovalRequest,
) -> HumanApprovalResponse:
    """
    Process a human approval or rejection.

    This function only records the decision.
    It does NOT execute the operational action.
    """

    if request.decision == "approved":
        message = (
            f"Action '{request.action}' approved for "
            f"{request.order_number} by {request.reviewer}. "
            "The action is now eligible for execution."
        )

    else:
        message = (
            f"Action '{request.action}' rejected for "
            f"{request.order_number} by {request.reviewer}. "
            "No operational action will be executed."
        )

    return HumanApprovalResponse(
        success=True,
        action=request.action,
        order_number=request.order_number,
        decision=request.decision,
        reviewer=request.reviewer,
        comment=request.comment,
        message=message,
    )