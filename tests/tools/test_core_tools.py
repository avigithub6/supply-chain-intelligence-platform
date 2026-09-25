from unittest.mock import MagicMock, patch

from app.models.tool_schemas import (
    GetInventoryToolInput,
    GetShipmentToolInput,
    GetSupplierToolInput,
)
from app.tools.inventory_tools import get_inventory_tool
from app.tools.shipment_tools import get_shipment_tool
from app.tools.supplier_tools import get_supplier_tool


def test_get_inventory_tool_success():
    fake_inventory = MagicMock()

    fake_inventory.id = 77
    fake_inventory.product_sku = "SKU-0077"
    fake_inventory.warehouse = "Mumbai"
    fake_inventory.current_stock = 35
    fake_inventory.reorder_point = 250

    request = GetInventoryToolInput(
        product_sku="sku-0077",
    )

    with patch(
        "app.tools.inventory_tools.get_inventory_by_sku",
        return_value=fake_inventory,
    ):
        result = get_inventory_tool(request)

    assert result.success is True
    assert result.inventory is not None
    assert result.inventory.product_sku == "SKU-0077"
    assert result.inventory.warehouse == "Mumbai"
    assert result.inventory.current_stock == 35
    assert result.inventory.reorder_point == 250
    assert result.error is None


def test_get_inventory_tool_not_found():
    request = GetInventoryToolInput(
        product_sku="SKU-9999",
    )

    with patch(
        "app.tools.inventory_tools.get_inventory_by_sku",
        return_value=None,
    ):
        result = get_inventory_tool(request)

    assert result.success is False
    assert result.inventory is None
    assert result.error == (
        "Inventory not found for SKU: SKU-9999"
    )


def test_get_inventory_tool_normalizes_sku():
    request = GetInventoryToolInput(
        product_sku="  sku-0077  ",
    )

    assert request.product_sku == "SKU-0077"


def test_get_supplier_tool_success():
    fake_supplier = MagicMock()

    fake_supplier.id = 17
    fake_supplier.supplier_code = "SUP-017"
    fake_supplier.name = "Supplier 017 Industries"
    fake_supplier.location = "Pune"
    fake_supplier.reliability_score = 62.5

    request = GetSupplierToolInput(
        supplier_code="sup-017",
    )

    with patch(
        "app.tools.supplier_tools.get_supplier_by_code",
        return_value=fake_supplier,
    ):
        result = get_supplier_tool(request)

    assert result.success is True
    assert result.supplier is not None
    assert result.supplier.supplier_code == "SUP-017"
    assert result.supplier.name == "Supplier 017 Industries"
    assert result.supplier.location == "Pune"
    assert result.supplier.reliability_score == 62.5
    assert result.error is None


def test_get_supplier_tool_not_found():
    request = GetSupplierToolInput(
        supplier_code="SUP-999",
    )

    with patch(
        "app.tools.supplier_tools.get_supplier_by_code",
        return_value=None,
    ):
        result = get_supplier_tool(request)

    assert result.success is False
    assert result.supplier is None
    assert result.error == "Supplier not found: SUP-999"


def test_get_shipment_tool_success():
    fake_shipment = MagicMock()

    fake_shipment.id = 482
    fake_shipment.shipment_number = "SHIP-20482"
    fake_shipment.order_number = "ORD-10482"
    fake_shipment.supplier_code = "SUP-017"
    fake_shipment.status = "delayed"

    from datetime import date

    fake_shipment.expected_delivery = date(
        2026,
        9,
        16,
    )

    request = GetShipmentToolInput(
        shipment_number="ship-20482",
    )

    with patch(
        "app.tools.shipment_tools.get_shipment_by_number",
        return_value=fake_shipment,
    ):
        result = get_shipment_tool(request)

    assert result.success is True
    assert result.shipment is not None
    assert result.shipment.shipment_number == "SHIP-20482"
    assert result.shipment.order_number == "ORD-10482"
    assert result.shipment.supplier_code == "SUP-017"
    assert result.shipment.status == "delayed"
    assert result.shipment.expected_delivery == date(
        2026,
        9,
        16,
    )
    assert result.error is None


def test_get_shipment_tool_not_found():
    request = GetShipmentToolInput(
        shipment_number="SHIP-99999",
    )

    with patch(
        "app.tools.shipment_tools.get_shipment_by_number",
        return_value=None,
    ):
        result = get_shipment_tool(request)

    assert result.success is False
    assert result.shipment is None
    assert result.error == (
        "Shipment not found: SHIP-99999"
    )