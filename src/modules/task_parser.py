"""
Task parser for TASKS.md checkbox format.

Parses markdown files with checkbox-format tasks:
    - [ ] Incomplete task
    - [x] Completed task
"""

import re
from pathlib import Path
from typing import List


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


def count_tasks(file_path: Path) -> tuple:
    """
    Count completed and pending tasks.

    Returns (completed, pending) tuple.
    """
    if not file_path.exists():
        return 0, 0

    content = file_path.read_text(encoding='utf-8')
    completed = content.count("- [x]") + content.count("- [X]")
    pending = content.count("- [ ]")
    return completed, pending
