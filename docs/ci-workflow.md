# CI Workflow (staging-pipeline style)

**File:** [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

One vertical column in the GitHub Actions UI (same pattern as `lint → … → build-staging`):

```text
lint
unit
integration
functional
regression
blackbox
e2e
all
```

Each job `needs` only the previous one — so Actions draws **one stacked group**, not a wide fork/join graph.

| Job | What it runs |
| --- | --- |
| **lint** | compile + config-yaml + secret-pattern + doc drift/links |
| **unit** | `tests/unit` |
| **integration** | `tests/integration` |
| **functional** | `tests/functional` |
| **regression** | `tests/regression` |
| **blackbox** | `tests/blackbox` |
| **e2e** | `tests/e2e` + frontend build |
| **all** | full suite + evaluation gates (final join) |
