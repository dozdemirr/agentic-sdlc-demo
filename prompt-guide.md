# Prompt Guide — Working with Agents and Skills

> **Purpose**: Practical templates and patterns for directing AI agents effectively
> across every phase of the modernisation journey.
>
> **Audience**: Developers at Level 2+ on the [adoption ladder](README.md)
>
> **Companion**: [Agentic Developer Guide](agentic-developer-guide.md)

---

## Prompt Structure

Every effective prompt has four parts. Miss one and the output quality drops:

```
1. SKILL/AGENT   — which capability to use
2. SCOPE          — what's in, what's out
3. INPUTS         — what to read before starting
4. QUALITY BAR    — what "done" looks like
```

### Minimal Template

```
Using the [skill/agent], [action] for [scope].

Inputs:
- [file or artefact 1]
- [file or artefact 2]

Constraints:
- [what to include]
- [what to exclude]
- [format requirements]
```

---

## Phase 1 — Discovery Prompts (`@01-discovery`)

### Basic: System Inventory

```
@01-discovery Inventory this repository.

Identify:
- Languages, frameworks, and build system
- Directory structure with business purpose per module (3–5 sentences each)
- Database connections and table access patterns
- Entry points and startup sequence
- Configuration parameters and their impact
- External integrations

Create an unknowns register with at least 10 items and resolution paths.
Flag anything inferred (not proven from code) as [INFERRED].
```

### Targeted: Single Module Deep Dive

```
@01-discovery Analyse the [module/folder name] module.

Focus on:
- What business capability does it implement?
- What data does it own (read/write)?
- What does it depend on (internal and external)?
- What depends on it?
- What are the key classes and their responsibilities?

Reference file paths for every claim.
```

### Targeted: Unknowns Resolution

```
@01-discovery Investigate the following unknowns
from the discovery report:

1. [Unknown item 1 — e.g., "What triggers the nightly batch job?"]
2. [Unknown item 2]
3. [Unknown item 3]

For each, provide:
- Evidence found (with file paths)
- Confidence level (confirmed / likely / unknown)
- Remaining gaps and how to resolve them
```

---

## Phase 2 — Documentation Prompts (`@02-documentation`)

### Basic: Full Documentation Suite

```
@02-documentation Produce current-state documentation
for this repository.

Create:
1. HLD — system overview, components, data stores, runtime assumptions
2. LLD — key classes per domain, request flows, coupling hotspots
3. ADRs — one per discovered architectural pattern (separate files)
4. Runbook — build, run, test commands; local dependencies; known limitations

Rules:
- Every claim must cite a source file
- Module descriptions must be 3–5 sentences minimum
- Mark anything uncertain as [INFERRED]
- Do not propose future-state design
```

### Targeted: Single ADR

```
@02-documentation Write an ADR for the following
pattern observed in the codebase:

Pattern: [describe what you've observed — e.g., "All database access goes
through a single shared DbContext with no domain separation"]

Include:
- Context — why does this pattern exist?
- Decision — what was the implicit choice made?
- Consequences — what does this enable and what does it prevent?
- Evidence — cite 3+ file paths that demonstrate this pattern
```

### Targeted: Runbook from Scratch

```
@02-documentation Produce an operational runbook
for this repository.

Cover:
- Prerequisites (runtime, SDK, tools)
- How to build (exact commands)
- How to run locally (with required config/env vars)
- How to run tests
- Known issues or workarounds
- Environment differences (dev vs staging vs prod, if discoverable)

Test every command you document. If a command can't be verified,
mark it as [UNVERIFIED].
```

---

## Phase 3 — Domain Analysis Prompts (`@03-domain-analysis`)

### Basic: Bounded Context Identification

```
@03-domain-analysis Analyse the domain structure
of this codebase.

Based on existing documentation in /docs/, identify:
1. Business capability groups mapped to code modules
2. Data ownership patterns — which modules read/write which tables
3. Candidate bounded contexts with autonomy ratings (high/medium/low)
4. Shared-write risks — tables written by multiple modules
5. Candidate seams ranked by extraction feasibility

For each bounded context, provide:
- 3–5 sentence business description
- Key classes and files
- Data it owns vs data it shares
- Dependencies on other contexts

Flag ambiguous boundaries with evidence from both sides.
```

### Targeted: Seam Feasibility Assessment

```
@03-domain-analysis Assess the feasibility of
extracting [module/context name] as an independent service.

Analyse:
- What data does it own exclusively?
- What data does it share with other modules (read and write)?
- What would the API surface look like?
- What would break if you enforced the separation today?
- What must change before extraction is safe?

Rate feasibility: ready / needs preparation / high risk.
Explain the rating with evidence.
```

---

## Phase 4 — Modernisation Design Prompts (`@04-modernisation`)

### Basic: Target Architecture

```
@04-modernisation Propose a target architecture for
this system.

Inputs:
- /docs/HLD.md
- /docs/LLD.md
- /docs/domain-analysis-report.md (or equivalent)
- Existing ADRs

Constraints:
- Container-based deployment (Azure Container Apps)
- Incremental migration, strangler-fig pattern preferred
- No big-bang rewrite
- First slice must be lowest risk, highest independence

Produce:
1. Target architecture with service boundaries (Target-Architecture.md)
2. Machine-readable target-architecture.yml following the schema in
   .github/templates/target-architecture.yml
3. Migration plan with phased steps
4. Risk assessment with rollback approach per phase
4. ADRs for new architectural decisions
```

### Targeted: Migration Pattern Selection

```
@04-modernisation Evaluate which migration
pattern is best for extracting [bounded context name].

Consider:
- Strangler fig — route traffic to new service behind gateway
- Branch by abstraction — replace internal module behind interface
- Parallel run — run both old and new, compare output
- Dual-write — sync data between old and new stores

For each pattern, assess:
- Complexity for this specific context
- Risk to existing behaviour
- Reversibility
- Team skill requirements

Recommend one pattern with justification.
```

---

## Phase 5 — Testing Strategy Prompts (`@05-testing`)

### Basic: Test Strategy and Baseline

```
@05-testing Create a testing strategy and
baseline test suite.

Inputs:
- /docs/HLD.md
- /docs/LLD.md
- /docs/Migration-Plan.md

Produce:
1. Test strategy document covering:
   - Test pyramid approach
   - Critical flows and how they're tested
   - Known test gaps
2. Smoke tests — does the app start and respond?
3. Critical path tests — top 5 user journeys
4. CI workflow to run tests on PR

Rules:
- Tests must be deterministic
- No time-dependent or order-dependent tests
- Name tests by behaviour, not implementation
- Prefer service/API level tests over UI tests
```

### Targeted: Characterisation Tests for a Module

```
@05-testing Generate characterisation tests for
the [module name] module.

Purpose: Lock current behaviour so refactoring can be validated.

For each public method/endpoint in the module:
- Capture current output for known inputs
- Include edge cases (null, empty, boundary values)
- Store expected output as golden files where appropriate

Tests must pass against the current code without any changes.
If current behaviour appears buggy, test the bug — document it,
don't fix it.
```

### Targeted: Gherkin Scenarios for a Bounded Context

```
@05-testing Write Gherkin feature files for
the [bounded context name] domain.

Cover:
- Happy path for each core operation
- Key error/edge cases
- Business rules and invariants

Format: .feature.md files with Given/When/Then syntax.
Each scenario should be independently understandable by a
business stakeholder.

Do not implement step definitions yet — scenarios only.
```

---

## Phase 6 — Candidate Slices Prompts

### Basic: Identify and Rank All Slices

```
@06-candidate-slices Identify and rank migration slices for this system.

Inputs:
- /docs/Target-Architecture.md (and /docs/target-architecture.yml)
- /docs/Domain-Analysis-Report.md
- /docs/HLD.md and /docs/LLD.md
- /docs/Test-Strategy.md

For each candidate slice, document:
- Name, bounded context, migration pattern
- Current state (file paths) and target state
- Scope in/out, dependencies, acceptance criteria
- Risk rating with justification
- Rollback approach
- Complexity (S/M/L) and learning value

Rank slices by: risk (lowest first), independence, pattern value,
visibility, team learning.

Produce a dependency graph showing slice ordering.
Map every slice to a component in target-architecture.yml.
```

### Targeted: Evaluate a Specific Slice

```
@06-candidate-slices Evaluate extracting [component name] as a
migration slice.

Current code location: [file paths]
Target architecture component: [name from target-architecture.yml]

Assess:
- Can this run independently without other slices complete?
- What data does it own vs share?
- What's the smallest useful scope?
- What migration pattern fits best?
- What's the rollback approach?
- What would the team learn from this slice?

Rate: risk, independence, complexity.
```

### Targeted: Validate Slice Ordering

```
@06-candidate-slices Review the slice ordering in /docs/Candidate-Slices.md.

Check:
- Is the first slice genuinely lowest risk?
- Are dependencies consistent (no circular refs)?
- Could any slices run in parallel?
- Does the ordering build team skills progressively?
- Does every target architecture component have a slice mapped to it?

Suggest reordering if the current sequence has issues.
```

---

## Programme-Level Prompts

### Intelligent Migration Plan

```
@07-intelligent-migration Design the programme-level migration
operating model.

Inputs:
- /docs/HLD.md
- /docs/LLD.md
- /docs/Migration-Plan.md
- /docs/Candidate-Slices.md
- Business constraints: [timeline, budget, risk tolerance]

Produce:
1. Intelligent Migration Plan — phased roadmap with go/no-go gates
2. Team Model — roles, responsibilities, AI augmentation per role
3. Risk and Governance — Chaos Report failure mapping, control mechanisms
4. ROI and Budget — traditional vs AI-augmented cost comparison

Plans must be executable by a delivery lead without additional
interpretation.
```

### Security Assessment

```
@08-security Assess the security posture of this codebase.

Focus on:
- OWASP Top 10 alignment
- Authentication and authorisation patterns
- Secrets management
- Input validation
- Data protection (at rest and in transit)

For each finding:
- Severity (critical / high / medium / low)
- Evidence (file path and line)
- Remediation recommendation
- Whether it blocks the current migration slice
```

---

## Prompt Patterns — What Works

### Pattern: Scope Narrowing

When agent output is too broad or generic, narrow the scope:

```
❌ "Document this system"
✅ "Document the payment processing module. Focus on the flow from
   checkout request to payment gateway call. Cite file paths."
```

### Pattern: Evidence Requirement

Force the agent to show its work:

```
❌ "Identify the bounded contexts"
✅ "Identify bounded contexts. For each, list the tables it writes,
   the tables it reads, and the files that contain the write operations.
   Flag any table written by more than one context."
```

### Pattern: Uncertainty Surfacing

Ask the agent to be honest about what it doesn't know:

```
Add to any prompt:
"Flag anything you cannot confirm from the code as [INFERRED].
Create an unknowns register for items that need human verification."
```

### Pattern: Output Format Control

Specify format when it matters:

```
"Present findings as a markdown table with columns:
Component | Business Purpose | Key Files | Data Owned | Dependencies"
```

### Pattern: Incremental Build

Don't try to generate everything in one prompt. Build up:

```
Step 1: "@01-discovery Inventory the modules in this repository"
Step 2: "@02-documentation Document the checkout flow end-to-end"
Step 3: "@05-testing Write Gherkin scenarios for the checkout flow"
Step 4: "@06-candidate-slices Define a slice for extracting the checkout module"
```

### Pattern: Comparison Request

When evaluating options:

```
"Compare strangler fig and branch by abstraction for extracting
the pricing engine. For each, assess: complexity, risk, reversibility,
and team skill requirements. Recommend one with justification."
```

---

## Prompt Anti-Patterns — What Fails

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| **"Do everything"** — "modernise this system" | Scope is unbounded; output will be shallow and generic | Break into phases; one prompt per phase |
| **No inputs referenced** — "write documentation" | Agent guesses what to document | Point it at specific files, existing docs, or artefacts |
| **Contradictory constraints** — "rewrite everything but change nothing" | Agent gets confused, picks one | Be consistent; resolve tensions before prompting |
| **Implicit quality bar** — no definition of done | You can't review without knowing what "good" looks like | State what success looks like in the prompt |
| **Over-specification** — 1000-word prompt for a simple task | Agent ignores half, or gets confused by priority conflicts | Keep it focused; one task per prompt |
| **Chain prompting without validation** — running phase 2 on unreviewed phase 1 output | Errors compound through the pipeline | Review and correct each output before using it as input |

---

## Correction Prompts — When Output Needs Fixing

### Factual Correction

```
Your documentation says [module X] connects to [database Y].
This is incorrect — it connects to [database Z] via [file path].
Correct this and check for similar errors in other module descriptions.
```

### Scope Correction

```
The output includes analysis of [module A] and [module B].
This phase should only cover [module A]. Remove all references to
[module B] and re-run the analysis with the reduced scope.
```

### Depth Correction

```
The module description for [module X] is too shallow — "handles pricing"
is not sufficient. Expand it to 3–5 sentences covering:
- What business capability it implements
- What data it reads and writes
- What triggers its execution
- What its key classes are
```

### Quality Correction

```
The generated tests have the following issues:
1. [Test name] asserts true == true — add a meaningful assertion
2. [Test name] depends on system time — make it deterministic
3. [Test name] doesn't clean up test data — add teardown

Fix these and verify all tests still pass.
```

---

## Quick Reference

| # | Phase | Agent | Prompt Focus |
|---|---|---|---|
| 1 | Discovery | `@01-discovery` | What exists? Evidence-based inventory |
| 2 | Documentation | `@02-documentation` | How does it work? Cite files |
| 3 | Domain Analysis | `@03-domain-analysis` | Where are the boundaries? Data ownership |
| 4 | Design | `@04-modernisation` | What should it look like? Incremental path |
| 5 | Testing | `@05-testing` | How do we change it safely? Lock behaviour |
| 6 | Candidate Slices | `@06-candidate-slices` | What do we build first? Ranked backlog |
| 7 | Programme | `@07-intelligent-migration` | Plan, team, risk, budget |
| 8 | Security | `@08-security` | OWASP, auth, secrets, data protection |
