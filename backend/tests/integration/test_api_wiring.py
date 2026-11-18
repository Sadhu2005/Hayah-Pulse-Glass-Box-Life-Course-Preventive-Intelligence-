"""Integration: FastAPI routers + schemas wired under /api/v1."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_v1_wired():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_residents_and_fairness_endpoints_exist():
    residents = client.get("/api/v1/residents")
    fairness = client.get("/api/v1/metrics/fairness")
    assert residents.status_code == 200
    assert fairness.status_code == 200
    assert isinstance(residents.json(), list)
    assert "funnel" in fairness.json()


def test_unversioned_api_health_is_gone():
    res = client.get("/api/health")
    assert res.status_code == 404
