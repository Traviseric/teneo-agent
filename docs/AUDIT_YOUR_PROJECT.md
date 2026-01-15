# Audit Your Project for Agent Optimization

Use Claude Code to analyze your project against best practices and get recommendations for better agent performance.

---

## Quick Start

### 1. Clone teneo-agent (if you haven't)

```bash
git clone https://github.com/Traviseric/teneo-agent.git
```

### 2. Open Claude Code in YOUR project

```bash
cd /path/to/your/project
claude
```

### 3. Run the Audit

Paste this prompt into Claude Code:

```
Read the best practices guide at:
D:\path\to\teneo-agent\BEST_PRACTICES.md

Then audit THIS project against those practices. Check:

1. CLAUDE.md - Does it exist? Is it under 100 lines? Does it have a lookup table?
2. Project structure - Is it feature-based? Are files organized logically?
3. Documentation - Is there a docs/ folder? Is root clean (< 15 files)?
4. Testing - Are tests present? Is there a clear test command?
5. Commands - Are build/test/dev commands documented?

Give me a scorecard (1-10 for each area) and specific recommendations to improve.
```

---

## What the Audit Checks

### 1. CLAUDE.md Quality

| Check | Good | Needs Work |
|-------|------|------------|
| Exists | ✅ Has CLAUDE.md | ❌ No CLAUDE.md |
| Length | ✅ Under 100 lines | ❌ Over 100 lines |
| Lookup table | ✅ Has concept→files table | ❌ No lookup table |
| Commands | ✅ Build/test documented | ❌ Commands missing |
| Current focus | ✅ States what's active | ❌ No focus section |

### 2. Project Structure

| Check | Good | Needs Work |
|-------|------|------------|
| Organization | ✅ Feature-based folders | ❌ Type-based (all controllers together) |
| Naming | ✅ Consistent conventions | ❌ Mixed naming styles |
| Depth | ✅ Shallow (2-3 levels) | ❌ Deep nesting (5+ levels) |
| Root | ✅ Clean (< 15 files) | ❌ Cluttered (20+ files) |

### 3. Documentation

| Check | Good | Needs Work |
|-------|------|------------|
| docs/ folder | ✅ Organized documentation | ❌ Docs scattered everywhere |
| README | ✅ Clear setup instructions | ❌ Missing or outdated |
| Specs | ✅ specs/ for features | ❌ No specifications |

### 4. Testing

| Check | Good | Needs Work |
|-------|------|------------|
| Tests exist | ✅ Has test files | ❌ No tests |
| Test command | ✅ `npm test` or equivalent works | ❌ No clear way to run tests |
| Coverage | ✅ Critical paths tested | ❌ Minimal coverage |

---

## Sample Audit Output

When you run the audit, Claude will give you something like:

```
## Project Audit: your-project

### Scorecard
| Area | Score | Status |
|------|-------|--------|
| CLAUDE.md | 3/10 | ❌ Missing |
| Structure | 6/10 | 🟡 Needs work |
| Documentation | 4/10 | ❌ Scattered |
| Testing | 7/10 | ✅ Good |
| Commands | 5/10 | 🟡 Partial |

### Recommendations

**High Priority:**
1. Create CLAUDE.md with lookup table (template below)
2. Move docs from root to docs/ folder
3. Document build command in CLAUDE.md

**Medium Priority:**
4. Reorganize src/ to feature-based structure
5. Add specs/ folder for feature specifications

**Low Priority:**
6. Add .claudeignore for large files
7. Consolidate config files
```

---

## After the Audit

### Create CLAUDE.md

Use this template:

```markdown
# Project: [Your Project Name]

## What This Is
One-line description.

## Lookup Table
| Concept | Files | Search Terms |
|---------|-------|--------------|
| [Main Feature] | src/[folder]/ | [keywords] |
| API | src/routes/ | endpoint, handler |
| Database | prisma/ or src/db/ | query, model |
| Tests | __tests__/ or src/**/*.test.ts | test, mock |

## Commands
```bash
npm run build    # Build the project
npm test         # Run tests
npm run dev      # Start dev server
```

## Conventions
- [Your coding conventions]
- [Naming patterns]
- [Test requirements]

## Current Focus
[What you're actively working on]
```

### Fix Common Issues

| Issue | Fix |
|-------|-----|
| No CLAUDE.md | Create one using template above |
| CLAUDE.md too long | Split into linked docs, keep root < 100 lines |
| No lookup table | Add concept→files mapping |
| Cluttered root | Move to docs/, config/, scripts/ |
| No test command | Add to package.json scripts |
| Type-based structure | Reorganize to feature-based |

---

## Re-run After Changes

After making improvements, run the audit again:

```
Re-audit this project against the best practices.
Show me the updated scorecard and what improved.
```

---

## Path Reference

When running the audit, use the correct path to BEST_PRACTICES.md:

**Windows:**
```
D:\path\to\teneo-agent\BEST_PRACTICES.md
```

**Mac/Linux:**
```
/path/to/teneo-agent/BEST_PRACTICES.md
```

Or if teneo-agent is in a standard location:
```
~/code/teneo-agent/BEST_PRACTICES.md
```

---

## Learn More

**Free Resources:**
- [AI-First Fundamentals](https://traviseric.com/courses/ai-first-fundamentals) - 37 lessons on engineering principles
- [BEST_PRACTICES.md](../BEST_PRACTICES.md) - The 10 principles used in this audit

**Go Deeper:**
- [Complete AI Development System](https://traviseric.com/products/ai-development-system) - 32 advanced guides including full codebase design patterns ($197)
- [AI Orchestra Method](https://traviseric.com/courses/ai-orchestra-method) - Scale to 18+ instances ($97)
