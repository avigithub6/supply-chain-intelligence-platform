from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_existing_order() -> None:
    response = client.get(
        "/orders/ORD-10482"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_number"] == "ORD-10482"
    assert data["status"] == "delayed"
    assert data["product_sku"] == "SKU-0077"


def test_get_missing_order() -> None:
    response = client.get(
        "/orders/ORD-999999"
    )

    assert response.status_code == 404


def test_get_delayed_orders() -> None:
    response = client.get(
        "/orders?status=delayed&limit=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for order in data:
        assert order["status"] == "delayed"