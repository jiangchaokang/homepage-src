#!/usr/bin/env python3
"""Fail loudly on CSS that the browser would silently discard.

`jekyll build` copies CSS verbatim and never parses it, so a single unclosed
brace produces a clean build and a destroyed site: every rule after the error
is dropped, layouts collapse, and nothing in the toolchain says a word. That
happened once. This catches it.

Usage:  python3 tools/check-css.py
Exit:   0 clean, 1 problems found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "assets/css/main.css"


def main() -> int:
    raw = TARGET.read_text(encoding="utf-8")
    # Blank out comments while preserving line numbers.
    text = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), raw, flags=re.S)
    lines = text.split("\n")

    problems = []
    open_blocks = []
    for lineno, line in enumerate(lines, 1):
        for ch in line:
            if ch == "{":
                open_blocks.append(lineno)
            elif ch == "}":
                if open_blocks:
                    open_blocks.pop()
                else:
                    problems.append((lineno, "closing brace with no matching open block"))

    for lineno in open_blocks:
        problems.append((lineno, f"block opened here is never closed: {lines[lineno - 1].strip()[:60]}"))

    # A declaration that lost its semicolon swallows the selector that follows it.
    # Multi-line values (gradients, shadows) legitimately end without punctuation,
    # so only flag a line that both looks complete and is followed by a selector.
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or ":" not in stripped or stripped.startswith("@"):
            continue
        if stripped.endswith((";", "{", "}", ",")) or "{" in stripped:
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if nxt.endswith("{") and not nxt.startswith(("@", "from", "to")):
            problems.append((i + 1, f"declaration missing ';' before the next rule: {stripped[:60]}"))

    rel = TARGET.relative_to(ROOT)
    if problems:
        for lineno, msg in sorted(problems):
            print(f"{rel}:{lineno}: {msg}")
        print(f"\n{len(problems)} problem(s). The browser would drop every rule after the first one.")
        return 1

    print(f"{rel}: OK ({len(lines)} lines, braces balanced)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
