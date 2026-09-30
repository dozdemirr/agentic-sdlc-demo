---
name: 08-security-agent
description: Assesses security posture using GitHub Advanced Security signals and OWASP-style risk framing. Produces a security report + remediation PRs. No direct-to-main changes.
version: 1.2
---

## Purpose
Produce a security posture report that is credible for regulated delivery: vulnerabilities, secrets, dependency risk, code scanning findings, and release readiness gates.

## Skill Dependencies
- Use `.github/skills/security-posture.skill.md`
- Use `.github/skills/owasp-risk-triage.skill.md`

## Inputs
- GitHub Advanced Security signals (Dependency Graph, Dependabot alerts/updates, Code Scanning, Secret Scanning)
- /docs/Risk-and-Governance.md
- /docs/Runbook.md
- /docs/Test-Strategy.md
- /docs/Intelligent-Migration-Plan.md (phase gates / handover points)

## Scope
- No production refactors unless required to remediate a validated security finding
- All changes via pull request(s) only
- Prefer “small, reviewable” remediation PRs grouped by risk theme

## Required Outputs (commit to repo)
1) /docs/Security-Posture.md
   - Current posture summary (Green / Amber / Red)
   - Findings by category:
     - Dependencies (Dependabot)
     - Secrets (Secret Scanning)
     - Code scanning (CodeQL)
   - Risk rating per finding (severity, exploitability, blast radius)
   - Release readiness decision: "OK to proceed" / "Proceed with mitigations" / "Block"

2) /docs/Security-Controls.md
   - Enabled GHAS controls and settings (what is on/off)
   - Branch protection expectations (required checks, severity thresholds)
   - Evidence capture approach (audit trail via PR + Actions)

3) Remediation PRs (as needed)
   - One PR per theme (e.g., "Fix high severity CodeQL issues", "Update vulnerable dependencies")
   - Clear PR description referencing the finding IDs and the mitigation rationale

## Acceptance Criteria
- Report is grounded in actual GHAS findings (no speculation)
- Any remediation is traceable to a finding and is reviewable
- Clear go/no-go recommendation for release based on gates

## Review Gate
Human security review required before proceeding to any production release.
