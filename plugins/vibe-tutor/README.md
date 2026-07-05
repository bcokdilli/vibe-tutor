# Vibe Tutor

Vibe Tutor is a local Codex skill/plugin scaffold for concise, diff-based tutoring. It helps beginners learn from the actual code changes Codex just made.

It does not generate long courses, document an entire codebase, replace learning to code, or prove that all criticism of vibe coding is wrong. The narrower claim is: agentic coding can be paired with concise, diff-based, just-in-time tutoring so beginners can gradually understand the code they are building.

## Local Install

This repo exposes the plugin through `.agents/plugins/marketplace.json`.

From the repo root, add the repo marketplace if your Codex app does not discover it automatically:

```bash
codex plugin marketplace add .
codex plugin add vibe-tutor@vibe-tutor
```

Then install or enable `vibe-tutor` from the local marketplace. Start a new Codex thread if the plugin list does not refresh immediately.

## Usage

Call it only when you want to learn from recent code changes:

```text
@vibe-tutor summary
@vibe-tutor quiz
@vibe-tutor why src/path/file.ts
@vibe-tutor next
```

The skill teaches from the latest staged and unstaged git diff. It is not a generic tutorial generator.

## Verification Limits

Vibe Tutor can report tests, lint, or build results only when the current agent knows they ran. If no check ran, it must say the change was not verified by test/lint/build.

## Utilities

```bash
python3 skills/vibe-tutor/scripts/collect_diff_context.py --json
python3 skills/vibe-tutor/scripts/evaluate_digest.py path/to/digest.md
```
