from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.schemas import ShipmentResponse
from app.services.shipment_service import (
    get_shipment_by_number,
    get_shipments,
)


router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"],
)


@router.get(
    "",
    response_model=list[ShipmentResponse],
)
def list_shipments(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    shipment_status: str | None = Query(
        default=None,
        alias="status",
    ),
    db: Session = Depends(get_db),
) -> list[ShipmentResponse]:
    shipments = get_shipments(
        db=db,
        skip=skip,
        limit=limit,
        status=shipment_status,
    )

    return shipments


@router.get(
    "/{shipment_number}",
    response_model=ShipmentResponse,
)
def retrieve_shipment(
    shipment_number: str,
    db: Session = Depends(get_db),
) -> ShipmentResponse:
    shipment = get_shipment_by_number(
        db=db,
        shipment_number=shipment_number,
    )

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Shipment '{shipment_number}' not found."
            ),
        )

    return shipment