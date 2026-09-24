CREATE_CONSTRAINTS_QUERY = """
CREATE CONSTRAINT supplier_code_unique IF NOT EXISTS
FOR (supplier:Supplier)
REQUIRE supplier.supplier_code IS UNIQUE
"""


CREATE_PRODUCT_CONSTRAINT_QUERY = """
CREATE CONSTRAINT product_sku_unique IF NOT EXISTS
FOR (product:Product)
REQUIRE product.product_sku IS UNIQUE
"""


CREATE_WAREHOUSE_CONSTRAINT_QUERY = """
CREATE CONSTRAINT warehouse_name_unique IF NOT EXISTS
FOR (warehouse:Warehouse)
REQUIRE warehouse.name IS UNIQUE
"""


CREATE_ORDER_CONSTRAINT_QUERY = """
CREATE CONSTRAINT order_number_unique IF NOT EXISTS
FOR (order:Order)
REQUIRE order.order_number IS UNIQUE
"""


CREATE_SHIPMENT_CONSTRAINT_QUERY = """
CREATE CONSTRAINT shipment_number_unique IF NOT EXISTS
FOR (shipment:Shipment)
REQUIRE shipment.shipment_number IS UNIQUE
"""


CREATE_GRAPH_CONSTRAINTS = [
    CREATE_CONSTRAINTS_QUERY,
    CREATE_PRODUCT_CONSTRAINT_QUERY,
    CREATE_WAREHOUSE_CONSTRAINT_QUERY,
    CREATE_ORDER_CONSTRAINT_QUERY,
    CREATE_SHIPMENT_CONSTRAINT_QUERY,
]

MERGE_SUPPLIER_QUERY = """
MERGE (supplier:Supplier {
    supplier_code: $supplier_code
})
SET
    supplier.name = $name,
    supplier.location = $location,
    supplier.reliability_score = $reliability_score
"""


MERGE_PRODUCT_QUERY = """
MERGE (product:Product {
    product_sku: $product_sku
})
"""


MERGE_WAREHOUSE_QUERY = """
MERGE (warehouse:Warehouse {
    name: $warehouse
})
"""


MERGE_SUPPLIES_RELATIONSHIP_QUERY = """
MATCH (supplier:Supplier {
    supplier_code: $supplier_code
})
MATCH (product:Product {
    product_sku: $product_sku
})
MERGE (supplier)-[:SUPPLIES]->(product)
"""


MERGE_STORED_AT_RELATIONSHIP_QUERY = """
MATCH (product:Product {
    product_sku: $product_sku
})
MATCH (warehouse:Warehouse {
    name: $warehouse
})
MERGE (product)-[:STORED_AT]->(warehouse)
"""


MERGE_ORDER_QUERY = """
MERGE (order_node:Order {
    order_number: $order_number
})
SET
    order_node.customer_name = $customer_name,
    order_node.product_sku = $product_sku,
    order_node.quantity = $quantity,
    order_node.status = $status
"""


MERGE_ORDER_CONTAINS_RELATIONSHIP_QUERY = """
MATCH (order_node:Order {
    order_number: $order_number
})
MATCH (product:Product {
    product_sku: $product_sku
})
MERGE (order_node)-[:CONTAINS]->(product)
"""


MERGE_SHIPMENT_QUERY = """
MERGE (shipment:Shipment {
    shipment_number: $shipment_number
})
SET
    shipment.order_number = $order_number,
    shipment.supplier_code = $supplier_code,
    shipment.status = $status,
    shipment.expected_delivery = $expected_delivery
"""


MERGE_ORDER_SHIPMENT_RELATIONSHIP_QUERY = """
MATCH (order_node:Order {
    order_number: $order_number
})
MATCH (shipment:Shipment {
    shipment_number: $shipment_number
})
MERGE (order_node)-[:HAS_SHIPMENT]->(shipment)
"""


MERGE_SHIPMENT_SUPPLIER_RELATIONSHIP_QUERY = """
MATCH (shipment:Shipment {
    shipment_number: $shipment_number
})
MATCH (supplier:Supplier {
    supplier_code: $supplier_code
})
MERGE (shipment)-[:PROVIDED_BY]->(supplier)
"""

# ============================================================
# Batch ingestion queries
# ============================================================

MERGE_SUPPLIERS_BATCH_QUERY = """
UNWIND $rows AS row

MERGE (supplier:Supplier {
    supplier_code: row.supplier_code
})

SET
    supplier.name = row.name,
    supplier.location = row.location,
    supplier.reliability_score = row.reliability_score
"""


MERGE_PRODUCTS_BATCH_QUERY = """
UNWIND $rows AS row

MERGE (product:Product {
    product_sku: row.product_sku
})
"""


MERGE_WAREHOUSES_BATCH_QUERY = """
UNWIND $rows AS row

MERGE (warehouse:Warehouse {
    name: row.name
})
"""


MERGE_ORDERS_BATCH_QUERY = """
UNWIND $rows AS row

MERGE (order_node:Order {
    order_number: row.order_number
})

SET
    order_node.customer_name = row.customer_name,
    order_node.product_sku = row.product_sku,
    order_node.quantity = row.quantity,
    order_node.status = row.status
"""


MERGE_SHIPMENTS_BATCH_QUERY = """
UNWIND $rows AS row

MERGE (shipment:Shipment {
    shipment_number: row.shipment_number
})

SET
    shipment.order_number = row.order_number,
    shipment.supplier_code = row.supplier_code,
    shipment.status = row.status,
    shipment.expected_delivery = row.expected_delivery
"""


MERGE_ORDER_CONTAINS_BATCH_QUERY = """
UNWIND $rows AS row

MATCH (order_node:Order {
    order_number: row.order_number
})

MATCH (product:Product {
    product_sku: row.product_sku
})

MERGE (order_node)-[:CONTAINS]->(product)
"""


MERGE_ORDER_SHIPMENT_BATCH_QUERY = """
UNWIND $rows AS row

MATCH (order_node:Order {
    order_number: row.order_number
})

MATCH (shipment:Shipment {
    shipment_number: row.shipment_number
})

MERGE (order_node)-[:HAS_SHIPMENT]->(shipment)
"""


MERGE_SHIPMENT_SUPPLIER_BATCH_QUERY = """
UNWIND $rows AS row

MATCH (shipment:Shipment {
    shipment_number: row.shipment_number
})

MATCH (supplier:Supplier {
    supplier_code: row.supplier_code
})

MERGE (shipment)-[:PROVIDED_BY]->(supplier)
"""


MERGE_STORED_AT_BATCH_QUERY = """
UNWIND $rows AS row

MATCH (product:Product {
    product_sku: row.product_sku
})

MATCH (warehouse:Warehouse {
    name: row.warehouse
})

MERGE (product)-[inventory:STORED_AT]->(warehouse)

SET
    inventory.current_stock = row.current_stock,
    inventory.reorder_point = row.reorder_point
"""


MERGE_SUPPLIES_FROM_GRAPH_QUERY = """
MATCH (shipment:Shipment)-[:PROVIDED_BY]->(supplier:Supplier)

MATCH (order_node:Order {
    order_number: shipment.order_number
})-[:CONTAINS]->(product:Product)

MERGE (supplier)-[:SUPPLIES]->(product)
"""