# Documentation Organization for AI Agents

How to structure your project documentation so AI agents can navigate efficiently.

---

## The Problem

AI agents waste tokens when:
- Documentation is scattered across the project
- No clear index or entry point exists
- Files are named inconsistently
- Important docs are buried in deep folders

---

## The Solution: Clean Root + docs/ Folder

```
your-project/
├── CLAUDE.md              ← Agent entry point (required)
├── README.md              ← Human entry point
├── package.json           ← Config files at root
├── src/                   ← Source code
├── tests/                 ← Test files
└── docs/                  ← All documentation here
    ├── README.md          ← Documentation index
    ├── guides/            ← How-to guides
    ├── specs/             ← Feature specifications
    ├── architecture/      ← System design docs
    └── api/               ← API documentation
```

---

## Rule 1: Clean Root (< 15 files)

Your project root should only contain:
- `CLAUDE.md` - Agent instructions
- `README.md` - Project overview
- Config files (`package.json`, `tsconfig.json`, etc.)
- Source folders (`src/`, `tests/`, `docs/`)

**Move everything else to `docs/` or appropriate folders.**

### Before (cluttered):
```
project/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── ARCHITECTURE.md
├── DEPLOYMENT.md
├── TROUBLESHOOTING.md
├── API_REFERENCE.md
├── SECURITY.md
├── ... (20+ files)
```

### After (clean):
```
project/
├── CLAUDE.md
├── README.md
├── docs/
│   ├── README.md          ← Index linking to all docs
│   ├── CONTRIBUTING.md
│   ├── CHANGELOG.md
│   ├── guides/
│   │   ├── deployment.md
│   │   └── troubleshooting.md
│   ├── architecture/
│   │   └── overview.md
│   └── api/
│       └── reference.md
```

---

## Rule 2: Create a Documentation Index

Every `docs/` folder needs a `README.md` that indexes its contents:

```markdown
# Project Documentation

## Quick Links
| Guide | Description |
|-------|-------------|
| [Getting Started](guides/getting-started.md) | First-time setup |
| [Architecture](architecture/overview.md) | System design |
| [API Reference](api/reference.md) | Endpoint documentation |

## Guides
- [Deployment](guides/deployment.md) - How to deploy
- [Troubleshooting](guides/troubleshooting.md) - Common issues

## Contributing
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines
```

**Why this matters:** Agents can read the index and navigate directly to relevant docs without searching.

---

## Rule 3: Consistent Naming

| Convention | Example | Use For |
|------------|---------|---------|
| `kebab-case.md` | `getting-started.md` | Guide files |
| `UPPER_CASE.md` | `CONTRIBUTING.md` | Standard project files |
| `PascalCase.md` | `ApiReference.md` | Avoid (inconsistent) |

Pick one and stick with it. `kebab-case` is recommended for most files.

---

## Rule 4: Use Lookup Tables in CLAUDE.md

Link your documentation in the CLAUDE.md lookup table:

```markdown
## Lookup Table
| Concept | Files | Search Terms |
|---------|-------|--------------|
| Setup | docs/guides/getting-started.md | install, setup, config |
| API | docs/api/reference.md, src/routes/ | endpoint, handler |
| Architecture | docs/architecture/overview.md | design, system |
| Deployment | docs/guides/deployment.md | deploy, production |
```

Agents use this to find documentation without searching.

---

## Rule 5: Specs for Complex Features

Before building complex features, create a spec:

```
docs/
└── specs/
    ├── user-authentication.md
    ├── payment-integration.md
    └── notification-system.md
```

### Spec Template:

```markdown
# Feature: [Name]

## Overview
One paragraph describing what this feature does.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Technical Approach
How it will be implemented.

## API Changes
New endpoints or modifications.

## Database Changes
Schema changes needed.

## Testing Strategy
How to verify it works.
```

---

## Quick Checklist

### Project Root
- [ ] < 15 files in root
- [ ] CLAUDE.md exists
- [ ] README.md exists
- [ ] docs/ folder exists

### Documentation Folder
- [ ] docs/README.md indexes all docs
- [ ] Consistent file naming
- [ ] Logical folder structure
- [ ] No orphaned files

### CLAUDE.md
- [ ] Lookup table includes doc paths
- [ ] Under 100 lines
- [ ] Links to detailed docs (not inline)

---

## Learn More

**In This Repo:**
- [BEST_PRACTICES.md](../BEST_PRACTICES.md) - 10 principles for agents
- [MCP_OPTIMIZATION.md](MCP_OPTIMIZATION.md) - Optimize MCP servers
- [AUDIT_YOUR_PROJECT.md](AUDIT_YOUR_PROJECT.md) - Audit your project structure

**Go Deeper:**
- [Complete AI Development System](https://traviseric.com/products/ai-development-system) - Includes full documentation organization guide ($197)
