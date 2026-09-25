from app.database.session import SessionLocal
from app.models.schemas import SupplierResponse
from app.models.tool_schemas import (
    GetSupplierToolInput,
    SupplierToolOutput,
)
from app.services.supplier_service import get_supplier_by_code


def get_supplier_tool(
    request: GetSupplierToolInput,
) -> SupplierToolOutput:
    """
    Retrieve supplier information from PostgreSQL
    using the existing supplier service layer.

    This is a read-only tool.
    """

    db = SessionLocal()

    try:
        supplier = get_supplier_by_code(
            db=db,
            supplier_code=request.supplier_code,
        )

        if supplier is None:
            return SupplierToolOutput(
                success=False,
                error=(
                    "Supplier not found: "
                    f"{request.supplier_code}"
                ),
            )

        return SupplierToolOutput(
            success=True,
            supplier=SupplierResponse.model_validate(
                supplier
            ),
        )

    except Exception as exc:
        return SupplierToolOutput(
            success=False,
            error=f"Get Supplier Tool error: {exc}",
        )

    finally:
        db.close()