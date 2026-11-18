# Roadmap — Pilot to Emirate-Wide Scale

**Status:** Ready  
**Scope:** Post-prototype (does **not** block v1.0 prototype ship)  
**Prototype checklist:** [v1.0-prototype-build-checklist.md](./v1.0-prototype-build-checklist.md)

---

## Purpose

After the interactive synthetic prototype is complete, this roadmap guides validation and scale inside Abu Dhabi’s preventive ecosystem (Malaffi, Well-Child, IFHAS).

---

## Phase table

| Phase | Timeline | Key milestones | Success criteria |
| --- | --- | --- | --- |
| **Phase 1: Retrospective Sandbox Validation** | Months 1–3 | Deploy engine inside an isolated, de-identified health data sandbox; validate risk calibration, SHAP explanations, and subgroup parity against historical screening outcomes. | Calibration slope 0.90–1.10; zero small-cell (`n < 10`) leakage; clinician audit approval of top-3 reason explanations. |
| **Phase 2: Primary Care Clinic Pilot** | Months 4–9 | Launch in 3–5 primary healthcare centers for Well-Child and IFHAS outreach; integrate Clinician Decision Cards into EHR workflows and test bilingual WhatsApp/portal Transparency Ledgers. | ≥25% lift in timely screening attendance; ≥80% physician trust/usability score; &lt;5% opt-out rate. |
| **Phase 3: Household Graph & Trajectory Triggers** | Months 10–18 | Activate authorized household/family bundling (linking newborn/pediatric and adult screenings) and continuous sub-threshold trajectory alerts (growth curves, HbA1c/BP drift). | Measurable reduction in overdue pediatric recalls and earlier detection of pre-diabetes/hypertension. |
| **Phase 4: Emirate-Wide Life-Course Scale** | 18+ months | Expand across the broader primary care network with automated capacity-aware scheduling, full pharmacogenomic/genomic pathway integration, and continuous healthspan outcome tracking. | Sustained population-wide increase in preventive coverage and measurable gains in healthy life years. |

---

## Phase notes

### Phase 1

- Move from synthetic labels to historical outcomes in a governed sandbox.
- Re-run fairness auditor and small-cell suppressor on real aggregate cells.
- Lock explanation style with clinician reviewers before pilot UI go-live.

### Phase 2

- EHR-embedded Reason-for-Flag cards.
- Production messaging channels with consent and audit trails.
- Measure attendance lift vs control clinics / prior baselines.

### Phase 3

- Authorized household graph (consent-scoped).
- Continuous trajectory monitors, not only calendar overdue flags.

### Phase 4

- Capacity-aware scheduling at network scale.
- Broader genomic/pharmacogenomic pathway integration under DoH policy.
- Healthspan / early-detection yield as primary outcome metrics.

---

## Explicit non-goals for prototype

- No live HIE connectivity
- No real PHI
- No production WhatsApp send
- No claim of clinical validation study completion
