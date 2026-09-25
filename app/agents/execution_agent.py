from app.agents.state import AgentState
from app.models.tool_schemas import ExecuteWorkflowActionRequest
from app.tools.execution_tools import execute_workflow_action


def execution_agent_node(state: AgentState) -> AgentState:
    """
    Execute a workflow action only after human approval.

    Execution rules:

    1. No pending action
       -> No execution required.

    2. Action rejected by human
       -> Skip execution.

    3. Action still pending approval
       -> Wait for approval.

    4. Action approved
       -> Execute the workflow action.

    5. Execution error
       -> Capture the error in AgentState.
    """

    pending_action = state.get("pending_action")

    # ---------------------------------------------------------
    # No action requires execution
    # ---------------------------------------------------------

    if not pending_action:
        return {
            **state,
            "execution_status": "not_required",
            "execution_result": None,
            "completed_agents": [
                *state.get("completed_agents", []),
                "execution_agent",
            ],
        }

    # ---------------------------------------------------------
    # Read current human approval status
    # ---------------------------------------------------------

    approval_status = state.get(
        "approval_status",
        "not_required",
    )

    # ---------------------------------------------------------
    # Human rejected the action
    # ---------------------------------------------------------

    if approval_status == "rejected":
        return {
            **state,
            "execution_status": "skipped",
            "execution_result": {
                "success": False,
                "status": "skipped",
                "reason": "Human approval was rejected.",
            },
            "completed_agents": [
                *state.get("completed_agents", []),
                "execution_agent",
            ],
        }

    # ---------------------------------------------------------
    # Human approval is still pending
    # ---------------------------------------------------------

    if approval_status != "approved":
        return {
            **state,
            "execution_status": "pending",
            "execution_result": {
                "success": False,
                "status": "pending",
                "reason": (
                    "Human approval is required before execution."
                ),
            },
            "completed_agents": [
                *state.get("completed_agents", []),
                "execution_agent",
            ],
        }

    # ---------------------------------------------------------
    # Human approved the action
    # ---------------------------------------------------------

    try:
        request = ExecuteWorkflowActionRequest(
            action=pending_action["action"],
            order_number=pending_action["order_number"],
            reason=pending_action["reason"],
            executed_by=(
                state.get("approved_by")
                or "human_reviewer"
            ),
        )

        result = execute_workflow_action(request)

        return {
            **state,
            "execution_status": "executed",
            "execution_result": result.model_dump(),
            "completed_agents": [
                *state.get("completed_agents", []),
                "execution_agent",
            ],
        }

    # ---------------------------------------------------------
    # Execution failure
    # ---------------------------------------------------------

    except Exception as exc:
        return {
            **state,
            "execution_status": "failed",
            "execution_result": {
                "success": False,
                "status": "failed",
                "reason": str(exc),
            },
            "errors": [
                *state.get("errors", []),
                f"Execution Agent error: {exc}",
            ],
            "completed_agents": [
                *state.get("completed_agents", []),
                "execution_agent",
            ],
        }