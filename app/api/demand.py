from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.forecasting.demand_service import get_demand_history
from app.models.schemas import DemandHistoryResponse


router = APIRouter(
    prefix="/demand",
    tags=["Demand History"],
)


@router.get(
    "/history",
    response_model=list[DemandHistoryResponse],
)
def demand_history(
    product_sku: str = Query(
        ...,
        min_length=1,
        max_length=50,
    ),
    warehouse: str | None = Query(
        default=None,
        max_length=100,
    ),
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = Query(
        default=180,
        ge=1,
        le=365,
    ),
    db: Session = Depends(get_db),
) -> list[DemandHistoryResponse]:
    return get_demand_history(
        db=db,
        product_sku=product_sku,
        warehouse=warehouse,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )
