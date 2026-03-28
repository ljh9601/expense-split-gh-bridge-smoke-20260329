# AGENTS.md

## Mission

This repository uses a layered autonomous collaboration model.

The human provides:
- an initial brief,
- constraints and non-goals,
- approvals only for destructive, externally privileged, production, or paid actions,
- policy decisions only when the checked-in context cannot safely resolve ambiguity.

The agent system provides:
- decomposition,
- architecture iteration,
- implementation,
- testing,
- review,
- security and performance checks when relevant,
- documentation sync,
- durable handoff and memory.

## Operating Model

This template separates responsibility into two planes.

Control plane:
- `Codex`
  - owns the queue,
  - issues or refines work packets,
  - decides when design is sufficiently mature,
  - reviews Claude's integrated output,
  - decides whether to iterate or move to the next task,
  - is the only actor allowed to declare a meaningful task closed.

Execution plane:
- `Claude main`
  - acts as execution manager,
  - receives the active work packet from Codex,
  - delegates bounded tasks to specialists,
  - integrates specialist outputs,
  - updates shared state and reports,
  - returns a concrete result to Codex,
  - must not self-approve closeout.

Specialist layer:
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

## Default Workflow

Follow this loop unless the repo or human explicitly overrides it.

1. Intake
   - restate the goal, constraints, and success criteria,
   - identify what is in and out of scope,
   - create or update the active backlog item.
2. Architecture loop
   - Codex and Claude refine architecture, workflow, and interfaces,
   - use `product-analyst` or `architect` when needed,
   - stop the loop when the chosen design is good enough to execute safely,
   - if the loop stalls, Codex decides after at most three serious rounds.
3. Work packet issue
   - Codex writes or approves a bounded work packet,
   - the work packet must define scope, owned files or surfaces, required artifacts, validation, and exit criteria.
4. Claude execution chain
   - gather references or repo context if needed,
   - clarify acceptance and scope when needed,
   - refine design details,
   - implement the smallest coherent change,
   - run security, performance, or UX evaluation when applicable,
   - run an independent code review,
   - update docs if behavior or operations changed.
5. Codex review
   - inspect the result,
   - either send concrete feedback for another cycle or approve moving forward.
6. Next-step selection
   - if more work remains, Codex selects or approves the next work packet,
   - if the milestone is complete, Codex records closure and refreshes handoff state.

## Git And PR Discipline

Treat each meaningful work packet as one logical PR.

- default branch: `main`
- packet branch pattern: `packet/<packet-id-lower>-<packet-slug>`
- logical PR author: Claude programmer lane
- final approver and merge owner: Codex
- PR body and review comment language: Korean

Every packet closeout should leave:
- a local PR body under `team/pull-requests/`,
- a local PR metadata file,
- a Codex review comment artifact,
- a merge result that matches the packet verdict.

When `team/policies/github-bridge.yaml` is enabled:
- publish PRs with the author account from `team/policies/github-author.env.local`,
- post approval and merge with the reviewer account from `team/policies/github-reviewer.env.local`,
- fail closed if the two GitHub identities resolve to the same login.

Use `docs/14-git-pr-workflow.md` and `team/policies/git-workflow.yaml` as the source of truth.

## Shared State Files

Do not rely on chat transcripts as the only memory.
These files are the durable source of truth:

- `team/backlog/active.yaml`
  - active milestones, queue, and current work packet pointer.
- `team/session-state/active-handoff.md`
  - current objective, phase, next actions, and open risks.
- `team/session-state/next-session-prompt.md`
  - minimal resume prompt for the next session.
- `team/memory/project-facts.md`
  - stable facts, invariants, commands, and boundaries.
- `team/memory/decisions.jsonl`
  - one decision record per line for significant design or policy choices.
- `docs/09-work-log.md`
  - chronological history of meaningful work and repair loops.

Keep these current during long or multi-cycle tasks.

## Required Artifacts

Every non-trivial task should leave durable artifacts.

Codex-side artifacts:
- active backlog entry,
- approved work packet,
- updated handoff,
- final review result or next-step decision.

Claude-side artifacts:
- research note when external references or source-backed guidance mattered,
- design brief when architecture or interfaces changed,
- implementation summary through changed files and validation evidence,
- verification report,
- independent review report,
- docs updates when behavior or operations changed.

Use the checked-in templates in `team/contracts/`.

## Task Decomposition Rules

Every delegated task must include:
- objective,
- scope boundary,
- owned files or surfaces,
- expected artifact,
- validation expectation,
- handoff format.

Parallelize only when file ownership is disjoint.
Do not assign the same file set to multiple writers.

Preferred parallel lanes after implementation starts:
- `security-manager`
- `performance-engineer`
- `docs-curator`
- `code-reviewer`

Keep research, architecture, and first-pass implementation sequential unless the packet explicitly defines disjoint ownership.

## Role Activation Matrix

Use these activation heuristics:

- `researcher`
  - external references,
  - current docs or standards,
  - vendor or tool behavior checks,
  - source-backed landscape scans.
- `product-analyst`
  - ambiguous asks,
  - missing acceptance criteria,
  - rollout or edge-case discovery,
  - packet splitting or scope control.
- `architect`
  - new features,
  - refactors,
  - interface or schema changes,
  - dependency boundaries,
  - migration planning.
- `ui-designer`
  - UX flows,
  - information architecture,
  - accessibility-sensitive interaction work,
  - visual direction changes.
- `programmer`
  - code, config, script, and test implementation.
- `tester`
  - every non-trivial behavior change,
  - bug fixes,
  - regression-prone work.
- `security-manager`
  - auth,
  - secrets,
  - external APIs,
  - untrusted input,
  - file permissions,
  - supply-chain or dependency risk.
- `performance-engineer`
  - hot paths,
  - fanout,
  - concurrency,
  - memory, latency, or scale-sensitive work.
- `docs-curator`
  - public interface changes,
  - operator workflow changes,
  - onboarding or runbook drift.
- `code-reviewer`
  - every non-trivial change before Codex closeout.

## Non-Negotiable Gates

Do not close meaningful work unless all applicable gates are satisfied:
- the active work packet is complete or explicitly narrowed,
- targeted validation ran or a blocker is documented,
- review happened,
- docs were updated when behavior changed,
- security review happened for risky changes,
- performance review happened for performance-sensitive changes,
- handoff and work-log state are current,
- residual risks are explicit.

Codex is the gatekeeper for:
- architecture signoff,
- scope expansion,
- milestone closure,
- final closeout of a meaningful task.

## Auto-Approval Boundary

Assume repo-local inspection, editing, formatting, testing, and non-destructive git work are allowed unless the checked-in policy says otherwise.

Interrupt the human only when:
- a destructive action is required,
- a new secret or login is required,
- a production or paid side effect is required,
- legal or compliance interpretation is required,
- repeated repair loops still cannot produce a safe result,
- the repo contains multiple materially different product directions and the files do not justify one choice.

Project-specific unattended rules should live in `team/policies/auto-approval.yaml`.

## Session Continuity

Refresh handoff state before:
- an intentional session reset,
- a long pause,
- another broad implementation or review batch,
- closing a session with unfinished work,
- or when context quality starts to degrade.

The next session should be able to:
- identify the current objective,
- see the current work packet and next gate,
- reopen only the files that matter,
- know what validation already ran,
- continue without asking the human to choose among routine next steps.

## Self-Improvement Loop

After each meaningful task, ask:
- what had to be rediscovered,
- what should become a permanent gate,
- what report or memory file was missing,
- what skill, hook, test, or script would reduce repeat friction,
- whether the current role set is too broad or too fragmented.

Codify repeated friction in this order:
1. docs or `AGENTS.md`
2. contract template
3. skill
4. test or validation command
5. hook or automation
6. new specialist role
