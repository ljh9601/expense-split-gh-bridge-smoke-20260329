#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


EXCLUDED_NAMES = {
    ".DS_Store",
    ".git",
    ".agentic-team-template-manifest",
}

EXCLUDED_DIRS = {
    ".git",
    ".claude/skills",
    "__pycache__",
}


def should_skip(relative_path: Path) -> bool:
    path_string = relative_path.as_posix()
    if relative_path.name in EXCLUDED_NAMES:
        return True
    if "__pycache__" in relative_path.parts:
        return True
    return any(path_string == excluded or path_string.startswith(f"{excluded}/") for excluded in EXCLUDED_DIRS)


def copy_tree(source_root: Path, target_root: Path, force: bool) -> None:
    for source_path in sorted(source_root.rglob("*")):
        relative_path = source_path.relative_to(source_root)
        if should_skip(relative_path):
            continue

        destination_path = target_root / relative_path

        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue

        if destination_path.exists() and not force:
            raise SystemExit(f"Refusing to overwrite existing file without --force: {destination_path}")

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy the agentic-team template into a new project root and initialize project config.")
    parser.add_argument("project_name_positional", nargs="?", help="Project name. If provided, --project-name may be omitted.")
    parser.add_argument("--target-root", help="Directory for the new project scaffold. Defaults to <projects-root>/<project-name>.")
    parser.add_argument("--project-name", help="Project name.")
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
    parser.add_argument("--force", action="store_true", help="Allow overwriting existing files in the target root.")
    args = parser.parse_args()
    args.project_name = args.project_name or args.project_name_positional
    if not args.project_name:
        parser.error("project name is required via positional argument or --project-name")
    return args


def main() -> None:
    args = parse_args()
    source_root = Path(__file__).resolve().parents[1]
    projects_root = Path(os.environ.get("AGENTIC_PROJECTS_ROOT", str(source_root.parent))).resolve()
    target_root = Path(args.target_root).resolve() if args.target_root else projects_root / args.project_name
    target_root.mkdir(parents=True, exist_ok=True)

    if any(target_root.iterdir()) and not args.force:
        raise SystemExit(f"Target root is not empty: {target_root}. Use --force to overwrite agentic template files.")

    copy_tree(source_root, target_root, args.force)

    init_args = [
        sys.executable,
        str(target_root / "scripts" / "init_team_config.py"),
        "--project-root",
        str(target_root),
        "--project-name",
        args.project_name,
        "--summary",
        args.summary,
        "--runtime-setup-cmd",
        args.runtime_setup_cmd,
        "--install-cmd",
        args.install_cmd,
        "--lint-cmd",
        args.lint_cmd,
        "--typecheck-cmd",
        args.typecheck_cmd,
        "--review-cmd",
        args.review_cmd,
        "--unit-test-cmd",
        args.unit_test_cmd,
        "--integration-test-cmd",
        args.integration_test_cmd,
        "--e2e-test-cmd",
        args.e2e_test_cmd,
        "--perf-smoke-cmd",
        args.perf_smoke_cmd,
        "--security-smoke-cmd",
        args.security_smoke_cmd,
    ]

    for value in args.primary_language:
        init_args.extend(["--primary-language", value])
    for value in args.domain:
        init_args.extend(["--domain", value])
    for value in args.hub_file:
        init_args.extend(["--hub-file", value])
    for value in args.sensitive_path:
        init_args.extend(["--sensitive-path", value])

    subprocess.run(init_args, check=True)
    subprocess.run(["./scripts/sync-claude-skills"], cwd=target_root, check=True)

    print(f"Bootstrapped agentic-team scaffold into {target_root}")


if __name__ == "__main__":
    main()
