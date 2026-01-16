"""
Worker prompts for Teneo Agent.

Contains prompt templates for workers and setup tasks.
"""

from datetime import datetime
from pathlib import Path


def create_worker_prompt(
    task: str,
    project_path: Path,
    round_num: int,
    lane_num: int,
    output_dir: Path
) -> str:
    """
    Create prompt content for a Claude worker.

    This is "The Pin" from Huntley's Ralph Loop - the immutable
    intent anchor that tells the worker exactly what to do.
    """
    worker_id = f"R{round_num}L{lane_num}"
    log_file = output_dir / "LOG.md"
    handoff_file = output_dir / "HANDOFF.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""# Teneo Agent Worker: {worker_id}

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


def create_setup_prompt(project_path: Path) -> str:
    """
    Create a setup task prompt for projects that aren't ready.

    This task tells the first worker to set up the project
    for overnight agent runs.
    """
    return f"""Set up this project for overnight AI agents.

**Your job:**
1. Explore the project structure at `{project_path}`
2. Create a `CLAUDE.md` file with:
   - Project description (1-2 sentences)
   - Lookup table mapping concepts to files
   - Build/test commands
   - Current focus
   - Keep it under 60 lines
3. Create a `TASKS.md` file with 5-10 specific tasks based on what you find:
   - Look for TODOs, FIXMEs in code
   - Check for missing tests
   - Look for incomplete features
   - Use checkbox format: `- [ ] Task description`
4. If root directory is cluttered (>20 files), suggest which files to move to docs/

**Quality check:**
- CLAUDE.md exists and has lookup table
- TASKS.md has at least 3 actionable tasks
- Tasks are specific (not vague like "improve code")

When done, write HANDOFF.md explaining what you set up."""
