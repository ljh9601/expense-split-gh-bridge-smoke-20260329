# Control Plane And Execution Plane

## Purpose

This template deliberately splits the project loop into:
- a control plane run by Codex,
- an execution plane run by Claude.

The split exists to keep approval, priority, and critique independent from implementation.

## Codex Responsibilities

- interpret the human brief,
- own backlog priority,
- drive architecture convergence,
- issue or approve work packets,
- review Claude's integrated result,
- decide whether to iterate or move on,
- maintain handoff quality across Codex session resets.

## Claude Responsibilities

- receive the active work packet,
- choose the right specialists,
- gather missing references or repo context,
- execute the work in the required sequence,
- integrate subagent outputs,
- update reports and shared state,
- maintain handoff quality across Claude session resets.

## Why This Is Better Than A Flat Agent Swarm

- one final approver reduces self-confirmation bias,
- one execution manager keeps specialist work coherent,
- state files replace fragile conversational memory,
- work packets prevent vague “just continue” behavior.
