# Domain Analysis Report — PolicyHub

> Output of [03-domain-analysis-playbook.md](../../../03-domain-analysis-playbook.md) — identifying natural boundaries and candidate separation points.

---

## Business Capability Groups

| # | Capability Group | Business Capabilities |
|---|---|---|
| 1 | **Policy Lifecycle** | Create Quote, Bind Policy, Mid-Term Adjust, Cancel, Lapse, Reinstate |
| 2 | **Pricing & Rating** | Calculate Premium, Apply Discounts, Load Factors, NCD Validation |
| 3 | **Claims Management** | Register FNOL, Set Reserves, Process Payments, Settle, Recover |
| 4 | **Customer Management** | Register Customer, Validate Address, Manage Preferences, KYC |
| 5 | **Document Production** | Generate Certificate, Endorsement, Renewal Letter, Claims Correspondence |
| 6 | **Payments & Billing** | Collect Payment, Manage Instalments, Direct Debit, Refunds |
| 7 | **Broker Distribution** | Receive Broker Quotes, Send Policy Data, EDI Translation |
| 8 | **Regulatory Reporting** | Bordereaux, IPT Returns, FCA Complaints Reporting |
| 9 | **Renewals** | Identify Eligible, Calculate Renewal Premium, Generate Invite, Track Uptake |

---

## Capability-to-Code Cross-Reference Matrix

| Capability Group | Modules | Tables (Read) | Tables (Write) |
|---|---|---|---|
| Policy Lifecycle | `PolicyHub.Core`, `AgentPortal`, `CustomerPortal` | Policy, PolicyVersion, Customer, Vehicle, Property, Cover | Policy, PolicyVersion, Cover, AuditTrail |
| Pricing & Rating | `RatingEngine`, `PolicyHub.Core` | RatingFactor, FactorTable, Discount, Loading, NCD | — (read-only in normal flow) |
| Claims Management | `PolicyHub.Core`, `AgentPortal`, `ClaimsImportService` | Claim, ClaimReserve, Policy, Customer | Claim, ClaimReserve, ClaimPayment, ClaimNote |
| Customer Management | `PolicyHub.Core`, `AgentPortal`, `CustomerPortal` | Customer, Address, CustomerPreference | Customer, Address |
| Document Production | `DocumentService`, `PolicyHub.Core` | Policy, PolicyVersion, Customer, Cover, Claim | Document |
| Payments & Billing | `PaymentGateway`, `PolicyHub.Core` | PaymentPlan, Instalment, Policy | PaymentPlan, Instalment, PaymentTransaction |
| Broker Distribution | `BrokerFeed`, `PolicyHub.Core` | Policy, PolicyVersion, Customer, Claim | BrokerMessage, BrokerLog |
| Regulatory Reporting | `BordereauxService`, SSRS | Policy, PolicyVersion, Claim, Premium | BordereauxExtract |
| Renewals | `RenewalService`, `PolicyHub.Core` | Policy, PolicyVersion, Premium, RenewalInvitation | RenewalInvitation, PolicyVersion |

---

## Data Ownership Classification

| Table | Owner (Primary Writer) | Other Writers | Classification |
|---|---|---|---|
| Policy | Policy Lifecycle | Renewals (status update) | ⚠️ Shared write |
| PolicyVersion | Policy Lifecycle | Renewals (new version) | ⚠️ Shared write |
| Customer | Customer Management | — | ✅ Single owner |
| Address | Customer Management | — | ✅ Single owner |
| Claim | Claims Management | Claims Import | ⚠️ Shared write |
| ClaimReserve | Claims Management | — | ✅ Single owner |
| ClaimPayment | Claims Management | — | ✅ Single owner |
| Premium | Policy Lifecycle | — | ✅ Single owner |
| RatingFactor | — (reference data, manual DB updates) | — | ℹ️ Reference data |
| PaymentPlan | Payments & Billing | — | ✅ Single owner |
| Instalment | Payments & Billing | — | ✅ Single owner |
| Document | Document Production | — | ✅ Single owner |
| RenewalInvitation | Renewals | — | ✅ Single owner |
| BrokerMessage | Broker Distribution | — | ✅ Single owner |
| BordereauxExtract | Regulatory Reporting | — | ✅ Single owner |

**Key finding**: `Policy` and `PolicyVersion` have shared writes from both Policy Lifecycle and Renewals — this is the primary coupling point.

---

## Workflow Traceability — Key User Journeys

### Journey 1: Customer Gets a Motor Quote

| Step | Module | Tables | Capability Group |
|---|---|---|---|
| Enter vehicle reg | CustomerPortal | — (external DVLA call) | Customer Management |
| Enter driver details | CustomerPortal | Customer, Address | Customer Management |
| Calculate premium | PolicyHub.Core → RatingEngine | RatingFactor, FactorTable, Discount | Pricing & Rating |
| Save quote | PolicyHub.Core → DataAccess | Policy, PolicyVersion, Cover, Premium | Policy Lifecycle |
| **Crosses**: 3 capability groups, 2 modules |

### Journey 2: Agent Processes a Claim

| Step | Module | Tables | Capability Group |
|---|---|---|---|
| Search policy | AgentPortal → DataAccess | Policy, Customer | Policy Lifecycle |
| Register FNOL | PolicyHub.Core | Claim | Claims Management |
| Set initial reserve | PolicyHub.Core | ClaimReserve | Claims Management |
| Generate acknowledgement letter | DocumentService | Claim, Customer, Policy | Document Production |
| **Crosses**: 3 capability groups, 3 modules |

### Journey 3: Nightly Renewal Batch

| Step | Module | Tables | Capability Group |
|---|---|---|---|
| Find eligible policies | RenewalService → DataAccess | Policy, PolicyVersion | Renewals |
| Calculate renewal premium | RenewalService → spCalculatePremium (SP) | RatingFactor, FactorTable | Pricing & Rating |
| Create renewal invitation | RenewalService → DataAccess | RenewalInvitation, PolicyVersion | Renewals + Policy Lifecycle |
| Generate renewal letter | DocumentService | Policy, Customer, Premium | Document Production |
| **Crosses**: 3 capability groups, 2 modules, **and the SP boundary** |

---

## Bounded Context Proposals

### BC1: Policy Administration

| Attribute | Detail |
|---|---|
| **Responsibility** | Manages the full policy lifecycle from quote creation through binding, mid-term adjustments, cancellation, and lapse. Owns the authoritative state of every policy. |
| **Owned modules** | `PolicyHub.Core/PolicyService.cs`, `PolicyHub.Core/PolicyValidator.cs`, `PolicyHub.Core/UnderwritingRules.cs` |
| **Owned tables** | `Policy`, `PolicyVersion`, `Cover`, `AuditTrail` |
| **Depends on** | Pricing (premium calculation), Customer (customer data), Documents (certificate generation) |
| **Autonomy** | 3/5 — high coupling to Pricing and Customer data |
| **Confidence** | High — clear domain boundary, well-defined in code |

### BC2: Pricing Engine

| Attribute | Detail |
|---|---|
| **Responsibility** | Calculates premiums using rating factors, loadings, discounts, and NCD rules. Stateless — given a risk, returns a price. |
| **Owned modules** | `RatingEngine/`, `PolicyHub.Core/PremiumCalculator.cs` |
| **Owned tables** | `RatingFactor`, `FactorTable`, `Discount`, `Loading`, `NCD` |
| **Depends on** | None (pure calculation from inputs) |
| **Autonomy** | 5/5 — fully stateless, no writes to shared tables |
| **Confidence** | High — cleanest boundary in the system, except for the SP duplication |

### BC3: Claims

| Attribute | Detail |
|---|---|
| **Responsibility** | Manages the claims lifecycle from FNOL through reserves, payments, and settlement. |
| **Owned modules** | `PolicyHub.Core/ClaimsHandler.cs`, `ClaimsImportService/` |
| **Owned tables** | `Claim`, `ClaimReserve`, `ClaimPayment`, `ClaimNote` |
| **Depends on** | Policy (reads policy data for validation), Customer (reads customer details), Documents (claims correspondence) |
| **Autonomy** | 4/5 — reads from Policy but doesn't write to it |
| **Confidence** | High — claims is a well-understood subdomain with clear ownership |

### BC4: Payments & Billing

| Attribute | Detail |
|---|---|
| **Responsibility** | Manages payment collection, instalment plans, direct debits, and refunds. |
| **Owned modules** | `PaymentGateway/`, `PolicyHub.Core/PaymentProcessor.cs` |
| **Owned tables** | `PaymentPlan`, `Instalment`, `PaymentTransaction` |
| **Depends on** | Policy (reads premium amounts), External (WorldPay, BACS) |
| **Autonomy** | 4/5 — clean separation, external integration is well-encapsulated |
| **Confidence** | Medium — WorldPay integration details need deeper analysis |

### BC5: Document Production

| Attribute | Detail |
|---|---|
| **Responsibility** | Generates all customer-facing documents — certificates, endorsements, letters, claims correspondence. |
| **Owned modules** | `DocumentService/`, `PolicyHub.Core/DocumentGenerator.cs` |
| **Owned tables** | `Document` |
| **Depends on** | Policy, Claims, Customer (reads data to merge into templates) |
| **Autonomy** | 4/5 — pure consumer of other contexts' data |
| **Confidence** | Medium — Word Interop dependency is a migration risk |

---

## Candidate Seams — Ranked by Feasibility

| Rank | Seam | Between Contexts | Shared-Write Tables | Feasibility | Rationale |
|---|---|---|---|---|---|
| 1 | **Pricing extraction** | Policy Admin ↔ Pricing Engine | None | ✅ High | Pricing is stateless, no shared writes, already a separate WCF service. Wrap in REST API. |
| 2 | **Claims separation** | Policy Admin ↔ Claims | None (reads only) | ✅ High | Claims reads Policy but never writes to it. Event-based notification for policy changes. |
| 3 | **Payments extraction** | Policy Admin ↔ Payments | None | ✅ High | Clean boundary, external integrations already encapsulated. |
| 4 | **Document production** | All ↔ Documents | None | ⚠️ Medium | Clean data ownership, but Word Interop needs replacing. Combine with template modernisation. |
| 5 | **Renewals separation** | Policy Admin ↔ Renewals | Policy, PolicyVersion ⚠️ | ⚠️ Medium | Shared write to Policy/PolicyVersion. Need to resolve: does Renewals create a new policy or extend existing? |
| 6 | **Broker distribution** | Policy Admin ↔ Broker | None | ⚠️ Medium | Clean boundary but requires async messaging for format translation. |

**Recommended first seam**: **Pricing Engine** — highest autonomy (5/5), zero shared writes, already physically separated as a WCF service, and the stateless nature means it can be extracted with minimal risk.
