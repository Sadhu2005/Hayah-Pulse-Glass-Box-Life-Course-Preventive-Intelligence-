#!/usr/bin/env python3
"""Validate critical YAML files parse."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    ROOT / ".github" / "workflows" / "ci.yml",
    ROOT / ".github" / "workflows" / "test-pipeline.yml",
]


def main() -> int:
    if yaml is None:
        # Minimal structural check without PyYAML
        for path in FILES:
            text = path.read_text(encoding="utf-8")
            if "jobs:" not in text or "on:" not in text:
                print(f"config-yaml: {path.name} missing jobs/on")
                return 1
        print("config-yaml: ok (structural)")
        return 0

    for path in FILES:
        with path.open(encoding="utf-8") as f:
            yaml.safe_load(f)
    print("config-yaml: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
