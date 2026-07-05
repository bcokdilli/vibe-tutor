from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "plugins/vibe-tutor/skills/vibe-tutor/scripts/evaluate_digest.py"

spec = importlib.util.spec_from_file_location("evaluate_digest", SCRIPT)
assert spec and spec.loader
evaluate_digest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate_digest)


VALID_DIGEST = """## Ne değişti?
- `file.py` changed one small behavior.

## Neden önemli?
- The change is easier to inspect from the diff.

## Öğrenilecek kavramlar
1. Diff: a focused view of changed lines.
2. Validation: proof from tests or checks.

## Kodda nereye bakmalı?
- `file.py`

## Kendini test et
- What evidence would prove this change works?

## Doğrulama durumu
- Bu değişiklik test/lint/build ile doğrulanmadı.
"""


class EvaluateDigestTests(unittest.TestCase):
    def test_accepts_valid_short_digest(self) -> None:
        result = evaluate_digest.evaluate(VALID_DIGEST, max_words=150)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["concept_count"], 2)

    def test_rejects_banned_overclaim(self) -> None:
        result = evaluate_digest.evaluate(VALID_DIGEST + "\nperfect\n", max_words=150)
        self.assertFalse(result["ok"])
        self.assertTrue(any("perfect" in failure for failure in result["failures"]))

    def test_rejects_too_many_concepts(self) -> None:
        digest = VALID_DIGEST.replace(
            "2. Validation: proof from tests or checks.",
            "2. Validation: proof from tests or checks.\n3. Scope: keep the lesson narrow.\n4. Parser: extract structure safely.",
        )
        result = evaluate_digest.evaluate(digest, max_words=150)
        self.assertFalse(result["ok"])
        self.assertTrue(any("concept count" in failure for failure in result["failures"]))

    def test_rejects_long_code_fence(self) -> None:
        code = "```python\n" + "\n".join(f"line_{index} = {index}" for index in range(13)) + "\n```"
        result = evaluate_digest.evaluate(VALID_DIGEST + "\n" + code, max_words=300)
        self.assertFalse(result["ok"])
        self.assertTrue(any("code fence" in failure for failure in result["failures"]))


if __name__ == "__main__":
    unittest.main()
