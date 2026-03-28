---
name: team-docs-curator
description: Use for keeping architecture docs, runbooks, onboarding notes, changelogs, operator instructions, work logs, and handoff files aligned with the latest behavior.
---

# Team Docs Curator

Use when:
- behavior changed,
- setup or operations changed,
- public interfaces changed,
- the repo needs durable continuity after a work cycle.

## First Steps

1. Read `AGENTS.md` and `team/config.yaml` if present.
2. Read the active work packet and touched code or tests.
3. Read `references/docs-delta-checklist.md`.

## Workflow

1. Map behavior changes to the exact docs surfaces they affect.
2. Update only the docs that actually drifted.
3. Keep `docs/09-work-log.md` current for meaningful work.
4. Refresh `team/session-state/active-handoff.md` and `team/session-state/next-session-prompt.md` when continuity is part of the task.
5. Update `team/memory/project-facts.md` if a durable fact changed.

## Output

Return:
- docs changed,
- why each doc changed,
- whether any expected doc update was intentionally unnecessary,
- handoff or memory updates made.

## Guardrails

- Do not create broad docs churn for a narrow patch.
- Keep docs concrete and operational.
- If behavior changed and no doc needs updating, say why.
