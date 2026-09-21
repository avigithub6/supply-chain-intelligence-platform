from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database_models import Order


def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: str | None = None,
) -> list[Order]:
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    query = (
        query
        .order_by(Order.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query).all())


def get_order_by_number(
    db: Session,
    order_number: str,
) -> Order | None:
    query = select(Order).where(
        Order.order_number == order_number
    )

    return db.scalars(query).first()