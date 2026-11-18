# Hayah-Pulse

**Glass-Box Life-Course Preventive Intelligence**

Explainable, consent-first population health engine that converts longitudinal clinical, genomic, developmental, and environmental data into timely, culturally tailored preventive action.

> Prototype uses **100% synthetic data**. No real patient records.

**Branch for this work:** `feat/ci-workflow-v1`

## Documentation

Start at **[docs/README.md](./docs/README.md)** (v0.1 → v1.0).

Governance audit: **[docs/governance-compliance-audit.md](./docs/governance-compliance-audit.md)**

## Repository layout

```
backend/          FastAPI + risk engine + layered tests
frontend/         React + Vite + Tailwind (3 screens)
data/synthetic/   Generated cohort & evaluation artifacts
docs/             Product & build specifications
.github/workflows CI DAG (Unit → … → E2E + portable + static checks)
scripts/ci/       CI helper checkers
```

## Quick start

```bash
python -m pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

python backend/scripts/generate_synthetic_cohort.py
python backend/scripts/run_engine.py
python backend/scripts/run_evaluation.py

python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
# other terminal
cd frontend && npm run dev
```

Open http://127.0.0.1:5173

## API surface (v1)

| Method | Path |
| --- | --- |
| GET | `/api/v1/health` |
| GET | `/api/v1/residents` |
| GET | `/api/v1/residents/{id}` |
| GET | `/api/v1/engine/outputs` |
| GET | `/api/v1/metrics/evaluation` |
| GET | `/api/v1/metrics/fairness` |

## Tests (required layers)

```bash
# all layers
python -m pytest backend/tests -q

# by layer
python -m pytest backend/tests/unit -q
python -m pytest backend/tests/integration -q
python -m pytest backend/tests/functional -q
python -m pytest backend/tests/regression -q
python -m pytest backend/tests/blackbox -q
python -m pytest backend/tests/e2e -q
```

Or `make test-unit`, `make test-integration`, … / `make test-all`

## CI workflow UI

GitHub Actions shows **one grouped box / one column** (staging-pipeline style) via reusable workflow:

`ci.yml` → `test-pipeline.yml` → nested `lint` / `unit` / `integration` / `functional` / `regression` / `blackbox` / `e2e` / `all`

## Environment

Copy `.env.example` → `.env`. `LLM_API_KEY` is optional.
