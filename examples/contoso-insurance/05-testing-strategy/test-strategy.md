# Test Strategy — PolicyHub Modernisation

> Output of [05-testing-strategy-playbook.md](../../../05-testing-strategy-playbook.md) — testing baseline to protect current behaviour during migration.

---

## Current State Assessment

| Metric | Value |
|---|---|
| Existing tests | 41 files in `PolicyHub.Tests/` |
| Coverage estimate | ~22% (mostly `PremiumCalculator` unit tests) |
| Test framework | MSTest v1 |
| Integration tests | 3 (database-dependent, often fail on dev machines) |
| UI tests | None |
| CI test execution | TeamCity runs tests on build — ~40% of builds have test failures ignored |

**Key gap**: No tests cover `PolicyService.cs` (God Class), `ClaimsHandler.cs`, or any of the WCF service endpoints.

---

## Test Pyramid

```
        ╱  E2E  ╲           5 scenarios — customer quote journey, agent MTA
       ╱─────────╲
      ╱ Integration╲        20 tests — API contracts, database round-trips
     ╱───────────────╲
    ╱  Characterisation ╲   50+ tests — capture current output for safe refactoring
   ╱─────────────────────╲
  ╱      Unit Tests       ╲  100+ tests — business logic, validation rules
 ╱─────────────────────────╲
```

---

## Priority Matrix

| Priority | Category | Scope | Count | Purpose |
|---|---|---|---|---|
| P0 | **Smoke** | App starts, DB connects, key endpoints respond | 5 | Catch deployment-breaking changes |
| P1 | **Critical Path** | Top 5 user journeys end-to-end | 10 | Protect revenue-critical flows |
| P2 | **Characterisation** | Capture current output of complex logic | 50+ | Safe refactoring of God Class and rating engine |
| P3 | **Integration** | Service-to-service, service-to-database | 20 | Validate component communication |
| P4 | **Security** | OWASP top 5 for this application | 10 | Ensure no regressions during migration |

---

## Test Framework Selection

| Concern | Choice | Rationale |
|---|---|---|
| Unit test framework | **xUnit** | Modern, .NET 8 native, parallel execution, better assertions than MSTest |
| Assertions | **FluentAssertions** | Readable failure messages, complex object comparison |
| Mocking | **NSubstitute** | Simpler syntax than Moq for the team's experience level |
| Integration tests | **WebApplicationFactory** | In-process testing of .NET 8 APIs without deployment |
| API contract tests | **Verify** | Snapshot testing for JSON responses — catches unintended contract changes |
| Database tests | **Testcontainers** | Disposable SQL Server containers, no shared test database |
| BDD scenarios | **Gherkin `.feature.md`** | Human-readable scenarios, convertible to xUnit tests |

---

## P0: Smoke Tests

```csharp
// Tests/Smoke/ApplicationStartupTests.cs
public class ApplicationStartupTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApplicationStartupTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task HealthCheck_ReturnsOk()
    {
        var response = await _client.GetAsync("/health");
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }

    [Fact]
    public async Task PricingEndpoint_ReturnsValidResponse()
    {
        var risk = new { VehicleType = "Car", DriverAge = 35, PostCode = "SW1A 1AA" };
        var response = await _client.PostAsJsonAsync("/api/pricing/calculate", risk);
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var result = await response.Content.ReadFromJsonAsync<PricingResult>();
        result.Premium.Should().BeGreaterThan(0);
    }

    [Fact]
    public async Task DatabaseConnection_IsHealthy()
    {
        var response = await _client.GetAsync("/health/db");
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}
```

---

## P1: Critical Path — Gherkin Scenarios

```gherkin
# Tests/CriticalPath/CustomerQuote.feature.md

Feature: Customer Motor Quote

  Scenario: Standard driver gets a quote
    Given a customer aged 35
    And they want to insure a 2020 Ford Focus
    And they live in postcode "SW1A 1AA"
    And they have 5 years NCD
    When they request a motor quote
    Then a quote reference is returned
    And the annual premium is between £280 and £450
    And the quote is saved with status "Open"

  Scenario: Young driver gets loaded premium
    Given a customer aged 19
    And they want to insure a 2018 Vauxhall Corsa
    And they have 0 years NCD
    When they request a motor quote
    Then the premium includes a young driver surcharge
    And the annual premium is between £1200 and £2500

  Scenario: Quote converts to live policy
    Given an existing quote with reference "QT-001234"
    When the customer accepts the quote
    And provides valid payment details
    Then the policy status changes to "Live"
    And a certificate of insurance is generated
    And a confirmation email is sent
```

---

## P2: Characterisation Tests — Rating Engine

```csharp
// Tests/Characterisation/PremiumCalculatorCharacterisationTests.cs
// Purpose: Capture the CURRENT output of the existing calculator
// so we can refactor with confidence.

public class PremiumCalculatorCharacterisationTests
{
    [Theory]
    [MemberData(nameof(GoldenFileTestCases))]
    public async Task Premium_Matches_GoldenFile(string testCaseId, RiskProfile risk)
    {
        // Arrange
        var calculator = CreateCalculatorWithProductionFactorTables();

        // Act
        var result = calculator.Calculate(risk);

        // Assert — snapshot comparison
        await Verify(result)
            .UseDirectory("GoldenFiles")
            .UseFileName(testCaseId);
    }

    public static IEnumerable<object[]> GoldenFileTestCases()
    {
        // 200 representative risks exported from production
        yield return new object[] { "STD-35-FOCUS-5NCD", new RiskProfile { Age = 35, Vehicle = "Ford Focus", NCD = 5 } };
        yield return new object[] { "YNG-19-CORSA-0NCD", new RiskProfile { Age = 19, Vehicle = "Vauxhall Corsa", NCD = 0 } };
        yield return new object[] { "SEN-70-JAZZ-9NCD", new RiskProfile { Age = 70, Vehicle = "Honda Jazz", NCD = 9 } };
        // ... 197 more cases from production sample
    }
}
```

**Golden file example** (`GoldenFiles/STD-35-FOCUS-5NCD.verified.json`):
```json
{
  "BasePremium": 420.00,
  "Loadings": {
    "AreaRating": 1.15,
    "VehicleGroup": 1.08
  },
  "Discounts": {
    "NCD": 0.70,
    "OnlineDiscount": 0.95
  },
  "FinalPremium": 312.47,
  "IPT": 37.50,
  "TotalPayable": 349.97
}
```

---

## P4: Security Tests

| OWASP Risk | Test | Approach |
|---|---|---|
| A01: Broken Access Control | Agent-only endpoints reject customer tokens | Integration test with role-specific JWTs |
| A02: Cryptographic Failures | No PII in logs | Log capture test — submit policy, grep logs for name/DOB |
| A03: Injection | SQL injection on search fields | Parameterised input fuzzing on policy search |
| A05: Security Misconfiguration | CORS, headers, HTTPS enforcement | HTTP response header assertions |
| A07: Auth Failures | Brute force protection on login | Rate limit test — 10 rapid login attempts |

---

## CI Pipeline

```yaml
# .github/workflows/ci.yml
name: PolicyHub CI

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      sqlserver:
        image: mcr.microsoft.com/mssql/server:2022-latest
        env:
          ACCEPT_EULA: Y
          SA_PASSWORD: ${{ secrets.TEST_DB_PASSWORD }}
        ports:
          - 1433:1433

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Restore
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore

      - name: Unit + Characterisation Tests
        run: dotnet test --filter "Category!=Integration" --logger trx

      - name: Integration Tests
        run: dotnet test --filter "Category=Integration" --logger trx
        env:
          ConnectionStrings__PolicyHub: "Server=localhost;Database=PolicyHubTest;User=sa;Password=${{ secrets.TEST_DB_PASSWORD }};TrustServerCertificate=true"

      - name: Publish Test Results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: Test Results
          path: '**/*.trx'
          reporter: dotnet-trx
```
