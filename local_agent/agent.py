"""AIOS Local Agent v0.2

Local-only execution bridge for AIOS development and verification.

The agent intentionally exposes a small allowlisted set of operations rather
than an arbitrary shell. Remote transport is out of scope for this Stem and
must be added only with authentication and audit logging.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence


DEFAULT_ROOT = Path(r"C:\AIOS\Coordinator")
DEFAULT_QUERY_TIMEOUT_SECONDS = 300

STANDARD_REGRESSION_CASES = (
    ("R1", "current weather in philippines"),
    ("R2", "tallest mountain in the philippines"),
    ("R3", "what is 2+2"),
)


def _run(
    command: Sequence[str],
    cwd: Path,
    timeout: int = 300,
    stdin_text: str | None = None,
) -> dict:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd),
            input=stdin_text,
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
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        return {
            "ok": False,
            "command": list(command),
            "cwd": str(cwd),
            "returncode": None,
            "stdout": stdout,
            "stderr": stderr,
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


def run_regression(root: Path, timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS) -> dict:
    """Run the standard real-AIOS regression queries and return one report.

    The coordinator remains the execution owner.  This agent only drives its
    existing developer interaction and records a bounded result for each case.
    """
    started = time.perf_counter()
    cases = []

    for case_id, query in STANDARD_REGRESSION_CASES:
        result = query_aios(root, query, timeout=timeout)
        if result.get("error") == "timeout":
            status = "timeout"
        elif result.get("ok"):
            status = "passed"
        else:
            status = "failed"

        cases.append(
            {
                "id": case_id,
                "query": query,
                "status": status,
                "success": result.get("ok", False),
                "returncode": result.get("returncode"),
                "elapsed_seconds": result.get("elapsed_seconds"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
                "error": result.get("error"),
                "command": result.get("command"),
                "cwd": result.get("cwd"),
            }
        )

    return {
        "ok": all(case["success"] for case in cases),
        "report_type": "aios_standard_regression",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(root),
        "query_timeout_seconds": timeout,
        "elapsed_seconds": round(time.perf_counter() - started, 4),
        "cases": cases,
    }


def git_status(root: Path) -> dict:
    return _run(["git", "status", "--short", "--branch"], root)


def query_aios(root: Path, query: str, timeout: int = 300) -> dict:
    """Run one AIOS query through the real Coordinator interactive loop.

    This reproduces the developer workflow without modifying coordinator.py:
    start Coordinator, enable developer mode, submit the query, then exit.
    """
    python = root / ".venv" / "Scripts" / "python.exe"
    coordinator = root / "coordinator.py"

    if not python.is_file():
        return {"ok": False, "error": f"Missing virtualenv Python: {python}"}
    if not coordinator.is_file():
        return {"ok": False, "error": f"Coordinator not found: {coordinator}"}
    if not query.strip():
        return {"ok": False, "error": "Query must not be empty"}

    interaction = f"/dev on\n{query.strip()}\n/exit\n"
    return _run(
        [str(python), str(coordinator)],
        root,
        timeout=timeout,
        stdin_text=interaction,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="AIOS local development agent")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_QUERY_TIMEOUT_SECONDS,
        help="Per-query timeout in seconds for query and regression actions",
    )
    parser.add_argument(
        "action",
        choices=("verify", "regression", "git-status", "query"),
        help="Controlled local operation to execute",
    )
    parser.add_argument(
        "query_text",
        nargs="*",
        help="Query text when action=query",
    )
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    root = args.root.resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "error": f"Workspace not found: {root}"}, indent=2))
        return 2

    if args.action == "verify":
        result = verify(root)
    elif args.action == "regression":
        result = run_regression(root, timeout=args.timeout)
    elif args.action == "git-status":
        result = git_status(root)
    else:
        result = query_aios(root, " ".join(args.query_text), timeout=args.timeout)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
