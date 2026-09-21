from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.schemas import InventoryResponse
from app.services.inventory_service import (
    get_inventory,
    get_inventory_by_sku,
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.get(
    "",
    response_model=list[InventoryResponse],
)
def list_inventory(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    warehouse: str | None = Query(
        default=None,
    ),
    low_stock: bool = Query(
        default=False,
    ),
    db: Session = Depends(get_db),
) -> list[InventoryResponse]:
    inventory = get_inventory(
        db=db,
        skip=skip,
        limit=limit,
        warehouse=warehouse,
        low_stock=low_stock,
    )

    return inventory


@router.get(
    "/{product_sku}",
    response_model=InventoryResponse,
)
def retrieve_inventory(
    product_sku: str,
    db: Session = Depends(get_db),
) -> InventoryResponse:
    inventory = get_inventory_by_sku(
        db=db,
        product_sku=product_sku,
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory for '{product_sku}' not found.",
        )

    return inventory