from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database_models import Supplier


def get_suppliers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Supplier]:
    query = (
        select(Supplier)
        .order_by(Supplier.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query).all())


def get_supplier_by_code(
    db: Session,
    supplier_code: str,
) -> Supplier | None:
    query = select(Supplier).where(
        Supplier.supplier_code == supplier_code
    )

    return db.scalars(query).first()