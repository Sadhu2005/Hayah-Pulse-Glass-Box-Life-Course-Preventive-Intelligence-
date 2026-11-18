# Hayah-Pulse Documentation

**Product:** Hayah-Pulse (Glass-Box Life-Course Preventive Intelligence)  
**Scope:** Problem → solution → architecture → prototype build (v0.1 → v1.0)  
**Data policy:** Zero real patient data. Prototype uses 100% synthetic cohorts only.

## Reading order

Read and implement in sequence. Do not skip build steps.

| Version | Document | Role | Status |
| --- | --- | --- | --- |
| Index | [README.md](./README.md) | Reading order and status | Ready |
| v0.1 | [v0.1-challenge-and-problem.md](./v0.1-challenge-and-problem.md) | Challenge, problem, objective, outcomes | Ready |
| v0.2 | [v0.2-solution-concept.md](./v0.2-solution-concept.md) | Concept, ecosystem fit, gaps, principles | Ready |
| v0.3 | [v0.3-system-architecture.md](./v0.3-system-architecture.md) | Five-layer architecture | Ready |
| v0.4 | [v0.4-outputs-and-ux.md](./v0.4-outputs-and-ux.md) | Clinician / Citizen / Regulator outputs | Ready |
| v0.5 | [v0.5-synthetic-cohort-and-data-model.md](./v0.5-synthetic-cohort-and-data-model.md) | **Build Step 1** — synthetic data | Ready |
| v0.6 | [v0.6-risk-engine-spec.md](./v0.6-risk-engine-spec.md) | **Build Step 2** — risk & routing engine | Ready |
| v0.7 | [v0.7-prototype-screens-spec.md](./v0.7-prototype-screens-spec.md) | **Build Step 3** — three screens | Ready |
| v0.8 | [v0.8-validation-and-metrics.md](./v0.8-validation-and-metrics.md) | **Build Step 4** — validation | Ready |
| v0.9 | [v0.9-repo-layout-and-tech-stack.md](./v0.9-repo-layout-and-tech-stack.md) | Repo layout & tech stack | Ready |
| v1.0 | [v1.0-prototype-build-checklist.md](./v1.0-prototype-build-checklist.md) | **Ship** — end-to-end checklist | Ready |
| Post-v1 | [roadmap-pilot-to-scale.md](./roadmap-pilot-to-scale.md) | Pilot → emirate-wide (out of prototype scope) | Ready |

## Implementation rule

After docs are ready, implement **only** the next unfinished build doc:

1. v0.5 → synthetic cohort  
2. v0.6 → risk / uncertainty / routing engine  
3. v0.7 → three interactive screens  
4. v0.8 → validation & stress test  
5. v1.0 → package demo artifacts  

Status values: `Draft` → `Ready` → `Implemented`.

## Locked stack (prototype)

- **Backend / ML:** Python (`pandas`, `numpy`, `scikit-learn`, `shap`)
- **UI:** React + Vite + Tailwind CSS
- **Engagement previews:** LLM API with strict prompt guardrails (Arabic + English)
- **Data:** Synthetic only (`data/synthetic/`)

## Retired docs

- `01-problem-and-solution-overview.md` — absorbed into v0.1 + v0.2; see redirect stub if present.
