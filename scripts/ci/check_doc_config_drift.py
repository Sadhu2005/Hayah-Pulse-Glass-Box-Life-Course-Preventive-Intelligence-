#!/usr/bin/env python3
"""Ensure docs/README still mention versioned API and CI test layers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = (ROOT / "README.md").read_text(encoding="utf-8")
DOCS_README = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
CI = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

required_readme = ["/api/v1/health", "/api/v1/residents"]
required_ci_jobs = [
    "lint",
    "unit",
    "integration",
    "functional",
    "regression",
    "blackbox",
    "e2e",
    "all",
]


def main() -> int:
    errors: list[str] = []
    for needle in required_readme:
        if needle not in README:
            errors.append(f"README.md missing `{needle}`")
    if "governance-compliance-audit.md" not in DOCS_README:
        errors.append("docs/README.md missing governance audit link")
    for job in required_ci_jobs:
        if f"name: {job}" not in CI and f"name: {job.lower()}" not in CI:
            # accept either display name casing used in workflow
            if f"{job.lower()}:" not in CI and f"{job}:" not in CI:
                errors.append(f"ci.yml missing job related to {job}")
    if errors:
        print("doc-config-drift failures:")
        print("\n".join(errors))
        return 1
    print("doc-config-drift: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
