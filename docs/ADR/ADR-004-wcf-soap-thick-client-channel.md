# ADR-004: WCF SOAP over basicHttpBinding as the Thick-Client Integration Channel

**Status**: Observed (reconstructed from code — no original ADR exists)

---

## Context

`eShopLegacyNTier` separates a Windows Forms desktop client from the data it displays. The client
needed remote access to catalog data, plus two capabilities the web applications do not have:
time-phased stock levels and date-ranged discounts.

WCF over HTTP was chosen as the channel, with a `basicHttpBinding` endpoint and a Visual Studio
"Add Service Reference" generated proxy on the client.

## Decision

1. Expose the service as a `.svc` endpoint hosted in IIS, contract `ICatalogService` decorated with
   `[ServiceContract]` / `[OperationContract]`.
2. Use `basicHttpBinding` (SOAP 1.1 over plain HTTP, no WS-Security).
3. Generate the client proxy with Add Service Reference and check the generated code into source
   control.
4. Configure the endpoint address in the client's `App.config`.
5. Put stock and discount operations on this contract and nowhere else.

## Evidence

| Evidence | Location |
|---|---|
| Service contract, ten operations | `eShopLegacyNTier/src/eShopWCFService/ICatalogService.cs` |
| Implementation | `eShopLegacyNTier/src/eShopWCFService/CatalogService.svc.cs` |
| Binding and metadata configuration | `eShopLegacyNTier/src/eShopWCFService/Web.config` — `<protocolMapping><add binding="basicHttpsBinding" scheme="https" /></protocolMapping>`, `<serviceMetadata httpGetEnabled="true" httpsGetEnabled="true" />` |
| Generated proxy, checked in | `eShopLegacyNTier/src/eShopWinForms/Connected Services/eShopServiceReference/Reference.cs` — 669 lines, the largest file in the repository |
| Hard-coded endpoint address | `eShopLegacyNTier/src/eShopWinForms/App.config` — `<endpoint address="http://localhost:62314/CatalogService.svc" binding="basicHttpBinding" ... />` |
| Client constructed inline | `eShopLegacyNTier/src/eShopWinForms/Program.cs::Main` — `new CatalogServiceClient()` with no address override |
| Capabilities unique to this channel | `eShopWCFService/Models/CatalogItemsStock.cs`, `eShopWCFService/Models/DiscountItem.cs` |

### The startup sequence is chatty

`src/eShopWinForms/Controllers/CatalogController.cs::LoadView` issues six SOAP calls before the
window is displayed:

| Order | Call | Issued by |
|---|---|---|
| 1 | `GetDiscount(today)` | `CheckForDiscounts` |
| 2 | `GetCatalogItems(0, 0)` | `LoadCatalogItems` |
| 3 | `GetDiscount(today)` | `LoadCatalogItems`, internally |
| 4 | `GetCatalogBrands()` | `LoadBrandFilters` |
| 5 | `GetCatalogTypes()` | `LoadTypeFilters` |
| 6 | `GetCatalogItems(0, 0)` | `SetShipmentView` |

Calls 3 and 6 duplicate calls 1 and 2 with identical arguments. `Program.Main` invokes `LoadView()`
**before** `ShowDialog()`, with no `try`/`catch`, so an unreachable service produces an unhandled
exception and no application window at all.

### The service ships against its own warnings

`eShopWCFService/Web.config` contains, immediately adjacent to the settings they describe:

- a comment stating metadata should be set to `false` before deployment — `httpGetEnabled` and
  `httpsGetEnabled` are both `true`;
- a comment stating directory browsing should be disabled — `<directoryBrowse enabled="true" />`;
- `<compilation debug="true" ... />`.

### There is an orphaned second client

`eShopLegacyNTier/src/eShopWCFService/CatalogServiceClient.cs` is a hand-written client that is
**not in `eShopWCFService.csproj`'s compile list** and could not compile if it were:

- it declares `GetCatalogItems()` with no parameters against a contract requiring `(int, int)`;
- it omits `GetDiscount` and `Dispose`, both required by `ICatalogService`;
- five of its nine methods `throw new NotImplementedException()`.

### The client references a data-access stack it never uses

`eShopWinForms.csproj` lines 57–62 reference `EntityFramework` and `EntityFramework.SqlServer`
(6.1.3) and `packages.config` pins them, yet no source file in `eShopWinForms` imports
`System.Data.Entity`. The thick client carries an ORM it does not use.

## Consequences

### Negative

- **The endpoint is not configurable per environment in any meaningful way.** It is a literal
  `http://localhost:62314` in a file that is deployed alongside the executable, with no environment
  variable or registry override in code.
- **No transport security.** `basicHttpBinding` over `http` with no `<security mode>` element means
  catalog data and all writes travel in clear text. There is no authentication on the channel.
- **`CreateCatalogItem`, `UpdateCatalogItem` and `RemoveCatalogItem` are exposed anonymously over
  SOAP** to anyone who can reach the endpoint, and metadata publication tells them the contract.
- **The generated proxy is a compile-time snapshot.** A change to a service-side signature is not a
  build error in the client until someone regenerates the service reference; it becomes a runtime
  SOAP fault instead.
- **WCF server-side hosting has no equivalent on modern .NET.** `System.ServiceModel` service hosting
  was not carried forward past .NET Framework; only the client stack was.
- **Startup latency and failure are coupled to the network.** Six sequential round trips before the
  first pixel, and no window at all if any of them fail.

### Positive

- The contract is explicit, strongly typed and machine-readable; the client compiles against it.
- IIS hosting means the service inherits IIS process management, logging and recycling for free.
- SOAP over `basicHttpBinding` is maximally interoperable and passes through ordinary HTTP
  infrastructure.
- The stock and discount capabilities are isolated behind one contract, so the blast radius of
  changing them is one service and one client.

## Implications for Change

- The service contract is the cleanest migration seam in the estate: ten operations, one consumer,
  and a generated proxy that can be replaced wholesale.
- Any migration must replace server-side WCF, not port it. The client-side `System.ServiceModel`
  packages do have a modern equivalent; the `.svc` host does not.
- The duplicate startup calls should be resolved before measuring any migration's performance, or the
  baseline will be misleading.
- `CatalogServiceClient.cs` should be deleted; it is dead code that reads like a supported client.
- Whether any consumer other than `eShopWinForms` calls this service is unknown
  ([Discovery-Report.md §12](../Discovery-Report.md#12-unknowns-register)).
