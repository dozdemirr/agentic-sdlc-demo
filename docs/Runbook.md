# Runbook: Current Repository

This runbook records commands consistent with checked-in solution/project files. The commands below were **not executed** while preparing this document; no builds or tests were run. The legacy solutions use classic .NET Framework project formats. **[INFERRED]** No single supported developer toolchain or CI command can be asserted from the checked-in solutions and project files alone. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopLegacyMVC.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/eShopLegacyNTier.sln`; the corresponding project files.

## Local prerequisites

- **For Web Forms, MVC 5, WinForms, and WCF:** **[INFERRED]** A Windows environment with a .NET Framework targeting pack for the relevant project targets and Visual Studio MSBuild/web build targets is the local toolchain indicated by the classic project formats and IIS Express settings. The Web Forms and MVC 5 projects target .NET Framework 4.7.2; WinForms targets 4.7; WCF targets 4.6.1. Their classic project files import Visual Studio/MSBuild targets. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/eShopWinForms.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`.
- **For `eShopPorted`:** a .NET SDK capable of restoring/building the SDK-style project and .NET Framework 4.6.1 targeting assemblies are needed by its `net461` target. It references ASP.NET Core 2.2 and EF Core 2.2 packages. Exact required SDK version is not recorded in the project. Source: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj`.
- **For database-backed runs:** SQL Server LocalDB is the configured provider in the checked-in settings. **[INFERRED]** LocalDB needs to be installed and available only when a database-backed service path is selected. Web Forms and MVC 5 use named `CatalogDBContext` LocalDB connection strings; `eShopPorted` uses `DefaultConnection` with database `eShopPorted`; WCF uses `EntityModel`/`eShopDatabase` unless the `ConnectionString` environment variable overrides it. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Models/Infrastructure/CatalogConfiguration.cs`.
- **For the desktop client:** the WCF service must be reachable at the configured client endpoint `http://localhost:62314/CatalogService.svc`, or the endpoint configuration must be changed for the actual host. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/App.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.config`.

## Restore and build

Run the classic solution commands from a Visual Studio Developer Command Prompt on Windows with the required .NET Framework and web build tooling installed. Package restore behavior for classic `packages.config` projects depends on NuGet/Visual Studio tooling; the solution files do not define a repository-wide restore wrapper. The MVC solution also includes the SDK-style `eShopPorted` project. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopLegacyMVC.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/eShopLegacyNTier.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj`.

```powershell
msbuild .\eShopLegacyWebFormsSolution\eShopLegacyWebForms.sln /t:Build /p:Configuration=Debug
msbuild .\eShopLegacyMVCSolution\eShopLegacyMVC.sln /t:Build /p:Configuration=Debug
msbuild .\eShopLegacyNTier\eShopLegacyNTier.sln /t:Build /p:Configuration=Debug
dotnet restore .\eShopLegacyMVCSolution\eShopPorted\eShopPorted.csproj
dotnet build .\eShopLegacyMVCSolution\eShopPorted\eShopPorted.csproj --no-restore
```

The projects declare the build targets and package references; the commands above have not been tested in this session and do not establish a supported toolchain/version. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/eShopWinForms.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`.

## Run

### ASP.NET Core MVC port

From the repository root, run the SDK-style web project with its explicit project launch profile. The checked-in project profile sets `http://localhost:5000` and `https://localhost:5001`, and `ASPNETCORE_ENVIRONMENT=Development`; the checked-in `UseMockData` value is true. `dotnet run` and the listed port/profile behavior have not been verified here. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Program.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Properties/launchSettings.json`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Startup.cs`.

```powershell
dotnet run --project .\eShopLegacyMVCSolution\eShopPorted\eShopPorted.csproj --launch-profile eShopPorted
```

### Web Forms and MVC 5

The projects set `UseIISExpress=true`, and their `.csproj` files specify IIS Express URLs. From the repository root, run the following from Windows PowerShell after building the solutions. These commands use the project paths and ports declared in the project files; they have not been executed here. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Global.asax.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Global.asax.cs`.

```powershell
& "$env:ProgramFiles\IIS Express\iisexpress.exe" /path:"$PWD\eShopLegacyWebFormsSolution\src\eShopLegacyWebForms" /port:50586
& "$env:ProgramFiles\IIS Express\iisexpress.exe" /path:"$PWD\eShopLegacyMVCSolution\src\eShopLegacyMVC" /port:52429
```

### WCF service and WinForms client

Start the WCF service first, then launch the built WinForms executable. The service project specifies IIS Express at port 62314, and the client uses `http://localhost:62314/CatalogService.svc`; the client calls the service during startup before showing the form. The service's local database settings are independent of the WinForms endpoint setting. These commands have not been executed here. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/Program.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/App.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/CatalogService.svc`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWinForms/eShopWinForms.csproj`.

```powershell
& "$env:ProgramFiles\IIS Express\iisexpress.exe" /path:"$PWD\eShopLegacyNTier\src\eShopWCFService" /port:62314
& "$PWD\eShopLegacyNTier\src\eShopWinForms\bin\Debug\eShopWinForms.exe"
```

## Tests

No test project or repository-level test command is declared in the three checked-in solution files. Therefore there is no source-backed test command to provide, and no tests were executed for this documentation-only task. Evidence: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopLegacyMVC.sln`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/eShopLegacyNTier.sln`.

## Configuration notes and limitations

- Web Forms' checked-in `UseMockData=true`, MVC 5's value is false, and `eShopPorted`'s value is true. The corresponding service registrations and EF context setup are conditional, so changing the values changes the active code path. Sources: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Modules/ApplicationModule.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/src/eShopLegacyMVC/Modules/ApplicationModule.cs`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyMVCSolution/eShopPorted/Startup.cs`.
- LocalDB database names configured across projects are not proof of one shared database instance; confirm deployment connection strings before operating on persistent data. Sources: the connection configuration files cited under local prerequisites.
- The WCF service configuration enables HTTP/HTTPS metadata retrieval and directory browsing; verify environment-specific transforms and deployment configuration before exposing a host. Source: `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.config`; transforms are `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.Debug.config` and `/home/runner/work/agentic-sdlc-demo/agentic-sdlc-demo/eShopLegacyNTier/src/eShopWCFService/Web.Release.config`.
- The repository does not specify supported Visual Studio/MSBuild/.NET SDK versions, deployment endpoint values, environment-specific connection strings, or a test harness. These are unresolved operational details, not assumed defaults. Evidence: project and configuration files cited throughout this runbook; the three solution files cited above.
