from engine.uncertainty import assess_uncertainty


def test_sparse_record_triggers_high_uncertainty():
    result = assess_uncertainty(
        {"ehr_months_history": 3, "consented_genomic_tier": None}
    )
    assert result["uncertainty"] == "HIGH"
    assert "Baseline" in result["force_pathway"] or "Baseline" in result["confidence_badge"]


def test_rich_record_low_uncertainty():
    result = assess_uncertainty(
        {"ehr_months_history": 48, "consented_genomic_tier": "actionable"}
    )
    assert result["uncertainty"] == "LOW"
