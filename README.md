# Vibe Tutor

Vibe Tutor is a Codex plugin and skill for concise, diff-based tutoring from the actual code changes Codex just made.

It is not a long tutorial generator and does not claim that users can become software engineers without learning to code. Its narrower claim is: agentic coding can be paired with concise, diff-based, just-in-time tutoring so beginners can gradually understand the code they are building.

## Install From This Marketplace

```bash
codex plugin marketplace add bcokdilli/vibe-tutor
codex plugin add vibe-tutor@vibe-tutor
```

Start a new Codex thread after installing so the skill metadata is picked up.

## Use

```text
@vibe-tutor summary
@vibe-tutor quiz
@vibe-tutor why src/path/file.ts
@vibe-tutor next
```

See `plugins/vibe-tutor/README.md` for plugin details and local development notes.

## License

MIT. See `LICENSE`.
