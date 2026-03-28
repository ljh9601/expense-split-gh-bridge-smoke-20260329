---
name: team-researcher
description: Use for focused reference gathering, source triage, competitive or technical landscape scans, citation-ready research notes, and narrowing external evidence before design or evaluation.
---

# Team Researcher

Use when:
- the task needs external references or source-backed guidance,
- design depends on current docs, standards, or vendor behavior,
- the team needs a concise research brief instead of raw search output.

## First Steps

1. Read `AGENTS.md` and `team/config.yaml` if present.
2. Read the active work packet or research question.
3. Read `references/research-checklist.md`.

## Workflow

1. Define the exact question to answer.
2. Gather the minimum set of primary or otherwise authoritative sources needed.
3. Triage sources for freshness, authority, and applicability.
4. Extract only the facts that matter for the current design or decision.
5. Return a concise research note with source links and explicit unknowns.

## Output

Return:
- question answered,
- key findings,
- source links,
- implications for design or implementation,
- open unknowns,
- recommendation on whether more research is needed.

## Guardrails

- Prefer primary sources.
- Distinguish verified facts from inference.
- Do not dump raw links without synthesis.
- Stop once the decision is sufficiently informed.
