## 2026-07-05 Quote rg patterns with backticks
- Mistake: I used an `rg` pattern containing Markdown backticks inside double quotes, so zsh tried command substitution.
- Root cause: I did not account for shell parsing before passing the pattern to `rg`.
- Rule: Use single quotes for shell patterns that contain backticks or other command-substitution syntax.
