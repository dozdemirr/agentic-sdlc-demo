# ADR-002: Autofac with Assembly Scanning, and Three Different Injection Styles

**Status**: Observed (reconstructed from code — no original ADR exists)

---

## Context

Three of the four applications needed to substitute `ICatalogService` implementations without editing
call sites (see [ADR-003](ADR-003-mock-data-configuration-flag.md)). Autofac was adopted as the
container.

Each application, however, integrates it through a different ASP.NET extension point, because each
uses a different hosting model. The WinForms client uses no container at all.

## Decision

1. Use Autofac as the IoC container.
2. Register the service layer in an `ApplicationModule` per application.
3. Discover controllers by **assembly scanning** rather than by explicit registration.
4. Accept whatever injection style each host supports, rather than normalising on one:
   constructor injection for MVC and Web API, property injection for WebForms,
   `IServiceProvider` for ASP.NET Core, and manual `new` for WinForms.

## Evidence

| Application | Registration | Resolution | Location |
|---|---|---|---|
| MVC | `builder.RegisterControllers(typeof(MvcApplication).Assembly)`, `builder.RegisterApiControllers(...)`, `builder.RegisterModule(new ApplicationModule(mockData))` | `DependencyResolver.SetResolver(new AutofacDependencyResolver(container))` and `GlobalConfiguration.Configuration.DependencyResolver = new AutofacWebApiDependencyResolver(container)` | `src/eShopLegacyMVC/Global.asax.cs::RegisterContainer` |
| WebForms | `builder.RegisterModule(new ApplicationModule(mockData))` only — page types are **not** registered | `ContainerProvider` reached through `IContainerProviderAccessor`, plus the `PropertyInjection` HTTP module from `Autofac.Integration.Web` declared in `Web.config` under `<system.webServer><modules>` | `src/eShopLegacyWebForms/Global.asax.cs::ConfigureContainer`, `src/eShopLegacyWebForms/Web.config` |
| Ported | `builder.Populate(services)`, `builder.RegisterModule(new ApplicationModule(...))` | `return new AutofacServiceProvider(ApplicationContainer)` from `ConfigureServices` | `eShopPorted/Startup.cs::ConfigureServices` |
| WinForms | — | `var client = new CatalogServiceClient(); var controller = new CatalogController(view, client);` | `src/eShopWinForms/Program.cs::Main` |

Property injection surfaces in every WebForms page as a settable public property, for example:

```
public ICatalogService CatalogService { get; set; }
```

— `src/eShopLegacyWebForms/Default.aspx.cs`, `src/eShopLegacyWebForms/Catalog/Create.aspx.cs`,
and the other `Catalog/*.aspx.cs` code-behind files.

The MVC project additionally carries a build-level conflict around the container itself:

| Mechanism | Autofac version |
|---|---|
| `src/eShopLegacyMVC/packages.config` | `4.9.1` (and `Autofac.Mvc5 4.0.2`) |
| `src/eShopLegacyMVC/eShopLegacyMVC.csproj` `<PackageReference>` | `6.1.0` |
| `src/eShopLegacyMVC/eShopLegacyMVC.csproj` `<Reference>` | `Autofac.Integration.Mvc, Version=4.0.0.0` from `packages\Autofac.Mvc5.4.0.2\lib\net45\` |
| `src/eShopLegacyMVC/Web.config` `<bindingRedirect>` | forced to `6.1.0.0` |

The project therefore uses `packages.config` and `PackageReference` at the same time, and
binding-redirects an integration assembly built against Autofac 4 onto Autofac 6.

## Consequences

### Negative

- **The dependency graph is not visible from the composition root.** `RegisterControllers` scans an
  assembly, so adding a controller changes the container's contents with no edit to `Global.asax.cs`.
- **Three integration styles means three failure modes.** A missing registration is a constructor
  resolution exception in MVC, a `NullReferenceException` on first use in WebForms (an unset property
  is just `null`), and a startup failure in the ported project.
- **Property injection defeats the compiler.** Nothing forces a WebForms page to have its
  `CatalogService` property populated; the omission is only detectable at runtime.
- **The WinForms client cannot substitute its dependency at all.** `CatalogServiceClient` is
  constructed inline in `Program.Main`, so there is no seam for a fake service, and therefore no way
  to run the client without a live WCF endpoint.
- **The Autofac version conflict is a latent runtime risk.** `MethodMissingException`-class failures
  from an Autofac 4 integration assembly running against Autofac 6 would appear only at container
  build time.

### Positive

- The service layer is genuinely abstracted behind `ICatalogService` in three of four applications,
  which is what makes the mock/real swap possible at all.
- `InstancePerLifetimeScope` scoping for the real service gives correct `DbContext` lifetime in the
  web applications without any manual disposal code.
- Assembly scanning removes a class of "forgot to register the new controller" errors.

## Implications for Change

- Resolve the Autofac version conflict before any other change to the MVC project; migrate fully to
  either `packages.config` or `PackageReference`, not both.
- WebForms property injection is the hardest style to carry forward — ASP.NET Core has no equivalent,
  so each page's dependency becomes an explicit constructor parameter during any port.
- The WinForms client needs an injected `ICatalogService` before it can be tested at all.
