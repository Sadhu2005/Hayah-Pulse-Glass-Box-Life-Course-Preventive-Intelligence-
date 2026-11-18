from engine.rules import evaluate_rules


def test_well_child_overdue_rule():
    hits = evaluate_rules(
        {
            "age": 2,
            "milestone_overdue_days": 64,
            "ifhas_overdue_days": None,
            "family_history_flag": False,
            "consented_genomic_tier": "none",
            "hba1c_trend": 0,
            "bp_trend": 0,
            "weight_for_length_percentile_delta": 0,
        }
    )
    assert any(h["id"] == "WC_OVERDUE_30" for h in hits)


def test_ifhas_overdue_rule():
    hits = evaluate_rules(
        {
            "age": 42,
            "milestone_overdue_days": None,
            "ifhas_overdue_days": 90,
            "family_history_flag": True,
            "consented_genomic_tier": "actionable",
            "hba1c_trend": 0.1,
            "bp_trend": 0,
            "weight_for_length_percentile_delta": None,
        }
    )
    ids = {h["id"] for h in hits}
    assert "IFHAS_OVERDUE_30" in ids
    assert "FHX_PRESENT" in ids
