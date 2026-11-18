from engine.router import route_pathway


def test_sparse_forces_baseline_onboarding():
    routed = route_pathway(
        {"age": 30, "consented_genomic_tier": None},
        uncertainty={
            "uncertainty": "HIGH",
            "force_pathway": "Baseline Wellness Onboarding",
        },
        rule_hits=[],
        risk_tier="high",
    )
    assert routed["risk_tier"] == "baseline_onboarding"
    assert "Baseline" in routed["pathway"]


def test_pediatric_well_child_track():
    routed = route_pathway(
        {"age": 2, "consented_genomic_tier": "none"},
        uncertainty={"uncertainty": "LOW", "force_pathway": ""},
        rule_hits=[{"id": "WC_OVERDUE_30", "theme": "Care Gap", "detail": "overdue"}],
        risk_tier="medium",
    )
    assert routed["pathway"] == "Well-Child & Developmental"
