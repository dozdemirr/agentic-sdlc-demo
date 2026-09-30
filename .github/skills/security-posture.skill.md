---
name: security-posture
version: 1.0
purpose: Produce a security posture report and release readiness recommendation using GHAS evidence and OWASP-style risk framing.
inputs:
  - GHAS findings (Dependabot alerts, CodeQL alerts, Secret scanning alerts)
  - /docs/Risk-and-Governance.md
  - /docs/Runbook.md
  - /docs/Test-Strategy.md
outputs:
  - /docs/Security-Posture.md
  - /docs/Security-Controls.md
guardrails:
  - evidence-based only (link each claim to a finding, PR, or workflow run)
  - no direct-to-main changes
  - prefer small remediation PRs
definition_of_done:
  - posture report completed, controls documented, release recommendation made, remediation PRs raised where required
---
## Procedure
1) Collect evidence
   - List open Dependabot alerts and security updates status.
   - List open CodeQL alerts and their severities.
   - List secret scanning findings (if any) and whether push protection is enabled.

2) Classify risk per finding
   - Severity (High/Med/Low)
   - Exploitability (easy/medium/hard)
   - Blast radius (local/service-wide/tenant-wide)

3) Decide release readiness
   - Block if: high severity unresolved OR secrets present OR CodeQL critical paths failing.
   - Proceed-with-mitigations if: medium issues exist with compensating controls and documented plan.
   - OK if: no high issues and controls are enabled.

4) Raise remediation PRs
   - Group by theme. Keep PRs reviewable. Reference finding IDs.

5) Update controls doc
   - Document what is enabled and what checks are required for merge.

## Diagram Requirements

All diagrams must comply with `mermaid-syntax-guide.skill.md`. Validate with `scripts/validate_mermaid.py`.

Include the following Mermaid diagrams in output artefacts:

### Release Readiness Decision Tree (required - in Security-Posture.md)
Use `graph TD` to show release gate logic:
- decision nodes for each severity check (high findings, secrets, CodeQL critical)
- terminal nodes: Block, Proceed with Mitigations, OK
- label edges with conditions

### Finding Severity Breakdown (recommended - in Security-Posture.md)
Use `pie` to show distribution of findings by severity:
- High, Medium, Low categories
- helps stakeholders quickly grasp posture
