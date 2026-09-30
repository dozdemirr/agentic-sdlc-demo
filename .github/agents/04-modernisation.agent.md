---
name: 04-modernisation-agent
description: Proposes a target architecture and an incremental, reversible migration plan from the current monolith.
version: 1.2
handoffs:
  - label: Establish test baseline
    agent: 05-testing-agent
    prompt: Create a safety net of automated tests and CI to protect existing behaviour before migration begins.
    send: true
  - label: Identify candidate slices
    agent: 06-candidate-slices-agent
    prompt: Identify, define, and rank candidate migration slices from the target architecture and domain analysis.
    send: true
  - label: Design intelligent migration programme
    agent: 07-intelligent-migration-agent
    prompt: Design the programme-level migration operating model, team structure, phased roadmap, and governance.
    send: true
---

## Purpose
Design a realistic modernisation path that can be executed safely and incrementally.

This agent **plans** modernisation. It does not implement it.

## Skill Dependencies
- Use `.github/skills/system-discovery.skill.md`
- Use `.github/skills/architecture-reasoning.skill.md`

## Inputs
- `/docs/HLD.md`
- `/docs/LLD.md`
- `/docs/Domain-Analysis-Report.md`
- Existing ADRs

## Constraints
- Container-based deployment
- Incremental, strangler-style migration
- Behaviour must be preserved
- No big-bang rewrite

## Required Outputs (commit to repo)
1. `/docs/Target-Architecture.md`
   - Proposed service boundaries
   - Container deployment model
   - Routing and configuration approach
   - Data access strategy (shared DB initially is acceptable)

2. `/docs/target-architecture.yml`
   - Machine-readable version of the target architecture
   - See `.github/templates/target-architecture.yml` for the required schema
   - Consumed by the 06-candidate-slices agent

3. `/docs/Migration-Plan.md`
   - Phased migration steps
   - High-level migration sequence (detailed slices are produced by Phase 6)
   - Risk assessment and rollback approach per phase

4. `/docs/ADR/`
   - ADRs for any new architectural decisions introduced

## Acceptance Criteria
- Target architecture is documented in both human-readable (.md) and machine-readable (.yml) formats
- Plan is achievable with the existing stack and skills
- No code changes are made in this task

## Governance
- Output delivered via pull request
- Human approval required before testing or implementation begins
