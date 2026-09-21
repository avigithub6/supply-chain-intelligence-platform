from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_inventory_by_sku() -> None:
    response = client.get(
        "/inventory/SKU-0077"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_sku"] == "SKU-0077"
    assert data["current_stock"] == 35
    assert data["reorder_point"] == 250


def test_get_missing_inventory() -> None:
    response = client.get(
        "/inventory/SKU-9999"
    )

    assert response.status_code == 404


def test_low_stock_inventory() -> None:
    response = client.get(
        "/inventory?low_stock=true&limit=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for item in data:
        assert item["current_stock"] <= item["reorder_point"]