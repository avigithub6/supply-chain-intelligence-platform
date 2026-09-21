from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database.connection import engine
from app.models.database_models import Inventory, Order, Shipment, Supplier


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

RANDOM_SEED = 42

random.seed(RANDOM_SEED)


WAREHOUSES = [
    "Delhi-NCR",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Pune",
]

CITIES = [
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Ahmedabad",
    "Kolkata",
    "Jaipur",
    "Lucknow",
]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Automotive",
    "Industrial",
    "Packaging",
    "Consumer Goods",
]

ORDER_STATUSES = [
    "processing",
    "confirmed",
    "in_transit",
    "delayed",
    "delivered",
]

SHIPMENT_STATUSES = [
    "preparing",
    "in_transit",
    "delayed",
    "delivered",
]


def write_csv(
    filename: str,
    rows: list[dict],
) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = DATA_DIR / filename

    with file_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(rows)


def generate_suppliers(count: int = 50) -> list[dict]:
    suppliers = []

    for index in range(1, count + 1):
        supplier_code = f"SUP-{index:03d}"

        suppliers.append(
            {
                "supplier_code": supplier_code,
                "name": f"Supplier {index:03d} Industries",
                "location": random.choice(CITIES),
                "reliability_score": round(
                    random.uniform(55, 99),
                    2,
                ),
            }
        )

    return suppliers


def generate_inventory(count: int = 150) -> list[dict]:
    inventory = []

    for index in range(1, count + 1):
        product_sku = f"SKU-{index:04d}"

        reorder_point = random.randint(50, 500)

        current_stock = random.randint(
            max(0, reorder_point - 250),
            reorder_point + 1000,
        )

        inventory.append(
            {
                "product_sku": product_sku,
                "warehouse": random.choice(WAREHOUSES),
                "current_stock": current_stock,
                "reorder_point": reorder_point,
            }
        )

    return inventory


def generate_orders(
    inventory: list[dict],
    count: int = 1000,
) -> list[dict]:
    orders = []

    for index in range(1, count + 1):
        order_number = f"ORD-{10000 + index}"

        inventory_item = random.choice(inventory)

        quantity = random.randint(10, 500)

        status = random.choices(
            ORDER_STATUSES,
            weights=[15, 25, 20, 20, 20],
            k=1,
        )[0]

        orders.append(
            {
                "order_number": order_number,
                "customer_name": f"Customer {index:04d}",
                "product_sku": inventory_item["product_sku"],
                "quantity": quantity,
                "status": status,
            }
        )

    return orders


def generate_shipments(
    orders: list[dict],
    suppliers: list[dict],
) -> list[dict]:
    shipments = []

    for index, order in enumerate(orders, start=1):
        supplier = random.choice(suppliers)

        order_number = order["order_number"]

        status = random.choices(
            SHIPMENT_STATUSES,
            weights=[10, 35, 20, 35],
            k=1,
        )[0]

        expected_delivery = date.today() + timedelta(
            days=random.randint(-15, 30)
        )

        shipments.append(
            {
                "shipment_number": f"SHIP-{20000 + index}",
                "order_number": order_number,
                "supplier_code": supplier["supplier_code"],
                "status": status,
                "expected_delivery": expected_delivery.isoformat(),
            }
        )

    return shipments


def apply_known_scenario(
    suppliers: list[dict],
    inventory: list[dict],
    orders: list[dict],
    shipments: list[dict],
) -> None:
    """
    Creates one deterministic investigation scenario
    for future AI-agent testing.
    """

    target_order = next(
        order
        for order in orders
        if order["order_number"] == "ORD-10482"
    )

    target_supplier = suppliers[16]

    target_inventory = next(
        item
        for item in inventory
        if item["product_sku"] == target_order["product_sku"]
    )

    target_supplier["reliability_score"] = 62.5

    target_inventory["current_stock"] = 35
    target_inventory["reorder_point"] = 250

    target_order["status"] = "delayed"

    target_shipment = next(
        shipment
        for shipment in shipments
        if shipment["order_number"] == "ORD-10482"
    )

    target_shipment["supplier_code"] = (
        target_supplier["supplier_code"]
    )

    target_shipment["status"] = "delayed"

    target_shipment["expected_delivery"] = (
        date.today() - timedelta(days=5)
    ).isoformat()


def insert_data(
    suppliers: list[dict],
    inventory: list[dict],
    orders: list[dict],
    shipments: list[dict],
) -> None:
    with Session(engine) as session:
        session.execute(delete(Shipment))
        session.execute(delete(Order))
        session.execute(delete(Inventory))
        session.execute(delete(Supplier))

        session.commit()

        supplier_objects = [
            Supplier(**supplier)
            for supplier in suppliers
        ]

        inventory_objects = [
            Inventory(**item)
            for item in inventory
        ]

        order_objects = [
            Order(**order)
            for order in orders
        ]

        shipment_objects = [
            Shipment(
                shipment_number=shipment["shipment_number"],
                order_number=shipment["order_number"],
                supplier_code=shipment["supplier_code"],
                status=shipment["status"],
                expected_delivery=date.fromisoformat(
                    shipment["expected_delivery"]
                ),
            )
            for shipment in shipments
        ]

        session.add_all(supplier_objects)
        session.add_all(inventory_objects)
        session.add_all(order_objects)
        session.add_all(shipment_objects)

        session.commit()


def main() -> None:
    print("Generating supply-chain dataset...")

    suppliers = generate_suppliers()
    inventory = generate_inventory()
    orders = generate_orders(inventory)
    shipments = generate_shipments(
        orders,
        suppliers,
    )

    apply_known_scenario(
        suppliers,
        inventory,
        orders,
        shipments,
    )

    write_csv(
        "suppliers.csv",
        suppliers,
    )

    write_csv(
        "inventory.csv",
        inventory,
    )

    write_csv(
        "orders.csv",
        orders,
    )

    write_csv(
        "shipments.csv",
        shipments,
    )

    insert_data(
        suppliers,
        inventory,
        orders,
        shipments,
    )

    print()
    print("Dataset generated successfully.")
    print(f"Suppliers : {len(suppliers)}")
    print(f"Inventory : {len(inventory)}")
    print(f"Orders    : {len(orders)}")
    print(f"Shipments : {len(shipments)}")
    print()
    print(f"CSV files created in: {DATA_DIR}")
    print("Database tables populated successfully.")


if __name__ == "__main__":
    main()