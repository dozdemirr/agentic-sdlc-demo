# ADR 0002: Configurable Mock Data Registration

- **Status:** Observed; inferred, not recorded as an explicit decision.
- **Date:** Not present in repository evidence.

## Context

The Web Forms, MVC 5, and ASP.NET Core MVC applications each define an `ICatalogService`, a mock implementation, and a database-backed implementation. Their startup modules read `UseMockData` to select the mock or real implementation; startup only configures the EF context/initializer on the non-mock branch. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Modules/ApplicationModule.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Global.asax.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Modules/ApplicationModule.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Modules/ApplicationModule.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Startup.cs`.

## Observed decision

**[INFERRED]** Each web application retains a configuration-controlled way to register either mock catalog data or database-backed services through its service abstraction. The checked-in defaults are not uniform: Web Forms and `eShopPorted` set `UseMockData` to true, while MVC 5 sets it to false. The repository does not document the environments for which those values are intended. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; the registration files cited above.

## Consequences visible in source

The setting changes the services resolved at runtime, and in the database-backed path it also changes whether EF context/initializer configuration is performed. Accordingly, identical UI requests can exercise different code paths under the checked-in app configurations. This records source behavior and does not identify a prescribed operational value. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Global.asax.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Global.asax.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Startup.cs`.
