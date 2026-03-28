# Agentic Team Template

Reusable bootstrap scaffold for a Codex-led, Claude-executed project workflow.

This template is designed for the operating model below:
- the human provides the initial brief, constraints, and approvals when safety or cost requires it,
- `Codex` acts as the control plane and final reviewer,
- `Claude` acts as the execution plane and manages specialist subagents,
- durable project state lives in files so work survives session resets.

## Team Shape

Control plane:
- `Codex`
  - clarifies goals,
  - decides the next meaningful work packet,
  - approves architecture and closeout,
  - reviews Claude's integrated output.

Execution plane:
- `Claude main`
  - receives a work packet from Codex,
  - chooses the right subagents,
  - runs the execution chain,
  - updates shared state and reports back.

Specialists:
- `researcher`
- `product-analyst`
- `architect`
- `ui-designer`
- `programmer`
- `tester`
- `security-manager`
- `performance-engineer`
- `docs-curator`
- `code-reviewer`

Default execution order inside Claude:
1. research and reference gathering when needed
2. scope clarification when needed
3. design refinement
4. implementation
5. security, performance, or UX evaluation when applicable
6. independent review
7. report back to Codex

## Layout

- `AGENTS.md`: Codex-side operating constitution and final approval rules.
- `CLAUDE.md`: Claude-side execution-manager protocol.
- `team/config.example.yaml`: project-specific knobs to fill in per repo.
- `team/backlog/active.yaml`: durable queue, milestones, and active work packet pointer.
- `team/contracts/`: templates for work packets, design briefs, verification reports, and review reports.
- `team/pull-requests/`: packet-level local PR artifacts with Korean body and review-comment conventions.
- `team/memory/`: durable facts and decisions that survive session resets.
- `team/policies/auto-approval.example.yaml`: what unattended work is allowed to proceed without asking.
- `team/policies/git-workflow.yaml`: default branch, packet branch, and merge conventions for unattended local work.
- `team/reports/`: cycle reports and other generated artifacts.
- `team/run-state/`: active run pointer and append-only ledger for execution attempts.
- `team/session-state/`: active handoff and next-session prompt files.
- `codex/skills/`: source-of-truth skills for Codex-style sessions.
- `.claude/agents/`: Claude Code specialist definitions.
- `.claude/skills/`: mirrored project skills for Claude Code.
- `.github/workflows/agentic-quality-gates.yml`: baseline CI gate workflow.
- `docs/`: operating notes and rationale.
- `scripts/bootstrap_agentic_project.py`: copy this scaffold into a new project root.
- `scripts/init_team_config.py`: generate `team/config.yaml`, `team/quality-gates.env`, and any missing state files.
- `scripts/refresh_session_handoff.py`: refresh handoff files and optionally append a work-log entry.
- `scripts/run-quality-gates.sh`: run review-hygiene, tests, and security checks locally or in CI.

## Recommended Adoption Flow

1. For a brand-new repo, run `python3 scripts/bootstrap_agentic_project.py your-project`.
   By default this creates the repo at `<template-parent>/<project-name>`.
   Override the parent with `AGENTIC_PROJECTS_ROOT=/some/path` or use `--target-root` explicitly.
2. For a repo that already has this scaffold checked in, run `python3 scripts/init_team_config.py --project-root /path/to/project --project-name your-project`.
3. Fill `team/config.yaml`, `team/backlog/active.yaml`, `team/memory/project-facts.md`, `team/run-state/active-run.yaml`, and `team/policies/auto-approval.yaml` with repo-specific reality.
4. Keep architecture decisions in docs or ADRs, and link the current one from the active work packet.
5. Install or refresh Codex skills with `./scripts/install-codex-skills`.
6. If you also use Claude Code, mirror the same skills with `./scripts/sync-claude-skills`.
7. Run `./scripts/run-quality-gates.sh all` locally and wire the same script into CI.
8. Use `python3 scripts/refresh_session_handoff.py ...` whenever a session grows crowded or pauses.
9. Prefer work packets and report files over long conversational context.

## Design Principles

- Codex owns control, priorities, acceptance, and final closure.
- Claude owns execution planning, subagent selection, and integrated delivery.
- Shared state lives in versioned files, not only in chat.
- Packet reports and execution attempts should be traceable through `team/reports/` and `team/run-state/`.
- Review is independent from implementation.
- Every non-trivial task should move through an explicit gate.
- Unattended work must follow a checked-in policy.
- Repeated friction should become docs, skills, tests, hooks, or scripts.
