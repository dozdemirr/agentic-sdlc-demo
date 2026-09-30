---
name: intelligent-application-migration
version: 2.0
purpose: Design and govern a low-risk, high-confidence application migration programme using AI-augmented delivery models, with comparative economic modelling.
inputs:
  - /docs/HLD.md
  - /docs/LLD.md
  - /docs/Migration-Plan.md
  - Assessment or scan outputs (if available)
  - Business constraints (timeline, budget sensitivity, risk tolerance)
outputs:
  - /docs/Intelligent-Migration-Plan.md
  - /docs/Intelligent-Team-Model.md
  - /docs/Risk-and-Governance.md
  - /docs/ROI-and-Budget.md
guardrails:
  - no code changes or infrastructure deployment
  - programme design and governance only
  - plans must be evidence-based and traceable to system reality
  - all assumptions must be stated with confidence level
  - if inputs are incomplete, explicitly state assumptions
definition_of_done:
  - programme can be executed by a delivery lead without additional interpretation
  - outputs clearly show how AI improves delivery outcomes vs traditional approach
---


## Reasoning Framework

### Step 1 — Anchor to Failure Patterns (Non-Negotiable)
Map the migration context against known Chaos Report failure risks:
- lack of executive sponsorship
- poor requirements / scope clarity
- weak user involvement
- unrealistic timelines
- insufficient skills / capacity
- large batch delivery risk
- weak governance
- technology misalignment
- change / adoption failure

For each risk:
- identify risk presence (high / medium / low)
- provide mitigation embedded into the programme design
- tie mitigation to a **specific control or decision point** in the roadmap

### Step 2 — Define the Intelligent Team Model
Design a lean, high-impact, cross-functional team:
- executive sponsor
- delivery lead / PM
- cloud architect
- developers
- DevOps
- QA

For each role define:
- core responsibilities
- decision authority
- AI augmentation (GitHub Copilot, agents, M365 Copilot)
- expected productivity uplift (qualitative + % estimate)

Also define:
- accountability model (who owns success vs who owns output)
- escalation paths

### Step 3 — Build a Phased, Low-Risk Roadmap
Structure delivery into clear phases:
- initiation & planning
- environment & pipeline setup
- migration & development (slice-based, incremental)
- testing & hardening
- deployment & closure

Each phase must include:
- deliverables
- dependencies
- entry criteria
- exit criteria
- success metrics
- explicit go/no-go checkpoints

Constraints:
- must enforce small batch, reversible slices
- no "big bang" migrations

### Step 4 — Embed Governance by Design
Define a governance system that ensures:
- continuous visibility of risk
- early detection of failure signals
- controlled use of AI

Include:
- review cadence (weekly, per-slice, executive checkpoints)
- risk escalation model
- human-in-the-loop approvals (PR-based control)
- rollback strategy per migration slice
- telemetry and audit expectations

Explicitly position AI as:
- acceleration layer
- drafting and analysis engine
- **not** decision authority

### Step 5 — Model Cost, Productivity, and ROI

#### 5a — Baseline (Traditional Delivery)
- team size and cost
- delivery duration
- risk-adjusted cost (rework, delays)

#### 5b — AI-Augmented Delivery (Copilot + Agents)
- reduced team effort assumptions
- cycle time reduction
- quality improvement (defect reduction proxy)

#### 5c — Comparison Output
Provide:
- % productivity gain (engineering, testing, documentation)
- estimated cost reduction
- time-to-delivery reduction
- ROI breakeven point

Tie all assumptions to:
- team structure
- AI usage intensity
- migration complexity

Be explicit where assumptions are directional vs evidence-backed.

## Output Quality Bar
- Programme increases success probability relative to industry baseline
- Risks are managed explicitly, not implicitly
- Outputs are suitable for executive review and funding approval
- Traditional vs AI-augmented comparison is clear and quantified
- Clarity over completeness. Decisions over descriptions. Control over optimism.

## Diagram Requirements

All diagrams must comply with `mermaid-syntax-guide.skill.md`. Validate with `scripts/validate_mermaid.py`.

Include the following Mermaid diagrams in output artefacts:

### Phased Roadmap (required - in Intelligent-Migration-Plan.md)
Use `gantt` to show programme phases and milestones:
- one section per phase (initiation, environment setup, migration slices, testing, deployment)
- show dependencies using `after taskId`
- mark go/no-go checkpoints with `:milestone, id, date, 0d`
- use `dateFormat YYYY-MM-DD` and day/week durations only

### Team Model (required - in Intelligent-Team-Model.md)
Use `graph TB` to show team structure and AI augmentation:
- one node per role
- group by function using subgraphs (leadership, engineering, quality)
- label edges with reporting/escalation relationships
- annotate AI-augmented roles

### Governance Flow (required - in Risk-and-Governance.md)
Use `stateDiagram-v2` to show slice lifecycle:
- states: Planning, In Progress, Review, Approved, Deployed, Rolled Back
- transitions with gate conditions
- show human-in-the-loop approval points

### Risk Matrix (recommended - in Risk-and-Governance.md)
Use `graph TB` to visualise failure pattern risks:
- group by severity (high, medium, low)
- show mitigation linkage to roadmap control points

### ROI Comparison (recommended - in ROI-and-Budget.md)
Use `graph LR` to show traditional vs AI-augmented delivery comparison:
- parallel tracks showing team size, duration, cost
- highlight productivity gain areas
