# Sample Output — Contoso Insurance / PolicyHub

> **This is a fictitious example** demonstrating the outputs generated at each playbook stage. Use it to understand the depth, structure, and tone of each deliverable before running the playbooks against your own codebase.

---

## The Organisation

**Contoso Insurance Ltd** is a mid-size UK motor and home insurance provider, operating since 2004. They sell direct-to-consumer through a web portal and via broker integrations. Annual GWP (Gross Written Premium) is ~£180M.

## The System

**PolicyHub** is the company's core policy administration system, originally built in 2009 and extended continuously since.

| Attribute | Detail |
|---|---|
| **Age** | ~15 years (first commit 2009) |
| **Language** | C# (.NET Framework 4.8) |
| **Frontend** | ASP.NET WebForms (agent portal) + MVC 5 (customer portal) |
| **Database** | SQL Server 2017, ~420 tables, ~180 stored procedures |
| **Services** | 4 WCF services (rating engine, document generation, payment gateway, broker feed) |
| **Batch** | 3 Windows Services (renewals, bordereaux reporting, claims FNOL import) |
| **Reporting** | SSRS (32 operational reports) |
| **CI/CD** | TeamCity → Octopus Deploy, manual approvals |
| **Hosting** | On-premises Windows Server 2019, IIS 10 |
| **Solution size** | ~380K LOC across 47 projects in 1 solution |
| **Team** | 6 developers, 1 DBA, 1 tester (2 original developers left in 2022) |

## Why Modernise?

- .NET Framework 4.8 is in maintenance-only mode — no new features from Microsoft
- Release cadence is ~1 deployment per month due to monolith risk
- Customer portal performance degrades during renewal season (Jan/Jun peaks)
- Broker API integration takes 6–8 weeks per new partner
- Two senior developers who built the system have left — institutional knowledge is fading
- Board has approved a digital transformation programme targeting cloud-native on Azure

## Sample Outputs

Each subfolder contains realistic excerpt outputs from the corresponding playbook stage:

| Folder | Playbook | Key Artifacts |
|---|---|---|
| [01-discovery/](01-discovery/) | Discovery | Technology inventory, module sampling, unknowns register |
| [02-documentation/](02-documentation/) | Documentation | HLD, LLD, ADR, Runbook |
| [03-domain-analysis/](03-domain-analysis/) | Domain Analysis | Capability groups, data ownership, bounded contexts, candidate seams |
| [04-modernisation-design/](04-modernisation-design/) | Modernisation Design | Target architecture, migration plan, risk register |
| [05-testing-strategy/](05-testing-strategy/) | Testing Strategy | Test strategy, sample test code |
| [06-implementation/](06-implementation/) | Candidate Slices | First slice definition, scope, risk assessment, rollback |
| [07-intelligent-migration/](07-intelligent-migration/) | Intelligent Migration | Migration plan, team model, risk/governance, ROI/budget |

> **Note**: These are excerpts — real outputs would be more detailed, with full file-path evidence citations from the actual codebase.
