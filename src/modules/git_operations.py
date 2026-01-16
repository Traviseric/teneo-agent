"""
Git operations for Teneo Agent.

Provides checkpoint (add + commit + push) functionality
following the "Landing the Plane" pattern from Yegge.
"""

import subprocess
from datetime import datetime
from pathlib import Path

from .logging_utils import log


def git_checkpoint(project_path: Path, message: str = None) -> bool:
    """
    Create a git checkpoint (add + commit + push).

    This is the "Landing the Plane" pattern from Yegge -
    always push your work so it's not lost.

    Args:
        project_path: Path to the git repository
        message: Optional commit message (auto-generated if not provided)

    Returns:
        True if checkpoint was successful
    """
    if not (project_path / ".git").exists():
        return False

    try:
        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=project_path,
            capture_output=True,
            timeout=30
        )

        # Check if there's anything to commit
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if not status.stdout.strip():
            return True  # Nothing to commit, that's fine

        # Commit
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        commit_msg = message or f"teneo-agent checkpoint: {timestamp}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=project_path,
            capture_output=True,
            timeout=30
        )

        # Push (don't fail if push fails - might be offline)
        subprocess.run(
            ["git", "push"],
            cwd=project_path,
            capture_output=True,
            timeout=60
        )

        return True
    except Exception as e:
        log(f"[WARN] Git checkpoint failed: {e}")
        return False


def get_current_branch(project_path: Path) -> str:
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def get_short_hash(project_path: Path) -> str:
    """Get the short git hash for current HEAD."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"
