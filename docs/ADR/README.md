# Architecture Decision Records — eShop Legacy Estate

These ADRs are **reconstructed, not original**. No ADRs exist in the repository; each record below
documents a decision inferred from the code as it stands, so that the reasoning is written down
before any modernisation work begins.

All records carry `Status: Observed` — meaning the decision is visibly in force in the codebase, but
no contemporaneous record of who made it, when, or why has been found.

| ADR | Title |
|---|---|
| [ADR-001](ADR-001-entity-framework-6-shared-database.md) | Entity Framework 6 Code First with a per-application context over a shared database |
| [ADR-002](ADR-002-autofac-assembly-scanning-di.md) | Autofac with assembly scanning, and three different injection styles |
| [ADR-003](ADR-003-mock-data-configuration-flag.md) | Mock vs real data selected by a configuration flag at container-build time |
| [ADR-004](ADR-004-wcf-soap-thick-client-channel.md) | WCF SOAP over basicHttpBinding as the thick-client integration channel |
| [ADR-005](ADR-005-webconfig-configuration-and-secrets.md) | Web.config-based configuration with connection strings in source control |
| [ADR-006](ADR-006-client-side-hilo-key-generation.md) | Client-side HiLo key generation in a singleton |

Format follows the worked example at
[`examples/contoso-insurance/02-documentation/`](../../examples/contoso-insurance/02-documentation/).
