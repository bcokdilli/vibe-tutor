#!/usr/bin/env python3
"""Evaluate a Vibe Tutor digest for size and safety rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


REQUIRED_HEADINGS = (
    "## Ne değişti?",
    "## Neden önemli?",
    "## Öğrenilecek kavramlar",
    "## Kodda nereye bakmalı?",
    "## Kendini test et",
    "## Doğrulama durumu",
)
BANNED = (
    "kesin doğru",
    "garanti",
    "bug yok",
    "production-ready",
    "100% correct",
    "perfect",
)


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def concept_count(text: str) -> int:
    match = re.search(r"^## Öğrenilecek kavramlar\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    if not match:
        return 0
    return len(re.findall(r"^\s*\d+\.\s+", match.group(1), re.MULTILINE))


def max_code_fence_lines(text: str) -> int:
    max_lines = 0
    in_fence = False
    current = 0
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_fence:
                max_lines = max(max_lines, current)
                current = 0
                in_fence = False
            else:
                in_fence = True
                current = 0
            continue
        if in_fence:
            current += 1
    if in_fence:
        max_lines = max(max_lines, current)
    return max_lines


def evaluate(text: str, max_words: int) -> dict[str, object]:
    failures: list[str] = []
    warnings: list[str] = []
    words = word_count(text)
    concepts = concept_count(text)
    code_lines = max_code_fence_lines(text)
    lower = text.lower()

    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    if missing:
        failures.append("missing headings: " + ", ".join(missing))
    if words > max_words:
        failures.append(f"word count {words} exceeds {max_words}")
    if concepts > 3:
        failures.append(f"concept count {concepts} exceeds 3")
    if code_lines > 12:
        failures.append(f"code fence has {code_lines} lines, exceeds 12")
    for phrase in BANNED:
        if phrase in lower:
            failures.append(f"banned overclaim: {phrase}")
    if "## Doğrulama durumu" not in text:
        failures.append("missing verification section")
    if concepts == 0 and "## Öğrenilecek kavramlar" in text:
        warnings.append("no numbered concepts found")

    return {
        "ok": not failures,
        "word_count": words,
        "concept_count": concepts,
        "max_code_fence_lines": code_lines,
        "failures": failures,
        "warnings": warnings,
    }


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a Vibe Tutor digest.")
    parser.add_argument("digest", type=Path)
    parser.add_argument("--max-words", type=int, default=150)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    text = args.digest.read_text(encoding="utf-8")
    result = evaluate(text, args.max_words)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("ok" if result["ok"] else "failed")
        for key in ("word_count", "concept_count", "max_code_fence_lines"):
            print(f"{key}: {result[key]}")
        for failure in result["failures"]:
            print(f"failure: {failure}")
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
