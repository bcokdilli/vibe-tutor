#!/usr/bin/env python3
"""Collect compact, redacted git diff context for Vibe Tutor."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Iterable


RISKY_PATTERNS = (".env", ".pem", ".key", "id_rsa", "secrets", "credentials", "token")
SECRET_KEY_RE = re.compile(
    r"(?i)(secret|token|credential|password|api[_-]?key|private[_-]?key|access[_-]?key)"
    r"([\"']?\s*[:=]\s*[\"']?)([^\"'\s,;]+)"
)
LONG_VALUE_RE = re.compile(r"(?<![A-Za-z0-9_/+=-])[A-Za-z0-9_/+=-]{32,}(?![A-Za-z0-9_/+=-])")


def run_git(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr


def is_git_repo() -> bool:
    code, _, _ = run_git(["rev-parse", "--is-inside-work-tree"])
    return code == 0


def risky_path(path: str) -> bool:
    lower = path.lower()
    base = os.path.basename(lower)
    return any(pattern in lower or pattern in base for pattern in RISKY_PATTERNS)


def redact_line(line: str) -> tuple[str, bool]:
    changed = False

    def replace_secret(match: re.Match[str]) -> str:
        nonlocal changed
        changed = True
        return f"{match.group(1)}{match.group(2)}[REDACTED]"

    redacted = SECRET_KEY_RE.sub(replace_secret, line)
    new_redacted = LONG_VALUE_RE.sub("[REDACTED_LONG_VALUE]", redacted)
    if new_redacted != redacted:
        changed = True
    return new_redacted, changed


def sanitize_stat(text: str) -> tuple[str, list[str]]:
    notices: list[str] = []
    output: list[str] = []
    for line in text.splitlines():
        path = line.split("|", 1)[0].strip()
        if path and risky_path(path):
            output.append("[redacted-risky-file] | changes hidden")
            notices.append(f"redacted risky stat path: {path}")
            continue
        redacted, changed = redact_line(line)
        if changed:
            notices.append("redacted secret-looking stat value")
        output.append(redacted)
    return "\n".join(output), notices


def sanitize_diff(text: str) -> tuple[str, list[str]]:
    notices: list[str] = []
    output: list[str] = []
    skip_file: str | None = None

    for line in text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            path = parts[2][2:] if len(parts) >= 3 and parts[2].startswith("a/") else line
            skip_file = path if risky_path(path) else None
            if skip_file:
                output.append("diff --git [redacted-risky-file] [redacted-risky-file]")
                notices.append(f"skipped risky diff hunks: {skip_file}")
                continue

        if skip_file:
            continue

        redacted, changed = redact_line(line)
        if changed:
            notices.append("redacted secret-looking diff value")
        output.append(redacted)

    return "\n".join(output), notices


def changed_files(staged: bool) -> list[str]:
    args = ["diff", "--name-only"]
    if staged:
        args.append("--cached")
    code, out, _ = run_git(args)
    if code != 0:
        return []
    files = []
    for path in out.splitlines():
        files.append("[redacted-risky-file]" if risky_path(path) else path)
    return files


def untracked_files() -> list[str]:
    code, out, _ = run_git(["ls-files", "--others", "--exclude-standard"])
    if code != 0:
        return []
    return ["[redacted-risky-file]" if risky_path(path) else path for path in out.splitlines()]


def collect(args: argparse.Namespace) -> dict[str, object]:
    if not is_git_repo():
        return {
            "repo_status": "not_git_repo",
            "diff_stat": "",
            "changed_files": [],
            "untracked_files": [],
            "diff_excerpt": "",
            "truncation_notice": "",
            "redaction_notice": [],
        }

    include_unstaged = not args.staged_only
    include_staged = not args.unstaged_only
    sections: list[str] = []
    files: list[str] = []
    notices: list[str] = []
    stats: list[str] = []
    untracked: list[str] = []

    if include_unstaged:
        code, stat, _ = run_git(["diff", "--stat"])
        safe_stat, stat_notices = sanitize_stat(stat if code == 0 else "")
        stats.append(safe_stat)
        notices.extend(stat_notices)
        code, diff, _ = run_git(["diff", "--unified=3"])
        safe_diff, diff_notices = sanitize_diff(diff if code == 0 else "")
        notices.extend(diff_notices)
        if safe_diff.strip():
            sections.append("## unstaged\n" + safe_diff)
        files.extend(changed_files(staged=False))
        untracked = untracked_files()
        files.extend(untracked)

    if include_staged:
        code, stat, _ = run_git(["diff", "--cached", "--stat"])
        safe_stat, stat_notices = sanitize_stat(stat if code == 0 else "")
        stats.append(safe_stat)
        notices.extend(stat_notices)
        code, diff, _ = run_git(["diff", "--cached", "--unified=3"])
        safe_diff, diff_notices = sanitize_diff(diff if code == 0 else "")
        notices.extend(diff_notices)
        if safe_diff.strip():
            sections.append("## staged\n" + safe_diff)
        files.extend(changed_files(staged=True))

    excerpt = "\n\n".join(sections).strip()
    truncation_notice = ""
    if len(excerpt) > args.max_chars:
        excerpt = excerpt[: args.max_chars].rstrip()
        truncation_notice = f"diff_excerpt truncated to {args.max_chars} chars"

    return {
        "repo_status": "ok",
        "diff_stat": "\n".join(part for part in stats if part.strip()),
        "changed_files": sorted(set(files)),
        "untracked_files": sorted(set(untracked)),
        "diff_excerpt": excerpt,
        "truncation_notice": truncation_notice,
        "redaction_notice": sorted(set(notices)),
    }


def print_text(data: dict[str, object]) -> None:
    for key in (
        "repo_status",
        "diff_stat",
        "changed_files",
        "untracked_files",
        "diff_excerpt",
        "truncation_notice",
        "redaction_notice",
    ):
        value = data[key]
        print(f"{key}:")
        if isinstance(value, list):
            for item in value:
                print(f"- {item}")
        else:
            print(value)
        print()


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect redacted git diff context.")
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--staged-only", action="store_true")
    parser.add_argument("--unstaged-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv))
    if args.staged_only and args.unstaged_only:
        parser.error("--staged-only and --unstaged-only cannot be used together")
    return args


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    data = collect(args)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_text(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
