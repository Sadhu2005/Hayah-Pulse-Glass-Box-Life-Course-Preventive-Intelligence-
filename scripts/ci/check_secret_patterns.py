#!/usr/bin/env python3
"""Fail if obvious secret patterns appear in tracked source (not synthetic data)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "data", "dist", "assets"}
PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]"),
    re.compile(r"(?i)secret[_-]?key\s*=\s*['\"][^'\"]{12,}['\"]"),
]


def main() -> int:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".json", ".yml", ".yaml", ".md", ".env.example"}:
            continue
        if path.name == "check_secret_patterns.py":
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in PATTERNS:
            if pat.search(text):
                hits.append(f"{path.relative_to(ROOT)} :: {pat.pattern}")
    if hits:
        print("Secret pattern hits:")
        print("\n".join(hits))
        return 1
    print("secret-pattern: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
