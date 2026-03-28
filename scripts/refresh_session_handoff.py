#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from datetime import datetime
from pathlib import Path


def now_string() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")


def git_changed_files(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return []

    paths: list[str] = []
    for line in result.stdout.splitlines():
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            paths.append(path)
    return paths


def markdown_list(items: list[str], empty_text: str) -> str:
    if not items:
        return f"- {empty_text}"
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str], empty_text: str) -> str:
    if not items:
        return f"1. {empty_text}"
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def render_active_handoff(args: argparse.Namespace, changed_files: list[str]) -> str:
    must_read = dedupe_keep_order(
        args.must_read or ["`AGENTS.md`", "`team/backlog/active.yaml`", "`team/memory/project-facts.md`", "`docs/09-work-log.md`"]
    )
    return f"""# Active Handoff

Last updated: {now_string()}
Current objective: {args.objective}
Current phase: {args.phase}
Active work packet: {args.work_packet or 'Not set'}
Next gate: {args.next_gate or 'Not set'}

## Must Read First

{markdown_list(must_read, 'AGENTS.md')}

## Completed Work

{markdown_list(args.completed, 'None recorded')}

## Current In-Progress Work

{markdown_list(args.in_progress, 'None recorded')}

## Pending Next Actions

{numbered_list(args.next, 'Define the next action before using this handoff')}

## Changed Files Worth Rereading

{markdown_list(changed_files, 'No changed files recorded')}

## Validation Status

{markdown_list(args.validation, 'Not run yet')}

## Open Risks Or Blockers

{markdown_list(args.risk, 'No open risks recorded')}

## Delegation Status

{markdown_list(args.delegation, 'No active delegated work recorded')}

## Notes For The Next Session

- Start with the first pending next action.
- Reopen the active work packet before delegating or editing.
- Do not trust old chat memory over these files if they disagree.
"""


def render_next_prompt(args: argparse.Namespace) -> str:
    first_action = args.next[0] if args.next else "Define the next action before resuming."
    return f"""Read these first:
- `AGENTS.md`
- `CLAUDE.md` if this is a Claude-led session
- `team/config.yaml` if present
- `team/backlog/active.yaml`
- `team/memory/project-facts.md`
- `team/session-state/active-handoff.md`
- latest entries in `docs/09-work-log.md`

Continue from the active work packet and next gate recorded in `active-handoff.md`.

Your first actions:
1. Confirm the current objective, phase, active work packet, and next gate.
2. Reopen only the files listed under `Changed Files Worth Rereading` and the active work packet artifacts.
3. Execute this next action first: {first_action}
4. Keep `team/backlog/active.yaml`, `docs/09-work-log.md`, and `team/session-state/active-handoff.md` current before any future reset.
"""


def append_work_log(root: Path, args: argparse.Namespace, changed_files: list[str]) -> None:
    if not args.append_work_log:
        return

    work_log_path = root / "docs" / "09-work-log.md"
    work_log_path.parent.mkdir(parents=True, exist_ok=True)
    if not work_log_path.exists():
        raise SystemExit(f"Missing work log: {work_log_path}")

    entry = f"""
### {now_string()} | {args.log_task} | {args.log_status}
- Goal: {args.log_goal or args.objective}
- Scope: {args.log_scope or args.phase}
- Work packet: {args.work_packet or 'Not set'}
- Next gate: {args.next_gate or 'Not set'}
- Changed: {', '.join(changed_files) if changed_files else 'No changed files recorded'}
- Validation: {'; '.join(args.validation) if args.validation else 'Not run yet'}
- Risks: {'; '.join(args.risk) if args.risk else 'No open risks recorded'}
- Next: {'; '.join(args.next) if args.next else 'Define the next action before resuming'}
"""
    with work_log_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh session handoff files and optionally append a work-log entry.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--phase", default="implementation")
    parser.add_argument("--work-packet", default="")
    parser.add_argument("--next-gate", default="")
    parser.add_argument("--must-read", action="append", default=[])
    parser.add_argument("--completed", action="append", default=[])
    parser.add_argument("--in-progress", action="append", default=[])
    parser.add_argument("--next", action="append", default=[])
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--validation", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--delegation", action="append", default=[])
    parser.add_argument("--append-work-log", action="store_true")
    parser.add_argument("--log-task", default="checkpoint")
    parser.add_argument("--log-status", default="updated")
    parser.add_argument("--log-goal", default="")
    parser.add_argument("--log-scope", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve()
    session_dir = root / "team" / "session-state"
    session_dir.mkdir(parents=True, exist_ok=True)

    changed_files = args.changed_file or git_changed_files(root)

    active_handoff_path = session_dir / "active-handoff.md"
    next_prompt_path = session_dir / "next-session-prompt.md"

    active_handoff_path.write_text(render_active_handoff(args, changed_files), encoding="utf-8")
    next_prompt_path.write_text(render_next_prompt(args), encoding="utf-8")
    append_work_log(root, args, changed_files)

    print(f"Wrote {active_handoff_path}")
    print(f"Wrote {next_prompt_path}")
    if args.append_work_log:
        print(f"Updated {root / 'docs' / '09-work-log.md'}")


if __name__ == "__main__":
    main()
