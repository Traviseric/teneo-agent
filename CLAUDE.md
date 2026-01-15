# Teneo Agent

Open source overnight AI agent runner. Part of the Teneo ecosystem.

## Lookup Table

| Concept | Files | Search Terms |
|---------|-------|--------------|
| Relay Runner | teneo_agent.py | spawn, worker, continuous, relay |
| Ralph Runner | ralph_runner.py | ralph, fresh context, PROMPT.md |
| Task Parsing | teneo_agent.py:65-116 | parse_tasks, checkbox, incomplete |
| Git Operations | teneo_agent.py:119-175 | checkpoint, commit, push |
| Worker Prompts | teneo_agent.py:182-271 | create_worker_prompt, WORKER.md |
| Worker Spawning | teneo_agent.py:274-348 | spawn_worker, terminal, wt |
| Main Loop | teneo_agent.py:389-466 | run_continuous, round |
| Best Practices | BEST_PRACTICES.md | principles, CLAUDE.md, tasks |
| MCP Guide | docs/MCP_OPTIMIZATION.md | token, CLI, config |
| Doc Organization | docs/DOC_ORGANIZATION.md | clean root, docs folder |
| Project Audit | docs/AUDIT_YOUR_PROJECT.md | scorecard, audit |

## Stack

- Language: Python 3.8+
- CLI: Claude Code
- Terminal: Windows Terminal / macOS Terminal / gnome-terminal
- Version Control: Git

## Commands

```bash
# Run single round
python teneo_agent.py start --project /path/to/project

# Run continuous until tasks done
python teneo_agent.py start --project /path/to/project --continuous

# Multiple parallel workers
python teneo_agent.py start --project /path/to/project --lanes 2 --continuous

# Check status
python teneo_agent.py status
```

## Conventions

- Single-file runner (no external dependencies)
- Inline implementations (self-contained)
- Cross-platform terminal spawning
- Checkbox task format (`- [ ]` / `- [x]`)

## Current Focus

Public open source tool for the community. Keep it simple.

## Upgrade Path

- **Free**: This repo (teneo-agent)
- **Pro**: [teneo-agent-pro](https://traviseric.com/products/ai-development-system) - Enhanced capabilities ($197)
