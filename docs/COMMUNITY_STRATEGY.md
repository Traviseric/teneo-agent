# Community Strategy

How Teneo Agent connects with the AI-first development community.

---

## Goal

**Become a recognized contributor** to the AI agent ecosystem by:
1. Building genuinely useful software (Teneo Agent)
2. Contributing back to foundational projects
3. Creating bridges between tools

---

## Target Community

### Primary: The "Overnight Agent" Community

| Person | Project | Our Connection |
|--------|---------|---------------|
| **Steve Yegge** | [beads](https://github.com/steveyegge/beads), [gastown](https://github.com/steveyegge/gastown) | We implement his patterns; integration target |
| **Geoffrey Huntley** | [how-to-build-a-coding-agent](https://github.com/ghuntley/how-to-build-a-coding-agent), Ralph Loop | Our fresh-context-per-worker is his pattern |
| **Dex Horthy** | [12-factor-agents](https://github.com/humanlayer/12-factor-agents), [humanlayer](https://github.com/humanlayer/humanlayer) | We implement his factors; contribution target |

### Secondary: Users Who Need Simple Overnight Runners

- Developers who want "set and forget" overnight builds
- Teams not ready for complex orchestration (gastown)
- Windows users (much of the ecosystem is Unix-focused)

---

## Contribution Strategy

### Tier 1: Quick Wins (This Month)

| Target | Contribution | Why They'd Want It |
|--------|--------------|-------------------|
| **steveyegge/beads** | Windows installer PR | Opens Windows market |
| **humanlayer/12-factor-agents** | Python case study | Diversifies their examples |
| **ghuntley/how-to-build-a-coding-agent** | Python port | Expands audience beyond Go |

### Tier 2: Integration (Next Month)

| Target | Contribution | Why They'd Want It |
|--------|--------------|-------------------|
| **steveyegge/beads** | MCP server | Tool accessibility |
| **steveyegge/gastown** | Windows Terminal support RFC | Platform expansion |
| **humanlayer/humanlayer** | Pre-execution validation patterns | Production hardening |

### Tier 3: Ecosystem (Ongoing)

| Action | Goal |
|--------|------|
| Integrate beads into Teneo Agent | Become part of the Yegge toolchain |
| Case study on 12-factor-agents | Establish expertise |
| Cross-reference in all READMEs | Build discoverability |

---

## Messaging

### How We Position Teneo Agent

**NOT**: "We built a better overnight runner"

**YES**: "We built a Python entry point to the overnight agent ecosystem"

### Key Messages

1. **Independent implementation** - We built this ourselves, then found it aligned with community patterns
2. **Bridge, not competitor** - Teneo Agent → Beads → Gastown is a learning path
3. **Windows-first** - We fill a gap in the ecosystem (Unix-heavy tools)
4. **Python-native** - Alternative to Go/TypeScript implementations

---

## Outreach Plan

### Phase 1: Establish Presence

- [x] Open source Teneo Agent
- [ ] Star and watch target repos
- [ ] Engage in issues/discussions (helpful, not promotional)
- [ ] Submit first PR to beads (Windows installer)

### Phase 2: Build Credibility

- [ ] Get first PR merged
- [ ] Write case study for 12-factor-agents
- [ ] Cross-reference in YouTube comments/discussions
- [ ] Document our beads integration plans publicly

### Phase 3: Collaborate

- [ ] Propose Teneo Agent as "simple mode" in gastown docs
- [ ] Offer to maintain Windows support for community tools
- [ ] Join Discord/community channels

---

## What We Offer

### Unique Capabilities

| Capability | Value to Community |
|------------|-------------------|
| **Windows expertise** | Most tools are Mac/Linux only |
| **Python implementation** | Alternative to Go/TS |
| **Production overnight runs** | Real-world testing data |
| **Cross-platform terminal spawning** | Solved hard problem |

### Resources to Share

1. **Patterns documentation** - What we learned building overnight runners
2. **Windows testing** - We can test PRs on Windows
3. **Case studies** - Results from real overnight runs
4. **Integration examples** - How to connect tools

---

## Success Metrics

| Metric | Target |
|--------|--------|
| PRs merged to target repos | 3+ |
| Mentions in community docs | 2+ |
| GitHub stars on teneo-agent | 50+ |
| Contributors to teneo-agent | 5+ |

---

## Do's and Don'ts

### Do

- ✅ Be genuinely helpful in issues
- ✅ Credit their work explicitly
- ✅ Focus on integration, not competition
- ✅ Submit small, focused PRs
- ✅ Test thoroughly before submitting

### Don't

- ❌ Self-promote in unrelated discussions
- ❌ Claim to have "invented" patterns they documented first
- ❌ Submit large PRs without discussion first
- ❌ Criticize their architectural choices
- ❌ Rush contributions - quality over quantity

---

*This strategy guides how we engage with the community. Update as relationships develop.*
