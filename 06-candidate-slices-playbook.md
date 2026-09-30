# Phase 6 — Candidate Slices Playbook

> **Purpose**: Take the target architecture and domain analysis and produce a
> ranked backlog of migration slices — each with clear scope, acceptance criteria,
> risk, and rollback approach. This bridges the gap between planning and execution.
>
> **Time**: 2–4 hours (manual) | 30–60 minutes (assisted)
>
> **Agent**: `06-candidate-slices` | **Skills**: `architecture-reasoning`, `incremental-refactoring`
>
> **Prerequisite**: Phase 4 (Modernisation Design) and Phase 5 (Testing) complete

---

## Why This Phase Matters

Phases 1–5 answered "what have we got?" and "where are we going?" This phase answers
**"what do we build first, and in what order?"**

Without this, teams either:
- Pick a slice that's too risky and fail visibly
- Pick a slice that's too easy and learn nothing
- Try to migrate everything at once and lose control

**The rule: every slice must be independently valuable, reversible, and ≤500 LOC.**

---

## What Is a Slice?

A migration slice is a **single, bounded unit of modernisation work** that:

1. **Extracts, replaces, or restructures** one component from the current system
2. **Has a clear contract** — defined inputs, outputs, and behaviour
3. **Can be deployed independently** — does not require other slices to be complete
4. **Is reversible** — traffic can be routed back to the legacy path
5. **Proves a pattern** — early slices establish the approach for later ones

A slice is NOT:
- A full feature rewrite
- A database migration on its own
- A UI change without backend extraction
- "Refactor everything in module X"

---

## Steps

### Step 1: Review Target Architecture

Open `/docs/Target-Architecture.md` and `/docs/target-architecture.yml`. For each
target service/component, ask:

- [ ] What code in the monolith maps to this component?
- [ ] How much of the monolith does this touch?
- [ ] Does this share data (writes) with other components?
- [ ] Could this run independently if extracted?

### Step 2: Define Each Candidate Slice

For each candidate, document:

| Field | What to Write |
|---|---|
| **Name** | Business-oriented (e.g., "Extract Pricing Engine") |
| **Bounded Context** | Which domain context from Phase 3 |
| **Migration Pattern** | Strangler fig / branch by abstraction / parallel run / dual-write |
| **Description** | 3–5 sentences: what changes, what stays the same |
| **Current State** | File paths and key classes in the monolith |
| **Target State** | New service/module location |
| **Scope — In** | Explicit list of what's included |
| **Scope — Out** | What's explicitly excluded |
| **Dependencies** | What must exist first |
| **Acceptance Criteria** | How you know it's done |
| **Risk** | Low / Medium / High with justification |
| **Rollback** | How to revert |
| **Complexity** | S / M / L based on code analysis |
| **Learning Value** | What the team gains from this slice |

### Step 3: Choose the Migration Pattern Per Slice

| Pattern | Use When | Complexity |
|---|---|---|
| **Strangler fig** | New service replaces legacy behind API gateway | Medium |
| **Dual-write** | Migrating data from legacy to new database | High |
| **Branch by abstraction** | Replacing an internal module | Medium |
| **Parallel run** | Calculations that must match legacy exactly | High |

### Step 4: Rank the Slices

Order by these criteria (in priority order):

1. **Risk** — lowest risk first
2. **Independence** — fewest dependencies on other slices
3. **Pattern value** — establishes reusable patterns for later slices
4. **Visibility** — stakeholders can see something working
5. **Team learning** — builds skills progressively

The first slice should be:
- [ ] **Lowest risk** — fewest shared-write tables
- [ ] **Highest independence** — can run without other slices
- [ ] **Visible result** — stakeholders can see it working
- [ ] **Pattern-proving** — establishes the migration approach

### Step 5: Build the Dependency Graph

Map which slices depend on which others:
- Which must complete before others can start?
- Which can run in parallel?
- Where is Phase 0 (foundation/infrastructure) a prerequisite?

### Step 6: Map Slices to Target Architecture

For each component in `target-architecture.yml`, confirm which slice(s) deliver it.
Every target component must have at least one slice mapped to it.

---

## Level 2: Using the 06-Candidate-Slices Agent

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
```

---

## Completion Checklist

- [ ] Every target architecture component has at least one slice mapped to it
- [ ] First slice is demonstrably lowest-risk and highest-independence
- [ ] No slice spans multiple bounded contexts
- [ ] Each slice has explicit scope (in and out), acceptance criteria, and rollback
- [ ] Each slice is ≤500 LOC when implemented
- [ ] Dependency graph has no circular dependencies
- [ ] Slices are ordered with justification
- [ ] Stakeholders agree the first slice is the right starting point
