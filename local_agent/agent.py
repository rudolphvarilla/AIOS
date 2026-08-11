"""AIOS Local Agent v0.1

Local-only execution bridge for Phase 3.2.1v2.

This module intentionally exposes an allowlisted set of operations rather than
an arbitrary remote shell. Remote transport is out of scope for this first
Stem and must be added only with authentication and audit logging.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence


DEFAULT_ROOT = Path(r"C:\AIOS\Coordinator")


def _run(command: Sequence[str], cwd: Path, timeout: int = 300) -> dict:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        return {
            "ok": completed.returncode == 0,
            "command": list(command),
            "cwd": str(cwd),
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "elapsed_seconds": round(time.perf_counter() - started, 4),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "command": list(command),
            "cwd": str(cwd),
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "error": "timeout",
            "elapsed_seconds": round(time.perf_counter() - started, 4),
        }


def verify(root: Path) -> dict:
    venv_python = root / ".venv" / "Scripts" / "python.exe"
    return {
        "workspace_exists": root.is_dir(),
        "workspace": str(root),
        "venv_python_exists": venv_python.is_file(),
        "venv_python": str(venv_python),
        "agent_python": sys.executable,
    }


def run_regression(root: Path) -> dict:
    python = root / ".venv" / "Scripts" / "python.exe"
    if not python.is_file():
        return {"ok": False, "error": f"Missing virtualenv Python: {python}"}
    return _run([str(python), "-m", "pytest", "-v"], root)


def git_status(root: Path) -> dict:
    return _run(["git", "status", "--short", "--branch"], root)


def main() -> int:
    parser = argparse.ArgumentParser(description="AIOS local development agent")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "action",
        choices=("verify", "regression", "git-status"),
        help="Controlled local operation to execute",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "error": f"Workspace not found: {root}"}, indent=2))
        return 2

    if args.action == "verify":
        result = verify(root)
    elif args.action == "regression":
        result = run_regression(root)
    else:
        result = git_status(root)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
