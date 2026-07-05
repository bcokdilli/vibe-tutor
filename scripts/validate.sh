#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PLUGIN_ROOT="plugins/vibe-tutor"
SKILL_ROOT="$PLUGIN_ROOT/skills/vibe-tutor"
TMPDIR_VALIDATE="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_VALIDATE"' EXIT

python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
python3 -m json.tool "$PLUGIN_ROOT/.codex-plugin/plugin.json" >/dev/null
python3 -m py_compile "$SKILL_ROOT/scripts/collect_diff_context.py" "$SKILL_ROOT/scripts/evaluate_digest.py"

python3 - <<'PY'
from pathlib import Path
import json
import sys

plugin = json.loads(Path("plugins/vibe-tutor/.codex-plugin/plugin.json").read_text(encoding="utf-8"))
marketplace = json.loads(Path(".agents/plugins/marketplace.json").read_text(encoding="utf-8"))

errors = []
if plugin.get("name") != "vibe-tutor":
    errors.append("plugin name must be vibe-tutor")
if plugin.get("author", {}).get("name") != "Bahadir Cokdilli":
    errors.append("author name must be Bahadir Cokdilli")
if "email" in plugin.get("author", {}):
    errors.append("author email should not be published")
if plugin.get("homepage") != "https://github.com/bcokdilli/vibe-tutor":
    errors.append("homepage must point to the public repository")
if plugin.get("repository") != "https://github.com/bcokdilli/vibe-tutor":
    errors.append("repository must point to the public repository")
if plugin.get("license") != "MIT":
    errors.append("license must be MIT")
if plugin.get("interface", {}).get("developerName") != "Bahadir Cokdilli":
    errors.append("developerName must be Bahadir Cokdilli")
if marketplace.get("name") != "vibe-tutor":
    errors.append("marketplace name must be vibe-tutor")

required_keywords = {"codex", "codex-plugin", "codex-skill", "vibe-coding", "learning", "diff", "developer-tools", "ai-coding"}
missing = sorted(required_keywords.difference(plugin.get("keywords", [])))
if missing:
    errors.append("missing keywords: " + ", ".join(missing))

if errors:
    print("metadata_validation_failed")
    for error in errors:
        print(error)
    sys.exit(1)
PY

cat >"$TMPDIR_VALIDATE/sample.digest.md" <<'EOF'
## Ne değişti?
- `plugins/vibe-tutor/skills/vibe-tutor/SKILL.md` now teaches from the latest diff.

## Neden önemli?
- The lesson stays tied to actual code changes instead of becoming a generic tutorial.

## Öğrenilecek kavramlar
1. Git diff: the changed lines since the last committed version.
2. Trigger scope: the rules that decide when a skill activates.

## Kodda nereye bakmalı?
- `plugins/vibe-tutor/skills/vibe-tutor/SKILL.md`

## Kendini test et
- Why should this skill avoid explaining the whole codebase?

## Doğrulama durumu
- Bu değişiklik test/lint/build ile doğrulanmadı.
EOF

python3 "$SKILL_ROOT/scripts/evaluate_digest.py" "$TMPDIR_VALIDATE/sample.digest.md" --json >"$TMPDIR_VALIDATE/eval.json"
python3 -m json.tool "$TMPDIR_VALIDATE/eval.json" >/dev/null
python3 "$SKILL_ROOT/scripts/collect_diff_context.py" --json >"$TMPDIR_VALIDATE/diff.json"
python3 -m json.tool "$TMPDIR_VALIDATE/diff.json" >/dev/null

python3 -m unittest discover -s tests -v

python3 - <<'PY'
from pathlib import Path
import re
import subprocess
import sys

listed = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], check=True, capture_output=True).stdout
paths = [Path(item.decode("utf-8")) for item in listed.split(b"\0") if item]

patterns = [
    ("openai_api_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("github_legacy_pat", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", re.compile(r"BEGIN (?:RSA|OPENSSH|DSA|EC|PRIVATE) KEY")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
]

findings = []
for path in paths:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for line_number, line in enumerate(text.splitlines(), start=1):
        for name, pattern in patterns:
            if pattern.search(line):
                findings.append(f"{path}:{line_number}: {name}")

if findings:
    print("secret_pattern_scan_failed")
    for finding in findings:
        print(finding)
    sys.exit(1)
PY

echo "validation passed"
