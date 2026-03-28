# Claude Compatibility

## Mapping

This template is Codex-first but explicitly supports Claude Code:

- `AGENTS.md`
  - Codex-side operating constitution
- `CLAUDE.md`
  - Claude main execution-manager protocol
- `codex/skills/*/SKILL.md`
  - source-of-truth specialist behavior
- `.claude/agents/*.md`
  - Claude Code subagent definitions
- `.claude/skills/*/SKILL.md`
  - mirrored project skills for Claude Code

## Why Both Layers Matter

Use `AGENTS.md` to define control-plane policy and final approval rules.
Use `CLAUDE.md` to define how Claude main decomposes, delegates, and reports.
Use subagents and skills only for bounded execution work.

This avoids three common failure modes:
- Claude acting like the final approver,
- Codex losing execution detail,
- durable project state living only in chat.

## Claude Hook Recommendation

Use project-level hooks only when a rule must fire every time.
The shipped baseline config keeps one mandatory safety hook:

- `PreToolUse` for blocking destructive shell patterns.

Add stronger hooks only after project-specific commands are stable:
- `TaskCompleted` for “do not mark done until required gates pass”,
- `SubagentStop` for collecting structured artifacts,
- `InstructionsLoaded` for verifying required state files were loaded.

## Cross-Platform Recommendation

Keep source of truth in versioned project files:
- `AGENTS.md`
- `CLAUDE.md`
- `team/config.yaml`
- `team/backlog/active.yaml`
- `team/memory/`
- `codex/skills/`
- `.claude/agents/`

Then use scripts to mirror or refresh generated state.
