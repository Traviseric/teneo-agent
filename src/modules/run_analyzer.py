"""
Run analyzer for Teneo Agent.

Analyzes completed runs and generates reports.
"""

import json
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .logging_utils import log

# Crowdsource stats endpoint (opt-in)
STATS_ENDPOINT = "https://api.traviseric.com/teneo-stats"

# Global config - set by main runner
AGENT_DIR: Optional[Path] = None


def configure(agent_dir: Path):
    """Configure module globals."""
    global AGENT_DIR
    AGENT_DIR = agent_dir


def analyze_run(project_path: Path, rounds_completed: int, start_time: datetime) -> dict:
    """
    Analyze the completed run and generate metrics.

    Returns dict with:
        - metrics: aggregate statistics
        - patterns: detected issues
        - report_path: path to generated report
    """
    results = {
        "project": project_path.name,
        "timestamp": datetime.now().isoformat(),
        "duration_minutes": (datetime.now() - start_time).total_seconds() / 60,
        "rounds_completed": rounds_completed,
        "metrics": {},
        "patterns": [],
        "improvements": [],
    }

    if AGENT_DIR is None:
        log("[WARN] run_analyzer not configured")
        return results

    # Collect worker results
    workers = []
    for worker_dir in sorted(AGENT_DIR.glob("round_*_lane_*")):
        worker_info = _analyze_worker(worker_dir)
        if worker_info:
            workers.append(worker_info)

    # Calculate metrics
    total_workers = len(workers)
    completed = sum(1 for w in workers if w["status"] == "complete")
    failed = sum(1 for w in workers if w["status"] == "failed")
    timeout = sum(1 for w in workers if w["status"] == "timeout")

    results["metrics"] = {
        "total_workers": total_workers,
        "completed": completed,
        "failed": failed,
        "timeout": timeout,
        "success_rate": (completed / total_workers * 100) if total_workers > 0 else 0,
        "duration_minutes": results["duration_minutes"],
    }

    # Count tasks
    tasks_file = project_path / "TASKS.md"
    if tasks_file.exists():
        content = tasks_file.read_text(encoding='utf-8')
        results["metrics"]["tasks_completed"] = content.count("- [x]") + content.count("- [X]")
        results["metrics"]["tasks_pending"] = content.count("- [ ]")

    # Detect patterns
    results["patterns"] = _detect_patterns(workers, results["metrics"])

    # Generate improvements
    results["improvements"] = _generate_improvements(results["patterns"])

    return results


def _analyze_worker(worker_dir: Path) -> dict:
    """Analyze a single worker directory."""
    handoff = worker_dir / "HANDOFF.md"
    log_file = worker_dir / "LOG.md"
    worker_file = worker_dir / "WORKER.md"

    # Determine status
    if handoff.exists() and handoff.stat().st_size > 50:
        status = "complete"
    elif log_file.exists():
        log_content = log_file.read_text(encoding='utf-8', errors='replace').lower()
        if "error" in log_content or "failed" in log_content:
            status = "failed"
        else:
            status = "timeout"
    else:
        status = "timeout"

    # Extract task
    task = "Unknown"
    if worker_file.exists():
        content = worker_file.read_text(encoding='utf-8', errors='replace')
        for line in content.split('\n'):
            if line.strip().startswith('- [ ]') or line.strip().startswith('- [x]'):
                task = line.strip()
                break
            if 'task:' in line.lower():
                task = line.split(':', 1)[-1].strip()
                break

    return {
        "dir": worker_dir.name,
        "status": status,
        "task": task[:100],
    }


def _detect_patterns(workers: list, metrics: dict) -> list:
    """Detect patterns indicating issues."""
    patterns = []

    # High failure rate
    if metrics["total_workers"] > 0:
        failure_rate = (metrics["failed"] + metrics["timeout"]) / metrics["total_workers"]
        if failure_rate > 0.3:
            patterns.append({
                "type": "high_failure_rate",
                "severity": "high",
                "description": f"High failure rate: {failure_rate * 100:.0f}%",
                "recommendation": "Check worker logs for common errors. Tasks may be too complex.",
            })

    # No tasks completed
    if metrics.get("tasks_completed", 0) == 0 and metrics["completed"] > 0:
        patterns.append({
            "type": "tasks_not_marked",
            "severity": "medium",
            "description": "Workers completed but no tasks marked done",
            "recommendation": "Workers may not be updating TASKS.md. Check prompts.",
        })

    # Very fast completions (< 30 seconds average)
    if metrics["completed"] > 2 and metrics["duration_minutes"] < 2:
        patterns.append({
            "type": "shallow_work",
            "severity": "medium",
            "description": "Workers completing very quickly - may indicate shallow fixes",
            "recommendation": "Average time per task is very low. Workers may not be thorough.",
        })

    return patterns


def _generate_improvements(patterns: list) -> list:
    """Generate improvement suggestions from patterns."""
    improvements = []
    for p in patterns:
        improvements.append({
            "priority": "P0" if p["severity"] == "high" else "P1",
            "title": p["description"],
            "action": p["recommendation"],
        })
    return improvements


def write_run_report(project_path: Path, analysis: dict) -> Path:
    """Write RUN_REPORT.md to the project."""
    report_path = project_path / "RUN_REPORT.md"

    content = f"""# Teneo Agent Run Report

**Project:** {analysis['project']}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Duration:** {analysis['duration_minutes']:.1f} minutes
**Rounds:** {analysis['rounds_completed']}

## Metrics

| Metric | Value |
|--------|-------|
| Total Workers | {analysis['metrics']['total_workers']} |
| Completed | {analysis['metrics']['completed']} |
| Failed | {analysis['metrics']['failed']} |
| Timeout | {analysis['metrics']['timeout']} |
| Success Rate | {analysis['metrics']['success_rate']:.1f}% |
| Tasks Completed | {analysis['metrics'].get('tasks_completed', 'N/A')} |
| Tasks Pending | {analysis['metrics'].get('tasks_pending', 'N/A')} |

## Patterns Detected

"""
    if analysis['patterns']:
        for p in analysis['patterns']:
            content += f"### [{p['severity'].upper()}] {p['description']}\n\n"
            content += f"**Recommendation:** {p['recommendation']}\n\n"
    else:
        content += "*No significant patterns detected. Run looks healthy!*\n\n"

    content += """## Improvements

"""
    if analysis['improvements']:
        for imp in analysis['improvements']:
            content += f"- **[{imp['priority']}]** {imp['title']}: {imp['action']}\n"
    else:
        content += "*No improvements needed.*\n"

    content += f"""
---

*Generated by [Teneo Agent](https://github.com/Traviseric/teneo-agent)*

**Want to improve overnight agents for everyone?**
Run with `--share-stats` to anonymously contribute your run metrics.
"""

    report_path.write_text(content, encoding='utf-8')
    return report_path


def send_anonymous_stats(analysis: dict, model: str = "sonnet") -> bool:
    """
    Send anonymous stats to help improve Teneo Agent for everyone.

    Only sends:
    - Success rate, task counts, duration
    - Detected patterns (no code/content)
    - Model used, lanes

    Does NOT send:
    - Project name or path
    - Task descriptions
    - Any code or file contents
    """
    try:
        # Anonymize - only send aggregate metrics
        payload = {
            "version": "1.0.0",
            "model": model,
            "metrics": {
                "success_rate": analysis["metrics"]["success_rate"],
                "tasks_completed": analysis["metrics"].get("tasks_completed", 0),
                "tasks_pending": analysis["metrics"].get("tasks_pending", 0),
                "duration_minutes": analysis["duration_minutes"],
                "rounds": analysis["rounds_completed"],
                "workers": analysis["metrics"]["total_workers"],
            },
            "patterns": [p["type"] for p in analysis["patterns"]],  # Just pattern types, no details
            "timestamp": datetime.now().isoformat(),
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            STATS_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200

    except Exception:
        # Silently fail - stats are optional
        return False
