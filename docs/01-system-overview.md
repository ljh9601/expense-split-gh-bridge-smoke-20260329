# System Overview

## Goal

Provide a reusable scaffold for projects where:
- the human supplies the initial brief,
- Codex steers the project as control plane,
- Claude executes work through specialists,
- shared state files preserve progress across session resets.

## Why This Shape

A single long-running prompt degrades because:
- too much mixed context accumulates,
- task ownership becomes blurry,
- review and validation start getting skipped,
- session resets destroy tacit memory.

This template counters that by separating:
- control and acceptance,
- execution and delegation,
- implementation and review,
- live chat and durable state.

## Core Components

- `AGENTS.md`
  - Codex-side constitution and gate policy.
- `CLAUDE.md`
  - execution-manager protocol for Claude main.
- `team/backlog/active.yaml`
  - queue and active work packet pointer.
- `team/contracts/`
  - standardized artifacts.
- `team/memory/`
  - stable facts and decision history.
- `team/session-state/`
  - current resume state.

## Operating Philosophy

- Keep Codex focused on decisions, integration, and review.
- Keep Claude focused on bounded execution and reporting.
- Keep specialists narrow and reusable.
- Keep meaningful progress in files, not only in prompts.
- Treat review and validation as required gates, not cleanup.
