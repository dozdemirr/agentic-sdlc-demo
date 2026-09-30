# Phase 5 — Testing Strategy Playbook

> **Purpose**: Establish a testing baseline that protects current behaviour,
> enabling safe refactoring and migration.
>
> **Time**: 2–4 hours (planning) | varies (implementation)
>
> **Agent**: `05-testing` | **Skills**: `test-synthesis`, `security-posture`
>
> **Prerequisite**: Phase 4 (Design) complete

---

## Steps

### Step 1: Assess Current Test Coverage

- [ ] Does any automated testing exist? What kind? What coverage?
- [ ] What are the critical user journeys that MUST be protected?
- [ ] What is the current deployment/validation process?

### Step 2: Define Test Priorities

Not everything needs testing before you start. Prioritise:

| Priority | What to Test | Why |
|---|---|---|
| 1 | Smoke tests — does it start and respond? | Cheapest, highest ROI |
| 2 | Critical path tests — do the top 5 user journeys work? | Protects revenue-generating flows |
| 3 | Characterisation tests — capture current output for known inputs | Enables refactoring without behaviour change |
| 4 | Integration tests — do components communicate correctly? | Protects seams and interfaces |
| 5 | Security tests — OWASP top 10, auth flows, data handling | Protects against regression in security posture |

### Step 3: Select Approach

- [ ] What test framework fits the technology stack?
- [ ] Where will tests run? (local, CI, both?)
- [ ] What test data strategy? (synthetic, anonymised production, fixtures?)

### Step 4: Implement Minimum Viable Test Suite

Start with Priority 1 and 2 only. Expand as confidence grows.

---

## Completion Checklist

- [ ] Current test coverage assessed and documented
- [ ] Critical user journeys identified (top 5–10)
- [ ] Test framework selected for the technology stack
- [ ] Priority 1 (smoke) tests implementable
- [ ] Priority 2 (critical path) tests planned
- [ ] Security posture assessed (OWASP alignment)
- [ ] CI pipeline defined (or gap documented)

---

## Level 2: Using the 05-Testing Agent

```
@05-testing Create a testing strategy and baseline test suite
for this system.

Inputs:
- /docs/HLD.md
- /docs/LLD.md
- /docs/Migration-Plan.md

Produce:
1. Test strategy document (pyramid approach, critical flows, known gaps)
2. Smoke tests — does the app start and respond?
3. Critical path tests — top 5 user journeys
4. CI workflow to build and test on pull requests

Tests must be deterministic. Name tests by behaviour. Prefer
service/API level tests over UI tests.
```

## Next Phase
→ [06-candidate-slices-playbook.md](06-candidate-slices-playbook.md)
