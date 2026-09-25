from langgraph.types import interrupt

from app.agents.state import AgentState


def human_approval_checkpoint(state: AgentState) -> AgentState:
    """
    Pause the LangGraph workflow and request human approval.

    Workflow behavior:

    1. No pending action
       -> Approval is not required.

    2. Already approved
       -> Preserve approved state.

    3. Already rejected
       -> Preserve rejected state.

    4. Pending action
       -> Pause the LangGraph workflow using interrupt().

    5. When the graph resumes
       -> Read the human decision and continue.
    """

    pending_action = state.get("pending_action")

    # ---------------------------------------------------------
    # 1. No action requires approval
    # ---------------------------------------------------------

    if not pending_action:
        return {
            **state,
            "approval_status": "not_required",
            "approved_by": None,
            "approval_comment": None,
            "completed_agents": [
                *state.get("completed_agents", []),
                "human_approval",
            ],
        }

    # ---------------------------------------------------------
    # 2. Preserve already approved state
    # ---------------------------------------------------------

    if state.get("approval_status") == "approved":
        return {
            **state,
            "approval_status": "approved",
            "completed_agents": [
                *state.get("completed_agents", []),
                "human_approval",
            ],
        }

    # ---------------------------------------------------------
    # 3. Preserve already rejected state
    # ---------------------------------------------------------

    if state.get("approval_status") == "rejected":
        return {
            **state,
            "approval_status": "rejected",
            "completed_agents": [
                *state.get("completed_agents", []),
                "human_approval",
            ],
        }

    # ---------------------------------------------------------
    # 4. Pause workflow for human approval
    # ---------------------------------------------------------

    approval_request = {
        "type": "human_approval",
        "action": pending_action.get("action"),
        "order_number": pending_action.get("order_number"),
        "reason": pending_action.get("reason"),
        "requested_by": pending_action.get("requested_by"),
        "message": (
            "Human approval is required before "
            "this workflow action can be executed."
        ),
    }

    approval_response = interrupt(approval_request)

    # ---------------------------------------------------------
    # 5. Validate resumed human response
    # ---------------------------------------------------------

    if not isinstance(approval_response, dict):
        return {
            **state,
            "approval_status": "rejected",
            "approved_by": None,
            "approval_comment": (
                "Invalid approval response received."
            ),
            "errors": [
                *state.get("errors", []),
                "Human Approval Agent: invalid interrupt response.",
            ],
            "completed_agents": [
                *state.get("completed_agents", []),
                "human_approval",
            ],
        }

    decision = approval_response.get("decision")
    reviewer = approval_response.get("reviewer")
    comment = approval_response.get("comment", "")

    # ---------------------------------------------------------
    # 6. Approved
    # ---------------------------------------------------------

    if decision == "approved":
        return {
            **state,
            "approval_status": "approved",
            "approved_by": reviewer,
            "approval_comment": comment,
            "completed_agents": [
                *state.get("completed_agents", []),
                "human_approval",
            ],
        }

    # ---------------------------------------------------------
    # 7. Rejected
    # ---------------------------------------------------------

    if decision == "rejected":
        return {
            **state,
            "approval_status": "rejected",
            "approved_by": reviewer,
            "approval_comment": comment,
            "completed_agents": [
                *state.get("completed_agents", []),
                "human_approval",
            ],
        }

    # ---------------------------------------------------------
    # 8. Invalid decision
    # ---------------------------------------------------------

    return {
        **state,
        "approval_status": "rejected",
        "approved_by": reviewer,
        "approval_comment": (
            comment or "Invalid approval decision."
        ),
        "errors": [
            *state.get("errors", []),
            (
                "Human Approval Agent: "
                f"invalid decision '{decision}'."
            ),
        ],
        "completed_agents": [
            *state.get("completed_agents", []),
            "human_approval",
        ],
    }