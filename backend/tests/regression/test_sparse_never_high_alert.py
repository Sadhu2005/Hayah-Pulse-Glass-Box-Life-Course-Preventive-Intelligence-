"""Regression: sparse records must never become high-risk clinical alerts."""

from engine.pipeline import run_pipeline


def test_sparse_record_routes_to_baseline_not_high():
    residents = [
        {
            "resident_id": "R-SPARSE",
            "age": 40,
            "sex": "female",
            "household_id": "HH-1",
            "ehr_months_history": 2,
            "consented_genomic_tier": None,
            "days_since_last_preventive": 100,
            "hba1c_trend": 0.2,
            "bp_trend": 0.2,
            "weight_for_length_percentile_delta": None,
            "family_history_flag": True,
            "milestone_overdue_days": None,
            "ifhas_overdue_days": 90,
        }
    ]
    outputs = run_pipeline(residents, households=[], seed=42)
    assert len(outputs) == 1
    out = outputs[0]
    assert out["uncertainty"] == "HIGH"
    assert out["risk_tier"] == "baseline_onboarding"
    assert out["risk_tier"] != "high"
