# Operations Runbook — eShop Legacy Estate

> Output of [02-documentation-playbook.md](../02-documentation-playbook.md) / `02-documentation` agent.
>
> **Scope note.** Everything below is derived from files in this repository. No deployed environment,
> deployment script, CI pipeline or operational procedure exists in the repository, so all
> environment-specific detail is marked ⚠️ **unknown** rather than guessed. See
> [Discovery-Report.md §12](Discovery-Report.md#12-unknowns-register).

---

## 1. Solution and Project Map

| Solution | Projects |
|---|---|
| `eShopLegacyMVCSolution/eShopLegacyMVC.sln` | `src/eShopLegacyMVC` (ASP.NET MVC 5), `eShopPorted` (ASP.NET Core 2.2 on net461), `eShopLegacy.Utilities` (class library) |
| `eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln` | `src/eShopLegacyWebForms` (ASP.NET WebForms) |
| `eShopLegacyNTier/eShopLegacyNTier.sln` | `src/eShopWinForms` (Windows Forms), `src/eShopWCFService` (WCF service) |

Note that `eShopLegacy.Utilities` is referenced from `eShopLegacyMVC` and `eShopPorted`, both inside
the same solution. The WebForms and N-Tier solutions share no code with it or with each other.

---

## 2. Prerequisites

| Requirement | Why | Evidence |
|---|---|---|
| Windows | `System.Web` hosting, WCF service hosting, Windows Forms | `Global.asax`, `.svc`, `eShopWinForms.csproj` |
| Visual Studio with the *ASP.NET and web development* and *.NET desktop development* workloads, or MSBuild + IIS Express | `.csproj` files use `Microsoft.WebApplication.targets` and `WebProjectProperties` | `eShopLegacyMVC.csproj` |
| .NET Framework 4.7.2 developer pack | `<TargetFrameworkVersion>` of the web projects | `eShopLegacyMVC.csproj`, `eShopLegacyWebForms.csproj` |
| .NET Framework 4.7 developer pack | WinForms client | `eShopWinForms.csproj` — `<TargetFrameworkVersion>v4.7</TargetFrameworkVersion>` |
| .NET Framework 4.6.1 developer pack | WCF service and `eShopPorted` | `eShopWCFService.csproj`, `eShopPorted.csproj` — `<TargetFramework>net461</TargetFramework>` |
| .NET Core SDK 2.2 (or an SDK able to build `Microsoft.NET.Sdk.Web` targeting `net461`) | `eShopPorted` | `eShopPorted.csproj` — `Microsoft.AspNetCore 2.2.0` |
| SQL Server LocalDB, instance `MSSQLLocalDB` | All three connection strings | see §4 |
| NuGet package restore, both `packages.config` and `PackageReference` styles | `eShopLegacyMVC` uses both at once | `packages.config` + `<PackageReference>` in `eShopLegacyMVC.csproj` |

⚠️ **Unknown**: the exact Visual Studio or MSBuild version the estate was last built with. No
`global.json`, no `.vsconfig`, no build script and no CI definition exists.

---

## 3. Build and Run

### 3.1 Build

There is **no build script in the repository** — no `build.ps1`, no `Makefile`, no
`.github/workflows/`, no `azure-pipelines.yml`, no `Jenkinsfile`. Each solution is built
individually.

```powershell
# from the repository root
nuget restore .\eShopLegacyMVCSolution\eShopLegacyMVC.sln
msbuild .\eShopLegacyMVCSolution\eShopLegacyMVC.sln /p:Configuration=Debug

nuget restore .\eShopLegacyWebFormsSolution\eShopLegacyWebForms.sln
msbuild .\eShopLegacyWebFormsSolution\eShopLegacyWebForms.sln /p:Configuration=Debug

nuget restore .\eShopLegacyNTier\eShopLegacyNTier.sln
msbuild .\eShopLegacyNTier\eShopLegacyNTier.sln /p:Configuration=Debug
```

⚠️ **Unknown**: whether the solutions currently build. This was **not** verified during discovery —
no MSBuild run was performed. `eShopLegacyMVC` in particular mixes `packages.config` and
`PackageReference` for the same packages and binding-redirects Autofac 4 assemblies onto Autofac 6
(see [ADR-002](ADR/ADR-002-autofac-assembly-scanning-di.md)), which is a plausible source of restore
or load failures.

### 3.2 Start / stop

| Application | How it starts | Default local address | Stop |
|---|---|---|---|
| `eShopLegacyMVC` | F5 in Visual Studio (IIS Express) | `http://localhost:52429/` (`<IISUrl>` in `eShopLegacyMVC.csproj`) | Stop debugging / exit IIS Express |
| `eShopLegacyWebForms` | F5 in Visual Studio (IIS Express) | `http://localhost:50586/` (`<IISUrl>`) | as above |
| `eShopWCFService` | F5 in Visual Studio (IIS Express) | `http://localhost:62314/CatalogService.svc` (`<IISUrl>`) | as above |
| `eShopWinForms` | Run `eShopWinForms.exe` | n/a — desktop window | Close the window |
| `eShopPorted` | `dotnet run` or F5 | Kestrel `https://localhost:5001` / `http://localhost:5000`, IIS Express `http://localhost:52637` (ssl `44337`) — `Properties/launchSettings.json` | Ctrl+C / stop debugging |

**Start order matters for the N-Tier solution.** `eShopWCFService` must be listening on
`http://localhost:62314/CatalogService.svc` *before* `eShopWinForms.exe` starts. The client issues six
SOAP calls from `CatalogController.LoadView()`, which `Program.Main` invokes **before**
`view.ShowDialog()` and without a `try`/`catch` — so if the service is down the user sees an
unhandled-exception dialog and no application window.

⚠️ **Unknown**: how any of these are started in a real environment — as IIS sites, as a Windows
service, by ClickOnce, or otherwise. No publish profile, installer or deployment script exists.

---

## 4. Database

| Database | Used by | Connection string location |
|---|---|---|
| `Microsoft.eShopOnContainers.Services.CatalogDb` | `eShopLegacyMVC` **and** `eShopLegacyWebForms` | `src/eShopLegacyMVC/Web.config` and `src/eShopLegacyWebForms/Web.config`, `connectionStrings` entry named `CatalogDBContext` |
| `eShopDatabase` | `eShopWCFService` | `src/eShopWCFService/Web.config`, entry named `EntityModel` |
| `eShopPorted` | `eShopPorted` | `eShopPorted/appsettings.json`, `ConnectionStrings:DefaultConnection` |

All three use `Data Source=(localdb)\MSSQLLocalDB` with `Integrated Security=True`.

### 4.1 First-run creation

There is **no schema script to run by hand** and no `dotnet ef database update` step for the EF6
projects. The database is created on first use:

- **MVC / WebForms**: `CatalogDBInitializer : CreateDatabaseIfNotExists<CatalogDBContext>` is
  installed in `Global.asax.cs::ConfigDataBase`, but **only when `UseMockData` is `false`**.
- **WCF**: `EntityModel`'s constructor calls `Database.SetInitializer(new CatalogDBInitializer())`
  unconditionally.
- **eShopPorted**: has a migration (`Migrations/20201130044339_Initial.cs`) with seed data supplied
  through `HasData`, but **no `Migrate()` or `EnsureCreated()` call exists at startup**. The
  migration must be applied manually.

Seeding requires:

1. The three `dbo.*.Sequence.sql` files to be present next to the compiled assembly — they are read
   from `AppDomain.CurrentDomain.BaseDirectory` by `CatalogDBInitializer.ExecuteScript`.
2. A login with **DDL rights**, because those scripts issue `CREATE SEQUENCE`.
3. If `UseCustomizationData` is `true`, `Setup/CatalogBrands.csv`, `Setup/CatalogTypes.csv`,
   `Setup/CatalogItems.csv` and `Setup/CatalogItems.zip` under the web root.

`dbo.catalog_hilo.Sequence.sql` begins `USE [Microsoft.eShopOnContainers.Services.CatalogDb]`, so the
DDL names its target database literally rather than following the connection string.

### 4.2 Resetting local data

Because the initializer is `CreateDatabaseIfNotExists`, re-seeding requires dropping the database:

```powershell
sqlcmd -S "(localdb)\MSSQLLocalDB" -Q "DROP DATABASE [Microsoft.eShopOnContainers.Services.CatalogDb]"
```

Then start the application with `UseMockData=false`.

⚠️ **Unknown**: backup, restore and retention arrangements for any non-local database.

---

## 5. Configuration Reference

| Setting | File(s) | Shipped value | Effect |
|---|---|---|---|
| `UseMockData` | `src/eShopLegacyMVC/Web.config` | `false` | Real `CatalogService` + EF initializer |
| `UseMockData` | `src/eShopLegacyWebForms/Web.config` | **`true`** | `CatalogServiceMock`; the database is never touched |
| `UseMockData` | `eShopPorted/appsettings.json` | **`"true"`** | `AddDbContext` is never called |
| `UseCustomizationData` | `src/eShopLegacyMVC/Web.config`, `src/eShopLegacyWebForms/Web.config` | `false` | Seed from `PreconfiguredData` rather than `Setup/*.csv`; **and** leave `~/Pics` alone |
| `UseCustomizationData` | `eShopPorted/appsettings.json` | `"true"` | **Read by no code in that project** |
| WCF endpoint address | `src/eShopWinForms/App.config` | `http://localhost:62314/CatalogService.svc` | Where the desktop client connects |
| `ConnectionString` environment variable | read by `src/eShopWCFService/Models/Infrastructure/CatalogConfiguration.cs` | not set | Overrides `name=EntityModel` when present — the only environment-based override in the estate |
| Logging | `log4Net.xml` in MVC and WebForms | `logFiles\myapp.log`, `RollingFileAppender` | Relative to the **process working directory**, not the application root |

### ⚠️ Destructive setting

Setting `UseCustomizationData=true` in `eShopLegacyMVC` or `eShopLegacyWebForms` causes
`CatalogDBInitializer.AddCatalogItemPictures()` to **delete every file in the application's `Pics`
directory** before extracting `Setup/CatalogItems.zip` over it. This runs only during first-run
seeding, and only when `UseMockData` is also `false`, but the setting's name gives no indication that
it removes files.

### Framework-version notes

`src/eShopLegacyMVC/Web.config` and `src/eShopLegacyWebForms/Web.config` both declare
`<compilation targetFramework="4.7.2">` alongside `<httpRuntime targetFramework="4.6.1">`. The
`httpRuntime` value governs ASP.NET quirks behaviour, so both applications run under 4.6.1 semantics.
The WebForms file additionally sets `requestValidationMode="2.0"`.

`compilation debug="true"` is committed in the MVC, WebForms and WCF `Web.config` files.
`Web.Release.config` removes it on a Release publish, and changes nothing else — in particular it
does **not** repoint any connection string.

---

## 6. Testing

**There is no test project anywhere in this repository.** No `*.Tests.csproj`, no xUnit, NUnit or
MSTest package reference, no `[TestMethod]`, `[Fact]` or `[Test]` attribute, and no test runner
configuration.

There is therefore no `test` command to document and no regression safety net. Establishing one is
the subject of stage 05 of the accelerator, not of this runbook.

---

## 7. CI/CD, Containers and Infrastructure

| Artefact | Present? |
|---|---|
| `.github/workflows/` | ❌ none |
| `azure-pipelines.yml` | ❌ none |
| `Jenkinsfile` | ❌ none |
| `Dockerfile` / `docker-compose.yml` | ❌ none |
| Publish profiles (`*.pubxml`) | ❌ none |
| Infrastructure as code (ARM/Bicep/Terraform) | ❌ none |
| Installer / ClickOnce manifest | ❌ none |

Build, deployment and release are entirely manual and entirely undocumented. This is the single
largest operational gap in the estate.

---

## 8. Monitoring and Alerting

| Signal | Status |
|---|---|
| Application logs | log4net → `logFiles\myapp.log` in `eShopLegacyMVC` and `eShopLegacyWebForms` only. Controllers log at `Info` on action entry. |
| Logs — WCF service | ⚠️ **none**. No log4net, no `System.Diagnostics` tracing configured, no WCF message logging. |
| Logs — WinForms client | ⚠️ **none**. |
| Application Insights | ⚠️ **configured but inert**. The HTTP modules are registered in the MVC and WebForms `Web.config`, but `ApplicationInsights.config` contains no `<InstrumentationKey>`, so no telemetry is sent. |
| Health endpoint | ⚠️ **none** in any application. |
| Metrics / dashboards | ⚠️ **unknown** — nothing in the repository. |
| Alerting | ⚠️ **unknown** — nothing in the repository. |

### ⚠️ The correlation ID in the log layout never prints

`log4Net.xml` in **both** web projects uses the conversion pattern

```
%date [%thread] %property{activity} %level %logger - %property{requestinfo}%newline%message%newline%newline
```

while `Global.asax.cs::Application_BeginRequest` in both projects sets
`LogicalThreadContext.Properties["activityid"]` and `LogicalThreadContext.Properties["requestinfo"]`.

`requestinfo` matches and prints. `activity` does not match `activityid`, so the correlation
identifier is an empty field on every line that has ever been written. **Log lines cannot currently
be correlated to a request.** The `ActivityIdHelper` class exists, runs, and its output is discarded.

Additionally, `Properties/AssemblyInfo.cs` in both projects declares
`[assembly: log4net.Config.XmlConfigurator(ConfigFile = "log4net.xml")]` while the file on disk is
`log4Net.xml` — a capital `N`. This works on Windows and would silently disable all logging on a
case-sensitive filesystem.

---

## 9. Known Issues and Operational Limitations

| # | Issue | Impact | Evidence |
|---|---|---|---|
| 1 | No authentication or authorisation anywhere | Every endpoint, including `Create`, `Edit` and `Delete`, is anonymous | no `[Authorize]`, no `<authentication>` element, no OWIN/Identity package in any project |
| 2 | WCF endpoint has no transport security | Catalog data and all writes travel in clear text; service metadata is published (`httpGetEnabled="true"`) | `src/eShopWCFService/Web.config` |
| 3 | `directoryBrowse enabled="true"` on the WCF service | Directory listing exposed | `src/eShopWCFService/Web.config` — directly beneath a comment advising it be disabled |
| 4 | `BinaryFormatter` payload served over HTTP | `GET /api/files` returns a `BinaryFormatter` stream; the type is documented as insecure, obsoleted in .NET 5+ and removed in .NET 9 | `eShopLegacy.Utilities/Serializing.cs`, `Controllers/WebApi/FilesController.cs::Get` |
| 5 | `DELETE /api/brands/{id}` silently succeeds without deleting | A caller believes a brand was removed | `Controllers/WebApi/BrandsController.cs::Delete` — `// demo only - don't actually delete` |
| 6 | Catalog listing issues one extra query per image | A 10-item page costs 12 database round trips | `Controllers/PicController.cs::Index` calls `FindCatalogItem` before `File.ReadAllBytes` |
| 7 | WCF service filters in memory | `GetDiscount`, `GetCatalogItems`, `GetAvailableStock` and `CreateAvailableStock` call `.ToList()` before `.Where()` | `CatalogService.svc.cs` |
| 8 | WCF `CreateCatalogItem` uses `Max(Id) + 1` with no lock or transaction | Concurrent creates collide on the primary key | `CatalogService.svc.cs::CreateCatalogItem` |
| 9 | WinForms client fails before showing a window | Service outage produces an unhandled exception, not an error message | `Program.cs::Main` calls `LoadView()` before `ShowDialog()` |
| 10 | Duplicate calls in client startup | `GetCatalogItems` and `GetDiscount` are each issued twice with identical arguments | `eShopWinForms/Controllers/CatalogController.cs::LoadView` |
| 11 | Session state is `InProc` | Rules out multi-instance hosting without change | `<sessionState mode="InProc">` in both web `Web.config` files |
| 12 | Two applications share one database through two separately compiled contexts | A model change in one is a silent assumption break in the other | both `Models/CatalogDBContext.cs` |
| 13 | WebForms create page parses input with `decimal.Parse` / `int.Parse` | Malformed input produces an unhandled `FormatException` | `Catalog/Create.aspx.cs::CreateProduct_Click` |
| 14 | `PaginatedItemsViewModel` divides by `pageSize` | `?pageSize=0` reaches the division | `ViewModel/PaginatedItemsViewModel.cs` |
| 15 | `eShopPorted` error path points at a controller that does not exist | `UseExceptionHandler("/Home/Error")` with no `HomeController` in the project | `eShopPorted/Startup.cs`, `eShopPorted/Controllers/` |
| 16 | Dead code that reads as live code | `src/eShopWCFService/CatalogServiceClient.cs` and `src/eShopWinForms/Helpers/` (7 UWP files) are not in their projects' compile lists and could not compile | see [LLD §8](LLD.md#8-code-that-does-not-do-what-it-appears-to) |

---

## 10. Escalation

⚠️ **Unknown.** No `CODEOWNERS`, no `SUPPORT.md`, no on-call rota, no contact list and no issue
template exists in the repository. Ownership of each of the six projects is unidentified — recorded
as an open item in [Discovery-Report.md §12](Discovery-Report.md#12-unknowns-register).
