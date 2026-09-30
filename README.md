# Agentic SDLC — Demo Estate

A pre-modernisation .NET Framework estate with the **Agentic SDLC accelerator** installed,
used to demonstrate AI-assisted application modernisation end to end.

## The estate

3 solutions · 6 projects · ~8,800 lines of C#, Razor and WebForms · .NET Framework 4.6.1–4.7.2

| Solution | Stack | Role |
|---|---|---|
| `eShopLegacyWebFormsSolution` | ASP.NET WebForms, .NET Framework 4.7 | Back-office catalogue portal |
| `eShopLegacyMVCSolution` | ASP.NET MVC 5, Entity Framework 6 | Web storefront |
| `eShopLegacyNTier` | WinForms client + WCF services | Thick-client channel over SOAP |

Shared characteristics that make this representative of a real legacy estate:

- .NET Framework only — no .NET Core/5+ anywhere, three different target versions
- Entity Framework 6 with a shared `CatalogDBContext` reached from multiple applications
- Autofac assembly-scanning dependency injection
- `Web.config` / `App.config` driven configuration, connection strings in source, no secret management
- Mock-vs-real data selected by a config flag rather than by composition
- No automated test projects anywhere in the estate
- IIS and Windows Server hosting assumptions baked into the code

> **On scale.** This is a compact reference estate, deliberately chosen so a full
> discovery pass completes in minutes rather than hours. It demonstrates the
> mechanism, not the scale. For depth at realistic size, see the worked example in
> `examples/contoso-insurance/` — a 380K LOC, 47-project policy administration
> system taken through every stage.

> Modernised reference implementations, container assets and Kubernetes manifests
> from the upstream project have been **removed on purpose**. The point of the demo
> is that the agents derive the target architecture — it must not already be sitting
> in the repository.

## The accelerator

| Path | Contents |
|---|---|
| `.github/agents/` | 9 stage agents with explicit handoffs |
| `.github/skills/` | 9 versioned reasoning skills with guardrails |
| `.github/templates/` | `target-architecture.yml` output schema |
| `0*-playbook.md` | The same methodology written for humans |
| `examples/contoso-insurance/` | Worked reference output (PolicyHub) |
| `docs/` | **Empty — this is what the agents fill in** |

See [AGENTIC-SDLC.md](AGENTIC-SDLC.md) for the full methodology and adoption ladder.

## Running a stage

Open Copilot Chat in this repository and invoke the stage agent, for example:

```
Run the 01-discovery agent against this repository.
Produce the technology inventory, component map and unknowns register in docs/.
```

Each stage writes its artefacts to `docs/` and hands off to the next.

## Attribution

Legacy application source derives from
[dotnet-architecture/eShopModernizing](https://github.com/dotnet-architecture/eShopModernizing)
(MIT licence, retained in [LICENSE](LICENSE)).
