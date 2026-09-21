from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_supplier() -> None:
    response = client.get(
        "/suppliers/SUP-017"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["supplier_code"] == "SUP-017"
    assert data["reliability_score"] == 62.5


def test_get_missing_supplier() -> None:
    response = client.get(
        "/suppliers/SUP-999"
    )

    assert response.status_code == 404