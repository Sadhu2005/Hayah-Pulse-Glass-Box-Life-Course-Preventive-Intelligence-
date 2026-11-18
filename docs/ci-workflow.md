# CI Workflow (one column / one box UI)

Like `staging-pipeline.yml`: jobs appear **inside one grouped box**, stacked in a single column — not spread across the canvas as separate top-level nodes.

| File | Role |
| --- | --- |
| [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Parent — calls the reusable pipeline |
| [`.github/workflows/test-pipeline.yml`](../.github/workflows/test-pipeline.yml) | Nested jobs (the column inside the box) |

```text
┌─ pipeline ─────────────────┐
│  lint                      │
│  unit                      │
│  integration               │
│  functional                │
│  regression                │
│  blackbox                  │
│  e2e                       │
│  all                       │
└────────────────────────────┘
```

Order inside the box: each job waits for the previous (`needs`).
