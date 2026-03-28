# Architecture Seed

## Brief

- Title: Expense Split Calculator
- Problem: Friends often need to split meal or trip expenses, but the settlement math is commonly entered incorrectly by hand.

## Focus Areas

- security-sensitive flow

## Goals

- Calculate settlement results from a total set of participant payments.
- Show who owes whom and how much.
- Support both command-line input and JSON file input for the first milestone.

## Non-Goals

- Do not integrate with payment providers.
- Do not add user accounts or authentication.
- Do not build a web UI in the first milestone.

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

## Autonomy Boundaries

- Do not add payment-provider integrations, wallets, or account systems automatically.
- Pause for approval before adding any non-stdlib dependency.
- Do not expand scope into web, mobile, or cloud features unless explicitly approved.

## Artifact Boundaries

- `team/reports/WP-001-bundle.yaml` is the packet-level index for first-cycle report paths.
- `team/run-state/active-run.yaml` tracks the current or next run without relying on chat context.
- `team/run-state/runner-bridge.yaml` stores the latest outer-runner launch or resume attempt, including command, pid, log path, and failure details.
- `team/run-state/github-pr-bridge.yaml` stores the latest GitHub PR publication, review, and merge result when split-account bridge publication is enabled.
- `team/run-state/runner-checkpoint.yaml` is the runner-owned checkpoint for pause, approval, and resume state.
- `team/run-state/run-ledger.jsonl` is the append-only execution history for retries and approvals.
- `team/session-state/runner-resume.yaml` is the runner-to-session resume envelope for the next actor and action.

## Bootstrap Goal

Generate a repo that starts with durable backlog, memory, handoff, and work-packet files already aligned to the user's brief.

## Kernel Responsibilities

- parse the brief,
- derive a first milestone and packet queue,
- seed durable state files into a target root,
- leave Codex/Claude ready to continue autonomously.

## Initial Packets

- `WP-001`: Research security-sensitive flow references and constraints
- `WP-002`: Design the security-sensitive flow architecture and milestone contract
- `WP-003`: Implement the security-sensitive flow slice
- `WP-004`: Verify security-sensitive flow behavior and operator readiness
- `WP-005`: Review the security-sensitive flow milestone and prepare the next handoff
