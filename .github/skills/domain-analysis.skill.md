---
name: domain-analysis
version: 1.0
purpose: Identify bounded contexts, data ownership, candidate seams, and shared-model risks to inform modernisation boundaries.
inputs:
  - /docs/HLD.md
  - /docs/LLD.md
  - repository source code
outputs:
  - business capability map with code cross-reference
  - data ownership matrix (single-owner, shared-write, reference)
  - bounded context proposals with autonomy ratings
  - candidate seams ranked by feasibility
guardrails:
  - be strictly factual; cite file paths and symbols
  - do not propose target architecture (that is architecture-reasoning)
  - do not refactor production code
definition_of_done:
  - a team can identify where to cut if separation is needed, supported by evidence from the codebase
---

## Procedure

### Step 1 — List Business Capabilities
- Identify what the **business** does (e.g., manage users, process orders, generate invoices).
- Group related capabilities together.
- Name each group with a business name, not a technical name.

### Step 2 — Map Capabilities to Code
For each capability group, identify:
- which source modules implement it
- which database tables it reads
- which database tables it writes
- which UI screens / controllers / pages drive it

Produce a cross-reference matrix:

| Capability | Modules | Tables (Read) | Tables (Write) |
|---|---|---|---|
| *example* | *folder/module* | *TABLE_A, TABLE_B* | *TABLE_A* |

### Step 3 — Classify Data Ownership
For each table in the matrix, classify:
- **Single owner** — one capability writes, others only read → clean boundary
- **Shared write** — multiple capabilities write → coupling risk
- **Reference data** — many read, admin writes → normal, no concern

### Step 4 — Trace Key Workflows
Pick 3–5 important user actions. For each:
- Trace: user action → UI → service/API → business logic → data store
- Note every module boundary the workflow crosses
- Note every data table it touches
- Record whether the workflow is contained in one capability group or spans several

### Step 5 — Propose Bounded Contexts
For each proposed context, document:
- **Name** — business-oriented
- **Responsibility** — 3–5 sentences
- **Owns** — which modules and tables
- **Depends on** — what it needs from other contexts
- **Autonomy** — could this run independently? (1–5 scale)
- **Confidence** — how sure are you? What would change your mind?

### Step 6 — Identify Candidate Seams
For each candidate seam:
- Between which bounded contexts?
- How many files/connections cross this boundary?
- Which shared-write tables block clean separation?
- What would the interface between the two sides look like?
- What would break if separation were enforced?

Rank seams by feasibility (fewest shared-write crossings, fewest breaking changes).

## Output Format Standard
When referencing code, always include:
- file path
- class / method name
- short description of responsibility

Example:
- `Services/OrderService.cs::GetOrdersByCustomer` — retrieves order history for a given customer.

## Diagram Requirements

All diagrams must comply with `mermaid-syntax-guide.skill.md`. Validate with `scripts/validate_mermaid.py`.

Include the following Mermaid diagrams in output artefacts:

### Bounded Context Map (required)
Use `graph TB` with subgraphs to show proposed bounded contexts:
- one subgraph per context
- edges showing dependencies between contexts
- label edges with relationship type (e.g., "reads", "calls", "shares writes")

### Data Ownership Diagram (required)
Use `graph LR` to show tables and which contexts own them:
- colour-code or label single-owner vs shared-write vs reference
- highlight coupling hotspots (shared-write tables)

### Candidate Seams (recommended)
Use `graph TB` to visualise seam boundaries:
- show which modules sit on each side of a proposed seam
- label crossing points with connection count
