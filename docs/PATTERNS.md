# Teneo Agent Patterns

Core patterns implemented in Teneo Agent and their origins.

---

## Pattern Overview

| Pattern | Source | Implementation |
|---------|--------|---------------|
| Fresh Context | Huntley | Each worker starts with clean context |
| File-Based State | Original | TASKS.md as source of truth |
| Landing the Plane | Yegge | Git checkpoint after each round |
| Worker Isolation | Original | Independent terminal per worker |
| Handoff Continuity | Original | HANDOFF.md passes context forward |

---

## 1. Fresh Context Per Worker

**Origin**: Geoffrey Huntley's "Ralph Wiggum Loop"

**Problem**: Long-running agents accumulate context that degrades performance.

**Solution**: Each worker gets a completely fresh Claude session.

```
Round 1: Worker reads task → Executes → Writes handoff → Terminates
Round 2: NEW worker reads task → Reads previous handoff → Executes → ...
```

**Implementation**:
```python
# Each spawn_worker() creates a new terminal with new Claude session
def spawn_worker(project_path, round_num, lane_num, task):
    # Worker prompt is the ONLY context - no accumulated history
    worker_file = create_worker_prompt(...)
    # New terminal = new Claude session = fresh context
    subprocess.Popen(["wt", "new-tab", ..., "cat", worker_file, "|", "claude"])
```

**Why It Works**:
- No context pollution from previous tasks
- Each worker focused on exactly one task
- Failed workers don't corrupt future workers

---

## 2. File-Based State ("The Source of Truth")

**Origin**: Independent development, validated by community patterns

**Problem**: In-memory state is lost on crashes.

**Solution**: All state lives in files that survive restarts.

```
TASKS.md      → What needs to be done (checkbox list)
WORKER.md     → Current worker's instructions
LOG.md        → Progress during execution
HANDOFF.md    → What happened (for next worker)
```

**Implementation**:
```python
# State is ALWAYS in files, never in variables
def get_incomplete_tasks(file_path):
    return [t for t in parse_tasks(file_path) if not t['completed']]

# Check completion by file existence, not memory
def is_worker_complete(round_num, lane_num):
    handoff_file = AGENT_DIR / f"round_{round_num}_lane_{lane_num}" / "HANDOFF.md"
    return handoff_file.exists()
```

**Why It Works**:
- Crash? Just restart - files are still there
- Debug by reading files, not logs
- Multiple processes can coordinate via files

---

## 3. Landing the Plane

**Origin**: Steve Yegge's Vibe Coding principles

**Problem**: Work done but not committed is work that can be lost.

**Solution**: Aggressive git checkpoints - commit and push frequently.

```
Start run    → checkpoint
Every N rounds → checkpoint
End run      → checkpoint
On error     → checkpoint
```

**Implementation**:
```python
def git_checkpoint(project_path, message=None):
    # Stage everything
    subprocess.run(["git", "add", "-A"], cwd=project_path)
    # Commit with timestamp
    subprocess.run(["git", "commit", "-m", message], cwd=project_path)
    # Push immediately - don't let commits pile up
    subprocess.run(["git", "push"], cwd=project_path)
```

**Why It Works**:
- Power outage? Work is on remote
- Bad change? Git revert
- Review next morning? See commits

---

## 4. Worker Isolation

**Origin**: Independent development

**Problem**: Workers interfering with each other.

**Solution**: Each worker runs in its own terminal process.

```
Lane 1: Terminal Window 1 → Claude session 1 → Task A
Lane 2: Terminal Window 2 → Claude session 2 → Task B
```

**Implementation**:
```python
# Platform-specific terminal spawning
if sys.platform == "win32":
    cmd = ["wt", "new-tab", "--title", f"Worker {lane}", ...]
elif sys.platform == "darwin":
    cmd = ["osascript", "-e", 'tell app "Terminal" to do script "..."']
else:
    cmd = ["gnome-terminal", "--", "bash", "-c", "..."]
```

**Why It Works**:
- No shared state between workers
- One worker crash doesn't kill others
- Visual feedback (see all terminals working)

---

## 5. Handoff Continuity

**Origin**: Independent development

**Problem**: Next worker doesn't know what previous worker did.

**Solution**: Mandatory HANDOFF.md file at end of each worker.

```markdown
# R1L1 Handoff

## Completed
- Added login form component
- Created API route /api/auth/login

## Next Steps
- Add form validation
- Connect to database

## Notes
- Used shadcn/ui for components
- Auth strategy: JWT in httpOnly cookie
```

**Implementation**:
```python
# Worker prompt REQUIRES handoff
content = f"""
### Handoff (Required)
When done, write `{handoff_file}`:

```markdown
## Completed
- What you finished

## Next Steps  
- What the next worker should do
```
"""
```

**Why It Works**:
- Context survives across workers
- Human review in the morning
- Documentation of what happened

---

## 12-Factor Alignment

How Teneo Agent patterns map to [12-factor-agents](https://github.com/humanlayer/12-factor-agents):

| 12-Factor | Teneo Agent Pattern | Status |
|-----------|--------------------|---------|
| Factor 3: Own your context | Fresh Context | ✅ Implemented |
| Factor 5: Unify state | File-Based State | ✅ Implemented |
| Factor 6: Launch/Pause/Resume | - | ⚠️ Launch only |
| Factor 7: Contact humans | - | ❌ Not yet |
| Factor 9: Compact errors | LOG.md | ⚠️ Basic |
| Factor 10: Small agents | Worker Isolation | ✅ Implemented |
| Factor 12: Stateless reducer | - | ⚠️ Partial |

---

## Attribution

These patterns were developed independently and later found to align with community work:

- **Geoffrey Huntley**: Fresh context principle, Ralph Loop concept
- **Steve Yegge**: Landing the Plane, beads integration patterns
- **Dex Horthy**: 12-factor agents framework

We credit their public work which helped validate and refine our approach.

---

*See [ROADMAP.md](ROADMAP.md) for planned pattern improvements.*
