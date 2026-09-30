# ADR-003: Mock vs Real Data Selected by a Configuration Flag at Container-Build Time

**Status**: Observed (reconstructed from code — no original ADR exists)

---

## Context

The applications need to run without a database — for demos, for UI work, and for first-run
experience on a machine with no LocalDB instance.

Rather than introduce a build configuration, a feature-flag service or a separate test host, the
estate reads a boolean from configuration during application startup and registers a different
`ICatalogService` implementation.

A second, separate flag — `UseCustomizationData` — switches the *seed* data source when the real
implementation is in use.

## Decision

1. Read `UseMockData` from `appSettings` in `Application_Start`, before the container is built.
2. Pass it into `ApplicationModule` and branch the `ICatalogService` registration on it.
3. When mocking, also **skip installing the EF database initializer entirely**.
4. Use a second flag, `UseCustomizationData`, to select between compiled-in seed data and CSV/zip
   files on disk.

## Evidence

```
// src/eShopLegacyMVC/Modules/ApplicationModule.cs
if (this.useMockData)
{
    builder.RegisterType<CatalogServiceMock>().As<ICatalogService>().SingleInstance();
}
else
{
    builder.RegisterType<CatalogService>().As<ICatalogService>().InstancePerLifetimeScope();
}
```

| Evidence | Location |
|---|---|
| Flag read before container build | `src/eShopLegacyMVC/Global.asax.cs::RegisterContainer` — `var mockData = bool.Parse(ConfigurationManager.AppSettings["UseMockData"]);` |
| Initializer skipped when mocking | `src/eShopLegacyMVC/Global.asax.cs::ConfigDataBase` and `src/eShopLegacyWebForms/Global.asax.cs::ConfigDataBase` — both guard with `if (!mockData)` |
| Identical module in the WebForms project | `src/eShopLegacyWebForms/Modules/ApplicationModule.cs` — same five registrations, same branch |
| Ported project skips `AddDbContext` when mocking | `eShopPorted/Startup.cs::ConfigureServices` — the EF Core context is only registered on the real branch |
| Seed-source flag | `src/eShopLegacyMVC/Models/Infrastructure/CatalogDBInitializer.cs` — read in the constructor as `bool.Parse(ConfigurationManager.AppSettings["UseCustomizationData"])`, then branched on in `AddCatalogTypes`, `AddCatalogBrands` and `AddCatalogItems` |
| Picture side effect of the seed flag | `CatalogDBInitializer::AddCatalogItemPictures` — called unconditionally from `Seed`, guarded internally by `if (!useCustomizationData) return;` |

### The defaults are not the same across applications

| Application | Setting | Shipped value | Effect |
|---|---|---|---|
| `eShopLegacyMVC` | `Web.config` → `UseMockData` | `false` | Uses the database |
| `eShopLegacyWebForms` | `Web.config` → `UseMockData` | **`true`** | **Never touches the database as shipped** |
| `eShopPorted` | `appsettings.json` → `UseMockData` | **`"true"`** | `AddDbContext` is never called |
| `eShopLegacyMVC` | `Web.config` → `UseCustomizationData` | `false` | Seeds from `PreconfiguredData` |
| `eShopPorted` | `appsettings.json` → `UseCustomizationData` | `"true"` | **Read by no code in that project** |

### The two seed sources are not equivalent

| Source | Types | Brands | Items |
|---|---|---|---|
| `Models/Infrastructure/PreconfiguredData.cs` | 4 | 5 | 12 |
| `Setup/CatalogTypes.csv`, `CatalogBrands.csv`, `CatalogItems.csv` (data rows, excluding header) | 6 | 7 | 13 |

### The seed flag deletes files

```
// CatalogDBInitializer.AddCatalogItemPictures()
DirectoryInfo picturePath = new DirectoryInfo(picturesFolderPath);
foreach (FileInfo file in picturePath.GetFiles()) { file.Delete(); }
ZipFile.ExtractToDirectory(zipFileCatalogItemPictures, picturesFolderPath);
```

Setting `UseCustomizationData=true` empties the `~/Pics` directory before extracting
`Setup/CatalogItems.zip` over it.

## Consequences

### Negative

- **The flag changes object lifetime, not just implementation.** The mock is `SingleInstance()`; the
  real service is `InstancePerLifetimeScope()`. A mock-mode run therefore has entirely different
  concurrency behaviour: `CatalogServiceMock` holds one mutable `List<CatalogItem>` shared by every
  user of the process, so one user's create is visible to all, and all mutations vanish on the next
  application-pool recycle.
- **A production misconfiguration is silent.** `UseMockData=true` in a real environment produces a
  working site serving 12 hard-coded products with no error, no warning and no log entry.
- **The shipped WebForms and Ported applications do not exercise their own data layer.** Both default
  to `true`, so the `CatalogDBContext` code paths in those projects are unexercised by simply running
  them.
- **A configuration boolean performs a destructive filesystem operation.** `UseCustomizationData=true`
  deletes the contents of `~/Pics`. This is not discoverable from the setting's name.
- **The two flags interact.** `UseCustomizationData` only has any effect when `UseMockData` is false,
  because the initializer is not installed otherwise.
- **`bool.Parse` is unguarded.** A typo such as `UseMockData="True "` or a missing key throws during
  `Application_Start`, taking the whole application down at startup rather than degrading.

### Positive

- The application genuinely runs with no database and no setup. That is a real benefit for a demo
  estate and for onboarding.
- The seam is a clean one — `ICatalogService` — rather than conditional compilation or `#if` blocks
  scattered through the code.
- The decision is centralised in one file per application.

## Implications for Change

- Any environment promotion process must assert `UseMockData=false`; nothing in the code does so.
- `UseCustomizationData` should be renamed or documented before anyone runs it against a directory
  they care about.
- `eShopPorted`'s `UseCustomizationData` key is dead and should be removed or implemented — the
  project has a `wwwroot/Pics` folder but no `Setup/` folder for the flag to reference.
- Because the mock and real implementations have different lifetimes, any testing built on the mock
  will not reproduce the real implementation's per-request semantics.
