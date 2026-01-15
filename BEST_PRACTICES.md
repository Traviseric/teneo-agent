# Best Practices for Overnight Agents

Principles that make AI agents work better on your projects.

---

## CLAUDE.md Setup

Every project needs a `CLAUDE.md` file in the root. This is the agent's instruction manual.

### Keep It Short
- **Target: < 100 lines** (ideally 60)
- Agents read this every session
- Long files waste context tokens
- If it's over 100 lines, split into linked docs

### Use Lookup Tables
Instead of prose, use tables. Agents parse these efficiently:

```markdown
## Lookup Table
| Concept | Files | Search Terms |
|---------|-------|--------------|
| Auth | src/auth/, src/middleware/auth.ts | login, JWT, session |
| API | src/routes/api/ | endpoint, handler, POST |
| Database | prisma/schema.prisma, src/db/ | query, model, migration |
| Testing | __tests__/, src/**/*.test.ts | vitest, mock, expect |
| Config | src/config/, .env.example | environment, settings |
```

**Why this works:**
- Agent knows exactly where to look
- Reduces searching/guessing
- Search terms help find related code

### Include Commands
```markdown
## Commands
```bash
npm run build    # Build (must pass before commit)
npm test         # Run tests
npm run lint     # Check code style
```
```

### State Current Focus
```markdown
## Current Focus
Building user dashboard - see specs/dashboard.md
```

---

## The 10 Principles

### 1. One Task = One Context
- Each agent session should do ONE thing
- 5-15 minutes of focused work
- Don't ask for "build the whole feature"
- Break it into specific tasks

### 2. Fresh Context Every Time
- Agents don't remember previous sessions
- Each worker starts clean
- Write handoffs so next worker has context
- Don't rely on "we discussed this earlier"

### 3. Specific Tasks Get Specific Results

**Bad:**
```markdown
- [ ] Add authentication
```

**Good:**
```markdown
- [ ] Create login form component at src/components/LoginForm.tsx with email/password fields
- [ ] Add POST /api/auth/login endpoint that validates credentials and returns JWT
- [ ] Write tests for LoginForm component (test validation, submission, error states)
```

### 4. Include Acceptance Criteria
```markdown
- [ ] Add user profile page - DONE when: page loads user data, shows avatar, edit button works, tests pass
```

### 5. Order Tasks by Dependency
Put setup tasks before tasks that depend on them:
```markdown
- [ ] Create database schema for users table
- [ ] Add User model with TypeScript types
- [ ] Create API endpoint to fetch user
- [ ] Build UI component to display user
```

### 6. Tests = Quality Gate
- Include "run tests" or "verify build passes" in tasks
- Agents should not mark complete if tests fail
- Tests catch mistakes before you wake up

### 7. Git is Your Safety Net
- Agents commit their work
- Review commits in the morning
- `git diff` shows exactly what changed
- `git revert` if something went wrong

### 8. Delegate, Don't Micromanage

**Micromanaging (bad):**
```markdown
- [ ] Create function called validateEmail that takes string parameter email and uses regex /^[^\s@]+@[^\s@]+\.[^\s@]+$/ to return boolean
```

**Delegating (good):**
```markdown
- [ ] Add email validation to the signup form. Follow existing validation patterns in the codebase.
```

### 9. Working Code Only
- Agents should commit code that runs
- No placeholder comments like "// TODO: implement this"
- If it can't be fully done, note what's missing

### 10. Review the Handoffs
- Check `agent_runs/*/HANDOFF.md` files
- See what the agent did and struggled with
- Use this to write better tasks next time

---

## Project Structure That Works

Agents work best with organized projects:

```
your-project/
├── CLAUDE.md              # Agent instructions (required)
├── src/
│   ├── components/        # UI components
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   └── utils/             # Helpers
├── tests/                 # Test files
├── docs/                  # Documentation
│   └── specs/             # Feature specifications
├── package.json           # Dependencies & scripts
└── tsconfig.json          # TypeScript config
```

**Key points:**
- Feature-based organization (not type-based)
- Consistent naming conventions
- Tests next to or mirroring source structure
- Specs in docs/ for complex features

---

## Common Mistakes

### Too Many Tasks at Once
❌ 50 tasks in TASKS.md
✅ 5-10 focused tasks per overnight run

### Vague Tasks
❌ "Improve the UI"
✅ "Add loading spinner to submit button in LoginForm.tsx"

### No CLAUDE.md
❌ Agent guesses about project structure
✅ Agent knows exactly where things are

### Ignoring Handoffs
❌ Never read what the agent wrote
✅ Review handoffs, learn, improve tasks

### No Tests
❌ Agent makes changes, no verification
✅ Tests catch issues automatically

---

## Quick Checklist

Before running overnight:

- [ ] CLAUDE.md exists and is < 100 lines
- [ ] Lookup table maps concepts to files
- [ ] Build/test commands are documented
- [ ] Tasks are specific with acceptance criteria
- [ ] Tasks are ordered by dependency
- [ ] Git repo is clean (commit current work)
- [ ] Tests exist and pass currently

---

## Learn More

**Free Resources:**
- [AI-First Fundamentals](https://traviseric.com/courses/ai-first-fundamentals) - 37 lessons on engineering principles
- [GETTING_STARTED.md](GETTING_STARTED.md) - Project setup guide
- [MCP Optimization](docs/MCP_OPTIMIZATION.md) - Optimize your MCP servers

**Go Deeper:**
- [Complete AI Development System](https://traviseric.com/products/ai-development-system) - 32 advanced guides ($197)
- [AI Orchestra Method](https://traviseric.com/courses/ai-orchestra-method) - Scale to 18+ instances ($97)

**Community:**
- [GitHub Issues](https://github.com/Traviseric/teneo-agent/issues)
