# ADR-001: Entity Framework 6 Code First with a Per-Application Context over a Shared Database

**Status**: Observed (reconstructed from code — no original ADR exists)

---

## Context

The estate needs relational persistence for three entities: `CatalogItem`, `CatalogBrand` and
`CatalogType`. Four applications need that data.

The approach chosen was Entity Framework 6 Code First, with the C# model as the source of truth and
the database created on first run by an initializer. `eShopLegacyMVC/packages.config` pins
`EntityFramework 6.2.0`; `eShopWCFService/packages.config` pins `EntityFramework 6.1.3`.

Crucially, the context was **not** factored into a shared assembly. Each application compiles its own.

## Decision

1. Use EF6 Code First with fluent configuration in `OnModelCreating`, not attributes and not EDMX.
2. Give each application its own `DbContext` class, compiled into that application's assembly.
3. Create and seed the database at runtime with a `CreateDatabaseIfNotExists<T>` initializer rather
   than with EF Migrations or a versioned SQL script.
4. Point `eShopLegacyMVC` and `eShopLegacyWebForms` at the **same physical database** while keeping
   their contexts separate.

## Evidence

| Evidence | Location |
|---|---|
| EF6 context, fluent mapping | `eShopLegacyMVCSolution/src/eShopLegacyMVC/Models/CatalogDBContext.cs` — `OnModelCreating` → `ConfigureCatalogItem`, `ConfigureCatalogBrand`, `ConfigureCatalogType` |
| A second, independently compiled context | `eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Models/CatalogDBContext.cs` |
| A third context, different entity set, different database | `eShopLegacyNTier/src/eShopWCFService/Models/EntityModel.cs` |
| A fourth context, EF **Core**, different database | `eShopLegacyMVCSolution/eShopPorted/Models/CatalogDBContext.cs` |
| Same connection string in two applications | `src/eShopLegacyMVC/Web.config` and `src/eShopLegacyWebForms/Web.config` — both `connectionStrings/CatalogDBContext` name `Microsoft.eShopOnContainers.Services.CatalogDb` on `(localdb)\MSSQLLocalDB` |
| Runtime create-and-seed | `src/eShopLegacyMVC/Models/Infrastructure/CatalogDBInitializer.cs` — `class CatalogDBInitializer : CreateDatabaseIfNotExists<CatalogDBContext>` |
| Initializer installed conditionally | `src/eShopLegacyMVC/Global.asax.cs::ConfigDataBase` — `Database.SetInitializer(new CatalogDBInitializer())`, called only when `UseMockData` is false |
| Initializer installed unconditionally, in a constructor | `src/eShopWCFService/Models/EntityModel.cs` — `Database.SetInitializer(new CatalogDBInitializer())` inside `EntityModel()` |
| Raw DDL executed during seeding | `CatalogDBInitializer.ExecuteScript` → `context.Database.ExecuteSqlCommand(script)` over `dbo.catalog_hilo.Sequence.sql`, `dbo.catalog_brand_hilo.Sequence.sql`, `dbo.catalog_type_hilo.Sequence.sql` |
| No EF Migrations in the EF6 projects | no `Migrations/` folder in `eShopLegacyMVC`, `eShopLegacyWebForms` or `eShopWCFService` |
| EF Core project *does* use migrations | `eShopPorted/Migrations/20201130044339_Initial.cs` |

## Consequences

### Negative

- **Schema ownership is undefined.** Two applications create and map the same tables through two
  separately compiled contexts. Whichever runs first against an empty database wins; the other
  silently assumes the schema matches its own model.
- **`CreateDatabaseIfNotExists` never detects drift.** Once the database exists the initializer is a
  no-op, so a model change in either application produces runtime mapping errors rather than a
  migration failure at deploy time.
- **There is no versioned schema artefact.** Nothing in the repository describes the production
  schema; it can only be recovered by running the code or by inspecting a live database.
- **The application identity requires DDL rights** in every environment, because seeding issues
  `CREATE SEQUENCE`.
- **Four models must be changed together.** Adding a column to `CatalogItem` means editing four
  entity classes and four context configurations across three solutions — and regenerating the
  WinForms SOAP proxy.
- **The two databases cannot be joined.** `eShopWCFService` stores `CatalogItemsStock.CatalogItemId`
  as a plain `int` with no foreign key, in database `eShopDatabase`, while the `Catalog` rows it
  refers to live in `Microsoft.eShopOnContainers.Services.CatalogDb`. Referential integrity between
  stock and product exists only by convention.

### Positive

- The C# model is unambiguous and self-documenting; the mapping rules are visible in one method per
  entity rather than in an EDMX designer file.
- First-run setup is genuinely zero-touch on a developer machine — no script to run, no database to
  create by hand.
- EF6 and LocalDB are both long-supported and widely understood on the .NET Framework.

## Implications for Change

- The live schema must be captured before anything else; it is currently an unknown
  ([Discovery-Report.md §12](../Discovery-Report.md#12-unknowns-register), unknown #5).
- Any move toward a single owning service requires deciding which of the two web applications owns
  `Microsoft.eShopOnContainers.Services.CatalogDb`.
- `CreateDatabaseIfNotExists` must be removed from any environment where a real database exists;
  in the WCF service this requires changing a constructor, not configuration.
- The `.sql` sequence scripts are a hidden deployment dependency: they are read from
  `AppDomain.CurrentDomain.BaseDirectory` at runtime and must be present next to the binaries.
