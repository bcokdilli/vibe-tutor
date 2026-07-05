from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "plugins/vibe-tutor/skills/vibe-tutor/scripts/collect_diff_context.py"

spec = importlib.util.spec_from_file_location("collect_diff_context", SCRIPT)
assert spec and spec.loader
collect_diff_context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collect_diff_context)


class CollectDiffContextTests(unittest.TestCase):
    def test_redacts_secret_like_assignments(self) -> None:
        redacted, changed = collect_diff_context.redact_line("+ API_TOKEN=abc123def456")
        self.assertTrue(changed)
        self.assertIn("[REDACTED]", redacted)
        self.assertNotIn("abc123def456", redacted)

    def test_sanitizes_risky_diff_file(self) -> None:
        diff = """diff --git a/.env b/.env
index 123..456 100644
--- a/.env
+++ b/.env
@@ -1 +1 @@
-TOKEN=old
+TOKEN=new
"""
        output, notices = collect_diff_context.sanitize_diff(diff)
        self.assertIn("[redacted-risky-file]", output)
        self.assertNotIn("TOKEN=new", output)
        self.assertTrue(notices)

    def test_not_git_repo_json_is_graceful(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--json"],
                cwd=tmpdir,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["repo_status"], "not_git_repo")


if __name__ == "__main__":
    unittest.main()
