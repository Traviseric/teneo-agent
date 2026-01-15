#!/usr/bin/env python3
"""
Ralph Runner - Geoffrey Huntley's Ralph Loop Pattern
====================================================

A minimal implementation of Geoff Huntley's "Ralph Loop" for overnight agents.

The Core Idea:
    while :; do
      cat PROMPT.md | agent
    done

That's it. Each iteration gets fresh context. No memory accumulation.
No context degradation. Just read the prompt and work.

Learn more:
- Geoffrey Huntley's repo: https://github.com/ghuntley/how-to-ralph-wiggum
- Your First Agent: https://www.yourfirstagent.com/

This is my minimal implementation for testing the pattern.
Feedback welcome: https://github.com/Traviseric/teneo-agent/issues

Usage:
    python ralph_runner.py --project /path/to/project --max 5

Author: Travis Eric (traviseric.com)
Pattern by: Geoffrey Huntley (ghuntley.com)
License: MIT
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# =============================================================================
# THE RALPH LOOP
# =============================================================================

def find_claude_cmd() -> str:
    """Find Claude CLI."""
    paths = [
        Path.home() / "AppData" / "Roaming" / "npm" / "claude.cmd",
        Path("/usr/local/bin/claude"),
    ]
    for p in paths:
        if p.exists():
            return str(p)
    return "claude"

CLAUDE_CMD = find_claude_cmd()


def log(msg: str):
    """Timestamped log."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def run_iteration(project_path: Path, iteration: int) -> bool:
    """
    Run one iteration of the Ralph Loop.

    Each iteration:
    1. Read PROMPT.md (The Pin - immutable intent)
    2. Execute with fresh context
    3. Exit (context is garbage collected)
    """
    prompt_file = project_path / "PROMPT.md"

    if not prompt_file.exists():
        log(f"[ERROR] No PROMPT.md found in {project_path}")
        log("Create a PROMPT.md with your project intent and tasks.")
        return False

    log(f"[ITERATION {iteration}] Starting fresh context...")

    # Build command: cat PROMPT.md | claude
    claude_args = [CLAUDE_CMD, "-p", "--dangerously-skip-permissions"]

    if sys.platform == "win32":
        cmd = [
            "wt", "new-tab",
            "--title", f"Ralph {iteration}",
            "-d", str(project_path),
            "powershell", "-Command",
            f"Get-Content '{prompt_file}' | {' '.join(claude_args)}; "
            f"Write-Host 'Iteration {iteration} complete'; Start-Sleep 5"
        ]
    else:
        inner = f"cd '{project_path}' && cat '{prompt_file}' | {' '.join(claude_args)}"
        cmd = ["osascript", "-e", f'tell app "Terminal" to do script "{inner}"']

    try:
        subprocess.Popen(cmd)
        return True
    except Exception as e:
        log(f"[ERROR] {e}")
        return False


def ralph_loop(project_path: Path, max_iterations: int = 10, delay: int = 300):
    """
    The Ralph Loop: Fresh context per iteration.

    while :; do
      cat PROMPT.md | agent
    done

    Key insight: Memory is liability. Each iteration starts clean.
    """
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                     THE RALPH LOOP                               ║
║                                                                  ║
║  "Memory is Liability" - Geoffrey Huntley                        ║
║                                                                  ║
║  Each iteration: Read PROMPT.md → Work → Exit → Repeat           ║
║  No context accumulation. No degradation. Fresh every time.      ║
║                                                                  ║
║  Learn more: https://github.com/ghuntley/how-to-ralph-wiggum     ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    log(f"Project: {project_path}")
    log(f"Max iterations: {max_iterations}")
    log(f"Delay between: {delay}s")

    for i in range(1, max_iterations + 1):
        if not run_iteration(project_path, i):
            break

        if i < max_iterations:
            log(f"Waiting {delay}s before next iteration...")
            time.sleep(delay)

    log("Ralph Loop complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Ralph Runner - Geoffrey Huntley's fresh context pattern"
    )
    parser.add_argument("--project", "-p", type=str, default=".",
                        help="Project path (must have PROMPT.md)")
    parser.add_argument("--max", "-m", type=int, default=10,
                        help="Max iterations (default: 10)")
    parser.add_argument("--delay", "-d", type=int, default=300,
                        help="Seconds between iterations (default: 300)")

    args = parser.parse_args()
    project_path = Path(args.project).resolve()

    if not project_path.exists():
        print(f"Error: {project_path} does not exist")
        sys.exit(1)

    ralph_loop(project_path, args.max, args.delay)


if __name__ == "__main__":
    main()
