from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database_models import Shipment


def get_shipments(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: str | None = None,
) -> list[Shipment]:
    query = select(Shipment)

    if status:
        query = query.where(
            Shipment.status == status
        )

    query = (
        query
        .order_by(Shipment.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query).all())


def get_shipment_by_number(
    db: Session,
    shipment_number: str,
) -> Shipment | None:
    query = select(Shipment).where(
        Shipment.shipment_number == shipment_number
    )

    return db.scalars(query).first()


def get_shipment_by_order_number(
    db: Session,
    order_number: str,
) -> Shipment | None:
    query = select(Shipment).where(
        Shipment.order_number == order_number
    )

    return db.scalars(query).first()