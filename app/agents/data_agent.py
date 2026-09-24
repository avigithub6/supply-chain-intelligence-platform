from sqlalchemy.orm import Session

from app.agents.state import AgentState
from app.database.session import SessionLocal
from app.services.order_service import get_order_by_number
from app.services.shipment_service import get_shipment_by_order_number


def data_agent_node(state: AgentState) -> AgentState:
    """
    Retrieve factual order and shipment information
    from PostgreSQL using the existing service layer.
    """

    order_number = state.get("order_number")

    if not order_number:
        return {
            **state,
            "data_result": None,
            "completed_agents": [
                *state.get("completed_agents", []),
                "data_agent",
            ],
        }

    db: Session = SessionLocal()

    try:
        order = get_order_by_number(
            db=db,
            order_number=order_number,
        )

        if order is None:
            return {
                **state,
                "data_result": None,
                "completed_agents": [
                    *state.get("completed_agents", []),
                    "data_agent",
                ],
                "errors": [
                    *state.get("errors", []),
                    f"Order not found: {order_number}",
                ],
            }

        shipment = get_shipment_by_order_number(
            db=db,
            order_number=order_number,
        )

        data_result = {
            "order": {
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "product_sku": order.product_sku,
                "quantity": order.quantity,
                "status": order.status,
            },
            "shipment": None,
        }

        if shipment:
            data_result["shipment"] = {
                "shipment_number": shipment.shipment_number,
                "order_number": shipment.order_number,
                "supplier_code": shipment.supplier_code,
                "status": shipment.status,
                "expected_delivery": shipment.expected_delivery.isoformat(),
            }

        return {
            **state,
            "data_result": data_result,
            "completed_agents": [
                *state.get("completed_agents", []),
                "data_agent",
            ],
        }

    except Exception as exc:
        return {
            **state,
            "data_result": None,
            "completed_agents": [
                *state.get("completed_agents", []),
                "data_agent",
            ],
            "errors": [
                *state.get("errors", []),
                f"Data Agent error: {exc}",
            ],
        }

    finally:
        db.close()