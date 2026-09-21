from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.schemas import SupplierResponse
from app.services.supplier_service import (
    get_supplier_by_code,
    get_suppliers,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.get(
    "",
    response_model=list[SupplierResponse],
)
def list_suppliers(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
) -> list[SupplierResponse]:
    suppliers = get_suppliers(
        db=db,
        skip=skip,
        limit=limit,
    )

    return suppliers


@router.get(
    "/{supplier_code}",
    response_model=SupplierResponse,
)
def retrieve_supplier(
    supplier_code: str,
    db: Session = Depends(get_db),
) -> SupplierResponse:
    supplier = get_supplier_by_code(
        db=db,
        supplier_code=supplier_code,
    )

    if supplier is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier '{supplier_code}' not found.",
        )

    return supplier