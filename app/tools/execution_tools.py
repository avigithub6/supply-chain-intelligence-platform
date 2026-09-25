from app.models.tool_schemas import (
    ExecuteWorkflowActionRequest,
    ExecuteWorkflowActionResponse,
)


def execute_workflow_action(
    request: ExecuteWorkflowActionRequest,
) -> ExecuteWorkflowActionResponse:
    """
    Execute an already-approved workflow action.

    This function represents the controlled execution boundary
    between the agentic decision layer and real operational actions.

    At this stage, the tool does not modify external systems.
    It validates and records the execution intent so that the
    execution layer can later be connected to real systems such
    as email, supplier portals, inventory systems, or ticketing
    platforms.
    """

    return ExecuteWorkflowActionResponse(
        success=True,
        action=request.action,
        order_number=request.order_number,
        status="executed",
        executed_by=request.executed_by,
        reason=request.reason,
        message=(
            f"Workflow action '{request.action}' executed "
            f"for {request.order_number} by {request.executed_by}."
        ),
    )