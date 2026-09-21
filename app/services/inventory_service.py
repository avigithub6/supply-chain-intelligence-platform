from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database_models import Inventory


def get_inventory(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    warehouse: str | None = None,
    low_stock: bool = False,
) -> list[Inventory]:
    query = select(Inventory)

    if warehouse:
        query = query.where(
            Inventory.warehouse == warehouse
        )

    if low_stock:
        query = query.where(
            Inventory.current_stock <= Inventory.reorder_point
        )

    query = (
        query
        .order_by(Inventory.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(query).all())


def get_inventory_by_sku(
    db: Session,
    product_sku: str,
) -> Inventory | None:
    query = select(Inventory).where(
        Inventory.product_sku == product_sku
    )

    return db.scalars(query).first()