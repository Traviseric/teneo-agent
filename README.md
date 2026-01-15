# Teneo Agent

Run Claude agents overnight to build your projects autonomously.

Built by [Travis Eric](https://traviseric.com) as part of the Teneo ecosystem. Enhanced with insights from the AI-first development community including [Geoffrey Huntley](https://www.yourfirstagent.com/) and [Steve Yegge](https://github.com/steveyegge/beads).

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/Traviseric/teneo-agent.git
cd teneo-agent

# 2. Set your Anthropic API key (or use Claude CLI login)
claude login
# OR
export ANTHROPIC_API_KEY=your_key_here

# 3. Create your task file
cp TASKS.md.example TASKS.md
# Edit TASKS.md with your tasks

# 4. Run the agent
python teneo_agent.py start --project /path/to/your/project --continuous
```

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                     TENEO AGENT                         │
│                                                         │
│  TASKS.md ──► Agent reads task                          │
│      │                                                  │
│      ▼                                                  │
│  Spawn Claude worker in terminal                        │
│      │                                                  │
│      ▼                                                  │
│  Worker executes task autonomously                      │
│      │                                                  │
│      ▼                                                  │
│  Worker writes HANDOFF.md when done                     │
│      │                                                  │
│      ▼                                                  │
│  Git checkpoint (commit + push)                         │
│      │                                                  │
│      ▼                                                  │
│  Loop: Next task until done                             │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Python 3.8+**
- **Claude CLI** - `npm install -g @anthropic-ai/claude-code`
- **Git** - for checkpoints
- **Windows Terminal** (Windows) or Terminal.app (macOS) or gnome-terminal (Linux)

## Commands

```bash
# Run single round (1 task)
python teneo_agent.py start --project ./my-project

# Run continuously until all tasks done
python teneo_agent.py start --project ./my-project --continuous

# Run with 2 parallel workers
python teneo_agent.py start --project ./my-project --lanes 2 --continuous

# Check status
python teneo_agent.py status
```

## Task File Format

Create `TASKS.md` with checkbox-format tasks:

```markdown
# Project Tasks

## Phase 1: Setup
- [ ] Initialize project with Next.js and TypeScript
- [ ] Add Tailwind CSS configuration
- [ ] Create basic folder structure

## Phase 2: Features
- [ ] Create login page with email/password form
- [ ] Add user dashboard page
- [ ] Implement API routes for authentication

## Phase 3: Polish
- [ ] Add loading states to all buttons
- [ ] Write unit tests for auth functions
- [ ] Update README with setup instructions
```

Workers will:
1. Pick up the first incomplete task (`- [ ]`)
2. Execute it in your project
3. Mark it complete (`- [x]`) when done
4. Write a handoff for the next worker

## Directory Structure

```
teneo-agent/
├── teneo_agent.py      # Main script
├── TASKS.md            # Your task list (create this)
├── agent_runs/         # Worker output (auto-created)
│   └── round_1_lane_1/
│       ├── WORKER.md   # Worker instructions
│       ├── LOG.md      # Progress log
│       └── HANDOFF.md  # Completion handoff
└── README.md
```

## Core Patterns

Teneo Agent implements patterns I developed through months of overnight agent runs:

### Task Relay Pattern (Original)
- **File-based coordination** - TASKS.md is the source of truth
- **Worker isolation** - each worker gets a clean context
- **Checkpoint safety** - git commits protect your work
- **Handoff continuity** - workers pass context to the next

### Enhanced With Community Insights
After building the core system, I studied work from Huntley and Yegge:
- **Fresh context principle** (Huntley) - reinforced my worker isolation approach
- **Landing the Plane** (Yegge) - formalized my checkpoint discipline

## Configuration

### Environment Variables

```bash
# Optional - Claude CLI handles auth, but you can set this
ANTHROPIC_API_KEY=your_key_here
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--project`, `-p` | `.` | Path to your project |
| `--lanes`, `-l` | `1` | Parallel workers |
| `--continuous`, `-c` | `false` | Run until tasks done |
| `--max-rounds`, `-m` | `50` | Max rounds to run |

## Tips for Better Results

1. **Write clear tasks** - "Add login form with email validation" not "do auth stuff"

2. **One thing per task** - break big features into smaller tasks

3. **Include acceptance criteria** - "Add tests that verify login works"

4. **Order matters** - put dependencies first (setup before features)

5. **Run during low-stakes time** - overnight, when you can review in the morning

## Learn More

- **Free Course**: [AI-First Fundamentals](https://traviseric.com/courses/ai-first-fundamentals)
- **Geoffrey Huntley**: [Your First Agent](https://www.yourfirstagent.com/)
- **Steve Yegge**: [Beads](https://github.com/steveyegge/beads)

## License

MIT License - see [LICENSE](LICENSE)

## Author

**Travis Eric** - [traviseric.com](https://traviseric.com)

---

*An independent implementation enhanced by insights from the AI-first development community.*
