#!/usr/bin/env python3
"""
Teneo Agent - Overnight AI Agent Runner
========================================

Run Claude agents overnight to build your projects autonomously.

Part of the Teneo ecosystem. Built independently, enhanced with insights from
the AI-first development community (Huntley, Yegge, dexhorthy).

Learn more: https://traviseric.com/courses/ai-first-fundamentals

Usage:
    python teneo_agent.py start                     # Run once
    python teneo_agent.py start --continuous        # Run until tasks done
    python teneo_agent.py start --lanes 2           # 2 parallel workers
    python teneo_agent.py status                    # Check current status

Author: Travis Eric (traviseric.com)
License: MIT
"""

import subprocess
import time
import argparse
import re
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================

# Project root (where this script lives)
PROJECT_ROOT = Path(__file__).parent

# Task file - workers read from here
TASKS_FILE = PROJECT_ROOT / "TASKS.md"

# Working directory for agent output
AGENT_DIR = PROJECT_ROOT / "agent_runs"

# Find Claude CLI
def find_claude_cmd() -> str:
    """Find Claude CLI executable."""
    paths = [
        Path.home() / "AppData" / "Roaming" / "npm" / "claude.cmd",  # Windows npm
        Path.home() / ".npm-global" / "bin" / "claude",               # npm global
        Path("/usr/local/bin/claude"),                                # macOS/Linux
    ]
    for p in paths:
        if p.exists():
            return str(p)
    return "claude"  # Hope it's in PATH

CLAUDE_CMD = find_claude_cmd()

# =============================================================================
# TASK PARSING
# =============================================================================

def parse_tasks(file_path: Path) -> List[dict]:
    """
    Parse checkbox-format tasks from a markdown file.

    Format:
        - [ ] Task description here
        - [x] Completed task

    Returns list of {task, completed, line_num}
    """
    if not file_path.exists():
        return []

    tasks = []
    content = file_path.read_text(encoding='utf-8')

    for line_num, line in enumerate(content.split('\n'), 1):
        # Match: - [ ] task or - [x] task
        match = re.match(r'^[\s]*-\s*\[([ xX])\]\s*(.+)$', line)
        if match:
            completed = match.group(1).lower() == 'x'
            task_text = match.group(2).strip()
            tasks.append({
                'task': task_text,
                'completed': completed,
                'line_num': line_num
            })

    return tasks


def get_incomplete_tasks(file_path: Path) -> List[dict]:
    """Get only incomplete tasks."""
    return [t for t in parse_tasks(file_path) if not t['completed']]


def mark_task_complete(file_path: Path, task_text: str) -> bool:
    """Mark a specific task as complete in the file."""
    if not file_path.exists():
        return False

    content = file_path.read_text(encoding='utf-8')
    # Escape special regex chars in task text
    escaped = re.escape(task_text)
    pattern = rf'^([\s]*-\s*)\[ \](\s*{escaped})$'

    new_content, count = re.subn(pattern, r'\1[x]\2', content, flags=re.MULTILINE)

    if count > 0:
        file_path.write_text(new_content, encoding='utf-8')
        return True
    return False


# =============================================================================
# GIT OPERATIONS
# =============================================================================

def git_checkpoint(project_path: Path, message: str = None) -> bool:
    """
    Create a git checkpoint (add + commit + push).

    This is the "Landing the Plane" pattern from Yegge -
    always push your work so it's not lost.
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


# =============================================================================
# WORKER MANAGEMENT
# =============================================================================

def create_worker_prompt(
    task: str,
    project_path: Path,
    round_num: int,
    lane_num: int,
    output_dir: Path
) -> Path:
    """
    Create a WORKER.md file with instructions for the Claude worker.

    This is "The Pin" from Huntley's Ralph Loop - the immutable
    intent anchor that tells the worker exactly what to do.
    """
    worker_id = f"R{round_num}L{lane_num}"
    log_file = output_dir / "LOG.md"
    handoff_file = output_dir / "HANDOFF.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# Teneo Agent Worker: {worker_id}

## Assignment
**Project:** {project_path.name}
**Working Directory:** `{project_path}`
**Task File:** `{TASKS_FILE}`
**Started:** {timestamp}

## Your Task
{task}

## Instructions

1. **Navigate** to the project: `{project_path}`
2. **Execute** the task above completely
3. **Mark complete** when done (update the checkbox in TASKS.md)
4. **Write handoff** with what you did and any notes for the next worker

## Quality Standards

- **Working code only** - if you write it, it must run
- **Tests pass** - run the build/tests before marking complete
- **No placeholders** - implement fully or note what's missing
- **Git checkpoint** - commit your work with a clear message

## Output

### Progress Log
Write to `{log_file}` as you work:

```markdown
# {worker_id} Log

## Status: IN_PROGRESS | COMPLETED | BLOCKED

### Work Done
- [time] What you accomplished

### Files Changed
- path/to/file.ts - what changed

### Issues
- Any blockers or problems
```

### Handoff (Required)
When done, write `{handoff_file}`:

```markdown
# {worker_id} Handoff

## Completed
- What you finished

## Next Steps
- What the next worker should do

## Notes
- Anything important to know
```

## Important
- You are autonomous - make decisions and execute
- If stuck for 5+ minutes, document the blocker and move on
- Quality over quantity - one task done well beats many half-done
"""

    worker_file = output_dir / "WORKER.md"
    output_dir.mkdir(parents=True, exist_ok=True)
    worker_file.write_text(content, encoding='utf-8')

    return worker_file


def spawn_worker(
    project_path: Path,
    round_num: int,
    lane_num: int,
    task: str
) -> bool:
    """
    Spawn a Claude worker in a new terminal window.

    Uses Windows Terminal (wt) for Windows, or falls back to
    platform-specific terminal emulators.
    """
    worker_id = f"R{round_num}L{lane_num}"
    output_dir = AGENT_DIR / f"round_{round_num}_lane_{lane_num}"

    # Create worker prompt
    worker_file = create_worker_prompt(
        task=task,
        project_path=project_path,
        round_num=round_num,
        lane_num=lane_num,
        output_dir=output_dir
    )

    log(f"[{worker_id}] Spawning worker for: {task[:50]}...")

    # Build Claude command
    # --dangerously-skip-permissions allows autonomous operation
    # -p reads from stdin (the worker prompt)
    claude_args = [
        CLAUDE_CMD,
        "-p",
        "--dangerously-skip-permissions",
    ]

    # Platform-specific terminal spawning
    if sys.platform == "win32":
        # Windows Terminal
        cmd = [
            "wt", "new-tab",
            "--title", f"Teneo Agent {worker_id}",
            "-d", str(project_path),
            "powershell", "-Command",
            f"Get-Content '{worker_file}' | {' '.join(claude_args)}; "
            f"Write-Host 'Worker {worker_id} complete'; "
            f"Start-Sleep 5"
        ]
    elif sys.platform == "darwin":
        # macOS - use osascript to open Terminal
        inner_cmd = f"cd '{project_path}' && cat '{worker_file}' | {' '.join(claude_args)}"
        cmd = [
            "osascript", "-e",
            f'tell app "Terminal" to do script "{inner_cmd}"'
        ]
    else:
        # Linux - try common terminal emulators
        inner_cmd = f"cd '{project_path}' && cat '{worker_file}' | {' '.join(claude_args)}; sleep 5"
        for terminal in ["gnome-terminal", "konsole", "xterm"]:
            if subprocess.run(["which", terminal], capture_output=True).returncode == 0:
                if terminal == "gnome-terminal":
                    cmd = [terminal, "--", "bash", "-c", inner_cmd]
                else:
                    cmd = [terminal, "-e", f"bash -c '{inner_cmd}'"]
                break
        else:
            log(f"[ERROR] No terminal emulator found")
            return False

    try:
        subprocess.Popen(cmd, shell=False)
        time.sleep(2)  # Give terminal time to spawn
        return True
    except Exception as e:
        log(f"[ERROR] Failed to spawn worker: {e}")
        return False


def is_worker_complete(round_num: int, lane_num: int) -> bool:
    """Check if a worker has completed (HANDOFF.md exists)."""
    output_dir = AGENT_DIR / f"round_{round_num}_lane_{lane_num}"
    handoff_file = output_dir / "HANDOFF.md"
    return handoff_file.exists()


def wait_for_workers(num_lanes: int, round_num: int, timeout: int = 3600) -> bool:
    """Wait for all workers in a round to complete."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        completed = sum(
            1 for lane in range(1, num_lanes + 1)
            if is_worker_complete(round_num, lane)
        )

        if completed == num_lanes:
            log(f"[ROUND {round_num}] All {num_lanes} workers completed")
            return True

        log(f"[ROUND {round_num}] {completed}/{num_lanes} workers done, waiting...")
        time.sleep(60)  # Check every minute

    log(f"[ROUND {round_num}] Timeout after {timeout}s")
    return False


# =============================================================================
# MAIN LOOP
# =============================================================================

def log(message: str):
    """Print timestamped log message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


def run_continuous(
    project_path: Path,
    num_lanes: int = 1,
    max_rounds: int = 50,
    round_delay: int = 30
):
    """
    Main continuous loop - the heart of Teneo Agent.

    This implements Huntley's Ralph Loop:
    1. Fresh context per task (each worker is independent)
    2. File-based state (TASKS.md is the source of truth)
    3. Git checkpoints (work is never lost)

    And Yegge's Landing the Plane:
    - Always push to remote
    - Clear handoffs between workers
    """
    log("=" * 60)
    log("TENEO AGENT - Overnight Runner")
    log(f"Project: {project_path}")
    log(f"Lanes: {num_lanes}")
    log(f"Max rounds: {max_rounds}")
    log("=" * 60)

    # Pre-run git checkpoint
    log("Creating pre-run git checkpoint...")
    git_checkpoint(project_path, "teneo-agent: pre-run checkpoint")

    # Create agent directory
    AGENT_DIR.mkdir(exist_ok=True)

    for round_num in range(1, max_rounds + 1):
        log(f"\n{'='*40}")
        log(f"ROUND {round_num}")
        log(f"{'='*40}")

        # Get incomplete tasks
        tasks = get_incomplete_tasks(TASKS_FILE)

        if not tasks:
            log("No incomplete tasks found. Run complete!")
            break

        log(f"Found {len(tasks)} incomplete tasks")

        # Spawn workers (one per lane, up to available tasks)
        tasks_this_round = tasks[:num_lanes]

        for lane_num, task_info in enumerate(tasks_this_round, 1):
            spawn_worker(
                project_path=project_path,
                round_num=round_num,
                lane_num=lane_num,
                task=task_info['task']
            )

        # Wait for workers to complete
        log(f"Waiting for {len(tasks_this_round)} workers...")
        wait_for_workers(len(tasks_this_round), round_num)

        # Periodic git checkpoint
        if round_num % 5 == 0:
            log("Periodic git checkpoint...")
            git_checkpoint(project_path, f"teneo-agent: round {round_num} checkpoint")

        # Delay before next round
        if round_num < max_rounds:
            log(f"Waiting {round_delay}s before next round...")
            time.sleep(round_delay)

    # Final checkpoint
    log("Final git checkpoint...")
    git_checkpoint(project_path, "teneo-agent: run complete")

    log("\n" + "=" * 60)
    log("TENEO AGENT RUN COMPLETE")
    log("=" * 60)


def show_status():
    """Show current status of tasks and recent runs."""
    log("TENEO AGENT STATUS")
    log("=" * 40)

    # Task status
    if TASKS_FILE.exists():
        tasks = parse_tasks(TASKS_FILE)
        completed = sum(1 for t in tasks if t['completed'])
        log(f"Tasks: {completed}/{len(tasks)} complete")

        incomplete = [t for t in tasks if not t['completed']]
        if incomplete:
            log("\nNext tasks:")
            for t in incomplete[:5]:
                log(f"  - {t['task'][:60]}")
    else:
        log(f"No task file found at {TASKS_FILE}")
        log("Create TASKS.md with checkbox format:")
        log("  - [ ] Your first task")
        log("  - [ ] Your second task")

    # Recent runs
    if AGENT_DIR.exists():
        runs = sorted(AGENT_DIR.glob("round_*_lane_*"))
        if runs:
            log(f"\nRecent runs: {len(runs)} worker sessions")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Teneo Agent - Run Claude agents overnight"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start agent run")
    start_parser.add_argument(
        "--project", "-p",
        type=str,
        default=".",
        help="Path to project (default: current directory)"
    )
    start_parser.add_argument(
        "--lanes", "-l",
        type=int,
        default=1,
        help="Number of parallel workers (default: 1)"
    )
    start_parser.add_argument(
        "--continuous", "-c",
        action="store_true",
        help="Run continuously until tasks done"
    )
    start_parser.add_argument(
        "--max-rounds", "-m",
        type=int,
        default=50,
        help="Maximum rounds to run (default: 50)"
    )

    # Status command
    subparsers.add_parser("status", help="Show current status")

    args = parser.parse_args()

    if args.command == "start":
        project_path = Path(args.project).resolve()

        if not project_path.exists():
            print(f"Error: Project path does not exist: {project_path}")
            sys.exit(1)

        max_rounds = args.max_rounds if args.continuous else 1

        run_continuous(
            project_path=project_path,
            num_lanes=args.lanes,
            max_rounds=max_rounds
        )

    elif args.command == "status":
        show_status()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
