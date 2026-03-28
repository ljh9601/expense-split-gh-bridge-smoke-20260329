# Project Facts

## Summary

- Project: `Expense Split Calculator`
- Repo slug: `expense-split-calculator`
- Mission: Friends often need to split meal or trip expenses, but the settlement math is commonly entered incorrectly by hand.

## Focus Areas

- security-sensitive flow

## Important Paths

- `README.md`
- `docs/architecture.md`
- `team/backlog/active.yaml`
- `team/reports/`
- `team/run-state/active-run.yaml`
- `team/run-state/runner-bridge.yaml`
- `team/run-state/runner-checkpoint.yaml`
- `team/run-state/runner-audit.jsonl`
- `team/run-state/run-ledger.jsonl`
- `team/policies/git-workflow.yaml`
- `team/policies/github-bridge.yaml`
- `team/policies/github-author.env.example`
- `team/policies/github-reviewer.env.example`
- `team/policies/runner-launch.yaml`
- `team/pull-requests/`
- `team/session-state/active-handoff.md`
- `team/session-state/runner-resume.yaml`
- `team/run-state/github-pr-bridge.yaml`
- `team/memory/decisions.jsonl`
- `docs/14-git-pr-workflow.md`

## Commands

- Quality gates: `./scripts/run-quality-gates.sh all`
- Review hygiene: `./scripts/run-quality-gates.sh review_hygiene`
- Git workflow guide: `docs/14-git-pr-workflow.md`
- GitHub PR preflight: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli github-pr-preflight /tmp/generated-project`
- GitHub PR sync: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli github-sync-packet-pr /tmp/generated-project --packet-id WP-001`
- Runner dispatch: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-dispatch-once /tmp/generated-project`
- Runner bridge: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-bridge-once /tmp/generated-project`
- Runner supervisor: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-supervisor-once /tmp/generated-project`
- Runner supervisor loop: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-supervisor-loop /tmp/generated-project --poll-interval-seconds 2 --max-cycles 60`
- Runner launch scaffold: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-launch-scaffold /tmp/generated-project --preset local-batch --overwrite`
- Runner service plan: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-plan /tmp/generated-project`
- Runner service plan for systemd: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-plan /tmp/generated-project --service-manager systemd --systemd-user-dir ~/.config/systemd/user`
- Runner service plan for system scope: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-plan /tmp/generated-project --service-manager systemd --service-scope system`
- Runner service install: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-install /tmp/generated-project --activate`
- Runner service install for systemd: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-install /tmp/generated-project --service-manager systemd --systemd-user-dir ~/.config/systemd/user`
- Runner service install for system scope: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-install /tmp/generated-project --service-manager launchd --service-scope system`
- Runner service package: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-package /tmp/generated-project`
- Runner service distribution: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli runner-service-distribution /tmp/generated-project --service-scope all`
- Resolve approval pause: `PYTHONPATH=src python3 -m agent_bootstrap_interface.cli resolve-approval-pause /tmp/generated-project --decision approved --next-gate ready-for-implementation --codex-verdict approved`
- Lint: `python3 -m compileall scripts`
- Typecheck: `python3 -m py_compile scripts/*.py`
- Unit test: `not configured yet`

## Stack Preferences

- Python 3.11+
- CLI-first structure
- JSON input support
- `unittest`

## Goals

- Calculate settlement results from a total set of participant payments.
- Show who owes whom and how much.
- Support both command-line input and JSON file input for the first milestone.

## Users

- A single user who wants to settle small group expenses quickly from the terminal.

## Use Cases

- Enter participant names and paid amounts directly on the command line.
- Load a JSON input file with participant data and calculate the result.
- Copy the settlement output into chat after the command runs.

## Constraints

- Local single-user CLI only.
- Prefer Python standard library first.
- Keep output terminal-friendly and straightforward to copy into chat.
- Document rounding behavior clearly in the README.

## Acceptance Criteria

- A CLI command can calculate settlement results from participant payment data.
- The same calculation works from a JSON input file.
- The result shows who should pay whom and how much.
- Rounding behavior and limitations are documented in `README.md`.
- Core calculation logic has automated tests.

## Integrations

- None

## Repo Inputs

- Start from a new repo.
- No existing codebase or external dataset is required.

## Autonomy Boundaries

- Do not add payment-provider integrations, wallets, or account systems automatically.
- Pause for approval before adding any non-stdlib dependency.
- Do not expand scope into web, mobile, or cloud features unless explicitly approved.

## Invariants

- Durable repo files are the source of truth, not chat history alone.
- Generated projects must preserve Codex as control plane and Claude as execution plane.
- Replace placeholder quality-gate commands before relying on unattended execution.
- Respect explicit non-goals and constraints unless a later architecture decision changes them.

## WP-001 Research Findings

- Use `decimal.Decimal` with string-based parsing for all money values and define one explicit rounding rule before implementation starts.
- Treat CLI arguments and JSON payloads as untrusted input. Apply allowlist validation, bounded sizes, and clear rejection paths for malformed data.
- Keep file input narrow in milestone one: regular local JSON files only, no symlink-following workflow, no user-controlled output paths.
- Preserve the accounting invariant that the final normalized settlement nets to zero after rounding.
- Carry the remaining open questions on rounding policy and duplicate-participant handling into `WP-002`.
