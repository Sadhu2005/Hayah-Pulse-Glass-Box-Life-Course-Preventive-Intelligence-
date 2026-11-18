"""Black-box: behave only through public HTTP; no engine internals imported."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_contract():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    body = res.json()
    assert set(body.keys()) >= {"status", "service", "version", "data_policy"}
    assert body["data_policy"] == "synthetic_only"


def test_unknown_resident_is_404():
    res = client.get("/api/v1/residents/DOES-NOT-EXIST")
    assert res.status_code == 404


def test_fairness_small_cell_mask_string_when_suppressed():
    res = client.get("/api/v1/metrics/fairness")
    assert res.status_code == 200
    body = res.json()
    suppressed = [c for c in body.get("parity", []) if c.get("suppressed")]
    for cell in suppressed:
        assert cell["n"] == "<10 — Suppressed for Privacy"
