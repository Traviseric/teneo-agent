"""
Worker spawner for Teneo Agent.

Spawns Claude workers in new terminal windows across platforms.
"""

import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from .logging_utils import log

# Global config - set by main runner
AGENT_DIR: Optional[Path] = None
CLAUDE_CMD: str = "claude"


def configure(agent_dir: Path, claude_cmd: str):
    """Configure module globals."""
    global AGENT_DIR, CLAUDE_CMD
    AGENT_DIR = agent_dir
    CLAUDE_CMD = claude_cmd


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
**Task File:** `{project_path / "TASKS.md"}`
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
    if AGENT_DIR is None:
        log("[ERROR] worker_spawner not configured. Call configure() first.")
        return False

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
    # --model can be set via TENEO_MODEL env var (default: sonnet)
    model = os.environ.get("TENEO_MODEL", "sonnet")
    claude_args = [
        CLAUDE_CMD,
        "-p",
        "--dangerously-skip-permissions",
        "--model", model,
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
    if AGENT_DIR is None:
        return False
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
