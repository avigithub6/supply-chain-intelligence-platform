from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.schemas import OrderResponse
from app.services.order_service import (
    get_order_by_number,
    get_orders,
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get(
    "",
    response_model=list[OrderResponse],
)
def list_orders(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    order_status: str | None = Query(
        default=None,
        alias="status",
    ),
    db: Session = Depends(get_db),
) -> list[OrderResponse]:
    orders = get_orders(
        db=db,
        skip=skip,
        limit=limit,
        status=order_status,
    )

    return orders


@router.get(
    "/{order_number}",
    response_model=OrderResponse,
)
def retrieve_order(
    order_number: str,
    db: Session = Depends(get_db),
) -> OrderResponse:
    order = get_order_by_number(
        db=db,
        order_number=order_number,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order '{order_number}' not found.",
        )

    return order