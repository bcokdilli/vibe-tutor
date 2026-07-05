# Optional Learning State

Only create `.vibe-tutor/learning_state.json` when the user explicitly asks to store or resume learning state.

```json
{
  "known_concepts": [],
  "weak_concepts": [],
  "recent_lessons": [
    {
      "date": "YYYY-MM-DD",
      "task": "...",
      "files": [],
      "concepts": [],
      "verification": "tests passed | not verified | lint passed | build passed"
    }
  ]
}
```

Rules:

- Keep only the last 20 lessons.
- Do not commit the file.
- Do not store sensitive project details.
- Do not store personal psychological notes.
- Keep entries terse and based on the user's explicit request.
