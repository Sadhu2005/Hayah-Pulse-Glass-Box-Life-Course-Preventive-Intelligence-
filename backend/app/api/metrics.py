"""Evaluation and fairness endpoints."""

from fastapi import APIRouter, HTTPException

from app.schemas import EvaluationReport, FairnessResponse
from app.services.data_store import get_store
from app.services.fairness import build_fairness

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/evaluation", response_model=EvaluationReport)
def get_evaluation() -> EvaluationReport:
    store = get_store()
    raw = store.evaluation_report()
    if raw is None:
        raise HTTPException(
            status_code=404,
            detail="evaluation_report.json missing — run backend/scripts/run_evaluation.py",
        )
    return EvaluationReport.model_validate(raw)


@router.get("/fairness", response_model=FairnessResponse)
def get_fairness() -> FairnessResponse:
    return build_fairness(get_store())
