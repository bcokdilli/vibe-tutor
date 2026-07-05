# Vibe Tutor

Vibe Tutor is a Codex skill/plugin for concise, diff-based tutoring. It helps beginners learn from the actual code changes Codex just made.

It does not generate long courses, document an entire codebase, replace learning to code, or prove that all criticism of vibe coding is wrong. The narrower claim is: agentic coding can be paired with concise, diff-based, just-in-time tutoring so beginners can gradually understand the code they are building.

## What It Does

- Reads the latest staged and unstaged git diff.
- Produces a short digest by default.
- Names changed files and symbols when available.
- Teaches at most three concepts from the actual change.
- Includes one self-check question.
- Reports whether tests, lint, or build verification is known.

## What It Does Not Do

- Generate broad programming courses.
- Explain the entire repository.
- Store personal learning state without an explicit request.
- Claim code is correct without verification evidence.

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
@vibe-tutor expand
```

The skill teaches from the latest staged and unstaged git diff. It is not a generic tutorial generator.

## Modes

| Mode | Output |
| --- | --- |
| `summary` | Default digest under 150 words unless detail is requested. |
| `quiz` | Three questions grounded in the latest diff. |
| `why <file or symbol>` | A short explanation of one changed file or symbol. |
| `next` | One tiny concept to learn next. |
| `expand` | A deeper explanation of one concept, still repo-grounded. |

## Verification Limits

Vibe Tutor can report tests, lint, or build results only when the current agent knows they ran. If no check ran, it must say the change was not verified by test/lint/build.

## Privacy Notes

`collect_diff_context.py` skips common risky filenames and redacts common secret-looking values, but it is not a full secret scanner. Keep secrets out of diffs and prompts.

## Utilities

```bash
python3 skills/vibe-tutor/scripts/collect_diff_context.py --json
python3 skills/vibe-tutor/scripts/evaluate_digest.py path/to/digest.md
```

Run repository validation from the repository root:

```bash
make check
```

## License

MIT. See the repository root `LICENSE`.
