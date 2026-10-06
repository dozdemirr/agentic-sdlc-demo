# ADR 0003: WCF Boundary for the Desktop Client

- **Status:** Observed; inferred, not recorded as an explicit decision.
- **Date:** Not present in repository evidence.

## Context

The WinForms startup constructs a generated `CatalogServiceClient` and injects it into its `CatalogController`; that controller calls operations declared by the WCF `ICatalogService` contract. The service implementation creates or receives an EF6 `EntityModel`, and the WCF service project hosts it through `CatalogService.svc`. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/Program.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/Controllers/CatalogController.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/Connected Services/eShopServiceReference/Reference.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/ICatalogService.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/CatalogService.svc.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/CatalogService.svc`.

## Observed decision

**[INFERRED]** The desktop client obtains catalogue, discount, and stock behavior across a WCF service boundary instead of connecting directly to the service's EF context. The checked-in client endpoint uses `basicHttpBinding` at `http://localhost:62314/CatalogService.svc`, and the server declares a matching `basicHttpBinding` endpoint and a MEX endpoint. Source code does not state why this boundary was selected or which non-local endpoint should be used. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/App.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/EntityModel.cs`.

## Consequences visible in source

The client requires a reachable service matching the generated reference, configured address, and operation contract. Service persistence configuration and database access remain in the WCF project, separate from the WinForms UI. These are implementation consequences of the current code boundary, not a recommendation. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/App.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/Connected Services/eShopServiceReference/Reference.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/ICatalogService.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Models/Infrastructure/CatalogConfiguration.cs`.
