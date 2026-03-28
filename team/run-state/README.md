# Run State

Use this directory for machine-readable execution state that should survive session resets.

Files:
- `active-run.yaml`: the current in-flight or next-to-run packet pointer.
- `run-ledger.jsonl`: append-only history of execution attempts, retries, and final outcomes.
- `runner-audit.jsonl`: append-only runner event stream for dispatch, pause, retry-escalation, and approval-resolution transitions.
- `runner-bridge.yaml`: latest outer-runner launch or resume attempt, including command, pid, log path, and failure details.
- `launches/`: runner-owned stdout or stderr logs emitted by `runner-bridge-once`.
- `launchers/`: repo-local launcher wrappers referenced by `team/policies/runner-launch.yaml`.
- `services/`: generated launch-agent plists, service bundles, distributions, and service logs for OS-level runner supervision wiring.

Recommended run id format:
- `RUN-20260327-001`

Rules:
- Keep `active-run.yaml` aligned with the packet currently in progress.
- Append a new JSON line to `run-ledger.jsonl` for each new attempt or retry.
- Append a new JSON line to `runner-audit.jsonl` for each meaningful runner-facing transition or pause.
- Rewrite `runner-bridge.yaml` on each launch or resume attempt instead of treating it as append-only history.
- Regenerate `launchers/` through `runner-launch-scaffold` when Codex or Claude CLI paths change on the local machine.
- Do not rely on chat history alone for execution history or approval state.
