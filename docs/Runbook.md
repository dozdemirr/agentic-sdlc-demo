# Runbook: Build, Run, and Test

## Prerequisites

- Use Windows with Visual Studio/MSBuild and the .NET Framework targeting packs for the classic Web Forms, MVC 5, WCF, and Windows Forms projects. Their project files target .NET Framework 4.6.1 through 4.7.2 and include classic Visual Studio web application/MSBuild imports or Windows Forms/WCF framework references. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`; `/eShopLegacyNTier/src/eShopWinForms/eShopWinForms.csproj`.)
- Install NuGet CLI for the classic `packages.config` projects and the Visual Studio web application components required by their project imports. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/packages.config`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/packages.config`; `/eShopLegacyNTier/src/eShopWCFService/packages.config`; `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`.)
- Install SQL Server LocalDB for database-backed modes. The Web Forms and MVC 5 apps use a LocalDB connection string, `eShopPorted` uses a LocalDB connection string when `UseMockData` is disabled, and the WCF context configures LocalDB. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/eShopLegacyNTier/src/eShopWCFService/Web.config`; `/eShopLegacyNTier/src/eShopWCFService/EntityModel.cs`.)
- The ported app targets `net461` and references ASP.NET Core 2.2. Use a compatible .NET SDK/runtime and .NET Framework targeting pack; its launch profile declares the development URL ports. (Sources: `/eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj`; `/eShopLegacyMVCSolution/eShopPorted/Properties/launchSettings.json`.)

## Restore and Build Classic Solutions

Run these commands from the repository root in a Visual Studio Developer Command Prompt with NuGet CLI and MSBuild on `PATH`. Each solution contains its own project set; the commands restore packages and build the Debug configuration. (Sources: `/eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln`; `/eShopLegacyMVCSolution/eShopLegacyMVC.sln`; `/eShopLegacyNTier/eShopLegacyNTier.sln`.)

```powershell
nuget restore eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln
msbuild eShopLegacyWebFormsSolution/eShopLegacyWebForms.sln /p:Configuration=Debug

nuget restore eShopLegacyMVCSolution/eShopLegacyMVC.sln
msbuild eShopLegacyMVCSolution/eShopLegacyMVC.sln /p:Configuration=Debug

nuget restore eShopLegacyNTier/eShopLegacyNTier.sln
msbuild eShopLegacyNTier/eShopLegacyNTier.sln /p:Configuration=Debug
```

## Restore, Build, and Run the Ported Application

The ported application is an SDK-style project included in the MVC solution. The project targets `net461`; the commands below require an installed .NET SDK with support for that target and the required targeting pack. The `eShopPorted` launch profile sets `ASPNETCORE_ENVIRONMENT=Development`, launches a browser, and uses HTTP port 5000 / HTTPS port 5001. (Sources: `/eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj`; `/eShopLegacyMVCSolution/eShopPorted/Properties/launchSettings.json`.)

```sh
dotnet restore eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj
dotnet build eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj --configuration Debug
dotnet run --project eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj --launch-profile eShopPorted
```

The checked-in `appsettings.json` enables mock data, so the application does not register its SQL Server context by default. To use SQL Server, set `UseMockData` to `false` and provide a usable `ConnectionStrings:DefaultConnection`; `Startup.ConfigureServices` registers the SQL Server provider only in that case. (Sources: `/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/eShopLegacyMVCSolution/eShopPorted/Startup.cs`.)

## Run Web Applications and WCF/Windows Forms

- After building the classic web projects, these PowerShell commands start IIS Express from the project directories. Ports 5002 and 5003 are selected for these examples; WCF uses its configured port 62314. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`; `/eShopLegacyNTier/src/eShopWinForms/App.config`.)

```powershell
$iisExpress = Join-Path ${env:ProgramFiles(x86)} 'IIS Express\iisexpress.exe'
& $iisExpress /path:"$PWD\eShopLegacyWebFormsSolution\src\eShopLegacyWebForms" /port:5002
& $iisExpress /path:"$PWD\eShopLegacyMVCSolution\src\eShopLegacyMVC" /port:5003
& $iisExpress /path:"$PWD\eShopLegacyNTier\src\eShopWCFService" /port:62314
```

- The Web Forms default is mock data; the MVC 5 default is database-backed and therefore requires LocalDB. Start the WCF host before launching WinForms; its client configuration points to `http://localhost:62314/CatalogService.svc`. The WCF service uses `eShopDatabase` LocalDB and initializes it if it does not exist. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/eShopLegacyNTier/src/eShopWinForms/App.config`; `/eShopLegacyNTier/src/eShopWCFService/Web.config`; `/eShopLegacyNTier/src/eShopWCFService/EntityModel.cs`; `/eShopLegacyNTier/src/eShopWCFService/Models/Infrastructure/CatalogDBInitializer.cs`.)
- Launch the built Windows Forms executable from the repository root after starting the WCF host. The classic project uses `bin\Debug` as its Debug output directory. (Sources: `/eShopLegacyNTier/src/eShopWinForms/eShopWinForms.csproj`; `/eShopLegacyNTier/src/eShopWinForms/Program.cs`.)

```powershell
Start-Process .\eShopLegacyNTier\src\eShopWinForms\bin\Debug\eShopWinForms.exe
```
- WinForms catalog thumbnails are loaded from image files under `Assets/Images/Catalog` relative to the application working directory; keep the project content files available at runtime. (Sources: `/eShopLegacyNTier/src/eShopWinForms/Views/CatalogView.cs`; `/eShopLegacyNTier/src/eShopWinForms/eShopWinForms.csproj`.)

## Tests and Validation

The repository README states that there are no automated test projects in the estate, so there is no repository test command to run. The available Mermaid documentation validator can be run from the repository root to check documentation diagrams: (Sources: `/README.md`; `/scripts/validate_mermaid.py`.)

```sh
python scripts/validate_mermaid.py docs/
```

## Configuration Notes and Known Limitations

- The database names differ across the four applications: Web Forms and MVC 5 configure `Microsoft.eShopOnContainers.Services.CatalogDb`, the ported app configures `eShopPorted`, and WCF configures `eShopDatabase`. Use the corresponding configuration when comparing data across applications. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/eShopLegacyNTier/src/eShopWCFService/Web.config`.)
- The checked-in mock-data defaults are not consistent: Web Forms and `eShopPorted` use mock data, while MVC 5 uses SQL-backed data. The WCF service creates an `EntityModel` and does not read a mock-data flag in that context. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/eShopLegacyNTier/src/eShopWCFService/EntityModel.cs`; `/eShopLegacyNTier/src/eShopWCFService/Web.config`.)
- The WinForms endpoint is explicitly configured to localhost and the WCF project declares an IIS Express development URL. The supplied configuration does not establish a non-local service endpoint. (Sources: `/eShopLegacyNTier/src/eShopWinForms/App.config`; `/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`; `/eShopLegacyNTier/src/eShopWCFService/Web.config`.)
- The README characterizes the estate as having no secret management and configuration values in source. The connection strings in the checked-in files are local LocalDB development values. (Sources: `/README.md`; `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/Web.config`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/Web.config`; `/eShopLegacyMVCSolution/eShopPorted/appsettings.json`; `/eShopLegacyNTier/src/eShopWCFService/Web.config`.)
- The applications target older .NET Framework and ASP.NET Core 2.2 dependencies, and the classic projects require Visual Studio web application build targets. Runtime compatibility therefore depends on matching Windows/.NET Framework tooling. (Sources: `/eShopLegacyWebFormsSolution/src/eShopLegacyWebForms/eShopLegacyWebForms.csproj`; `/eShopLegacyMVCSolution/src/eShopLegacyMVC/eShopLegacyMVC.csproj`; `/eShopLegacyMVCSolution/eShopPorted/eShopPorted.csproj`; `/eShopLegacyNTier/src/eShopWCFService/eShopWCFService.csproj`.)
