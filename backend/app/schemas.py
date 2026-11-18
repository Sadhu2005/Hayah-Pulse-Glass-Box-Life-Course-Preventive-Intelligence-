"""API and engine shared schemas."""

from typing import Any, Literal

from pydantic import BaseModel, Field

RiskTier = Literal["high", "medium", "low", "baseline_onboarding"]
Uncertainty = Literal["HIGH", "MEDIUM", "LOW"]


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "hayah-pulse"
    version: str = "0.1.0"
    data_policy: str = "synthetic_only"


class ReasonItem(BaseModel):
    rank: int
    theme: str
    detail: str


class ResidentSummary(BaseModel):
    resident_id: str
    display_name: str
    age: int
    sex: str
    district: str
    household_id: str
    preferred_language: str
    resident_segment: str
    risk_tier: RiskTier | None = None
    pathway: str | None = None


class EngineOutput(BaseModel):
    resident_id: str
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_tier: RiskTier
    uncertainty: Uncertainty
    confidence_badge: str
    top_reasons: list[ReasonItem] = Field(default_factory=list)
    rule_hits: list[str] = Field(default_factory=list)
    pathway: str
    pathway_recommendation: str
    clinical_firewall: str
    data_sources_used: list[str] = Field(default_factory=list)
    data_sources_not_used: list[str] = Field(default_factory=list)
    household_bundle_hint: str | None = None


class ResidentDetail(BaseModel):
    resident: dict[str, Any]
    engine: EngineOutput | None = None


class EvaluationMetrics(BaseModel):
    n_residents: int = 0
    calibration_brier: float | None = None
    calibration_slope: float | None = None
    caregap_catch_rate_hayah: float | None = None
    caregap_catch_rate_age_only: float | None = None
    lift_vs_age_only: float | None = None
    uncertainty_abstain_rate: float | None = None
    small_cell_leak_count: int = 0
    reasons_coverage: float | None = None


class EvaluationReport(BaseModel):
    dataset: str = "hayah_pulse_synthetic_v0.5"
    reference_date: str | None = None
    metrics: EvaluationMetrics = Field(default_factory=EvaluationMetrics)
    pass_flags: dict[str, bool] = Field(default_factory=dict, alias="pass")
    disclaimer: str = "Synthetic evaluation only — not a clinical validation study"

    model_config = {"populate_by_name": True}


class FairnessCell(BaseModel):
    dimension: str
    key: str
    n: int | str
    recommendation_rate: float | str | None = None
    attendance_rate: float | str | None = None
    suppressed: bool = False


class FairnessResponse(BaseModel):
    funnel: dict[str, int] = Field(default_factory=dict)
    parity: list[FairnessCell] = Field(default_factory=list)
    small_cell_threshold: int = 10
    disclaimer: str = "Synthetic demo data — not real patients"
