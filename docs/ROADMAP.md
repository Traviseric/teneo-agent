# Teneo Agent Roadmap

## Vision

Teneo Agent is a **Python-native overnight runner** that bridges the gap between simple automation and complex multi-agent orchestration.

**Position**: Entry point for developers → Path to advanced tools (beads, gastown, 12-factor patterns)

---

## Current State (v1.0)

### What Works
- [x] Task file parsing (TASKS.md checkbox format)
- [x] Claude CLI integration
- [x] Multi-lane parallel workers
- [x] Git checkpoints (commit + push)
- [x] Cross-platform terminal spawning (Windows, macOS, Linux)
- [x] Worker handoff files (HANDOFF.md)
- [x] Continuous mode until tasks complete

### What's Missing
- [ ] No structured task dependencies
- [ ] No worker failure recovery
- [ ] No integration with external issue trackers
- [ ] No MCP server support
- [ ] No test suite

---

## Roadmap

### Phase 1: Hardening (Contributors Welcome!)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| **pytest suite** | HIGH | 4-8 hrs | Basic tests for task parsing, git ops |
| **Worker timeout** | HIGH | 2-4 hrs | Kill workers that hang too long |
| **Failure recovery** | HIGH | 4-8 hrs | Retry failed tasks, skip after N attempts |
| **Log aggregation** | MEDIUM | 2-4 hrs | Combine all worker logs into one file |
| **Status dashboard** | MEDIUM | 4-8 hrs | Terminal UI showing progress |

### Phase 2: Beads Integration

**Why**: [steveyegge/beads](https://github.com/steveyegge/beads) provides dependency-aware task tracking that's git-native.

| Feature | Priority | Description |
|---------|----------|-------------|
| **`bd` command detection** | HIGH | Auto-detect if beads is installed |
| **Beads task source** | HIGH | Read tasks from `bd ready` instead of TASKS.md |
| **Beads task completion** | HIGH | Mark beads tasks done when worker completes |
| **Dependency awareness** | MEDIUM | Don't start blocked tasks |
| **Hierarchical tasks** | MEDIUM | Support beads epic/task/subtask hierarchy |

**Integration Strategy**:
```python
# When beads is available, use it
if shutil.which('bd'):
    tasks = get_beads_ready_tasks()  # bd ready --json
else:
    tasks = parse_tasks(TASKS_FILE)  # Fallback to TASKS.md
```

### Phase 3: Gastown Alignment

**Why**: [steveyegge/gastown](https://github.com/steveyegge/gastown) is the next evolution - multi-agent workspace management.

| Concept | Teneo Agent | Gastown | Alignment Opportunity |
|---------|-------------|---------|----------------------|
| Work persistence | HANDOFF.md files | Git worktree hooks | Same pattern, different storage |
| Task tracking | TASKS.md | Beads + Convoys | Beads integration makes us compatible |
| Worker spawning | Platform terminals | tmux sessions | Could add tmux support |
| Coordination | File-based | Mayor orchestration | Teneo Agent is "Mayor-less" simple mode |

**Path Forward**:
1. Teneo Agent = Simple, single-project overnight runs
2. Gastown = Complex, multi-project, multi-agent orchestration
3. Migration path: Users can graduate from Teneo Agent to Gastown

### Phase 4: 12-Factor Compliance

**Why**: [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) defines production agent patterns.

| Factor | Current State | Improvement |
|--------|--------------|-------------|
| **Factor 3: Own context window** | ✅ Fresh context per worker | Add token budget tracking |
| **Factor 5: Unify execution state** | ✅ TASKS.md + HANDOFF.md | Align with beads state |
| **Factor 6: Launch/Pause/Resume** | ⚠️ Launch only | Add pause/resume via state file |
| **Factor 7: Contact humans** | ❌ Not implemented | Add notification on completion/failure |
| **Factor 9: Compact errors** | ⚠️ Basic logging | Summarize errors for context |
| **Factor 10: Small focused agents** | ✅ One task per worker | Document this pattern |

### Phase 5: Advanced Features

| Feature | Description |
|---------|-------------|
| **MCP Server** | Expose teneo-agent as an MCP tool |
| **Web dashboard** | Browser-based status + control |
| **Multi-project** | Run against multiple repos simultaneously |
| **Custom workers** | Support other agents (Codex, Cursor, etc.) |
| **Cloud mode** | Run workers in cloud VMs |

---

## Contribution Priorities

### 🔴 High Impact, Help Wanted

1. **Beads integration** - Makes us part of the Yegge ecosystem
2. **Worker failure recovery** - Critical for overnight reliability
3. **pytest suite** - Foundation for everything else

### 🟡 Medium Impact, Good First Issues

1. **Log aggregation** - Simple file I/O
2. **Worker timeout** - Add subprocess timeout handling
3. **tmux support** - Alternative to platform terminals

### 🟢 Documentation Contributions

1. **Case studies** - Share your overnight run results
2. **Platform guides** - Windows/macOS/Linux specifics
3. **Video tutorials** - Walkthrough videos

---

## Related Projects

| Project | Relationship |
|---------|-------------|
| [steveyegge/beads](https://github.com/steveyegge/beads) | Task tracking integration target |
| [steveyegge/gastown](https://github.com/steveyegge/gastown) | Advanced orchestration (graduation path) |
| [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents) | Pattern reference |
| [ghuntley/how-to-build-a-coding-agent](https://github.com/ghuntley/how-to-build-a-coding-agent) | Educational reference |

---

*This roadmap is a living document. Open an issue or PR to suggest changes.*
