"""
Preflight checks for Teneo Agent.

Validates system and project state before overnight runs.
"""

import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .logging_utils import log


@dataclass
class PreflightResults:
    """Results from preflight checks."""
    passed: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.passed = False


def run_preflight_checks(
    project_path: Path,
    claude_cmd: str = "claude"
) -> PreflightResults:
    """
    Run all preflight checks.

    Checks:
    - Claude CLI is available
    - Project path exists
    - CLAUDE.md exists (warning if not)
    - TASKS.md exists with tasks (warning if not)
    - Git repository state
    - Disk space
    """
    results = PreflightResults()

    # Check Claude CLI
    if not _check_claude_cli(claude_cmd):
        results.add_error(f"Claude CLI not found at: {claude_cmd}")

    # Check project exists
    if not project_path.exists():
        results.add_error(f"Project path does not exist: {project_path}")
        return results  # Can't continue without project

    # Check CLAUDE.md
    claude_md = project_path / "CLAUDE.md"
    if not claude_md.exists():
        results.add_warning("No CLAUDE.md found - workers won't have project context")

    # Check TASKS.md
    tasks_file = project_path / "TASKS.md"
    if not tasks_file.exists():
        results.add_warning("No TASKS.md found - will run setup worker")
    else:
        content = tasks_file.read_text(encoding='utf-8')
        if "- [ ]" not in content:
            results.add_warning("No incomplete tasks in TASKS.md")

    # Check git state
    git_warnings = _check_git_state(project_path)
    for w in git_warnings:
        results.add_warning(w)

    # Check disk space
    disk_warning = _check_disk_space(project_path)
    if disk_warning:
        results.add_warning(disk_warning)

    return results


def _check_claude_cli(claude_cmd: str) -> bool:
    """Check if Claude CLI is available."""
    try:
        # Try to run claude --version
        result = subprocess.run(
            [claude_cmd, "--version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        # Check if it's in PATH
        return shutil.which(claude_cmd) is not None


def _check_git_state(project_path: Path) -> List[str]:
    """Check git repository state."""
    warnings = []

    if not (project_path / ".git").exists():
        warnings.append("Not a git repository - work won't be checkpointed")
        return warnings

    try:
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            warnings.append(f"Uncommitted changes ({len(lines)} files)")

        # Check if remote is configured
        result = subprocess.run(
            ["git", "remote", "-v"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if not result.stdout.strip():
            warnings.append("No git remote configured - pushes will fail")

    except Exception as e:
        warnings.append(f"Could not check git state: {e}")

    return warnings


def _check_disk_space(project_path: Path, min_gb: float = 1.0) -> Optional[str]:
    """Check if there's enough disk space."""
    try:
        if sys.platform == "win32":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(str(project_path)),
                None, None,
                ctypes.pointer(free_bytes)
            )
            free_gb = free_bytes.value / (1024 ** 3)
        else:
            import os
            stat = os.statvfs(project_path)
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)

        if free_gb < min_gb:
            return f"Low disk space: {free_gb:.1f}GB free (recommend >{min_gb}GB)"

    except Exception:
        pass  # Non-critical, don't warn

    return None


def print_preflight_report(results: PreflightResults):
    """Print preflight results."""
    if results.passed:
        log("Preflight checks PASSED")
    else:
        log("Preflight checks FAILED")

    if results.errors:
        log("Errors:")
        for e in results.errors:
            log(f"  [ERROR] {e}")

    if results.warnings:
        log("Warnings:")
        for w in results.warnings:
            log(f"  [WARN] {w}")
