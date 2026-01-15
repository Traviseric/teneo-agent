# Getting Started with Teneo Agent

Set up your project for successful overnight agent runs.

## 1. Project Setup Checklist

Before running agents overnight, set up your project:

```
your-project/
├── CLAUDE.md           ← Agent instructions (create this)
├── src/                ← Your source code
├── tests/              ← Your tests
├── package.json        ← Or equivalent build config
└── .git/               ← Version controlled
```

### Create CLAUDE.md

This file tells the agent about your project. Keep it under 100 lines.

```markdown
# Project: [Your Project Name]

## What This Is
One-line description of what this project does.

## Lookup Table
| Concept | Files | Search Terms |
|---------|-------|--------------|
| Auth | src/auth/ | login, session |
| API | src/routes/ | endpoint, handler |
| Database | prisma/ | query, model |

## Stack
- Framework: [e.g., Next.js 14]
- Language: [e.g., TypeScript]
- Testing: [e.g., Vitest]

## Commands
```bash
npm run build    # Build the project
npm test         # Run tests
npm run dev      # Development server
```

## Conventions
- Write tests before implementation
- Use feature-based folder structure
- Commit working code only

## Current Focus
[What's being actively worked on]
```

## 2. Write Good Tasks

In `teneo-agent/TASKS.md`, write clear, specific tasks:

### Good Tasks
```markdown
- [ ] Add login form with email and password validation
- [ ] Create API endpoint POST /api/users that returns user object
- [ ] Write unit tests for the auth service (aim for 80% coverage)
- [ ] Fix TypeScript error in src/components/Header.tsx line 42
```

### Bad Tasks
```markdown
- [ ] Do the auth stuff
- [ ] Make it work
- [ ] Fix bugs
- [ ] Improve performance
```

### Task Guidelines

| Do | Don't |
|----|-------|
| One outcome per task | Multiple things in one task |
| Specific file/function | Vague "somewhere" |
| Measurable completion | Open-ended |
| Include acceptance criteria | Leave success undefined |

## 3. Run the Agent

```bash
# Navigate to teneo-agent
cd teneo-agent

# Single task (test run)
python teneo_agent.py start --project "C:\path\to\your\project"

# Continuous until tasks done
python teneo_agent.py start --project "C:\path\to\your\project" --continuous

# Multiple parallel workers
python teneo_agent.py start --project "C:\path\to\your\project" --continuous --lanes 2
```

## 4. Monitor Progress

While running:
- **Terminal windows** open for each worker
- **agent_runs/** folder contains logs and handoffs
- Workers write HANDOFF.md when complete

Check status anytime:
```bash
python teneo_agent.py status
```

## 5. Review in the Morning

1. Check git log for commits
2. Review HANDOFF.md files in agent_runs/
3. Run your tests to verify quality
4. Add follow-up tasks if needed

## Tips for Success

### Start Small
- Run one task first, verify it works
- Then try continuous mode with a few tasks
- Scale up lanes once you trust the system

### Quality Tasks = Quality Output
- Specific tasks get specific results
- Vague tasks get vague (or wrong) results
- Include "run tests" or "verify build" in tasks

### Fresh Context Per Task
- Each worker starts fresh (no memory of previous workers)
- Write handoffs so the next worker has context
- Don't rely on accumulated conversation history

### Git is Your Safety Net
- Agents commit their work
- You can always `git revert` if something goes wrong
- Review diffs before pushing to production

## Troubleshooting

### Agent doesn't start
- Check Claude CLI is installed: `claude --version`
- Check you're logged in: `claude login`

### Tasks not completing
- Check agent_runs/ for LOG.md files
- Look for BLOCKED status or errors
- Simplify the task and try again

### Wrong project changes
- Verify --project path is correct
- Check CLAUDE.md exists in project root

## Learn More

- **Free Course**: [AI-First Fundamentals](https://traviseric.com/courses/ai-first-fundamentals)
- **Community**: [GitHub Issues](https://github.com/Traviseric/teneo-agent/issues)
