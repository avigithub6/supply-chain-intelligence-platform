from app.database.session import SessionLocal
from app.models.schemas import ShipmentResponse
from app.models.tool_schemas import (
    GetShipmentToolInput,
    ShipmentToolOutput,
)
from app.services.shipment_service import get_shipment_by_number


def get_shipment_tool(
    request: GetShipmentToolInput,
) -> ShipmentToolOutput:
    """
    Retrieve shipment information from PostgreSQL
    using the existing shipment service layer.

    This is a read-only tool.
    """

    db = SessionLocal()

    try:
        shipment = get_shipment_by_number(
            db=db,
            shipment_number=request.shipment_number,
        )

        if shipment is None:
            return ShipmentToolOutput(
                success=False,
                error=(
                    "Shipment not found: "
                    f"{request.shipment_number}"
                ),
            )

        return ShipmentToolOutput(
            success=True,
            shipment=ShipmentResponse.model_validate(
                shipment
            ),
        )

    except Exception as exc:
        return ShipmentToolOutput(
            success=False,
            error=f"Get Shipment Tool error: {exc}",
        )

    finally:
        db.close()