#!/usr/bin/env bash
set -euo pipefail

mode="${1:-all}"
root_dir="${PROJECT_ROOT:-$(pwd)}"
env_file="${QUALITY_GATES_ENV:-$root_dir/team/quality-gates.env}"

if [ ! -f "$env_file" ]; then
  printf 'Missing %s\nRun python3 scripts/init_team_config.py first.\n' "$env_file" >&2
  exit 1
fi

# shellcheck disable=SC1090
. "$env_file"

cd "$root_dir"

section() {
  printf '\n==> %s\n' "$1"
}

run_optional_command() {
  local gate_name="$1"
  local command_text="$2"

  if [ -z "${command_text// }" ]; then
    printf 'skip %s\n' "$gate_name"
    return 0
  fi

  section "$gate_name"
  eval "$command_text"
}

review_hygiene() {
  local required_file
  local markers

  section "review_hygiene"

  for required_file in \
    "$root_dir/AGENTS.md" \
    "$root_dir/team/config.yaml" \
    "$root_dir/team/quality-gates.env" \
    "$root_dir/docs/09-work-log.md" \
    "$root_dir/team/session-state/active-handoff.md" \
    "$root_dir/team/session-state/next-session-prompt.md"; do
    if [ ! -f "$required_file" ]; then
      printf 'Missing required file: %s\n' "$required_file" >&2
      exit 1
    fi
  done

  if command -v rg >/dev/null 2>&1; then
    markers="$(
      rg -n '^(<<<<<<<|=======|>>>>>>>)' "$root_dir" \
        --glob '!**/.git/**' \
        --glob '!**/.claude/skills/**' \
        --glob '!**/node_modules/**' \
        --glob '!**/.venv/**' || true
    )"
  else
    markers="$(
      grep -R -n -E '^(<<<<<<<|=======|>>>>>>>)' "$root_dir" \
        --exclude-dir=.git \
        --exclude-dir=node_modules \
        --exclude-dir=.venv 2>/dev/null || true
    )"
  fi

  if [ -n "$markers" ]; then
    printf '%s\n' "$markers" >&2
    printf 'Merge-conflict markers detected.\n' >&2
    exit 1
  fi
}

run_all() {
  review_hygiene
  run_optional_command "runtime_setup" "${RUNTIME_SETUP_CMD:-}"
  run_optional_command "install" "${INSTALL_CMD:-}"
  run_optional_command "lint" "${LINT_CMD:-}"
  run_optional_command "typecheck" "${TYPECHECK_CMD:-}"
  run_optional_command "review" "${REVIEW_CMD:-}"
  run_optional_command "unit_test" "${UNIT_TEST_CMD:-}"
  run_optional_command "integration_test" "${INTEGRATION_TEST_CMD:-}"
  run_optional_command "e2e_test" "${E2E_TEST_CMD:-}"
  run_optional_command "perf_smoke" "${PERF_SMOKE_CMD:-}"
  run_optional_command "security_smoke" "${SECURITY_SMOKE_CMD:-}"
}

case "$mode" in
  all|ci)
    run_all
    ;;
  review_hygiene)
    review_hygiene
    ;;
  runtime_setup)
    run_optional_command "runtime_setup" "${RUNTIME_SETUP_CMD:-}"
    ;;
  install)
    run_optional_command "install" "${INSTALL_CMD:-}"
    ;;
  lint)
    run_optional_command "lint" "${LINT_CMD:-}"
    ;;
  typecheck)
    run_optional_command "typecheck" "${TYPECHECK_CMD:-}"
    ;;
  review)
    run_optional_command "review" "${REVIEW_CMD:-}"
    ;;
  unit_test)
    run_optional_command "unit_test" "${UNIT_TEST_CMD:-}"
    ;;
  integration_test)
    run_optional_command "integration_test" "${INTEGRATION_TEST_CMD:-}"
    ;;
  e2e_test)
    run_optional_command "e2e_test" "${E2E_TEST_CMD:-}"
    ;;
  perf_smoke)
    run_optional_command "perf_smoke" "${PERF_SMOKE_CMD:-}"
    ;;
  security_smoke)
    run_optional_command "security_smoke" "${SECURITY_SMOKE_CMD:-}"
    ;;
  *)
    printf 'Unknown mode: %s\n' "$mode" >&2
    exit 1
    ;;
esac
