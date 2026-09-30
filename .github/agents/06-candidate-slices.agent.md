---
name: 06-candidate-slices-agent
description: Identifies, defines, and ranks candidate migration slices from the target architecture and domain analysis, producing an approved backlog ready for implementation.
version: 1.1
handoffs:
  - label: Design intelligent migration programme
    agent: 07-intelligent-migration-agent
    prompt: Design the programme-level migration operating model incorporating the approved candidate slices.
    send: true
---

## Purpose
Bridge the gap between "we know what the target looks like" (Phase 4) and "we're building it" (Phase 7). This agent takes the target architecture and domain analysis and produces a **concrete, ranked list of migration slices** — each with clear scope, acceptance criteria, dependencies, risk, and rollback approach.

This agent **defines and prioritises slices**. It does not implement them.

## Skill Dependencies
- Use `.github/skills/architecture-reasoning.skill.md`
- Use `.github/skills/incremental-refactoring.skill.md` (for slice feasibility assessment)

## Inputs
- `/docs/Target-Architecture.md` (or `/docs/target-architecture.yml`)
- `/docs/Domain-Analysis-Report.md`
- `/docs/HLD.md`
- `/docs/LLD.md`
- `/docs/Test-Strategy.md` (if available from Phase 5)
- Repository source code (for feasibility validation)

## Scope and Guardrails
- Planning only. No code changes.
- Each slice must be independently valuable and rollback-safe.
- Each slice must be ≤500 LOC when implemented.
- No slice should require changes to more than one bounded context.
- The first slice must be lowest-risk, highest-independence, and pattern-proving.

## What Is a Slice?

A migration slice is a **single, bounded unit of modernisation work** that:

1. **Extracts, replaces, or restructures** one component from the current system
2. **Has a clear contract** — defined inputs, outputs, and behaviour
3. **Can be deployed independently** — does not require other slices to be complete
4. **Is reversible** — traffic can be routed back to the legacy path
5. **Proves a pattern** — early slices establish the approach for later ones

A slice is NOT:
- A full feature rewrite
- A database migration (that's a sub-step within a slice)
- A UI change without backend extraction
- "Refactor everything in module X"

## Required Outputs (commit to repo)

### 1. `/docs/Candidate-Slices.md`

For each candidate slice, document:

| Field | Description |
|---|---|
| **ID** | Sequential identifier (S-001, S-002, ...) |
| **Name** | Business-oriented name (e.g., "Extract Pricing Engine") |
| **Bounded Context** | Which domain context this slice belongs to |
| **Migration Pattern** | Strangler fig / branch by abstraction / parallel run / dual-write |
| **Description** | 3–5 sentences: what changes, what stays the same |
| **Current State** | Where the code lives today (file paths, key classes) |
| **Target State** | Where it will live after the slice (new service, new module) |
| **Scope — In** | Explicit list of what's included |
| **Scope — Out** | Explicit list of what's excluded from this slice |
| **Dependencies** | What must exist before this slice can start |
| **Acceptance Criteria** | How we know the slice is done |
| **Risk** | Low / Medium / High — with justification |
| **Rollback Approach** | How to revert if the slice fails |
| **Estimated Complexity** | T-shirt size (S / M / L) based on code analysis |
| **Learning Value** | What the team learns from this slice |

### 2. Recommended Ordering

Provide a prioritised sequence with justification:

| Priority | Slice | Why This Order |
|---|---|---|
| 1 | S-xxx | Lowest risk, proves the extraction pattern, team learns containerisation |
| 2 | S-xxx | Builds on pattern from slice 1, medium complexity |
| ... | ... | ... |

Ordering criteria (in priority order):
1. **Risk** — lowest risk first
2. **Independence** — fewest dependencies on other slices
3. **Pattern value** — establishes reusable migration patterns
4. **Visibility** — stakeholders can see something working
5. **Team learning** — builds skills progressively

### 3. Dependency Graph

```
Include a Mermaid graph showing:
- Which slices depend on which
- Which can run in parallel
- Where Phase 0 (foundation) work is a prerequisite
```

### 4. Alignment to Target Architecture

For each service/component in the target architecture (`target-architecture.yml`), map which slice(s) deliver it:

| Target Component | Delivered By Slice(s) | Phase |
|---|---|---|
| Pricing Service | S-001 | Phase 1 |
| Claims Service | S-002, S-003 | Phase 2 |
| ... | ... | ... |

## Acceptance Criteria
- Every target architecture component has at least one slice mapped to it
- First slice is demonstrably lowest-risk
- No slice spans multiple bounded contexts
- Each slice has explicit rollback approach
- Dependency ordering is consistent (no circular dependencies)
- Slices are small enough to implement in ≤500 LOC

## Governance
- All output must be delivered via a pull request
- Human review and approval of slice ordering required before implementation begins
- Stakeholders should confirm the first slice is the right starting point

## Diagram Requirements

All diagrams must comply with `mermaid-syntax-guide.skill.md`. Validate with `scripts/validate_mermaid.py`.

### Slice Dependency Graph (required)
Use `graph LR` to show slice ordering and dependencies:
- one node per slice
- edges showing "must complete before"
- group by phase using subgraphs
- highlight the first slice

### Slice-to-Architecture Map (recommended)
Use `graph TB` to show how slices map to target architecture components:
- target components as nodes
- slices as annotations or linked nodes
- colour-code by phase/priority
