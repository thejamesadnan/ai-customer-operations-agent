from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_vmc_investigation_requires_approval() -> None:
    response = client.post(
        "/investigate",
        json={
            "customer_id": "CUST-001",
            "machine_id": "MCH-102",
            "issue": "Repeated vend failures today",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["approval_required"] is True
    assert any("VMC" in finding for finding in data["findings"])
    assert any(a["action"] == "restart_vmc" for a in data["recommended_actions"])
    assert data["estimated_cost_usd"] == 0.0


def test_cross_customer_machine_is_rejected() -> None:
    response = client.post(
        "/investigate",
        json={
            "customer_id": "CUST-002",
            "machine_id": "MCH-102",
            "issue": "Investigate issue",
        },
    )
    assert response.status_code == 404
