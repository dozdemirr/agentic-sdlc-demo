---
name: owasp-risk-triage
version: 1.0
purpose: Convert raw security findings into a prioritised remediation plan using OWASP-style categories and practical exploit reasoning.
inputs:
  - finding list (dependencies, CodeQL, secrets)
outputs:
  - prioritised remediation backlog with rationale
guardrails:
  - do not invent vulnerabilities; map only what is observed
  - be explicit when mapping is approximate
definition_of_done:
  - backlog ranked with clear rationale and recommended mitigation approach
---
## Procedure
- Map each finding to a broad category (e.g., access control, injection, security misconfiguration, vulnerable components).
- Prioritise by: exploitability × blast radius × detectability.
- Recommend minimal change fixes first, structural changes second.
- Document rationale for each prioritisation decision, referencing the specific finding and potential impact.

## Diagram Requirements

All diagrams must comply with `mermaid-syntax-guide.skill.md`. Validate with `scripts/validate_mermaid.py`.

### Risk Priority Matrix (recommended)
Use `graph TD` to visualise prioritised findings:
- group by category (access control, injection, misconfiguration, vulnerable components)
- order by priority (exploitability x blast radius x detectability)
- label each node with finding ID and recommended action
