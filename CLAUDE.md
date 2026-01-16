# Teneo Agent

Run Claude agents overnight to build your projects autonomously.

## First Time Here?

**Welcome!** I'll help you set up overnight agents for your project.

**Tell me the path to your project** (e.g., `D:\Projects\my-app` or `/home/user/my-app`) and I'll:

1. Audit it against overnight agent best practices
2. Show you a scorecard with specific recommendations
3. Help you make the changes (CLAUDE.md, task file, folder cleanup)
4. Give you the exact command to start your first overnight run

Just say: **"Set up my project at [your-project-path]"**

---

## When User Provides a Project Path

When the user gives you a project path to set up, follow this process:

### Step 1: Audit
Read `BEST_PRACTICES.md` in this repo, then analyze their project against those practices. Give them a scorecard covering:
- CLAUDE.md (exists? under 100 lines? has lookup table?)
- Root directory cleanliness (count files, suggest moves to docs/)
- Task file (TASKS.md exists? tasks are specific?)
- Build/test commands documented?

### Step 2: Recommend Changes
Present specific recommendations with priorities (High/Medium/Low). Include exact commands they can run to reorganize files.

### Step 3: Offer to Help
Ask if they want you to:
- Create/update their CLAUDE.md
- Create a TASKS.md with initial tasks
- Move files to clean up root

### Step 4: Ask Run Preferences
After setup is complete, ask the user:

**"How do you want to run the overnight agent?"**

1. **Lanes** - How many parallel workers? (1-3 recommended for most projects)
   - 1 lane = sequential, safer for codebases with lots of interdependencies
   - 2-3 lanes = parallel, faster for independent tasks

2. **Mode** - Continuous or single round?
   - Continuous = keeps going until all tasks done (overnight use)
   - Single = does one round then stops (for testing)

### Step 5: Give Run Command or Offer to Start
Based on their answers, give them the exact command:

```
python teneo_agent.py start --project [THEIR_PATH] --lanes [N] --continuous
```

Then ask: **"Want me to start this for you, or do you want to run it yourself in a new terminal?"**

- If they want to run it themselves → tell them to open a new terminal and paste the command
- If they want you to start it → explain you'll spawn it and they can watch in the new window

---

## Already Set Up?

If your project is ready, run this in a **new terminal window**:

```bash
# Continuous mode - runs until all tasks done
python teneo_agent.py start --project /path/to/your/project --continuous

# Or with 2 parallel workers
python teneo_agent.py start --project /path/to/your/project --lanes 2 --continuous
```

---

## Reference

| Concept | Files |
|---------|-------|
| Relay Runner | teneo_agent.py |
| Ralph Runner | ralph_runner.py |
| Best Practices | BEST_PRACTICES.md |
| Audit Guide | docs/AUDIT_YOUR_PROJECT.md |

## Upgrade Path

- **Free**: This repo
- **Pro**: [teneo-agent-pro](https://traviseric.com/products/ai-development-system) - Crash recovery, smart context, 27 principles ($197)
