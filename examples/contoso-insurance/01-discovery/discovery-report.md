# Discovery Report — PolicyHub

> Output of [01-discovery-playbook.md](../../../01-discovery-playbook.md) run against the PolicyHub codebase.

---

## Technology Inventory

| Category | Technology | Version | Evidence |
|---|---|---|---|
| Language | C# | 7.3 | `*.csproj` — `<LangVersion>7.3</LangVersion>` |
| Framework | .NET Framework | 4.8 | `web.config` — `<targetFramework>4.8</targetFramework>` |
| Frontend (Agent) | ASP.NET WebForms | 4.8 | `AgentPortal/*.aspx` — 87 ASPX pages |
| Frontend (Customer) | ASP.NET MVC 5 | 5.2.9 | `CustomerPortal/Controllers/` — 14 controllers |
| ORM | Entity Framework | 6.4.4 | `packages.config` — multiple projects |
| Raw SQL | ADO.NET / Dapper | 2.0.123 | `DataAccess/Repositories/` — ~40 repository classes |
| Database | SQL Server | 2017 | `connectionStrings` in `web.config` |
| Services | WCF | 4.8 | `RatingEngine.svc`, `DocumentService.svc` — 4 service endpoints |
| Batch | Windows Service | — | `RenewalService/`, `BordereauxService/`, `ClaimsImportService/` |
| Reporting | SSRS | 2017 | `Reports/*.rdl` — 32 report definitions |
| Auth | OWIN / ASP.NET Identity | 2.2.3 | `Startup.Auth.cs`, `IdentityConfig.cs` |
| Logging | log4net | 2.0.15 | `log4net.config` across 6 projects |
| Build | MSBuild | — | `PolicyHub.sln` — 47 projects |
| CI | TeamCity | 2022.04 | `teamcity-settings.kts` |
| Deploy | Octopus Deploy | 2023.1 | `*.octopus` deployment process files |
| Package mgmt | NuGet (packages.config) | — | Not yet migrated to PackageReference |

---

## Directory Structure Classification

| Directory | Classification | File Count | Purpose |
|---|---|---|---|
| `AgentPortal/` | UI — WebForms | 142 | Internal agent-facing portal for policy admin |
| `CustomerPortal/` | UI — MVC | 89 | Customer self-service (quotes, renewals, claims) |
| `PolicyHub.Core/` | Domain Logic | 67 | Core business domain — policy, claims, pricing models |
| `PolicyHub.DataAccess/` | Data Layer | 53 | EF contexts, Dapper repos, stored proc wrappers |
| `RatingEngine/` | WCF Service | 28 | Pricing/rating calculations, factor tables |
| `DocumentService/` | WCF Service | 19 | Certificate and letter generation (Word interop) |
| `PaymentGateway/` | WCF Service | 15 | Integration with WorldPay and direct debit |
| `BrokerFeed/` | WCF Service | 22 | Polaris/iMarket broker data exchange |
| `RenewalService/` | Batch — Win Service | 11 | Nightly renewal invitation generation |
| `BordereauxService/` | Batch — Win Service | 8 | Monthly reporting extracts for reinsurers |
| `ClaimsImportService/` | Batch — Win Service | 9 | FNOL import from third-party claims handlers |
| `PolicyHub.Common/` | Shared Library | 34 | DTOs, constants, extension methods, helpers |
| `PolicyHub.Tests/` | Test Project | 41 | Mix of unit + integration tests (~22% coverage) |
| `Database/` | SQL Scripts | 180+ | Stored procedures, migration scripts, seed data |

---

## Module Sampling — `PolicyHub.Core` (Top 10 Files)

| File | LOC | Business Purpose |
|---|---|---|
| `PolicyService.cs` | 1,420 | Orchestrates full policy lifecycle — quote, bind, MTA, cancel, lapse |
| `PremiumCalculator.cs` | 890 | Applies rating factors, loadings, and discounts to base premium |
| `ClaimsHandler.cs` | 740 | FNOL registration, reserve setting, settlement workflow |
| `RenewalEngine.cs` | 680 | Selects eligible policies, recalculates premium, generates invite |
| `UnderwritingRules.cs` | 620 | Referral triggers, decline rules, validation against scheme rules |
| `DocumentGenerator.cs` | 510 | Merges policy data into Word templates via Interop |
| `PaymentProcessor.cs` | 480 | Manages instalment plans, direct debit, card payments |
| `BrokerTranslator.cs` | 440 | Maps between internal schema and broker EDI/XML formats |
| `PolicyValidator.cs` | 390 | Cross-field validation: dates, sums insured, driver eligibility |
| `AuditTrail.cs` | 280 | Records every policy state change with before/after snapshots |

**Observation**: `PolicyService.cs` at 1,420 LOC is a God Class — it orchestrates quotes, MTAs, cancellations, and renewals. This is a key complexity hotspot.

---

## Top 5 Complexity Hotspots

| Rank | File | LOC | Cyclomatic Complexity | Why It's Complex |
|---|---|---|---|---|
| 1 | `PolicyService.cs` | 1,420 | 87 | God class — handles entire policy lifecycle in one class |
| 2 | `PremiumCalculator.cs` | 890 | 64 | Deep nesting for 200+ rating factors with conditional overrides |
| 3 | `spCalculatePremium` (SQL) | 620 | — | Stored procedure duplicating C# rating logic for batch use |
| 4 | `ClaimsHandler.cs` | 740 | 52 | State machine with 12 claim statuses and manual transitions |
| 5 | `Quote.aspx.cs` | 580 | 48 | WebForms code-behind mixing UI logic, validation, and data access |

---

## Entry Points

| Type | Entry Point | Protocol | Purpose |
|---|---|---|---|
| UI | `AgentPortal/` (IIS) | HTTPS :443 | Internal staff portal — policy admin |
| UI | `CustomerPortal/` (IIS) | HTTPS :443 | Public customer portal — quotes & self-service |
| API | `RatingEngine.svc` | WCF/SOAP | Premium calculation for portals and brokers |
| API | `DocumentService.svc` | WCF/SOAP | PDF/Word document generation |
| API | `PaymentGateway.svc` | WCF/SOAP | Payment processing — WorldPay integration |
| API | `BrokerFeed.svc` | WCF/SOAP + FTP | Broker data exchange (iMarket, Polaris) |
| Batch | `RenewalService` | Windows Service | Nightly — generates renewal invitations |
| Batch | `BordereauxService` | Windows Service | Monthly — reinsurance reporting extracts |
| Batch | `ClaimsImportService` | Windows Service | Hourly — imports FNOL from claims handlers |
| Scheduled | SQL Agent Jobs (7) | T-SQL | Data cleanup, archive, aggregation |

---

## Unknowns Register

| # | Unknown | Impact | Resolution Path |
|---|---|---|---|
| 1 | Rating factor tables — are they fully in DB or partially hardcoded? | High — affects pricing migration | Trace `PremiumCalculator` → compare DB factors vs code constants |
| 2 | Which SSRS reports are still actively used? | Medium — avoid migrating dead reports | Check SSRS execution logs for last 90 days |
| 3 | `spCalculatePremium` — is this a duplicate of C# logic or authoritative? | High — data integrity risk | Compare SP output vs `PremiumCalculator` output for same inputs |
| 4 | BrokerFeed FTP credentials — where are they stored? | Medium — security + migration | Check Windows Credential Store + `app.config` transforms |
| 5 | Are there any undocumented API consumers beyond known brokers? | High — breaking change risk | Analyse IIS logs for `BrokerFeed.svc` unique callers |
| 6 | Document templates — Word `.dotx` files, where do they live? | Low — need for doc service migration | Search file shares + check `DocumentService` config |
| 7 | Direct debit mandate files — format and transmission method? | Medium — payment migration | Interview finance team, check `PaymentProcessor` BACS code |
| 8 | TeamCity build — are there any post-deploy smoke tests? | Low — testing gap assessment | Review TeamCity build steps + Octopus deploy scripts |
| 9 | Database backup/restore — RPO/RTO expectations? | High — DR planning for migration | Interview DBA, check SQL Agent backup jobs |
| 10 | Claims import — does the third-party send push or do we poll? | Medium — integration architecture | Check `ClaimsImportService` — FTP poll vs webhook |
| 11 | Are there any feature flags or A/B testing mechanisms? | Low — deployment strategy | Search for `FeatureToggle`, `ConfigurationManager` patterns |

---

## Domain Glossary

| Abbreviation | Meaning |
|---|---|
| MTA | Mid-Term Adjustment — change to a live policy |
| FNOL | First Notification of Loss — initial claim report |
| GWP | Gross Written Premium |
| NTU | Not Taken Up — quote that didn't convert |
| IPT | Insurance Premium Tax |
| Bordereaux | Detailed reporting file sent to reinsurers |
| NCD | No Claims Discount |
| TPA | Third-Party Administrator (claims handler) |
| EDI | Electronic Data Interchange (broker comms) |
| BACS | Bankers' Automated Clearing Services (direct debit) |
