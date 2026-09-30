# Low-Level Design — PolicyHub

> Output of [02-documentation-playbook.md](../../../02-documentation-playbook.md) — detailed internal structure documentation.

---

## Startup Sequence

```mermaid
sequenceDiagram
    participant IIS
    participant Global as Global.asax
    participant OWIN as Startup.Auth.cs
    participant EF as EF DbContext
    participant Log as log4net
    participant WCF as WCF Services

    IIS->>Global: Application_Start()
    Global->>Log: XmlConfigurator.Configure()
    Global->>OWIN: ConfigureAuth(app)
    OWIN->>OWIN: Cookie auth + OWIN middleware
    Global->>EF: Database.SetInitializer(null)
    Global->>Global: RouteConfig.RegisterRoutes()
    Global->>Global: BundleConfig.RegisterBundles()
    Note over IIS,WCF: WCF services hosted in same IIS app pool
    IIS->>WCF: Activate RatingEngine.svc, DocumentService.svc, etc.
```

**Key finding**: All components (portals + WCF services) share a single IIS application pool. A crash in the Document Service (Word Interop) can take down the entire system.

---

## Module Inventory

| Module | Projects | File Count | Key Files | Purpose |
|---|---|---|---|---|
| Agent Portal | `AgentPortal` | 142 | `Quote.aspx.cs`, `PolicyAdmin.aspx.cs`, `ClaimEntry.aspx.cs` | Internal staff UI |
| Customer Portal | `CustomerPortal` | 89 | `QuoteController.cs`, `RenewalController.cs`, `AccountController.cs` | Customer self-service |
| Core | `PolicyHub.Core` | 67 | `PolicyService.cs`, `PremiumCalculator.cs`, `ClaimsHandler.cs` | All business logic |
| Data Access | `PolicyHub.DataAccess` | 53 | `PolicyContext.cs`, `PolicyRepository.cs`, `ClaimsRepository.cs` | EF6 + Dapper repos |
| Common | `PolicyHub.Common` | 34 | `PolicyDto.cs`, `Constants.cs`, `DateExtensions.cs` | Shared types + helpers |

---

## Configuration per Module

| Module | Config File | Key Parameters |
|---|---|---|
| Agent Portal | `web.config` | `connectionStrings:PolicyHubDb`, `appSettings:SessionTimeout=30`, `appSettings:MaxQuoteAge=30` |
| Customer Portal | `web.config` | `connectionStrings:PolicyHubDb`, `appSettings:RecaptchaSiteKey`, `appSettings:WorldPayMerchantId` |
| Rating Engine | `RatingEngine.svc.config` | `appSettings:RatingVersion`, `appSettings:FactorTableCacheMins=60` |
| Renewal Service | `app.config` | `appSettings:RenewalLeadDays=21`, `appSettings:BatchSize=500`, `connectionStrings:PolicyHubDb` |
| Claims Import | `app.config` | `appSettings:FtpHost`, `appSettings:PollIntervalMins=60`, `connectionStrings:PolicyHubDb` |

---

## Key Workflows

### 1. New Quote → Bind (Customer Portal)

```mermaid
sequenceDiagram
    actor Customer
    participant CP as CustomerPortal
    participant Core as PolicyHub.Core
    participant RE as RatingEngine
    participant DA as DataAccess
    participant DB as SQL Server

    Customer->>CP: Submit quote details
    CP->>Core: PolicyService.CreateQuote(dto)
    Core->>Core: PolicyValidator.Validate(dto)
    Core->>RE: RatingEngine.Calculate(risk)
    RE->>DB: Load factor tables
    RE-->>Core: PremiumResult
    Core->>DA: PolicyRepository.SaveQuote(policy)
    DA->>DB: INSERT Policy, PolicyVersion, Premium
    Core-->>CP: QuoteReference + Premium
    Customer->>CP: Accept quote
    CP->>Core: PolicyService.BindQuote(ref)
    Core->>DA: UPDATE Policy SET Status='Live'
    Core->>Core: DocumentGenerator.GenerateCertificate(policy)
    Core-->>CP: Confirmation + documents
```

### 2. Mid-Term Adjustment (Agent Portal)

```mermaid
sequenceDiagram
    actor Agent
    participant AP as AgentPortal
    participant Core as PolicyHub.Core
    participant RE as RatingEngine
    participant DA as DataAccess
    participant DB as SQL Server

    Agent->>AP: Search policy, request MTA
    AP->>Core: PolicyService.InitiateMTA(policyId, effectiveDate)
    Core->>DA: Load current PolicyVersion
    Core->>Core: Clone PolicyVersion with changes
    Core->>RE: RatingEngine.Calculate(updatedRisk)
    RE-->>Core: Adjusted premium
    Core->>Core: Calculate pro-rata adjustment
    Core->>DA: INSERT new PolicyVersion, UPDATE Premium
    Core->>Core: DocumentGenerator.GenerateEndorsement(policy)
    Core-->>AP: Adjustment amount + endorsement doc
```

### 3. Nightly Renewal Batch

```mermaid
sequenceDiagram
    participant RS as RenewalService
    participant DA as DataAccess
    participant DB as SQL Server
    participant RE as RatingEngine
    participant DS as DocumentService

    RS->>DB: SELECT policies WHERE renewal_date = TODAY + 21
    loop Each eligible policy
        RS->>RE: Calculate renewal premium
        RE-->>RS: New premium
        RS->>DA: INSERT RenewalInvitation
        RS->>DS: Generate renewal letter
    end
    RS->>DB: UPDATE batch_log SET status='Complete'
```

---

## Data Access Patterns

| Module | Tables Read | Tables Written | Method |
|---|---|---|---|
| PolicyService | Policy, PolicyVersion, Customer, Vehicle, Property | Policy, PolicyVersion, Cover, Premium | EF6 |
| PremiumCalculator | RatingFactor, FactorTable, Discount, Loading | — (read-only) | Dapper |
| ClaimsHandler | Claim, ClaimReserve, Policy | Claim, ClaimReserve, ClaimPayment, ClaimNote | EF6 |
| RenewalEngine | Policy, PolicyVersion, Premium | RenewalInvitation, PolicyVersion | EF6 + SP |
| DocumentGenerator | Policy, PolicyVersion, Customer, Cover | Document | EF6 + Word Interop |
| PaymentProcessor | PaymentPlan, Instalment, Policy | PaymentPlan, Instalment, PaymentTransaction | EF6 |
| BrokerTranslator | Policy, PolicyVersion, Customer, Claim | BrokerMessage, BrokerLog | Dapper |

**Observation**: `Policy` and `PolicyVersion` tables are read by every module — these are the gravitational centre of the database.
