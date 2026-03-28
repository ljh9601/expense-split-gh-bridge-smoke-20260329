#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
from datetime import datetime, timezone
from pathlib import Path


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def yaml_list(items: list[str], indent: int = 2) -> str:
    pad = " " * indent
    return "\n".join(f"{pad}- {yaml_quote(item)}" for item in items)


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def render_config(args: argparse.Namespace) -> str:
    primary_languages = args.primary_language or ["typescript", "python"]
    domains = args.domain or ["backend", "frontend"]
    hub_files = args.hub_file or ["src/app.ts", "src/server.ts"]
    sensitive_paths = args.sensitive_path or [".env", "infra/", "migrations/", "auth/"]

    return f"""project:
  name: {yaml_quote(args.project_name)}
  summary: >
    {args.summary}
  primary_languages:
{yaml_list(primary_languages, 4)}
  domains:
{yaml_list(domains, 4)}

docs:
  required_read_order:
    - README.md
    - AGENTS.md
    - CLAUDE.md
    - team/config.yaml
    - team/backlog/active.yaml
    - team/memory/project-facts.md
    - team/policies/git-workflow.yaml
    - team/run-state/active-run.yaml
    - team/session-state/active-handoff.md
    - docs/architecture.md
    - docs/14-git-pr-workflow.md
    - docs/security.md
    - docs/runbook.md
    - docs/09-work-log.md

commands:
  install: {yaml_quote(args.install_cmd)}
  runtime_setup: {yaml_quote(args.runtime_setup_cmd)}
  quality_gate_runner: './scripts/run-quality-gates.sh all'
  review_hygiene: './scripts/run-quality-gates.sh review_hygiene'
  lint: {yaml_quote(args.lint_cmd)}
  typecheck: {yaml_quote(args.typecheck_cmd)}
  unit_test: {yaml_quote(args.unit_test_cmd)}
  integration_test: {yaml_quote(args.integration_test_cmd)}
  e2e_test: {yaml_quote(args.e2e_test_cmd)}
  perf_smoke: {yaml_quote(args.perf_smoke_cmd)}
  review_cmd: {yaml_quote(args.review_cmd)}
  security_smoke: {yaml_quote(args.security_smoke_cmd)}

paths:
  hub_files:
{yaml_list(hub_files, 4)}
  sensitive_paths:
{yaml_list(sensitive_paths, 4)}

coordination:
  control_plane_owner: 'codex'
  execution_plane_owner: 'claude'
  design_review_round_limit: 3
  mandatory_state_files:
    - 'team/backlog/active.yaml'
    - 'team/session-state/active-handoff.md'
    - 'team/memory/project-facts.md'
    - 'team/memory/decisions.jsonl'
    - 'team/run-state/active-run.yaml'
    - 'team/run-state/run-ledger.jsonl'
  mandatory_contract_templates:
    - 'team/contracts/work-packet.template.yaml'
    - 'team/contracts/design-brief.template.md'
    - 'team/contracts/verification-report.template.md'
    - 'team/contracts/review-report.template.md'
    - 'team/contracts/report-bundle.template.yaml'
    - 'team/contracts/run-ledger-entry.template.yaml'
    - 'team/contracts/pull-request.template.md'
    - 'team/contracts/pr-review-comment.template.md'
    - 'team/contracts/github-bridge-record.template.yaml'
  supporting_contract_templates:
    - 'team/contracts/research-note.template.md'
    - 'team/contracts/security-review.template.md'
    - 'team/contracts/performance-note.template.md'
    - 'team/contracts/ui-spec.template.md'
    - 'team/contracts/docs-delta.template.md'

workflow:
  default_phase_order:
    - 'intake'
    - 'architecture'
    - 'planning'
    - 'implementation'
    - 'verification'
    - 'review'
    - 'approval'
  claude_execution_order:
    - 'research'
    - 'scope'
    - 'design'
    - 'implement'
    - 'security_perf_ux'
    - 'review'
  codex_approval_required_for:
    - 'architecture signoff'
    - 'scope changes'
    - 'milestone closeout'

autonomy:
  default_parallelism: 3
  next_step_selection: 'codex_owns_default_queue'
  clarification_policy: 'ask_only_when_wrong_guess_is_expensive_or_unsafe'
  shell_command_policy: 'preapproved_for_local_repo_work_except_destructive_or_externally_privileged_actions'
  auto_approval_policy_file: 'team/policies/auto-approval.yaml'
  commit_policy: 'commit_each_meaningful_work_unit'
  interrupt_human_only_for:
    - 'destructive_action'
    - 'new_external_authentication'
    - 'production_or_paid_side_effect'
    - 'legal_or_compliance_ambiguity'
    - 'repeated_unsafe_failure'
  review_required: true
  docs_update_required_on_behavior_change: true
  repair_loops_before_escalation: 2
  security_review_required_when:
    - 'auth'
    - 'secrets'
    - 'payment'
    - 'user_input'
    - 'external_api'
    - 'filesystem'
  performance_review_required_when:
    - 'hot_path'
    - 'query_fanout'
    - 'render_loop'
    - 'background_job'

session_continuity:
  enabled: true
  backlog_file: 'team/backlog/active.yaml'
  project_facts_file: 'team/memory/project-facts.md'
  decision_log_file: 'team/memory/decisions.jsonl'
  work_log_file: 'docs/09-work-log.md'
  active_handoff_file: 'team/session-state/active-handoff.md'
  resume_prompt_file: 'team/session-state/next-session-prompt.md'
  latest_work_log_entries_to_read: 10
  refresh_handoff_when:
    - 'before an intentional session reset'
    - 'after a meaningful repair loop'
    - 'before starting another broad implementation or review batch'
  handoff_sections_required:
    - 'objective'
    - 'current_phase'
    - 'active_work_packet'
    - 'next_gate'
    - 'completed_work'
    - 'pending_next_actions'
    - 'changed_files'
    - 'validation_status'
    - 'open_risks'
    - 'delegation_status'

git_workflow:
  enabled: true
  default_branch: 'main'
  packet_branch_prefix: 'packet'
  logical_pr_author: 'claude-programmer'
  final_pr_approver: 'codex'
  local_pr_directory: 'team/pull-requests'
  workflow_doc: 'docs/14-git-pr-workflow.md'
  policy_file: 'team/policies/git-workflow.yaml'
  pull_request_template: 'team/contracts/pull-request.template.md'
  review_comment_template: 'team/contracts/pr-review-comment.template.md'
  publish_to_github_when:
    - 'optional GitHub bridge is configured'
    - 'network-backed publication is allowed by policy'

github_pr_bridge:
  policy_file: 'team/policies/github-bridge.yaml'
  state_file: 'team/run-state/github-pr-bridge.yaml'
  author_env_file: 'team/policies/github-author.env.local'
  reviewer_env_file: 'team/policies/github-reviewer.env.local'
  machine_global_author_env_file: '~/.config/agent-bootstrap/github-author.env'
  machine_global_reviewer_env_file: '~/.config/agent-bootstrap/github-reviewer.env'
  service_author_token_env: 'ABI_GITHUB_AUTHOR_TOKEN'
  service_reviewer_token_env: 'ABI_GITHUB_REVIEWER_TOKEN'
  service_author_env_file_env: 'ABI_GITHUB_AUTHOR_ENV_FILE'
  service_reviewer_env_file_env: 'ABI_GITHUB_REVIEWER_ENV_FILE'
  distinct_accounts_required: true
  default_auto_publish_completed_packets: true

definition_of_done:
  - 'active work packet updated coherently'
  - 'code or configuration updated coherently'
  - 'targeted validation run'
  - 'verification and review reports produced or linked'
  - 'findings from review resolved or documented'
  - 'docs or runbooks updated when behavior changed'
  - 'work log and handoff updated for meaningful work'
  - 'residual risks summarized'
"""


def render_quality_gates_env(args: argparse.Namespace) -> str:
    return f"""# Generated by scripts/init_team_config.py
RUNTIME_SETUP_CMD={shell_quote(args.runtime_setup_cmd)}
INSTALL_CMD={shell_quote(args.install_cmd)}
LINT_CMD={shell_quote(args.lint_cmd)}
TYPECHECK_CMD={shell_quote(args.typecheck_cmd)}
REVIEW_CMD={shell_quote(args.review_cmd)}
UNIT_TEST_CMD={shell_quote(args.unit_test_cmd)}
INTEGRATION_TEST_CMD={shell_quote(args.integration_test_cmd)}
E2E_TEST_CMD={shell_quote(args.e2e_test_cmd)}
PERF_SMOKE_CMD={shell_quote(args.perf_smoke_cmd)}
SECURITY_SMOKE_CMD={shell_quote(args.security_smoke_cmd)}
"""


def render_backlog(args: argparse.Namespace) -> str:
    return f"""meta:
  last_updated: {yaml_quote('YYYY-MM-DD')}
  current_objective: {yaml_quote('Replace with the current project objective.')}
  current_phase: {yaml_quote('intake')}
  active_work_packet: {yaml_quote('WP-001')}

milestones:
  - id: {yaml_quote('M1')}
    title: {yaml_quote('bootstrap collaboration kernel')}
    status: {yaml_quote('pending')}
    success_criteria:
      - {yaml_quote('Codex and Claude can resume from repo files alone.')}
      - {yaml_quote('Work packets, reports, and handoffs are standardized.')}
      - {yaml_quote('Bootstrap creates the baseline operating scaffold.')}

queue:
  - id: {yaml_quote('WP-001')}
    title: {yaml_quote('replace with the first real work packet title')}
    status: {yaml_quote('pending')}
    phase: {yaml_quote('architecture')}
    owner: {yaml_quote('codex')}
    depends_on: []
    artifacts:
      - {yaml_quote('team/contracts/work-packet.template.yaml')}
    notes: {yaml_quote('Replace with the first bounded task.')}
"""


def render_project_facts(args: argparse.Namespace) -> str:
    return f"""# Project Facts

## Summary

- Project: `{args.project_name}`
- Replace this file with stable facts, system boundaries, invariants, operator rules, and commands that future sessions should not rediscover.

## Important Paths

- `team/backlog/active.yaml`
- `team/run-state/active-run.yaml`
- `team/run-state/run-ledger.jsonl`
- `team/reports/`
- `team/session-state/active-handoff.md`
- `team/memory/decisions.jsonl`
- `docs/09-work-log.md`

## Commands

- Install: `{args.install_cmd}`
- Lint: `{args.lint_cmd}`
- Typecheck: `{args.typecheck_cmd}`
- Unit test: `{args.unit_test_cmd}`
- Integration test: `{args.integration_test_cmd}`
- E2E test: `{args.e2e_test_cmd}`

## Invariants

- Replace with architectural or operational constraints that must remain true.
"""


def render_active_run_state() -> str:
    return """run:
  run_id: 'RUN-000'
  packet_id: 'WP-000'
  phase: 'intake'
  status: 'idle'
  attempt: 0
  current_actor: 'codex'
  report_bundle_path: ''
  latest_handoff_path: 'team/session-state/active-handoff.md'
  latest_verification_report: ''
  latest_review_report: ''
  last_updated: 'YYYY-MM-DDTHH:MM:SSZ'
  notes:
    - 'Replace placeholder values when the first real execution cycle starts.'
"""


def render_run_ledger_seed() -> str:
    return ""


def render_decisions_log(args: argparse.Namespace) -> str:
    record = {
        "timestamp": now_iso(),
        "actor": "codex",
        "category": "bootstrap",
        "summary": f"Initialized collaborative scaffold for {args.project_name}.",
        "status": "seeded",
        "next_action": "Replace this placeholder with the first durable project decision.",
    }
    return json.dumps(record, ensure_ascii=True) + "\n"


def render_auto_approval_policy() -> str:
    return """allowed_without_human:
  - repo_local_read_search
  - repo_local_edit
  - formatters
  - lint
  - typecheck
  - unit_tests
  - integration_tests
  - non_destructive_git_status_diff_add_commit

require_human_approval:
  - destructive_file_operations
  - production_side_effects
  - paid_resource_usage
  - new_external_authentication
  - secret_creation_or_rotation
  - deployment
  - schema_or_data_migration_in_live_environment

notes:
  - Replace these defaults with repo-specific unattended execution policy.
"""


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate team/config.yaml and team/quality-gates.env.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--project-name", required=True, help="Project name.")
    parser.add_argument("--summary", default="Replace with a short project summary, system boundary, and non-goals.")
    parser.add_argument("--primary-language", action="append", default=[])
    parser.add_argument("--domain", action="append", default=[])
    parser.add_argument("--hub-file", action="append", default=[])
    parser.add_argument("--sensitive-path", action="append", default=[])
    parser.add_argument("--runtime-setup-cmd", default="")
    parser.add_argument("--install-cmd", default="npm install")
    parser.add_argument("--lint-cmd", default="npm run lint")
    parser.add_argument("--typecheck-cmd", default="npm run typecheck")
    parser.add_argument("--review-cmd", default="")
    parser.add_argument("--unit-test-cmd", default="npm test")
    parser.add_argument("--integration-test-cmd", default="npm run test:integration")
    parser.add_argument("--e2e-test-cmd", default="npm run test:e2e")
    parser.add_argument("--perf-smoke-cmd", default="npm run perf")
    parser.add_argument("--security-smoke-cmd", default="npm audit --production")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve()
    team_dir = root / "team"
    session_dir = team_dir / "session-state"
    backlog_dir = team_dir / "backlog"
    contracts_dir = team_dir / "contracts"
    memory_dir = team_dir / "memory"
    policies_dir = team_dir / "policies"
    reports_dir = team_dir / "reports"
    run_state_dir = team_dir / "run-state"

    for directory in (team_dir, session_dir, backlog_dir, contracts_dir, memory_dir, policies_dir, reports_dir, run_state_dir):
        directory.mkdir(parents=True, exist_ok=True)

    config_path = team_dir / "config.yaml"
    quality_env_path = team_dir / "quality-gates.env"
    backlog_path = backlog_dir / "active.yaml"
    facts_path = memory_dir / "project-facts.md"
    decisions_path = memory_dir / "decisions.jsonl"
    auto_approval_path = policies_dir / "auto-approval.yaml"
    active_run_path = run_state_dir / "active-run.yaml"
    run_ledger_path = run_state_dir / "run-ledger.jsonl"

    config_path.write_text(render_config(args), encoding="utf-8")
    quality_env_path.write_text(render_quality_gates_env(args), encoding="utf-8")
    write_if_missing(backlog_path, render_backlog(args))
    write_if_missing(facts_path, render_project_facts(args))
    write_if_missing(decisions_path, render_decisions_log(args))
    write_if_missing(auto_approval_path, render_auto_approval_policy())
    write_if_missing(active_run_path, render_active_run_state())
    write_if_missing(run_ledger_path, render_run_ledger_seed())

    print(f"Wrote {config_path}")
    print(f"Wrote {quality_env_path}")
    if backlog_path.exists():
        print(f"Ensured {backlog_path}")
    if facts_path.exists():
        print(f"Ensured {facts_path}")
    if decisions_path.exists():
        print(f"Ensured {decisions_path}")
    if auto_approval_path.exists():
        print(f"Ensured {auto_approval_path}")
    if active_run_path.exists():
        print(f"Ensured {active_run_path}")
    if run_ledger_path.exists():
        print(f"Ensured {run_ledger_path}")


if __name__ == "__main__":
    main()
