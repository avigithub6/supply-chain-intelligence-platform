from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_shipment() -> None:
    response = client.get(
        "/shipments/SHIP-20482"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_number"] == "SHIP-20482"
    assert data["order_number"] == "ORD-10482"
    assert data["supplier_code"] == "SUP-017"
    assert data["status"] == "delayed"


def test_get_missing_shipment() -> None:
    response = client.get(
        "/shipments/SHIP-99999"
    )

    assert response.status_code == 404