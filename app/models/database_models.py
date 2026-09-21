from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    supplier_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    reliability_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    customer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    product_sku: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    warehouse: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    current_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reorder_point: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    shipment_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    order_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    supplier_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    expected_delivery: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )