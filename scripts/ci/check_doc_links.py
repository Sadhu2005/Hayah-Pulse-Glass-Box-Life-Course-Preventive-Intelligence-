#!/usr/bin/env python3
"""Check relative markdown links under docs/ resolve."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def main() -> int:
    broken: list[str] = []
    for md in DOCS.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for _label, target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            dest = (md.parent / clean).resolve()
            if not dest.exists():
                broken.append(f"{md.relative_to(ROOT)} -> {target}")
    if broken:
        print("Broken doc links:")
        print("\n".join(broken))
        return 1
    print("doc-links: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
