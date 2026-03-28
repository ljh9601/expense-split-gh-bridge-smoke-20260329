# Research Notes

This template is grounded in current official Anthropic and OpenAI guidance and case studies.

## Key Findings

1. Claude Code subagents are most effective when they are narrow, reusable, and have separate context windows with restricted tools.
Source: [Create custom subagents](https://docs.claude.com/en/docs/claude-code/subagents)

2. Claude hooks can enforce lifecycle gates around tool use, subagent execution, and task completion. That makes them suitable for mandatory checks like destructive-command blocking or test-before-close policies.
Source: [Hooks reference](https://code.claude.com/docs/en/hooks)

3. Anthropic's internal Claude Code usage emphasizes codebase navigation, automated tests, documentation synthesis, and security workflows. The pattern is not “one magic prompt”; it is persistent project instructions plus specialized helpers.
Source: [How Anthropic teams use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code?vid=14)

4. Anthropic's multi-agent Research system uses an orchestrator-worker pattern. Their write-up highlights useful heuristics for this template:
- teach the orchestrator how to delegate,
- start wide then narrow,
- keep subagent outputs compact,
- use parallelism when tasks are actually independent,
- treat coding as less parallelizable than research,
- add evals and observability because multi-agent behavior is nonlinear.
Source: [How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)

5. Anthropic's Agent Skills article argues that durable procedural knowledge should live in files and folders, not only in prompts. That supports keeping specialist behavior in role `SKILL.md` files.
Source: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills?trk=public_post_comment-text)

6. OpenAI's eval guidance reinforces the need for reproducible evaluations and a quality flywheel. For this template, that means review and test gates should be explicit and repeatable rather than implied.
Source: [Evaluation best practices](https://platform.openai.com/docs/guides/evaluation-best-practices)

## Practical Implications

- Use one lead coordinator rather than a free-for-all.
- Prefer a small role set with sharp prompts over many vague agents.
- Keep role prompts stable and push project specifics into config and docs.
- Make testing, review, and security checks first-class steps in the loop.
- Add hooks only for rules worth enforcing every time.
