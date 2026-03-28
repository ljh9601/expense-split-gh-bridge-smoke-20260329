# Session Continuity

## Goal

The next session should resume from files, not from “continue from above”.

## Durable State Files

Use these files together:

- `team/backlog/active.yaml`
  - current queue, milestone state, and active work packet id.
- `team/session-state/active-handoff.md`
  - current snapshot of active work.
- `team/session-state/next-session-prompt.md`
  - immediate resume prompt.
- `team/memory/project-facts.md`
  - durable repo facts and boundaries.
- `team/memory/decisions.jsonl`
  - key design or policy decisions.
- `docs/09-work-log.md`
  - chronological history of meaningful progress and repair loops.

## When To Refresh Handoff State

Refresh the handoff before:
- an intentional session reset,
- a long pause,
- starting another broad implementation or review batch,
- closing the session with unfinished work,
- or when context quality starts to degrade.

## Handoff Quality Standard

The handoff should be good enough that a new session can:
- identify the current objective,
- identify the active work packet and next gate,
- understand what already changed,
- avoid rereading the entire repo blindly,
- know what validation already ran,
- continue without asking the human to choose among routine next steps.

## Recommended Resume Order

1. Read `AGENTS.md`.
2. Read `CLAUDE.md` if the session is Claude-driven.
3. Read `team/config.yaml` if present.
4. Read `team/backlog/active.yaml`.
5. Read `team/memory/project-facts.md`.
6. Read `team/session-state/active-handoff.md`.
7. Read the latest entries in `docs/09-work-log.md`.
8. Reopen only the files named by the handoff or active work packet.

## Anti-Patterns

Avoid these:
- relying on “continue from above” as the only handoff,
- leaving next steps only in chat,
- losing the current work packet id,
- storing decisions in prose without a durable record,
- asking the human to choose the next routine step when the checked-in state already supports a default.
