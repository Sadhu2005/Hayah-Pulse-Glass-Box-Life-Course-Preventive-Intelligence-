# CI Workflow (one vertical box)

**Wanted UI** (like staging-pipeline): one card, suites stacked in a **column** — not a long left-to-right chain.

**How:** one job + `strategy.matrix` + `max-parallel: 1`

```text
┌─ pipeline ──────────────┐
│ lint                    │
│ unit                    │
│ integration             │
│ functional              │
│ regression              │
│ blackbox                │
│ e2e                     │
│ all                     │
└─────────────────────────┘
```

- File: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Suites still run **one after another** (`max-parallel: 1`, `fail-fast: true`)
- Actions graph shows them as a **matrix group in one box** (vertical list)
