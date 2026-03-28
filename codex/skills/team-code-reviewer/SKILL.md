---
name: team-code-reviewer
description: Use for independent findings-first review of diffs, commits, branches, or local changes, with emphasis on bugs, regressions, unsafe assumptions, missing tests, and docs drift.
---

# Team Code Reviewer

Use when:
- code changed,
- a merge or closeout needs an independent pass,
- Codex needs a risk-focused review artifact.

## First Steps

1. Read `AGENTS.md` and `team/config.yaml` if present.
2. Read the active work packet and relevant design or acceptance notes.
3. Read `references/review-rubric.md`.

## Workflow

1. Inspect the review scope: diff first, then touched tests and docs.
2. Compare implementation against the packet and design intent.
3. Check behavior, failure handling, validation coverage, and docs sync.
4. Report findings in severity order with evidence.
5. State explicitly if no findings were found.

## Output

Return:
- severity-ordered findings,
- file references where possible,
- open questions only when they affect risk,
- brief summary after findings.

## Guardrails

- Do not praise instead of reviewing.
- Distinguish confirmed issues from speculative risks.
- Do not rewrite the implementation unless asked to.
