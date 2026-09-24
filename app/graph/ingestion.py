from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.graph.neo4j_client import Neo4jClient, neo4j_client
from app.graph.queries import (
    MERGE_ORDERS_BATCH_QUERY,
    MERGE_ORDER_CONTAINS_BATCH_QUERY,
    MERGE_ORDER_SHIPMENT_BATCH_QUERY,
    MERGE_PRODUCTS_BATCH_QUERY,
    MERGE_SHIPMENT_SUPPLIER_BATCH_QUERY,
    MERGE_SHIPMENTS_BATCH_QUERY,
    MERGE_STORED_AT_BATCH_QUERY,
    MERGE_SUPPLIERS_BATCH_QUERY,
    MERGE_SUPPLIES_FROM_GRAPH_QUERY,
    MERGE_WAREHOUSES_BATCH_QUERY,
)
from app.models.database_models import (
    Inventory,
    Order,
    Shipment,
    Supplier,
)


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GraphIngestionResult:
    """Summary of PostgreSQL to Neo4j ingestion."""

    suppliers: int
    products: int
    warehouses: int
    orders: int
    shipments: int
    contains_relationships: int
    shipment_relationships: int
    supplier_relationships: int
    inventory_relationships: int


class GraphIngestionService:
    """Build the Neo4j supply-chain graph from PostgreSQL data."""

    def __init__(
        self,
        neo4j: Neo4jClient,
        batch_size: int = 500,
    ) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than zero.")

        self.neo4j = neo4j
        self.batch_size = batch_size

    def _execute_batches(
        self,
        query: str,
        rows: list[dict],
    ) -> None:
        """Execute a parameterized Neo4j query in batches."""

        for start in range(0, len(rows), self.batch_size):
            batch = rows[start : start + self.batch_size]

            self.neo4j.execute_query(
                query,
                {"rows": batch},
            )

    def ingest(self, db: Session) -> GraphIngestionResult:
        """Read PostgreSQL data and build the Neo4j graph."""

        logger.info("Starting PostgreSQL to Neo4j graph ingestion.")

        suppliers = list(
            db.scalars(
                select(Supplier).order_by(Supplier.id)
            ).all()
        )

        inventory = list(
            db.scalars(
                select(Inventory).order_by(Inventory.id)
            ).all()
        )

        orders = list(
            db.scalars(
                select(Order).order_by(Order.id)
            ).all()
        )

        shipments = list(
            db.scalars(
                select(Shipment).order_by(Shipment.id)
            ).all()
        )

        logger.info(
            "Loaded PostgreSQL records: suppliers=%d inventory=%d "
            "orders=%d shipments=%d",
            len(suppliers),
            len(inventory),
            len(orders),
            len(shipments),
        )

        supplier_rows = [
            {
                "supplier_code": supplier.supplier_code,
                "name": supplier.name,
                "location": supplier.location,
                "reliability_score": supplier.reliability_score,
            }
            for supplier in suppliers
        ]

        product_skus = {
            inventory_item.product_sku
            for inventory_item in inventory
        }

        product_skus.update(
            order.product_sku
            for order in orders
        )

        product_rows = [
            {
                "product_sku": product_sku,
            }
            for product_sku in sorted(product_skus)
        ]

        warehouse_names = {
            inventory_item.warehouse
            for inventory_item in inventory
        }

        warehouse_rows = [
            {
                "name": warehouse_name,
            }
            for warehouse_name in sorted(warehouse_names)
        ]

        order_rows = [
            {
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "product_sku": order.product_sku,
                "quantity": order.quantity,
                "status": order.status,
            }
            for order in orders
        ]

        shipment_rows = [
            {
                "shipment_number": shipment.shipment_number,
                "order_number": shipment.order_number,
                "supplier_code": shipment.supplier_code,
                "status": shipment.status,
                "expected_delivery": shipment.expected_delivery,
            }
            for shipment in shipments
        ]

        contains_rows = [
            {
                "order_number": order.order_number,
                "product_sku": order.product_sku,
            }
            for order in orders
        ]

        order_shipment_rows = [
            {
                "order_number": shipment.order_number,
                "shipment_number": shipment.shipment_number,
            }
            for shipment in shipments
        ]

        shipment_supplier_rows = [
            {
                "shipment_number": shipment.shipment_number,
                "supplier_code": shipment.supplier_code,
            }
            for shipment in shipments
        ]

        inventory_relationship_rows = [
            {
                "product_sku": inventory_item.product_sku,
                "warehouse": inventory_item.warehouse,
                "current_stock": inventory_item.current_stock,
                "reorder_point": inventory_item.reorder_point,
            }
            for inventory_item in inventory
        ]

        # --------------------------------------------------------
        # Phase 1: Create / update nodes
        # --------------------------------------------------------

        self._execute_batches(
            MERGE_SUPPLIERS_BATCH_QUERY,
            supplier_rows,
        )

        self._execute_batches(
            MERGE_PRODUCTS_BATCH_QUERY,
            product_rows,
        )

        self._execute_batches(
            MERGE_WAREHOUSES_BATCH_QUERY,
            warehouse_rows,
        )

        self._execute_batches(
            MERGE_ORDERS_BATCH_QUERY,
            order_rows,
        )

        self._execute_batches(
            MERGE_SHIPMENTS_BATCH_QUERY,
            shipment_rows,
        )

        # --------------------------------------------------------
        # Phase 2: Create relationships
        # --------------------------------------------------------

        self._execute_batches(
            MERGE_ORDER_CONTAINS_BATCH_QUERY,
            contains_rows,
        )

        self._execute_batches(
            MERGE_ORDER_SHIPMENT_BATCH_QUERY,
            order_shipment_rows,
        )

        self._execute_batches(
            MERGE_SHIPMENT_SUPPLIER_BATCH_QUERY,
            shipment_supplier_rows,
        )

        self._execute_batches(
            MERGE_STORED_AT_BATCH_QUERY,
            inventory_relationship_rows,
        )

        # --------------------------------------------------------
        # Phase 3: Derive Supplier -> Product relationship
        # --------------------------------------------------------

        self.neo4j.execute_query(
            MERGE_SUPPLIES_FROM_GRAPH_QUERY
        )

        result = GraphIngestionResult(
            suppliers=len(supplier_rows),
            products=len(product_rows),
            warehouses=len(warehouse_rows),
            orders=len(order_rows),
            shipments=len(shipment_rows),
            contains_relationships=len(contains_rows),
            shipment_relationships=len(order_shipment_rows),
            supplier_relationships=len(shipment_supplier_rows),
            inventory_relationships=len(inventory_relationship_rows),
        )

        logger.info(
            "Graph ingestion completed: %s",
            result,
        )

        return result


def run_graph_ingestion() -> GraphIngestionResult:
    """Run the complete PostgreSQL to Neo4j ingestion."""

    from app.database.session import SessionLocal

    neo4j_client.verify_connection()

    db = SessionLocal()

    try:
        service = GraphIngestionService(
            neo4j=neo4j_client,
            batch_size=500,
        )

        return service.ingest(db)

    finally:
        db.close()


if __name__ == "__main__":
    result = run_graph_ingestion()

    print("\nNeo4j graph ingestion completed.")
    print(f"Suppliers: {result.suppliers}")
    print(f"Products: {result.products}")
    print(f"Warehouses: {result.warehouses}")
    print(f"Orders: {result.orders}")
    print(f"Shipments: {result.shipments}")
    print(
        f"Order -> Product relationships: "
        f"{result.contains_relationships}"
    )
    print(
        f"Order -> Shipment relationships: "
        f"{result.shipment_relationships}"
    )
    print(
        f"Shipment -> Supplier relationships: "
        f"{result.supplier_relationships}"
    )
    print(
        f"Product -> Warehouse relationships: "
        f"{result.inventory_relationships}"
    )