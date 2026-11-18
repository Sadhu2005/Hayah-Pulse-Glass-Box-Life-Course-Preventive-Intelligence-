# Engines & Implementation Phases

**Status:** Living document — fill **Implement when** as you start each phase.  
**Related:** [v0.3-system-architecture.md](./v0.3-system-architecture.md) · [roadmap-pilot-to-scale.md](./roadmap-pilot-to-scale.md) · [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 1. How many engines?

Hayah-Pulse is **one product engine** (`Hayah-Pulse` / Glass-Box Life-Course Preventive Intelligence) composed of **14 named sub-engines / modules** across five layers.

| Count | What |
| --- | --- |
| **1** | Parent product engine (Hayah-Pulse) |
| **14** | Named sub-engines / modules listed below |
| **6** | Already present in `backend/engine/` + fairness service (prototype depth) |
| **8** | Spec’d in architecture; stubbed, UI-only, or deferred to later phases |

### Code modules today (`backend/engine/`)

| File | Maps to |
| --- | --- |
| `rules.py` | Care-Gap Rule Engine |
| `model.py` | Trajectory & Risk Stratifier |
| `shap_explain.py` | Feature Attribution Module |
| `uncertainty.py` | Data-Completeness & Uncertainty Gate |
| `router.py` | Guideline-Constrained Pathway Router |
| `pipeline.py` | Orchestrator (runs all of the above) |
| `app/services/fairness.py` | Subgroup Disparity Auditor + Small-Cell Privacy Suppressor (prototype) |

---

## 2. Full inventory (14 modules)

### Layer 1 — Consent & Data Ingestion *(feeds engines; not scoring engines)*

| # | Module | Role |
| --- | --- | --- |
| L1.1 | Longitudinal EHR & Labs Ingest | Malaffi-compatible FHIR/HL7 longitudinal clinical + labs |
| L1.2 | Consented Genomic Ingest | Actionable genomic / pharmacogenomic tiers only |
| L1.3 | Registry & Visit History Ingest | Well-Child milestones, IFHAS completion, recalls |
| L1.4 | Contextual & Household Index | Geography, optional authorized family link |

> Layer 1 items are **data engines / connectors**. Prototype uses synthetic generator instead of live HIE.

### Layer 2 — Glass-Box Risk & Uncertainty Engine *(core scoring)*

| # | Engine | Role |
| --- | --- | --- |
| **E1** | Care-Gap Rule Engine | Missed / overdue screenings & vaccines (deterministic) |
| **E2** | Trajectory & Risk Stratifier | Calibrated GB / survival-style risk score |
| **E3** | Feature Attribution Module | SHAP / rule-hybrid top 3–5 drivers |
| **E4** | Data-Completeness & Uncertainty Gate | Abstain / Baseline Onboarding when sparse |

### Layer 3 — Guideline-Constrained Pathway Router

| # | Engine | Role |
| --- | --- | --- |
| **E5** | Pathway Router | Well-Child / IFHAS / Genetic / Onboarding tracks |
| **E6** | Capacity-Aware Scheduler | Balance invitations vs clinic slot supply |

### Layer 4 — Culturally Adapted Engagement & Choice

| # | Engine | Role |
| --- | --- | --- |
| **E7** | Language & Persona Adapter | AR / EN / UR / TL; parent / elder framing |
| **E8** | Transparency & Choice Ledger | Why You + Data Used + opt-in/out |
| **E9** | Closed-Loop Recall Navigator | Reminders & reschedule until attended |

### Layer 5 — Fairness, Privacy & Outcome Governance

| # | Engine | Role |
| --- | --- | --- |
| **E10** | Subgroup Disparity Auditor | TPR / FPR / uptake by segment |
| **E11** | Small-Cell Privacy Suppressor | Mask cells where `n < 10` |
| **E12** | Longitudinal Outcome Tracker | Bookings → completed visits → early detection yield |

**Scoring + routing + engagement + governance engines = E1–E12 (12).**  
**Plus Layer 1 connectors L1.1–L1.4 (4) = 16 buildable units**, of which **14 are named “engine/module” capabilities** in the architecture diagram (L2–L5 = E1–E12, and Layer 1 is treated as ingestion rather than decision engines).

**Decision engines to track for phase work: E1–E12 (12).**  
**Ingestion units to track: L1.1–L1.4 (4).**  
**Total tracked units: 16.**

---

## 3. Phase map

Use these phase IDs when filling the tracker:

| Phase ID | Name | Scope |
| --- | --- | --- |
| **P0** | Prototype (synthetic) | v0.5–v1.0 demo — no real PHI |
| **P1** | Retrospective Sandbox | Months 1–3 — de-identified historical validation |
| **P2** | Primary Care Clinic Pilot | Months 4–9 — 3–5 PHCs, EHR + bilingual outreach |
| **P3** | Household Graph & Trajectories | Months 10–18 — family bundling + continuous drift alerts |
| **P4** | Emirate-Wide Scale | 18+ months — network scheduling, full genomic pathways |

---

## 4. Implementation tracker

Fill **Implement when** (date or sprint) when you start that phase for the module. Leave blank until then.

| ID | Engine / module | Code today | Target phase | Depth in that phase | Implement when | Done? |
| --- | --- | --- | --- | --- | --- | --- |
| L1.1 | Longitudinal EHR & Labs Ingest | Synthetic CSV/JSON only | **P1** connect sandbox; **P2** live clinic feed | FHIR/HL7 Malaffi-compatible | | |
| L1.2 | Consented Genomic Ingest | Synthetic `consented_genomic_tier` | **P1** consented fields; **P4** full PGx | Actionable tiers + consent audit | | |
| L1.3 | Registry & Visit History Ingest | Synthetic visit / overdue fields | **P1**–**P2** | Well-Child + IFHAS registries | | |
| L1.4 | Contextual & Household Index | Synthetic HH + district | **P3** authorized household graph | Consent-scoped family links | | |
| E1 | Care-Gap Rule Engine | `engine/rules.py` (P0 done) | **P0** → harden **P1** | Guideline-aligned thresholds on real dates | | |
| E2 | Trajectory & Risk Stratifier | `engine/model.py` (P0 heuristic/GB) | **P0** → calibrate **P1** | Calibration slope 0.90–1.10 | | |
| E3 | Feature Attribution Module | `engine/shap_explain.py` (P0) | **P0** → clinician audit **P1** | Stable top-3 reason UX | | |
| E4 | Uncertainty Gate | `engine/uncertainty.py` (P0 done) | **P0** → tune **P1** | Sparse-record abstention on real completeness | | |
| E5 | Pathway Router | `engine/router.py` (P0 done) | **P0** → EHR embed **P2** | DoH guideline tracks only | | |
| E6 | Capacity-Aware Scheduler | Stub only | **P2** light; **P4** full | Slot supply balancing | | |
| E7 | Language & Persona Adapter | UI AR/EN toggle; templates | **P0** EN/AR; **P2** UR/TL + personas | Guardrailed LLM + templates | | |
| E8 | Transparency & Choice Ledger | Citizen screen (P0) | **P0** → production channel **P2** | WhatsApp/portal + audit log | | |
| E9 | Closed-Loop Recall Navigator | Not built | **P2** | Reminders / reschedule until attended | | |
| E10 | Subgroup Disparity Auditor | `fairness.py` prototype | **P0** → real metrics **P1** | TPR/FPR/uptake parity | | |
| E11 | Small-Cell Privacy Suppressor | `fairness.py` (`n < 10`) | **P0** → enforce **P1** | Zero small-cell leaks | | |
| E12 | Longitudinal Outcome Tracker | Funnel approx only | **P2** → yield **P3/P4** | Booked → completed → early detection | | |

### Suggested “implement when” examples (optional)

Leave blank until real. Examples of format:

- `2026-11-20 — P0 sprint`
- `Sprint 3 — start P1 sandbox`
- `Pilot week 1 — PHC go-live`

---

## 5. Recommended build order (by phase)

### P0 — Prototype (now)

1. L1 synthetic generator (stand-in for L1.1–L1.4)  
2. E1 → E2 → E3 → E4 → E5  
3. E8 + E7 (EN/AR) UI  
4. E10 + E11 prototype dashboard  
5. Package demo (v1.0 checklist)

**Defer from P0:** E6 full scheduler, E9 recall loop, live L1 connectors, E12 clinical yield.

### P1 — Sandbox

- Wire L1.1–L1.3 to de-identified feeds  
- Recalibrate E2; clinician-audit E3  
- Stress-test E10 / E11 on real aggregates  

### P2 — Clinic pilot

- Embed E5 clinician card in EHR  
- Production E7 / E8 messaging  
- Ship E9 recall navigator  
- Light E6 capacity rules  
- Start E12 attendance outcomes  

### P3 — Household & trajectories

- Activate L1.4 household graph  
- Continuous trajectory triggers inside E2  
- Strengthen E12 early-detection yield  

### P4 — Emirate-wide

- Full E6 capacity-aware network scheduling  
- Full L1.2 genomic / PGx pathways  
- Population-scale E10–E12 governance  

---

## 6. Quick answer

| Question | Answer |
| --- | --- |
| How many decision engines (E1–E12)? | **12** |
| How many ingestion units (L1.1–L1.4)? | **4** |
| Total tracked implementation units? | **16** |
| Parent product engines? | **1** (Hayah-Pulse) |
| In code under `backend/engine/` today? | **6 files** (+ fairness service for E10/E11) |

---

## 7. Change log

| Date | Change |
| --- | --- |
| 2026-11-18 | Initial inventory + phase tracker created |
