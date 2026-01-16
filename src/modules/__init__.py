"""
Teneo Agent Modules
===================

Reusable modules for overnight agent runners.

Available modules:
- logging_utils: Timestamped logging
- task_parser: Parse TASKS.md checkbox format
- git_operations: Git checkpoint, commit, push
- worker_spawner: Spawn Claude workers in terminals
- preflight_checks: Validate system before run
- sleep_prevention: Keep computer awake
- run_analyzer: Post-run analysis and reporting
"""

from .logging_utils import log, set_log_callback
from .task_parser import parse_tasks, get_incomplete_tasks, mark_task_complete, count_tasks
from .git_operations import git_checkpoint, get_current_branch, get_short_hash
from .worker_spawner import (
    spawn_worker, is_worker_complete, wait_for_workers,
    configure as configure_worker_spawner
)
from .preflight_checks import run_preflight_checks, PreflightResults, print_preflight_report
from .sleep_prevention import prevent_sleep, allow_sleep, SleepPrevention
from .run_analyzer import (
    analyze_run, write_run_report, send_anonymous_stats,
    configure as configure_run_analyzer
)

__all__ = [
    # Logging
    "log", "set_log_callback",
    # Tasks
    "parse_tasks", "get_incomplete_tasks", "mark_task_complete", "count_tasks",
    # Git
    "git_checkpoint", "get_current_branch", "get_short_hash",
    # Workers
    "spawn_worker", "is_worker_complete", "wait_for_workers", "configure_worker_spawner",
    # Preflight
    "run_preflight_checks", "PreflightResults", "print_preflight_report",
    # Sleep
    "prevent_sleep", "allow_sleep", "SleepPrevention",
    # Analysis
    "analyze_run", "write_run_report", "send_anonymous_stats", "configure_run_analyzer",
]
