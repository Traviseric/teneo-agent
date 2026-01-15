# MCP Optimization for Agents

MCP (Model Context Protocol) servers can make or break your agent performance. This guide helps you avoid common pitfalls.

---

## The Problem: MCP Token Bloat

Every MCP server you install consumes context tokens **before you even ask a question**.

```
200K advertised context window
- 16K model overhead
- 16K harness overhead
= 176K USABLE

With typical MCPs installed:
- GitHub MCP: ~4K tokens
- Chrome MCP: ~5K tokens
- AWS Lambda MCP: ~40K+ tokens (!)
= Down to <100K usable
```

**Real impact:** With heavy MCPs loaded, you lose 28%+ of your context before doing any work.

---

## The Rule: CLI > MCP

> "Do not install the GitHub MCP server. Just prompt the LLM to use the GitHub CLI." - Geoffrey Huntley

| Task | MCP Approach | CLI Approach | Winner |
|------|--------------|--------------|--------|
| GitHub issues | GitHub MCP (~4K overhead) | `gh issue list` | **CLI** |
| Git operations | Git MCP | `git status` | **CLI** |
| File search | Custom MCP | `rg`, `fd` | **CLI** |
| API calls | Custom MCP | `curl` | **CLI** |

**Why CLI wins:**
- Zero token overhead
- Claude already knows these tools
- No schema bloat

---

## Audit Your Current Setup

Run `/context` in Claude Code to see token breakdown:

```
System tools: 16.7k tokens (8.4%)   ← Built-in
MCP tools:    45.0k tokens (22.5%)  ← Problem area
```

Look for `mcp__` prefixed entries to identify culprits.

---

## Config File Locations

**Claude Desktop:**
```
Windows: C:/Users/[USER]/AppData/Roaming/Claude/claude_desktop_config.json
Mac:     ~/Library/Application Support/Claude/claude_desktop_config.json
```

**Claude Code:**
```
~/.claude.json        (user config)
.mcp.json             (project config)
```

---

## Minimal Config (Recommended)

Start with no MCPs, add only what you need:

```json
{
  "mcpServers": {}
}
```

Then add only project-specific servers via `.mcp.json` in your project root.

---

## Common Culprits

| MCP | Token Cost | Alternative |
|-----|------------|-------------|
| GitHub MCP | ~4K | Use `gh` CLI |
| AWS Lambda MCP | ~40K+ | Use `aws` CLI |
| Chrome MCP | ~5K | Disable when not needed |
| Memory MCP | ~2K | Usually unnecessary |

---

## Quick Fixes

### Disable Chrome MCP

In `~/.claude.json`:
```json
{
  "claudeInChromeDefaultEnabled": false
}
```

### Remove GitHub MCP

Just delete it from config. Use `gh` CLI instead:
```bash
gh issue list
gh pr list
gh pr create
```

### Switch Configs Based on Task

Keep multiple configs:
```bash
claude_desktop_config.minimal.json   # Daily use
claude_desktop_config.aws.json       # When debugging AWS
claude_desktop_config.full.json      # Rare, specific tasks
```

---

## Best Practices Summary

1. **Start minimal** - Empty MCP config by default
2. **Audit regularly** - Run `/context` to check usage
3. **Prefer CLI** - `gh`, `aws`, `kubectl` over MCP equivalents
4. **Load on demand** - Switch configs for specific tasks
5. **Project-specific** - Use `.mcp.json` for project needs

---

## Learn More

For advanced MCP optimization including custom server development and token budgeting:

- **Premium Guides**: [Complete AI Development System](https://traviseric.com/products/ai-development-system) - Includes full MCP Development Guide ($197)
