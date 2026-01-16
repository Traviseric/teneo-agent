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

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import modules
from modules import (
    log,
    parse_tasks, get_incomplete_tasks, mark_task_complete,
    git_checkpoint,
    spawn_worker, is_worker_complete, wait_for_workers,
    configure_worker_spawner,
    run_preflight_checks, print_preflight_report,
    prevent_sleep, allow_sleep,
    analyze_run, write_run_report, send_anonymous_stats,
    configure_run_analyzer,
)
from prompts import create_setup_prompt

# =============================================================================
# CONFIGURATION
# =============================================================================

# Script directory (where teneo_agent.py lives)
SCRIPT_DIR = Path(__file__).parent

# Working directory for agent output (in script dir)
AGENT_DIR = SCRIPT_DIR / "agent_runs"


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
# PROJECT VALIDATION & SETUP
# =============================================================================

def validate_project(project_path: Path) -> dict:
    """
    Check if project is ready for overnight agents.

    Returns dict with:
        - ready: bool
        - issues: list of problems found
        - has_claude_md: bool
        - has_tasks: bool
    """
    issues = []

    claude_md = project_path / "CLAUDE.md"
    has_claude_md = claude_md.exists()
    if not has_claude_md:
        issues.append("No CLAUDE.md found - agents need project context")

    tasks_file = project_path / "TASKS.md"
    has_tasks = False
    if tasks_file.exists():
        content = tasks_file.read_text(encoding='utf-8')
        incomplete_count = content.count("- [ ]")
        has_tasks = incomplete_count > 0
        if not has_tasks:
            issues.append("No incomplete tasks in TASKS.md")
    else:
        issues.append("No TASKS.md found - agents need tasks to execute")

    return {
        "ready": len(issues) == 0,
        "issues": issues,
        "has_claude_md": has_claude_md,
        "has_tasks": has_tasks,
    }


# =============================================================================
# MAIN LOOP
# =============================================================================

def run_continuous(
    project_path: Path,
    num_lanes: int = 1,
    max_rounds: int = 50,
    round_delay: int = 30,
    share_stats: bool = False
):
    """
    Main continuous loop - the heart of Teneo Agent.

    Three phases:
    - Phase 1: Validate project (setup if needed)
    - Phase 2: Execute tasks
    - Phase 3: Analyze run and generate report

    This implements Huntley's Ralph Loop:
    1. Fresh context per task (each worker is independent)
    2. File-based state (TASKS.md is the source of truth)
    3. Git checkpoints (work is never lost)

    And Yegge's Landing the Plane:
    - Always push to remote
    - Clear handoffs between workers
    """
    start_time = datetime.now()
    rounds_completed = 0
    model = os.environ.get("TENEO_MODEL", "sonnet")

    # Configure modules with runtime paths
    configure_worker_spawner(AGENT_DIR, CLAUDE_CMD)
    configure_run_analyzer(AGENT_DIR)

    log("=" * 60)
    log("TENEO AGENT - Overnight Runner")
    log(f"Project: {project_path}")
    log(f"Lanes: {num_lanes}")
    log(f"Max rounds: {max_rounds}")
    log(f"Model: {model}")
    log("=" * 60)

    # ===========================================
    # PHASE 1: VALIDATE PROJECT
    # ===========================================
    log("\n[PHASE 1] Validating project...")

    # Run preflight checks
    preflight = run_preflight_checks(project_path, CLAUDE_CMD)
    print_preflight_report(preflight)

    if not preflight.passed:
        log("[ERROR] Preflight checks failed. Fix errors and retry.")
        return

    validation = validate_project(project_path)

    if not validation["ready"]:
        log("Project needs setup:")
        for issue in validation["issues"]:
            log(f"  - {issue}")

        log("\n[SETUP] Running setup worker to prepare project...")

        # Create agent directory
        AGENT_DIR.mkdir(exist_ok=True)

        # Spawn setup worker
        setup_task = create_setup_prompt(project_path)
        spawn_worker(
            project_path=project_path,
            round_num=0,  # Round 0 = setup
            lane_num=1,
            task=setup_task
        )

        # Wait for setup to complete
        log("Waiting for setup worker to finish...")
        wait_for_workers(1, 0, timeout=1800)  # 30 min timeout for setup

        # Re-validate
        validation = validate_project(project_path)
        if not validation["ready"]:
            log("\n[WARN] Setup may not be complete. Check the HANDOFF.md")
            log("You may need to run again or manually create TASKS.md")
            return

        log("\n[SETUP COMPLETE] Project is ready for overnight run!")
        log("=" * 60)

    # ===========================================
    # PHASE 2: EXECUTE TASKS
    # ===========================================
    log("\n[PHASE 2] Starting task execution...")

    # Prevent sleep during run
    prevent_sleep()

    try:
        # Pre-run git checkpoint
        log("Creating pre-run git checkpoint...")
        git_checkpoint(project_path, "teneo-agent: pre-run checkpoint")

        # Create agent directory
        AGENT_DIR.mkdir(exist_ok=True)

        for round_num in range(1, max_rounds + 1):
            log(f"\n{'='*40}")
            log(f"ROUND {round_num}")
            log(f"{'='*40}")

            # Get incomplete tasks from project's TASKS.md
            tasks_file = project_path / "TASKS.md"
            tasks = get_incomplete_tasks(tasks_file)

            if not tasks:
                log("No incomplete tasks found. Run complete!")
                break

            rounds_completed = round_num
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

    finally:
        # Always allow sleep when done
        allow_sleep()

    # ===========================================
    # PHASE 3: ANALYZE & REPORT
    # ===========================================
    log("\n[PHASE 3] Analyzing run...")

    analysis = analyze_run(project_path, rounds_completed, start_time)
    report_path = write_run_report(project_path, analysis)

    log(f"\nRun Summary:")
    log(f"  Duration: {analysis['duration_minutes']:.1f} minutes")
    log(f"  Rounds: {rounds_completed}")
    log(f"  Workers: {analysis['metrics']['total_workers']}")
    log(f"  Success Rate: {analysis['metrics']['success_rate']:.1f}%")
    log(f"  Tasks Completed: {analysis['metrics'].get('tasks_completed', 'N/A')}")
    log(f"  Tasks Pending: {analysis['metrics'].get('tasks_pending', 'N/A')}")

    if analysis['patterns']:
        log(f"\nPatterns Detected: {len(analysis['patterns'])}")
        for p in analysis['patterns']:
            log(f"  [{p['severity'].upper()}] {p['description']}")

    log(f"\nReport: {report_path}")

    # Opt-in stats sharing
    if share_stats:
        log("\nSharing anonymous stats to help improve Teneo Agent...")
        if send_anonymous_stats(analysis, model):
            log("Stats shared successfully. Thank you for contributing!")
        else:
            log("Stats sharing failed (no worries, run completed successfully)")

    log("\n" + "=" * 60)
    log("TENEO AGENT RUN COMPLETE")
    log("=" * 60)


def show_status(project_path: Path = None):
    """Show current status of tasks and recent runs."""
    log("TENEO AGENT STATUS")
    log("=" * 40)

    if project_path is None:
        project_path = Path.cwd()

    tasks_file = project_path / "TASKS.md"

    log(f"Project: {project_path}")

    # Task status
    if tasks_file.exists():
        tasks = parse_tasks(tasks_file)
        completed = sum(1 for t in tasks if t['completed'])
        log(f"Tasks: {completed}/{len(tasks)} complete")

        incomplete = [t for t in tasks if not t['completed']]
        if incomplete:
            log("\nNext tasks:")
            for t in incomplete[:5]:
                log(f"  - {t['task'][:60]}")
    else:
        log(f"No task file found at {tasks_file}")
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
    start_parser.add_argument(
        "--share-stats",
        action="store_true",
        help="Share anonymous run stats to help improve Teneo Agent (opt-in)"
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Show current status")
    status_parser.add_argument(
        "--project", "-p",
        type=str,
        default=".",
        help="Path to project (default: current directory)"
    )

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
            max_rounds=max_rounds,
            share_stats=args.share_stats
        )

    elif args.command == "status":
        project_path = Path(args.project).resolve()
        show_status(project_path)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
