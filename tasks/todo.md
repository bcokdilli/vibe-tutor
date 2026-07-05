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

## Task: replace README cover with workflow infographic

### Steps
- [x] 1. Use the supplied CodexQB-style reference to design a text-readable workflow diagram.
- [x] 2. Add deterministic SVG source and render a README PNG asset.
- [x] 3. Remove the old AI-rendered cover, validate, and report commit/push status.

### Risks
- Generated bitmap diagrams can garble text, so this version uses SVG source rendered to PNG.

### Review (fill in when done)
- What changed: Replaced the README cover with `docs/assets/vibe-tutor-workflow.png` rendered from `docs/assets/vibe-tutor-workflow.svg`.
- How I verified it: Visually inspected the rendered PNG and ran `make check`.
- Side effect risk: Low; documentation asset only.

### Done?
- [x] Proved it works (test / log / output)
- [x] Showed the behavior diff to the user

## Task: clean README workflow icons

### Steps
- [x] 1. Remove visual icon clutter and overlap in the workflow infographic.
- [x] 2. Re-render the README PNG from the SVG source.
- [x] 3. Validate the repo checks.

### Risks
- The workflow image is documentation-only; product behavior is unchanged.

### Review (fill in when done)
- What changed: Simplified the workflow card icons, kept the validation lane removed, and aligned the title with the Vibe Tutor product name.
- How I verified it: Visually inspected `docs/assets/vibe-tutor-workflow.png` and ran `make check`.
- Side effect risk: Low; documentation asset only.

### Done?
- [x] Proved it works (test / log / output)
- [x] Showed the behavior diff to the user

## Task: apply open-source license

### Steps
- [x] 1. Choose a permissive license suitable for public reuse.
- [x] 2. Add license file and repo/plugin metadata.
- [x] 3. Validate, commit, push, and confirm GitHub recognizes it.

### Risks
- MIT is permissive and allows commercial/proprietary reuse; choose Apache-2.0 later only if explicit patent terms become important.

### Review (fill in when done)
- What changed: Added MIT license metadata.
- How I verified it: Plugin validation passed and the MIT license text check passed.
- Side effect risk: Low; license and docs metadata only.

### Done?
- [x] Proved it works (test / log / output)
- [x] Showed the behavior diff to the user

## Task: enrich public README, metadata, and validation

### Steps
- [x] 1. Expand the English README and plugin README without adding separate docs.
- [x] 2. Update public plugin metadata and GitHub repository description/topics.
- [x] 3. Add medium validation: Makefile, validation script, GitHub Action, and unit tests.
- [x] 4. Run checks, commit, push, and report the behavior diff.

### Risks
- README should stay product-focused without becoming a long tutorial.
- Validation should remain dependency-free and not require Codex local validator internals.

### Review (fill in when done)
- What changed: Expanded README surfaces, updated public plugin metadata, set GitHub description/topics, and added dependency-free validation with CI/unit tests.
- How I verified it: `make check`, plugin validator, skill validator, `git diff --check`, and GitHub metadata readback passed.
- Side effect risk: Low; no skill workflow semantics changed beyond documentation/metadata and validation infrastructure.

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
