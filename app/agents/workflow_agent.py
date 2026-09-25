from app.agents.state import AgentState


def workflow_action_node(state: AgentState) -> AgentState:
    """
    Convert the recommendation into a pending workflow action.

    No operational action is executed here.
    """

    recommendation = state.get("recommendation")

    if not recommendation:
        return {
            **state,
            "pending_action": None,
            "approval_status": "not_required",
            "completed_agents": [
                *state.get("completed_agents", []),
                "workflow_action",
            ],
        }

    recommendations = recommendation.get(
        "recommendations",
        [],
    )

    order_number = recommendation.get("order_number")

    if not recommendations or not order_number:
        return {
            **state,
            "pending_action": None,
            "approval_status": "not_required",
            "completed_agents": [
                *state.get("completed_agents", []),
                "workflow_action",
            ],
        }

    first_recommendation = recommendations[0]

    recommendation_text = first_recommendation.lower()

    if "supplier" in recommendation_text:
        action = "escalate_supplier"

    elif "shipment" in recommendation_text:
        action = "escalate_delayed_shipment"

    elif "replenishment" in recommendation_text:
        action = "initiate_replenishment"

    else:
        return {
            **state,
            "pending_action": None,
            "approval_status": "not_required",
            "completed_agents": [
                *state.get("completed_agents", []),
                "workflow_action",
            ],
        }

    pending_action = {
        "action": action,
        "order_number": order_number,
        "reason": first_recommendation,
        "requested_by": "recommendation_agent",
    }

    return {
        **state,
        "pending_action": pending_action,
        "approval_status": "pending",
        "completed_agents": [
            *state.get("completed_agents", []),
            "workflow_action",
        ],
    }