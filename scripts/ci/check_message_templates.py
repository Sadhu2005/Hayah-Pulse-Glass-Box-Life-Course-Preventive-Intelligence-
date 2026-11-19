#!/usr/bin/env python3
"""Ensure citizen message templates declare en/ar/ur/tl."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "frontend" / "src" / "lib" / "messageTemplates.ts"
REQUIRED = ["en", "ar", "ur", "tl"]


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    missing = [lang for lang in REQUIRED if f'"{lang}"' not in text and f"'{lang}'" not in text]
    if "SUPPORTED_LANGS" not in text:
        missing.append("SUPPORTED_LANGS")
    if missing:
        print("messageTemplates missing:", ", ".join(missing))
        return 1
    print("message-templates: ok (en/ar/ur/tl)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
