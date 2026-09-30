# ADR-001: Stored Procedure Duplication of Rating Logic

> Output of [02-documentation-playbook.md](../../../02-documentation-playbook.md) — Architecture Decision Record.

---

## Status

**Observed** — this pattern exists in the codebase but was not formally documented.

## Context

The premium rating logic exists in two places:

1. **C# — `PremiumCalculator.cs`** (890 LOC) — used by the Customer Portal, Agent Portal, and Rating Engine WCF service for real-time quote calculations.
2. **SQL — `spCalculatePremium`** (620 lines) — used by the Renewal Service Windows Service for batch overnight renewal pricing.

Based on commit history, the stored procedure was introduced in 2014 (`commit 3a7f2d1`, author: D. Thompson) with the message *"SP for batch renewals — faster than calling WCF per policy"*.

## Decision

Premium calculation was duplicated into a stored procedure to avoid the overhead of calling the WCF Rating Engine service for each of the ~2,000 nightly renewal calculations.

## Evidence

- `Database/StoredProcedures/spCalculatePremium.sql` — 620 lines, last modified 2023-01-14
- `PolicyHub.Core/PremiumCalculator.cs` — 890 lines, last modified 2024-02-28
- `RenewalService/RenewalEngine.cs:142` — calls `EXEC spCalculatePremium @PolicyId, @EffectiveDate`
- `RatingEngine/RatingService.cs:67` — calls `PremiumCalculator.Calculate(risk)`

## Consequences

### Negative
- **Drift risk**: The C# version has received 14 commits since the SP was last updated. Three rating factors (`YoungDriverSurcharge`, `FloodRiskLoading`, `EVDiscount`) exist only in C# — renewal premiums may differ from new-business premiums.
- **Testing gap**: The stored procedure has no automated tests. The C# calculator has 12 unit tests.
- **Knowledge cost**: Developers must maintain two implementations in different languages.

### Positive
- Batch renewal processing completes in ~8 minutes vs estimated ~45 minutes via WCF calls.

## Implications for Change

During modernisation, this duplication **must** be resolved. Options:
1. **Eliminate the SP** — call the rating service from the renewal batch (requires the service to be performant enough)
2. **Keep one authoritative source** — if SP is retained, it must be auto-generated from the C# logic or replaced with a shared calculation engine
3. **Validate parity first** — before any migration, run both calculators against the same 1,000 policies and compare outputs to quantify the current drift

---

# ADR-002: Mixed ORM Strategy (Entity Framework + Dapper)

## Status

**Observed**

## Context

The data access layer uses two ORM approaches:
- **Entity Framework 6** — used for CRUD operations on policy, claims, and customer entities (change tracking, lazy loading)
- **Dapper** — used for read-heavy queries, reporting, and the rating engine factor table lookups

## Decision

Dapper was introduced incrementally (first appearing in `commit 8b2e4fa`, 2017) to address EF6 performance problems with complex read queries, particularly in the rating engine where factor table lookups were generating N+1 queries.

## Evidence

- `PolicyHub.DataAccess/Contexts/PolicyContext.cs` — EF6 context with 28 DbSet properties
- `PolicyHub.DataAccess/Repositories/FactorTableRepository.cs` — Dapper with raw SQL
- `PolicyHub.DataAccess/Repositories/ReportRepository.cs` — Dapper for all report queries
- `PolicyHub.DataAccess/Repositories/PolicyRepository.cs` — **mixed** — EF for writes, Dapper for complex reads

## Consequences

- **Positive**: Performance-critical paths use appropriate tooling
- **Negative**: `PolicyRepository.cs` mixes both approaches — developers must understand two patterns in one class
- **Migration note**: Both EF6 and Dapper have .NET 8 equivalents (EF Core 8, Dapper stays the same), so this pattern can be preserved during migration
