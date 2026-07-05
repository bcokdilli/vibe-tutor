## Task: vibe-tutor local skill and plugin scaffold

### Steps
- [x] 1. Create plugin manifest, marketplace entry, README, and ignore files.
- [x] 2. Create the vibe-tutor skill, scripts, and reference files.
- [x] 3. Run validation commands and record the behavior diff.

### Risks
- Plugin availability still depends on Codex loading the repo marketplace.
- The digest helper can redact common secret-like values, but it is not a full secret scanner.

### Review (fill in when done)
- What changed: Added a local `vibe-tutor` Codex plugin scaffold, skill, stdlib scripts, references, README, marketplace entry, and tiny AGENTS note.
- How I verified it: Ran Python syntax checks, skill validation, plugin validation, JSON diff collection, and sample digest evaluation.
- Side effect risk: Low; files are new and the only root-level changes are `.gitignore`, `.agents/plugins/marketplace.json`, `AGENTS.md`, and this task log.

### Done?
- [x] Proved it works (test / log / output)
- [x] Showed the behavior diff to the user

## Task: publish vibe-tutor as public GitHub marketplace repo

### Steps
- [x] 1. Align marketplace name and README install commands for public GitHub distribution.
- [x] 2. Re-run plugin, skill, JSON, and secret-pattern checks.
- [x] 3. Commit, create the public GitHub repo, and push.

### Risks
- Public repo availability does not mean the plugin is installed for any user.
- No open-source license file was added; reuse rights remain unspecified unless added later.

### Review (fill in when done)
- What changed: Added root README and changed marketplace name to `vibe-tutor`.
- How I verified it: Plugin validation, skill validation, JSON validation, secret-pattern scan, public repo creation, and push passed.
- Side effect risk: Low; public-facing metadata and docs only.

### Done?
- [x] Proved it works (test / log / output)
- [x] Showed the behavior diff to the user
