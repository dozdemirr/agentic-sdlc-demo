# Phase 2 — Current-State Documentation Playbook

> **Purpose**: Produce factual documentation of the system as it exists today.
> No future-state design. No opinions. Just evidence.
>
> **Time**: 4–8 hours (manual) | 30–60 minutes (assisted)
>
> **Agent**: `02-documentation` | **Skills**: `system-discovery`, `architecture-reasoning`
>
> **Prerequisite**: Phase 1 (Discovery) complete

---

## Why This Phase Matters

Legacy systems die from knowledge drift. People leave, documentation goes stale,
new team members guess at behaviour. This phase produces documentation that is:

- **Evidence-based** — every claim cites a source file
- **Honest** — clearly marks what's proven vs assumed vs unknown
- **Practical** — written for someone who wasn't there when it was built

---

## Steps

### Step 1: High-Level Design (HLD)

Document the system at the 10,000-foot level:

- [ ] **System purpose** — what does it do for the business? Who uses it? (3–5 sentences)
- [ ] **Architecture overview** — how is it structured? Draw a diagram
- [ ] **Component inventory** — what are the major pieces and what does each do?
- [ ] **Data model** — what are the key entities/tables and their relationships?
- [ ] **Integrations** — what external systems does it connect to and how?
- [ ] **Technology stack** — language, runtime, framework, database, OS with versions

### Step 2: Low-Level Design (LLD)

For each major component, go deeper:

- [ ] **Startup sequence** — what happens when the system starts? (trace it)
- [ ] **Module inventory** — every module with file count, purpose, key representative files
- [ ] **Configuration** — what each parameter controls and what changes if you modify it
- [ ] **Key workflows** — trace the 3–5 most important user actions end-to-end
- [ ] **Data access patterns** — which modules access which tables/collections, read or write

### Step 3: Architecture Decision Records (ADRs)

For each pattern observed in the codebase, document it as a decision:

**Create one document per pattern**, using this structure:

```markdown
# Decision: [Title]

## Status
Observed (in production)

## Context
Why does this pattern exist? What problem was it solving?

## Decision
What pattern was chosen? How does it work?

## Evidence
Which files/configs prove this? (cite specific paths)

## Consequences
What are the trade-offs? What problems does this create?

## Implications for Change
What does this mean for anyone trying to modify or replace this system?
```

**Common patterns to look for:**
- [ ] How authentication/authorisation works
- [ ] How configuration is managed (hardcoded vs external)
- [ ] How data is accessed (ORM, raw SQL, direct table access, API calls)
- [ ] How code is reused (libraries, includes, inheritance, copy-paste)
- [ ] How different customers/tenants are handled
- [ ] How deployments are performed
- [ ] What testing exists (or doesn't)
- [ ] How errors and logging are handled

### Step 4: Operational Runbook

Document everything an operator would need:

- [ ] How to start/stop each component
- [ ] Configuration file locations with parameter explanations
- [ ] Database/data store connection details (sanitised)
- [ ] Batch job / scheduled task inventory
- [ ] Known issues and workarounds
- [ ] Monitoring and alerting (or the documented absence thereof)

---

## Level 2: Using the 02-Documentation Agent

```
@02-documentation Produce current-state documentation for this repository.

Create:
1. A High-Level Design document
2. Low-Level Design per major component
3. Individual architecture decision records (one per observed pattern)
4. An operational runbook

Every claim must cite the source file. Mark anything uncertain as [INFERRED].
```

Or use the skills directly in Copilot Chat:

```
Using the system-discovery and architecture-reasoning skills,
produce current-state documentation for this repository.

Create:
1. A High-Level Design document
2. Low-Level Design per major component
3. Individual architecture decision records (one per observed pattern)
4. An operational runbook

Every claim must cite the source file. Mark anything uncertain as inferred.
```

### Review Focus:
- Module descriptions: 3–5 sentences minimum, not one-liners
- ADRs: one per pattern (not a single monolithic document)
- ADR evidence: do the cited files actually exist and say what the doc claims?
- Config docs: impact described (not just parameter names)
- Unknowns: flagged honestly (not papered over)

---

## Completion Checklist

- [ ] HLD exists with architecture diagram
- [ ] Every component has a 3–5 sentence description
- [ ] Data model covers key entities with relationships
- [ ] Integration points documented with evidence
- [ ] LLD exists for each tier or major component
- [ ] Module inventory has file counts, purposes, and key files
- [ ] 3–5 key workflows traced end-to-end
- [ ] ADRs are individual documents (not monolithic)
- [ ] Each ADR has evidence citations and change implications
- [ ] Runbook covers startup, config, data, batch operations
- [ ] Unknowns from Phase 1 either resolved or explicitly carried forward

## Next Phase
→ [03-domain-analysis-playbook.md](03-domain-analysis-playbook.md)
