# Phase 3 — Domain Analysis Playbook

> **Purpose**: Identify where the natural boundaries are in the system — which
> parts belong together, which share too much, and where you could separate
> things if you needed to.
>
> **Time**: 4–8 hours (manual) | 30–60 minutes (assisted)
>
> **Agent**: `03-domain-analysis` | **Skills**: `domain-analysis`, `architecture-reasoning`
>
> **Prerequisite**: Phase 2 (Documentation) complete

---

## Why This Phase Matters

A monolith isn't inherently a problem. It becomes one when changes in one area
break things in another because the boundaries aren't clear.

This phase answers: **if we had to split this system, where would we cut?**
Even if you never split it, knowing where the seams are makes every change safer.

---

## Key Concepts (Plain English)

| Term | What It Means |
|---|---|
| **Bounded context** | A part of the system that could work independently. It has its own data, rules, and a clear interface to the rest. |
| **Shared model risk** | Two parts of the system both read AND write the same data. Changing one can break the other. |
| **Seam** | A natural dividing line. Fewer connections across a seam = cleaner separation. |
| **Data ownership** | For each data table/collection: who creates data? Who updates it? Who just reads it? |

---

## Steps

### Step 1: List Business Capabilities

Think about what the **business** does, not what the code looks like:

- [ ] List every business capability (e.g., "manage user accounts", "process orders", "generate invoices")
- [ ] Group related capabilities together
- [ ] Name each group with a business name, not a technical name

### Step 2: Map Capabilities to Code

For each business capability group:

- [ ] Which source modules implement it?
- [ ] Which database tables does it use?
- [ ] Which config files affect it?
- [ ] Which UI screens drive it?

Build a cross-reference matrix:

| Capability | Modules | Tables (Read) | Tables (Write) |
|---|---|---|---|
| User Management | users/, auth/ | USERS, ROLES, SESSIONS | USERS, SESSIONS |
| Order Processing | orders/, inventory/ | ORDERS, PRODUCTS, STOCK | ORDERS, ORDER_LINES |
| Invoicing | billing/ | ORDERS, CUSTOMERS | INVOICES, PAYMENTS |

### Step 3: Identify Data Ownership

For each table in your matrix, classify it:

- [ ] **Single owner** — one capability writes, others only read → clean boundary ✅
- [ ] **Shared write** — multiple capabilities write → coupling risk ⚠️
- [ ] **Reference data** — many read, admin writes → normal, no concern ℹ️

### Step 4: Trace Key Workflows

Pick 5 important user actions. For each:

- [ ] Trace: user action → UI → service/API → business logic → data store
- [ ] Note every module boundary the workflow crosses
- [ ] Note every data table it touches
- [ ] Is the workflow contained in one capability group, or does it span several?

### Step 5: Propose Bounded Contexts

Based on Steps 1–4, propose logical boundaries:

For each proposed context:
- [ ] **Name** — business-oriented (not folder/module name)
- [ ] **Responsibility** — 3–5 sentences: what does this context do?
- [ ] **Owns** — which modules and tables belong to it
- [ ] **Depends on** — what it needs from other contexts
- [ ] **Autonomy** — could this run independently? (1–5 scale)
- [ ] **Confidence** — how sure are you? What would change your mind?

### Step 6: Identify Candidate Seams

Where could you draw a line with the least pain?

For each candidate seam:
- [ ] Between which bounded contexts?
- [ ] How many files/connections cross this boundary?
- [ ] Which shared-write tables block clean separation?
- [ ] What would the interface between the two sides look like?
- [ ] What would break if you enforced the separation?
- [ ] What must be true before you could cut here?

---

## Level 2: Using the 03-Domain-Analysis Agent

```
@03-domain-analysis Analyse the domain structure of this codebase.

Based on the existing documentation in /docs/, identify:
1. Business capability groups mapped to code modules
2. Data ownership patterns (which modules write which tables)
3. Candidate bounded contexts with autonomy ratings
4. Shared model risks where multiple modules write the same data
5. Candidate seams ranked by feasibility

For each bounded context, provide a 3–5 sentence business description.
Flag any ambiguous boundaries with evidence from both sides.
```

Or use the skills directly in Copilot Chat:

```
Using the architecture-reasoning skill, analyse the domain
structure of this codebase.

Based on the existing documentation, identify:
1. Business capability groups mapped to code modules
2. Data ownership patterns (which modules write which tables)
3. Candidate bounded contexts with autonomy ratings
4. Shared model risks where multiple modules write the same data
5. Candidate seams ranked by feasibility

For each bounded context, provide a 3-5 sentence business description.
Flag any ambiguous boundaries with evidence from both sides.
```

---

## Completion Checklist

- [ ] Business capabilities listed and grouped
- [ ] Capability-to-code cross-reference matrix complete
- [ ] Data ownership classified for all key tables
- [ ] 5 key workflows traced end-to-end across module boundaries
- [ ] 3+ bounded contexts proposed with business descriptions
- [ ] Shared-write tables identified as coupling risks
- [ ] Candidate seams ranked by feasibility
- [ ] Ambiguous boundaries flagged with evidence

## Next Phase
→ [04-modernisation-design-playbook.md](04-modernisation-design-playbook.md)
