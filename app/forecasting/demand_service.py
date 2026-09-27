from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database_models import DemandHistory


def get_demand_history(
    db: Session,
    product_sku: str,
    warehouse: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 180,
) -> list[DemandHistory]:
    """
    Return historical daily demand for a product.

    Results are ordered oldest-to-newest so the same service can be
    consumed directly by forecasting algorithms.
    """

    statement = select(DemandHistory).where(
        DemandHistory.product_sku == product_sku,
    )

    if warehouse:
        statement = statement.where(
            DemandHistory.warehouse == warehouse,
        )

    if start_date:
        statement = statement.where(
            DemandHistory.demand_date >= start_date,
        )

    if end_date:
        statement = statement.where(
            DemandHistory.demand_date <= end_date,
        )

    statement = statement.order_by(
        DemandHistory.demand_date.desc(),
    ).limit(limit)

    rows = list(db.scalars(statement).all())
    rows.reverse()

    return rows
