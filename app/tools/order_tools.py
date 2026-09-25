from app.models.schemas import OrderResponse
from app.models.tool_schemas import (
    GetOrderToolInput,
    OrderToolOutput,
)
from app.database.session import SessionLocal
from app.services.order_service import get_order_by_number


def get_order_tool(request: GetOrderToolInput) -> OrderToolOutput:
    """
    Retrieve an order from PostgreSQL using the existing
    order service layer.

    This is a read-only tool.
    """

    db = SessionLocal()

    try:
        order = get_order_by_number(
            db=db,
            order_number=request.order_number,
        )

        if order is None:
            return OrderToolOutput(
                success=False,
                error=f"Order not found: {request.order_number}",
            )

        return OrderToolOutput(
            success=True,
            order=OrderResponse.model_validate(order),
        )

    except Exception as exc:
        return OrderToolOutput(
            success=False,
            error=f"Get Order Tool error: {exc}",
        )

    finally:
        db.close()