# Phase 4 — Modernisation Design Playbook

> **Purpose**: Define a target architecture and an incremental migration path
> that doesn't require a big-bang rewrite.
>
> **Time**: 4–8 hours (manual) | 1–2 hours (assisted)
>
> **Agent**: `04-modernisation` | **Skills**: `architecture-reasoning`, `intelligent-application-migration`
>
> **Prerequisite**: Phase 3 (Domain Analysis) complete

---

## Steps

### Step 1: Define Modernisation Goals

Before designing anything, clarify *why* you're modernising:

- [ ] What business outcomes are you targeting? (cost, speed, scale, compliance)
- [ ] What is the budget and timeline constraint?
- [ ] What is the team's capacity and skill set?
- [ ] What is the risk appetite? (can you tolerate downtime during migration?)

### Step 2: Evaluate Target Architecture Patterns

For each bounded context from Phase 3, consider:

| Pattern | When to Consider |
|---|---|
| **Rehost** (lift and shift) | Low risk, quick win, no code changes |
| **Replatform** (lift and reshape) | Change runtime/infra, minimal code changes |
| **Refactor** (restructure) | Improve internal structure, same functionality |
| **Rearchitect** (redesign) | Fundamental change in patterns or decomposition |
| **Rebuild** (rewrite) | Start over — only when the above can't work |
| **Retain** (do nothing) | Risk is acceptable, cost of change exceeds benefit |

### Step 3: Design Incremental Migration Path

For each bounded context:
- [ ] Which pattern applies?
- [ ] What is the sequence? (which context moves first?)
- [ ] What are the dependencies? (what must exist before this can move?)
- [ ] What is the rollback plan?

### Step 4: Risk Assessment

- [ ] What are the top 10 risks?
- [ ] For each risk: likelihood, impact, mitigation strategy

---

## Completion Checklist

- [ ] Modernisation goals documented with business outcomes
- [ ] Target architecture pattern selected per bounded context
- [ ] Migration sequence defined with dependencies
- [ ] Risk register with top 10 risks and mitigations
- [ ] Rollback strategy for each migration step

---

## Level 2: Using the 04-Modernisation Agent

```
@04-modernisation Design a target architecture and migration plan
for this system.

Inputs:
- /docs/HLD.md
- /docs/LLD.md
- /docs/Domain-Analysis-Report.md

Constraints:
- Container-based deployment
- Incremental migration, strangler-fig pattern preferred
- No big-bang rewrite
- Produce both Target-Architecture.md and target-architecture.yml

Output target-architecture.yml following the schema in
.github/templates/target-architecture.yml.
```

Or use the skills directly in Copilot Chat:

```
Using the architecture-reasoning skill, propose a target architecture
for this system based on the documentation in /docs/.

Produce:
1. Target architecture with service boundaries
2. Migration plan with phased steps and risk per phase
3. target-architecture.yml following the schema in
   .github/templates/target-architecture.yml
4. ADRs for new architectural decisions

Constraints: container-based, incremental, no big-bang rewrite.
```

## Next Phase
→ [05-testing-strategy-playbook.md](05-testing-strategy-playbook.md)
