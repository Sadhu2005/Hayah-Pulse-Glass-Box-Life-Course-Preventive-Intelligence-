# 90-second demo walkthrough

Record locally (screen capture). Order is fixed for judges.

| Time | Screen | Action | Say |
| --- | --- | --- | --- |
| 0:00–0:25 | `/clinician` | Pick overdue pediatric or cardiometabolic adult | “Glass-box flag: pathway + top reasons + confidence—not a black box.” |
| 0:25–0:55 | `/citizen` | Toggle EN → AR (optionally UR/TL stubs); show modality + opt-out | “Families see why, what data was used, and choose how to engage.” |
| 0:55–1:30 | `/fairness` | Point to funnel; enable “Show suppressed cells only” | “Equity and privacy: small cells masked, outcomes tracked.” |

## Prerequisites

```bash
python backend/scripts/generate_synthetic_cohort.py
python backend/scripts/run_engine.py
python backend/scripts/run_evaluation.py
python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
cd frontend && npm run dev
```

Open http://127.0.0.1:5173

## Stills in this folder

- `clinician-card.png`
- `citizen-en.png`
- `citizen-ar.png`
- `fairness-suppressed.png`
