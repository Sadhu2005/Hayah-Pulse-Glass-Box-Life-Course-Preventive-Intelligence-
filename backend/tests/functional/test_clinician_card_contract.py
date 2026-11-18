"""Functional: clinician Reason-for-Flag contract from public resident detail."""

from fastapi.testclient import TestClient

from app.main import app
from app.services.data_store import CLINICAL_FIREWALL

client = TestClient(app)


def test_resident_detail_exposes_clinician_card_fields_when_engine_present():
    listing = client.get("/api/v1/residents")
    assert listing.status_code == 200
    rows = listing.json()
    if not rows:
        return  # synthetic data not generated in this environment

    rid = rows[0]["resident_id"]
    detail = client.get(f"/api/v1/residents/{rid}")
    assert detail.status_code == 200
    body = detail.json()
    assert "resident" in body
    engine = body.get("engine")
    if engine is None:
        return
    assert "pathway_recommendation" in engine
    assert "top_reasons" in engine
    assert "confidence_badge" in engine
    assert engine["clinical_firewall"] == CLINICAL_FIREWALL
