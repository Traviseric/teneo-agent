# Contributing to Teneo Agent

Thank you for your interest in contributing to Teneo Agent! This project is part of a larger mission to make overnight AI development accessible and reliable.

## Quick Links

- [Roadmap](docs/ROADMAP.md) - Where we're headed
- [Patterns](docs/PATTERNS.md) - Core patterns we implement
- [Community Strategy](docs/COMMUNITY_STRATEGY.md) - How we connect with the community

## Ways to Contribute

### 1. Code Contributions

| Area | Priority | Description |
|------|----------|-------------|
| **Platform Support** | HIGH | Improve Windows/macOS/Linux terminal spawning |
| **Beads Integration** | HIGH | Connect with [steveyegge/beads](https://github.com/steveyegge/beads) |
| **Error Recovery** | MEDIUM | Better handling of worker failures |
| **MCP Support** | MEDIUM | Model Context Protocol integration |
| **Tests** | MEDIUM | pytest test suite |

### 2. Documentation

- Usage examples and tutorials
- Case studies from your overnight runs
- Troubleshooting guides

### 3. Ideas & Feedback

- Open an issue with your use case
- Share what worked (or didn't) in your overnight runs
- Suggest patterns from other agent frameworks

## Development Setup

```bash
# Clone the repo
git clone https://github.com/Traviseric/teneo-agent.git
cd teneo-agent

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Test with the example tasks
cp TASKS.md.example TASKS.md
python teneo_agent.py status
```

## Code Style

- **Python 3.8+** compatible
- **Type hints** encouraged but not required
- **Docstrings** for public functions
- **Comments** for non-obvious logic

## Pull Request Process

1. **Fork** the repo
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** and test locally
4. **Commit** with clear messages
5. **Push** and open a PR

### PR Checklist

- [ ] Code runs without errors
- [ ] Works on your platform (note which OS)
- [ ] Updated README if adding features
- [ ] No hardcoded paths

## Architecture Overview

```
teneo_agent.py
├── Configuration       # Paths, Claude CLI detection
├── Task Parsing        # Read/write TASKS.md
├── Git Operations      # Checkpoints (add/commit/push)
├── Worker Management   # Spawn workers in terminals
└── Main Loop           # The overnight runner logic
```

### Key Functions

| Function | Purpose |
|----------|--------|
| `parse_tasks()` | Read checkbox tasks from TASKS.md |
| `spawn_worker()` | Launch Claude in a new terminal |
| `git_checkpoint()` | Safe commit + push |
| `run_continuous()` | The main overnight loop |

## Integration Points

Teneo Agent is designed to integrate with the broader AI agent ecosystem:

### [steveyegge/beads](https://github.com/steveyegge/beads)
- Graph-based issue tracking
- Could replace TASKS.md with beads tasks
- See: [docs/ROADMAP.md](docs/ROADMAP.md#beads-integration)

### [steveyegge/gastown](https://github.com/steveyegge/gastown)
- Multi-agent workspace orchestration
- Hook-based persistence (similar to our checkpoint pattern)
- See: [docs/ROADMAP.md](docs/ROADMAP.md#gastown-alignment)

### [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)
- We implement several factors
- See: [docs/PATTERNS.md](docs/PATTERNS.md)

## Community

- **Author**: [Travis Eric](https://traviseric.com)
- **Course**: [AI-First Fundamentals](https://traviseric.com/courses/ai-first-fundamentals)
- **Issues**: Open a GitHub issue for bugs or features

## License

MIT License - contributions are licensed under the same terms.

---

*Built independently. Enhanced by insights from the AI-first development community.*
