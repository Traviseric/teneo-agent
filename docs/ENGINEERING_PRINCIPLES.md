# Engineering Principles for AI Projects

A sequential framework for evaluating and hardening any project that AI agents work on. Work through each gate in order — each builds on the last.

---

## The Idea

Most developers ask one question: "does my code work?" That's not enough when agents are building autonomously. You need to know whether the project is *structured* for agents, whether the *workflow* produces reliable output, whether it's *safe to deploy*, and whether it *earns trust*.

These are different questions answered by different evaluations. Running them in sequence — each gate building on the last — is the difference between a project that sort-of works and one that's production-hardened.

---

## The Gates

```
Gate 0: LLM-NATIVE CHECK      Should I even write code?
Gate 1: FOUNDATION             Is the project structured right?
Gate 2: DEVELOPMENT            Are we building right?
Gate 3: PRODUCTION READY       Is it safe to run?
Gate 4: ENGINEERING AUDIT      Does it pass inspection?
Gate 5: ENTERPRISE POLISH      Will serious users trust it?
Gate 6: EXECUTION PLAN         What's the roadmap to get there?
```

Pick the gate that matches your concern, or start at Gate 0 and ride all the way through.

---

## Gate 0: Should I Even Write Code?

**This is the most expensive mistake in AI development** — building Python modules that reimplement what an LLM does natively when given the right context document.

Before starting any gate, run this check:

1. **Am I building intelligence or plumbing?** If the core value is "understand text and give smart advice," you probably need a context document, not code.
2. **Would `.md` files + Claude do this?** If yes, write the context documents first. Code is for persistence, automation, integration, scale, and distribution.
3. **Am I reimplementing LLM capabilities in Python?** Pattern matching, classification, summarization, analysis — these are things the model already does. Write the context that tells it *how* to do it for your domain.

**The rule:** Intelligence lives in `.md` context documents. Reasoning lives in the LLM. Code is plumbing.

**Real example:** A 5,000-line Python relationship analysis module — with custom NLP, scoring algorithms, pattern matchers — was replaced by 500 lines of structured markdown that told Claude how to analyze relationships. Same quality output. 90% less code to maintain. The markdown was also easier to improve.

Ask yourself: "If I gave Claude a well-written document explaining exactly what I want analyzed and how, would it produce the same result as this code?" If yes, write the document.

---

## Gate 1: Foundation — Is the Project Structured Right?

**What it proves:** An agent dropped into this repo can orient itself in under 30 seconds, find any concept via lookup table, and start productive work without asking questions.

**Key checks:**
- CLAUDE.md exists, is under 100 lines, has a lookup table mapping concepts to files and search terms
- Feature-based directory structure (not layer-based)
- Consistent naming across files, functions, routes
- `docs/` directory with an index — no orphaned docs in root
- `.claudeignore` excludes noise (PDFs, binaries, node_modules, build artifacts)
- `specs/` directory for feature specifications
- No dead files or mystery directories

**The test:** Can an agent reading only CLAUDE.md find any concept in the project?

**Why feature-based structure matters:**
```
# Bad (layer-based) — agent has to search everywhere
src/
  controllers/
  models/
  services/
  routes/

# Good (feature-based) — agent finds everything about auth in one place
src/
  auth/       # login, signup, JWT, middleware
  billing/    # plans, checkout, invoices
  dashboard/  # widgets, layouts, data
```

---

## Gate 2: Development — Are We Building Right?

**What it proves:** The development workflow produces reliable, reviewable code. Agents build autonomously using a structured cycle. Back pressure rejects bad output before humans look.

**Key checks:**
- Tests exist and run green (TDD — tests written first, not after)
- Back pressure rejects bad output through types, linters, and CI — not just advisory warnings
- Development follows Research -> Plan -> Implement (separate contexts for each)
- No behavior drift between docs, tests, and runtime
- Tasks are delegating ("add notification capability") not prescriptive ("create POST endpoint with these exact fields")
- Specs committed alongside implementation
- CLI preferred over MCP where possible (lower token overhead)

**The workflow that works:**

```
Context 1: RESEARCH
  - Read existing code, understand patterns
  - Identify what needs to change
  - Output: findings document

Context 2: PLAN
  - Design the approach based on research
  - Write the spec
  - Output: committed spec in specs/

Context 3: IMPLEMENT
  - Write failing tests first
  - Implement until tests pass
  - Output: working code + passing tests
```

Each context is fresh. One task per context, 5-15 minutes of focused work. This prevents context degradation and keeps agent output quality high.

**Back pressure is the key insight:** When tests fail, they should *block the build*, not just warn. When types don't match, compilation should *fail*. The more your toolchain automatically rejects bad agent output, the less you need to review manually. This is the difference between "AI-assisted development" and "autonomous development."

---

## Gate 3: Production Readiness — Is It Safe to Run?

**What it proves:** The project won't lose data, leak secrets, crash silently, or fail without telling anyone.

**The layers (bottom-up):**

| Layer | Question |
|-------|----------|
| Security & Secrets | Are secrets managed properly? No plaintext keys? |
| Error Handling | Are errors classified and retried intelligently? |
| Observability | Is there structured logging and an audit trail? |
| Human-in-the-Loop | Is there an escalation path for high-risk actions? |
| State & Persistence | Can state survive a crash? |
| Configuration | Is there clear config precedence (env > file > default)? |
| Operational Controls | Does a kill switch or graceful shutdown exist? |
| Infrastructure | Is the deployment environment hardened? |
| Workflow & Testing | Do tests pass? Does CI run? |

**Exit criteria:**
- No plaintext secrets in code or config files
- Errors are classified and handled (not just caught and logged)
- Structured logging exists
- State survives a crash (checkpoints, event log, or database)
- Config has clear precedence
- Kill switch or graceful shutdown exists
- Tests pass, CI runs

---

## Gate 4: Engineering Audit — Does It Pass Inspection?

**What it proves:** The project meets a formal production engineering standard — not "does it work" but "does it meet standards."

**How to run it:**
1. Pick or build a 12-category audit checklist covering: security, error handling, logging, testing, deployment, monitoring, documentation, data integrity, performance, accessibility, dependency management, and operational procedures
2. Auto-detect the stack (serverless, container, static, CLI)
3. Run all categories in one uninterrupted pass
4. Score each category: Pass / Partial / Fail / Not Applicable
5. Generate a prioritized remediation roadmap

**Exit criteria:**
- Audit report generated
- No "Fail" items in security, data integrity, or error handling
- Remediation roadmap exists for any Partial items
- Stack-specific concerns reviewed

The audit should be project-specific. Don't force irrelevant rules. A CLI tool doesn't need RBAC. A static site doesn't need database migration procedures. `Not Applicable` is a valid answer — but it must be explained.

---

## Gate 5: Enterprise Polish — Will Serious Users Trust It?

**What it proves:** The project isn't just functional — it's credible. This is the layer between "works" and "wins."

**Prerequisite:** Must pass Gate 3 first. If production gaps exist, go back.

**The 8 pillars (in impact-per-dollar order for indie teams):**

```
1. Developer Experience     SDK, docs, quickstart, error messages
2. Documentation Portal     Searchable, versioned, example-rich
3. UX & Analytics           A/B testing, conversion tracking
4. Audit & Compliance       Logging, data governance
5. Trust & Social Proof     Testimonials, case studies, status page
6. Integrations             Webhooks, OAuth, marketplace presence
7. Load Testing             Benchmarks, capacity planning
8. Release Ops              Changelog, versioning, migration guides
```

**Exit criteria:**
- 8-pillar assessment completed
- Top 3 gaps identified and prioritized
- Blocking tasks identified

Most indie projects never think about this layer. That's why most indie projects feel indie. You don't need all 8 — but knowing which ones you're *deliberately skipping* versus which ones you never considered is the difference between strategic and accidental.

---

## Gate 6: Execution Plan — What's the Roadmap?

**What it proves:** Findings from Gates 1-5 are captured in an actionable, gated, parallelizable roadmap — not a loose TODO list.

**A valid roadmap answers:**
1. What is this project trying to become?
2. What major capabilities exist already?
3. What major capabilities are next?
4. What is blocked and why?
5. What must be proven before the project can advance?
6. How should parallel agents split the work?

**Exit criteria:**
- Roadmap exists with phases and clear entry/exit criteria per phase
- Findings from Gates 1-5 are encoded as roadmap items
- Blocked items have named blockers (not vague "needs work")
- Work is parallelizable — agents can pick up independent tracks

---

## Running This on Your Project

### Quick Check (pick a gate)
- "Is this structured right?" -> Gate 1
- "Are we building well?" -> Gate 2
- "Is this safe to deploy?" -> Gate 3
- "Does this meet standards?" -> Gate 4
- "Will enterprise users trust this?" -> Gate 5
- "What's the plan?" -> Gate 6

### Full Ride (all gates)
```
Start at Gate 0. For each gate:
1. Evaluate the checks against the target project
2. Score the exit criteria
3. Record pass/fail with evidence
4. Continue to next gate

Output: per-gate results + combined remediation plan.
```

### For Overnight Agents
Point an agent at this doc and your project path:
```
Read docs/ENGINEERING_PRINCIPLES.md
Target: my-project at ./

Run Gates 1-6 in order. Evaluate exit criteria.
Output: engineering-review.md with per-gate results.
```

---

## Key Principles Behind the Gates

These principles inform the gates but are worth internalizing on their own:

- **One context = one task.** Don't ask an agent to do three things. Give it one clear task with one clear output.
- **Fresh context every time.** Agents don't remember. Each session starts clean. Write handoffs.
- **Back pressure is blocking, not advisory.** Failed tests reject the build. Types reject bad code. Linters reject bad patterns. Automate rejection.
- **Delegate judgment, don't prescribe.** "Add notification capability, follow existing patterns" beats "Create POST endpoint with these exact fields."
- **Specs are source code.** Commit them alongside implementation.
- **Review research, not code.** Reviewing the spec before implementation is 10x more valuable than reviewing the code after.
- **Moat is in the workflow, not the model.** Models commoditize. Your defensible value is the pipeline — how tasks get defined, routed, validated, and deployed.
- **Tokens are cheaper than people.** Spend tokens liberally on evaluation, retries, and back pressure.
- **A feature today is tech debt tomorrow.** Build for easy deletion. Models improve faster than codebases evolve.

---

## Learn More

**Free Resources:**
- [AI Builders Lab](https://www.skool.com/ai-builders-lab-6883) - Community for overnight agent builders
- [AI-First Fundamentals](https://traviseric.com/courses/ai-first-fundamentals) - 37 lessons on engineering principles
- [BEST_PRACTICES.md](../BEST_PRACTICES.md) - Operational rules for overnight agents
- [Audit Your Project](AUDIT_YOUR_PROJECT.md) - Run Claude against your project

**Go Deeper:**
- [Complete AI Development System](https://traviseric.com/products/ai-development-system) - Full 27 rules + enhanced agent framework ($197)
- [AI Orchestra Method](https://traviseric.com/courses/ai-orchestra-method) - Scale to 18+ parallel instances ($97)

**Community:**
- [AI Builders Lab on Skool](https://www.skool.com/ai-builders-lab-6883) - Share runs, get feedback, learn patterns
