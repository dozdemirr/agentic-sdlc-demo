# ADR-005: Web.config-Based Configuration with Connection Strings in Source Control

**Status**: Observed (reconstructed from code — no original ADR exists)

---

## Context

Every application in the estate needs a database connection string, a handful of behaviour switches
and logging configuration. The .NET Framework era default — `Web.config` / `App.config` read through
`System.Configuration.ConfigurationManager` — was adopted without modification.

## Decision

1. Store all configuration in `Web.config` (web projects) or `App.config` (WinForms), checked into
   source control with real values.
2. Read it through `ConfigurationManager.AppSettings` / `ConfigurationManager.ConnectionStrings`,
   at startup, in the composition root.
3. Use Visual Studio `Web.Release.config` XDT transforms for environment differences.
4. In the ported project, use `appsettings.json` + `IConfiguration` instead.

## Evidence

| Setting | Location | Committed value |
|---|---|---|
| `CatalogDBContext` connection string | `src/eShopLegacyMVC/Web.config` and `src/eShopLegacyWebForms/Web.config` | `Data Source=(localdb)\MSSQLLocalDB; Initial Catalog=Microsoft.eShopOnContainers.Services.CatalogDb; Integrated Security=True; MultipleActiveResultSets=True;` |
| `EntityModel` connection string | `src/eShopWCFService/Web.config` | `(localdb)\MSSQLLocalDB` / `eShopDatabase` |
| `DefaultConnection` | `eShopPorted/appsettings.json` | `(localdb)\MSSQLLocalDB` / `eShopPorted` |
| `UseMockData`, `UseCustomizationData` | all four applications | see [ADR-003](ADR-003-mock-data-configuration-flag.md) |
| WCF endpoint address | `src/eShopWinForms/App.config` | `http://localhost:62314/CatalogService.svc` |
| Reads happen at startup | `src/eShopLegacyMVC/Global.asax.cs::RegisterContainer`, `src/eShopLegacyWebForms/Global.asax.cs::ConfigureContainer` | `bool.Parse(ConfigurationManager.AppSettings["UseMockData"])` |
| The one environment override in the estate | `src/eShopWCFService/Models/Infrastructure/CatalogConfiguration.cs` | prefers the `ConnectionString` **environment variable**, falling back to `name=EntityModel` |
| Release transform | `src/eShopLegacyMVC/Web.Release.config` | only `<compilation xdt:Transform="RemoveAttributes(debug)" />` is active; the connection-string example is commented out |
| Telemetry config with no key | `ApplicationInsights.config` in MVC and WebForms | no `<InstrumentationKey>` element |

### Framework-version mismatches inside single files

| File | `<compilation targetFramework>` | `<httpRuntime targetFramework>` |
|---|---|---|
| `src/eShopLegacyMVC/Web.config` | `4.7.2` | `4.6.1` |
| `src/eShopLegacyWebForms/Web.config` | `4.7.2` | `4.6.1` |

`httpRuntime targetFramework` controls ASP.NET quirks-mode behaviour, so both web applications run
under 4.6.1 semantics despite compiling against 4.7.2. The WebForms file additionally sets
`requestValidationMode="2.0"`, which reverts request validation to the pre-4.0 behaviour and weakens
the built-in cross-site-scripting guard.

`compilation debug="true"` is committed in the MVC, WebForms and WCF `Web.config` files.

### A configuration filename that only works on Windows

`src/eShopLegacyMVC/Properties/AssemblyInfo.cs` line 37 declares
`[assembly: log4net.Config.XmlConfigurator(ConfigFile = "log4net.xml")]`, as does
`src/eShopLegacyWebForms/Properties/AssemblyInfo.cs` line 37.
The file on disk in both projects is `log4Net.xml` — capital `N`. This resolves on a
case-insensitive filesystem and fails silently, with no logging at all, on a case-sensitive one.

### A logging property that is set but never printed

`log4Net.xml` in **both** web projects uses the layout

```
%date [%thread] %property{activity} %level %logger - %property{requestinfo}%newline...
```

while `Global.asax.cs::Application_BeginRequest` in both projects sets
`LogicalThreadContext.Properties["activityid"]` and
`LogicalThreadContext.Properties["requestinfo"]`.

`requestinfo` matches and prints. `activity` does not match `activityid`, so the correlation
identifier renders as an empty field on every log line. The `ActivityIdHelper` class that generates
it is therefore invoked but its output never reaches the log file.

The log destination itself is the relative path `logFiles\myapp.log`, resolved against the process
working directory rather than the application root.

## Consequences

### Negative

- **Credentials would be in source control.** Today the connection strings use
  `Integrated Security=True` against LocalDB, so no password is exposed — but the pattern places the
  connection string in a committed file, and moving to SQL authentication would commit a password
  with no other change required.
- **No secret management exists.** There is no Key Vault reference, no DPAPI-encrypted section, no
  `aspnet_regiis -pe` usage, and no user-secrets file.
- **Release transforms do not repoint the database.** A Release publish of any web project removes
  `debug="true"` and changes nothing else, so it deploys pointing at `(localdb)\MSSQLLocalDB`.
- **Configuration is read once, at startup.** Changing `UseMockData` requires an application restart.
  The log4net `XmlConfigurator` attribute does not set `Watch = true`, so even the logging
  configuration is not reloaded on change.
- **Startup is brittle.** `bool.Parse` on a missing or malformed key throws during
  `Application_Start`.
- **Four different configuration mechanisms.** `Web.config` appSettings, `App.config` client
  endpoints, `appsettings.json`, and one environment variable in `CatalogConfiguration` — with no
  shared convention between them.
- **Application Insights is wired up but inert**, which reads as "we have telemetry" without
  producing any.

### Positive

- Configuration is visible, diffable and version-controlled; there is no hidden environment state to
  discover.
- `CatalogConfiguration` demonstrates that an environment-variable override was already considered
  workable in at least one project.
- A developer can clone and run with no configuration step at all.

## Implications for Change

- The environment-variable pattern in `CatalogConfiguration.cs` is the natural template to generalise
  across the estate, and it is already proven in this codebase.
- Fixing `%property{activity}` → `%property{activityid}` is a one-character-class change that would
  make every existing log line correlatable — worth doing before any behavioural baseline is
  captured, because the current logs cannot be joined across a request.
- The `log4net.xml` / `log4Net.xml` case discrepancy must be resolved before any Linux or container
  hosting is attempted; it will fail silently rather than loudly.
- What the configuration looks like in a deployed environment, if one exists, is unknown
  ([Discovery-Report.md §12](../Discovery-Report.md#12-unknowns-register)).
