# Shared State Files

## Goal

Make session resets cheap and make multi-agent work auditable.

## Files

- `team/backlog/active.yaml`
  - current milestones, queue, and active work packet id.
- `team/contracts/`
  - templates for packet and report artifacts.
- `team/memory/project-facts.md`
  - stable facts, boundaries, commands, and invariants.
- `team/memory/decisions.jsonl`
  - append-only decision ledger.
- `team/session-state/active-handoff.md`
  - current task snapshot and exact next steps.
- `team/session-state/next-session-prompt.md`
  - minimal resume prompt for the next session.
- `docs/09-work-log.md`
  - chronological execution log with evidence.

## Rules

- If a fact will matter next session, write it down.
- If a decision changed scope or architecture, append it.
- If the queue changed, update the backlog.
- If a packet is active, reference it from the handoff.
- If a review or verification happened, store the artifact path in the report or backlog.
