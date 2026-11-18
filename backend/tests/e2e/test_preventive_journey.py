"""E2E: synthetic preventive journey Flagged → Card fields → Fairness dashboard."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_end_to_end_clinician_to_fairness_journey():
    health = client.get("/api/v1/health")
    assert health.status_code == 200

    residents = client.get("/api/v1/residents")
    assert residents.status_code == 200
    rows = residents.json()
    assert isinstance(rows, list)

    if rows:
        rid = rows[0]["resident_id"]
        detail = client.get(f"/api/v1/residents/{rid}")
        assert detail.status_code == 200
        body = detail.json()
        assert body["resident"]["resident_id"] == rid

    fairness = client.get("/api/v1/metrics/fairness")
    assert fairness.status_code == 200
    funnel = fairness.json()["funnel"]
    assert isinstance(funnel, dict)
