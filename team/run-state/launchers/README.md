# Runner Launchers

Use this directory for repo-local launcher wrappers referenced by `team/policies/runner-launch.yaml`.

Examples:
- `codex-local-batch.sh`: runs Codex in a non-interactive batch mode using the generated prompt file.
- `claude-local-batch.sh`: runs Claude Code in print mode using the generated prompt file and resume envelope.
- `rehearsal-fake-*.py`: test launchers that simulate Codex or Claude closeout during unattended rehearsal.

Rules:
- Treat these files as runner-owned support artifacts, not packet truth.
- Regenerate wrappers through `runner-launch-scaffold` instead of editing paths by hand in every repo.
- Keep actor profiles in `team/policies/runner-launch.yaml` aligned with the wrappers that live here.
