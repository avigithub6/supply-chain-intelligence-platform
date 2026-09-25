from app.database.session import SessionLocal
from app.models.schemas import InventoryResponse
from app.models.tool_schemas import (
    GetInventoryToolInput,
    InventoryToolOutput,
)
from app.services.inventory_service import get_inventory_by_sku


def get_inventory_tool(
    request: GetInventoryToolInput,
) -> InventoryToolOutput:
    """
    Retrieve inventory information from PostgreSQL
    using the existing inventory service layer.

    This is a read-only tool.
    """

    db = SessionLocal()

    try:
        inventory = get_inventory_by_sku(
            db=db,
            product_sku=request.product_sku,
        )

        if inventory is None:
            return InventoryToolOutput(
                success=False,
                error=(
                    "Inventory not found for SKU: "
                    f"{request.product_sku}"
                ),
            )

        return InventoryToolOutput(
            success=True,
            inventory=InventoryResponse.model_validate(
                inventory
            ),
        )

    except Exception as exc:
        return InventoryToolOutput(
            success=False,
            error=f"Get Inventory Tool error: {exc}",
        )

    finally:
        db.close()