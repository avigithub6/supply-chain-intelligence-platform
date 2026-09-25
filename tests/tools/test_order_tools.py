from unittest.mock import MagicMock, patch

from app.models.tool_schemas import GetOrderToolInput
from app.tools.order_tools import get_order_tool


def test_get_order_tool_success():
    fake_order = MagicMock()

    fake_order.id = 1
    fake_order.order_number = "ORD-10482"
    fake_order.customer_name = "Customer 0482"
    fake_order.product_sku = "SKU-0077"
    fake_order.quantity = 445
    fake_order.status = "delayed"

    request = GetOrderToolInput(
        order_number="ord-10482",
    )

    with patch(
        "app.tools.order_tools.get_order_by_number",
        return_value=fake_order,
    ):
        result = get_order_tool(request)

    assert result.success is True
    assert result.order is not None
    assert result.order.order_number == "ORD-10482"
    assert result.order.product_sku == "SKU-0077"
    assert result.order.quantity == 445
    assert result.order.status == "delayed"
    assert result.error is None


def test_get_order_tool_order_not_found():
    request = GetOrderToolInput(
        order_number="ORD-99999",
    )

    with patch(
        "app.tools.order_tools.get_order_by_number",
        return_value=None,
    ):
        result = get_order_tool(request)

    assert result.success is False
    assert result.order is None
    assert result.error == "Order not found: ORD-99999"


def test_get_order_tool_normalizes_order_number():
    request = GetOrderToolInput(
        order_number="  ord-10482  ",
    )

    assert request.order_number == "ORD-10482"


def test_get_order_tool_handles_service_error():
    request = GetOrderToolInput(
        order_number="ORD-10482",
    )

    with patch(
        "app.tools.order_tools.get_order_by_number",
        side_effect=Exception("Database unavailable"),
    ):
        result = get_order_tool(request)

    assert result.success is False
    assert result.order is None
    assert "Database unavailable" in result.error