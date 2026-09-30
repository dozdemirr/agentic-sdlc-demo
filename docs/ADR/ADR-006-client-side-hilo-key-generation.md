# ADR-006: Client-Side HiLo Key Generation in a Singleton

**Status**: Observed (reconstructed from code — no original ADR exists)

---

## Context

`CatalogItem.Id` needed values. The default choice — a SQL Server `IDENTITY` column with EF filling
the key after insert — was explicitly rejected in the MVC and WebForms projects.

Instead, the application allocates keys itself from a SQL `SEQUENCE`, in blocks, caching the block in
process memory. This is the classic HiLo pattern: fewer database round trips at the cost of holding
allocation state outside the database.

## Decision

1. Tell EF not to generate keys:
   `.Property(ci => ci.Id).HasDatabaseGeneratedOption(DatabaseGeneratedOption.None)`.
2. Create SQL sequences during database seeding via raw DDL.
3. Allocate ids in blocks of 10 from `catalog_hilo`, caching the block in a class that Autofac
   registers as `.SingleInstance()`.
4. Call the generator from `CatalogService.CreateCatalogItem` before `db.CatalogItems.Add(...)`.

## Evidence

| Evidence | Location |
|---|---|
| EF told not to generate keys | `src/eShopLegacyMVC/Models/CatalogDBContext.cs::ConfigureCatalogItem` — `HasDatabaseGeneratedOption(DatabaseGeneratedOption.None)` |
| The generator | `src/eShopLegacyMVC/Models/CatalogItemHiLoGenerator.cs` — 34 lines; `private const int HiLoIncrement = 10;`, mutable fields `sequenceId` and `remainningLoIds`, all access inside `lock (sequenceLock)` |
| Sequence query | same file — `SELECT NEXT VALUE FOR catalog_hilo` |
| Singleton registration | `src/eShopLegacyMVC/Modules/ApplicationModule.cs` — `builder.RegisterType<CatalogItemHiLoGenerator>().SingleInstance();` |
| Same registration in WebForms | `src/eShopLegacyWebForms/Modules/ApplicationModule.cs` |
| Call site | `src/eShopLegacyMVC/Services/CatalogService.cs::CreateCatalogItem` |
| Sequences created by raw DDL | `src/eShopLegacyMVC/Models/Infrastructure/CatalogDBInitializer.cs::ExecuteScript` over `dbo.catalog_hilo.Sequence.sql`, `dbo.catalog_brand_hilo.Sequence.sql`, `dbo.catalog_type_hilo.Sequence.sql` |

### Two applications, two generators, one sequence

`eShopLegacyMVC` and `eShopLegacyWebForms` point at the same database
(`Microsoft.eShopOnContainers.Services.CatalogDb`) and each register their own singleton
`CatalogItemHiLoGenerator`. `Models/Infrastructure/dbo.catalog_hilo.Sequence.sql` declares
`CREATE SEQUENCE [dbo].[catalog_hilo] AS [bigint] START WITH 1 INCREMENT BY 10`, and the generator's
`HiLoIncrement` is also 10 — so the two match and the blocks handed to each process are disjoint.
Correctness under multiple processes is enforced by SQL Server, not by the application.

That script begins `USE [Microsoft.eShopOnContainers.Services.CatalogDb]`, naming its target database
literally rather than relying on the connection it is executed over.

### The constant is misnamed

`CatalogDBInitializer` declares `private const string DBCatalogSequenceName = "catalog_type_hilo";`
and passes it to `GetSequenceIdFromSelectedDBSequence` from `AddCatalogTypes`. The name says
"Catalog"; the value and the use site are both about *types*. `DBBrandSequenceName` alongside it is
named consistently. All three sequences — `catalog_hilo`, `catalog_brand_hilo` and
`catalog_type_hilo` — are created and read, but only `catalog_hilo` is read outside the seeder.

### Seeding and serving share one generator instance

`CatalogDBInitializer` takes `CatalogItemHiLoGenerator` as a constructor parameter and calls
`indexGenerator.GetNextSequenceValue(context)` in `AddCatalogItems`. Because both the initializer and
the generator are resolved from the same container, the seeder consumes ids from the same cached
block the application will later serve from.

### Four projects, four different key strategies

| Project | Strategy | Evidence |
|---|---|---|
| `eShopLegacyMVC`, `eShopLegacyWebForms` | Client-side HiLo, block of 10, singleton cache | `Models/CatalogItemHiLoGenerator.cs` |
| `eShopWCFService` | `_context.CatalogItems.Max(i => i.Id); ++maxId;` — no lock, no transaction | `CatalogService.svc.cs::CreateCatalogItem` |
| `eShopPorted` | Database-generated (the `DatabaseGeneratedOption.None` call is absent) | `eShopPorted/Models/Config/CatalogItemConfig.cs` |
| `CatalogServiceMock` | `catalogItems.Max(c => c.Id) + 1` over an in-memory list | `Services/CatalogServiceMock.cs::CreateCatalogItem` |

## Consequences

### Negative

- **Single-process hosting is a deployment assumption, not a correctness requirement.** The sequence
  is declared `INCREMENT BY 10` to match `HiLoIncrement`, so a second worker process receives a
  disjoint block. What the in-process cache does cost is visibility: no process can see another's
  outstanding reservations, and the reservation is lost if the process dies.
- **Identifier gaps are permanent and unpredictable.** A recycle mid-block discards up to nine
  reserved ids. `Catalog.Id` is therefore non-contiguous, which rules it out as an audit or ordering
  key.
- **The generator and the sequence must be changed together.** `HiLoIncrement = 10` in C# and
  `INCREMENT BY 10` in `dbo.catalog_hilo.Sequence.sql` are two halves of one contract, in two
  languages, in two files, with nothing linking them. Changing either alone produces either
  duplicate-key failures or silent gaps.
- **The WCF service's `Max(Id) + 1` has no such protection.** No lock, no transaction, no retry — two
  concurrent creates produce the same id and one insert fails on the primary key. It is also a
  full-table scan per insert.
- **The estate has no single answer to "how is an id assigned".** Four strategies means any data
  consolidation must reconcile four id spaces.
- **A migration cannot simply switch the column to `IDENTITY`.** Existing rows were inserted with
  explicit keys, and the sequence's current value must be carried over or the two will collide.

### Positive

- The database is touched for a key only once per ten inserts.
- The entity has its identity **before** `SaveChanges`, so the application can build object graphs
  and return the id without a round trip — the actual reason HiLo is used.
- Key allocation is isolated in one 34-line class with a single public method, correctly guarded by
  a `lock`, which makes it straightforward to replace.

## Implications for Change

- `CatalogItemHiLoGenerator` is small and well-isolated; replacing it is a contained change. The hard
  part is the data, not the code.
- The `catalog_brand_hilo` and `catalog_type_hilo` sequences are only consumed by the seeder; whether
  they are still needed should be confirmed against the live database.
- `dbo.catalog_hilo.Sequence.sql` hard-codes the database name in a `USE` statement, so it cannot be
  reused against a differently named database without editing.
- Before any change, the current value of `catalog_hilo` and the maximum `Catalog.Id` in each
  database must be captured. Neither is knowable from the repository.
- The missing `lock` is a genuine defect under concurrency, but no evidence was found of it having
  been hit. Whether the applications have ever run under concurrent load is unknown
  ([Discovery-Report.md §12](../Discovery-Report.md#12-unknowns-register)).
