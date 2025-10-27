---
id: TASK-011F
title: Create maui-service-specialist agent for external systems
status: completed
created: 2025-10-12T10:00:00Z
updated: 2025-10-13T00:00:00Z
completed: 2025-10-13T00:00:00Z
previous_state: in_review
state_transition_reason: "Task completed: All acceptance criteria satisfied, 100% test pass rate"
duration_days: 1
estimated_days: 0.5
priority: high
tags: [maui, agents, template-migration, phase-2.3, service-layer]
epic: EPIC-MAUI-TEMPLATE-MIGRATION
feature: null
requirements: []
external_ids:
  epic_jira: null
  epic_linear: null
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: passed
  total_tests: 58
  passed: 58
  failed: 0
  coverage: 100
  last_run: "2025-10-13T00:00:00Z"
  validation_categories:
    - file_existence: 4/4
    - file_equality: 3/3
    - yaml_frontmatter: 5/5
    - section_completeness: 11/11
    - code_examples: 5/5
    - erroror_pattern: 3/3
    - anti_patterns: 5/5
    - testing_strategies: 7/7
    - architectural_boundary: 3/3
    - best_practices: 5/5
    - collaboration: 8/8
dependencies: []
complexity_evaluation:
  score: 2
  level: "simple"
  review_mode: "AUTO_PROCEED"
  factor_scores:
    - factor: "file_complexity"
      score: 1
      max_score: 3
      justification: "2 agent files (same content for both templates)"
    - factor: "pattern_familiarity"
      score: 0
      max_score: 2
      justification: "All familiar patterns - standard documentation structure"
    - factor: "risk_level"
      score: 0
      max_score: 3
      justification: "Zero risk - pure documentation task, no system impact"
    - factor: "dependencies"
      score: 1
      max_score: 2
      justification: "4 reference documents (internal, read-only)"
auto_approved: true
approved_by: "system"
approved_at: "2025-10-13T00:00:00Z"
related_documents:
  - docs/shared/maui-template-architecture.md
  - installer/global/templates/maui/templates/Service.cs
  - installer/global/templates/maui/agents/maui-usecase-specialist.md
---

# Task: Create maui-service-specialist agent for external systems

## Context

This is **Phase 2.3** of the MAUI template migration project. After successfully creating the maui-domain-specialist (Phase 2.1) and maui-data-specialist (Phase 2.2), we now need to create the maui-service-specialist agent focusing exclusively on **external system integration**.

The service layer handles:
- **API Integration** (HTTP clients, REST APIs)
- **Hardware Services** (GPS, Camera, Sensors)
- **External Services** (authentication, push notifications)
- **Caching Services** (in-memory, persistent)

**Critical Boundary**: Services do NOT access databases directly. Database access is exclusively through Repositories (handled by maui-data-specialist).

## Requirements

### Agent File Creation
- Create `installer/global/templates/maui-appshell/agents/maui-service-specialist.md`
- Create `installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md` (identical content)
- Both files should have exactly the same content (services are navigation-agnostic)

### Agent Definition Requirements

#### Core Expertise (MUST INCLUDE)
1. **External API Integration**
   - HTTP client patterns (HttpClient, RestSharp, Refit)
   - REST API best practices
   - Request/response handling
   - API authentication patterns (Bearer tokens, OAuth2, API keys)
   - Rate limiting and retry logic
   - Timeout handling

2. **Hardware Service Patterns**
   - Location services (GPS, geolocation)
   - Camera service integration
   - Sensor access (accelerometer, compass, etc.)
   - Platform-specific implementations
   - Permission handling

3. **Caching Services**
   - In-memory caching patterns
   - Persistent cache strategies
   - Cache invalidation logic
   - TTL (Time-To-Live) patterns
   - Cache-aside pattern

4. **Authentication Services**
   - Token management
   - Secure storage integration
   - Session handling
   - Biometric authentication integration

5. **ErrorOr Pattern Usage**
   - Functional error handling in services
   - Error mapping from external systems
   - Custom error types for service failures
   - Error propagation to domain layer

#### Clear Boundary Definition (CRITICAL)
- **NO database access** - Services NEVER touch SQLite/LiteDB
- **NO business logic** - Complex orchestration belongs in Domain layer
- **NO direct ViewModel interaction** - Services are called by Domain classes
- **Interface-first approach** - All services define interfaces

#### Collaboration Patterns
- **With maui-domain-specialist**: Services are consumed by Domain classes
- **With maui-data-specialist**: Services coordinate with repositories via Domain layer
- **Clear separation**: Domain orchestrates both Services and Repositories

#### Testing Strategies
- HTTP mocking (HttpClientInterception, WireMock.Net)
- Hardware service mocking (platform abstractions)
- Unit testing service logic
- Integration testing with mocked backends
- Error scenario testing

#### Code Patterns (MUST INCLUDE EXAMPLES)

**Example 1: HTTP API Service**
```csharp
using ErrorOr;

namespace MyApp.Services;

public interface IApiService
{
    Task<ErrorOr<T>> GetAsync<T>(string endpoint);
    Task<ErrorOr<T>> PostAsync<T>(string endpoint, object data);
    Task<ErrorOr<bool>> DeleteAsync(string endpoint);
}

public class ApiService : IApiService
{
    private readonly HttpClient _httpClient;
    private readonly ILogService _logService;

    public ApiService(HttpClient httpClient, ILogService logService)
    {
        _httpClient = httpClient;
        _logService = logService;
    }

    public async Task<ErrorOr<T>> GetAsync<T>(string endpoint)
    {
        try
        {
            _logService.TrackEvent("ApiGetStarted", new Dictionary<string, object>
            {
                { "Endpoint", endpoint }
            });

            var response = await _httpClient.GetAsync(endpoint);

            if (!response.IsSuccessStatusCode)
            {
                return Error.Failure(
                    code: "Api.HttpError",
                    description: $"HTTP {response.StatusCode}: {response.ReasonPhrase}");
            }

            var content = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<T>(content);

            if (result == null)
            {
                return Error.Failure(
                    code: "Api.DeserializationError",
                    description: "Failed to deserialize response");
            }

            return result;
        }
        catch (HttpRequestException ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Endpoint", endpoint }
            });

            return Error.Failure(
                code: "Api.NetworkError",
                description: "Network error occurred");
        }
        catch (TaskCanceledException ex)
        {
            return Error.Failure(
                code: "Api.Timeout",
                description: "Request timed out");
        }
    }
}
```

**Example 2: Hardware Service (Location)**
```csharp
using ErrorOr;

namespace MyApp.Services;

public interface ILocationService
{
    Task<ErrorOr<Location>> GetCurrentLocationAsync();
    Task<bool> IsLocationEnabledAsync();
}

public class LocationService : ILocationService
{
    private readonly IGeolocation _geolocation;
    private readonly ILogService _logService;

    public LocationService(IGeolocation geolocation, ILogService logService)
    {
        _geolocation = geolocation;
        _logService = logService;
    }

    public async Task<ErrorOr<Location>> GetCurrentLocationAsync()
    {
        try
        {
            var request = new GeolocationRequest(GeolocationAccuracy.Medium, TimeSpan.FromSeconds(10));
            var location = await _geolocation.GetLocationAsync(request);

            if (location == null)
            {
                return Error.Failure(
                    code: "Location.NotAvailable",
                    description: "Unable to get current location");
            }

            return location;
        }
        catch (FeatureNotSupportedException ex)
        {
            _logService.TrackError(ex);
            return Error.Failure(
                code: "Location.NotSupported",
                description: "Location services not supported on this device");
        }
        catch (PermissionException ex)
        {
            _logService.TrackError(ex);
            return Error.Failure(
                code: "Location.PermissionDenied",
                description: "Location permission denied");
        }
    }

    public async Task<bool> IsLocationEnabledAsync()
    {
        try
        {
            var status = await Permissions.CheckStatusAsync<Permissions.LocationWhenInUse>();
            return status == PermissionStatus.Granted;
        }
        catch
        {
            return false;
        }
    }
}
```

**Example 3: Cache Service**
```csharp
using ErrorOr;
using System.Collections.Concurrent;

namespace MyApp.Services;

public interface ICacheService
{
    Task<T?> GetAsync<T>(string key);
    Task SetAsync<T>(string key, T value, TimeSpan? expiry = null);
    Task RemoveAsync(string key);
    Task ClearAsync();
}

public class InMemoryCacheService : ICacheService
{
    private readonly ConcurrentDictionary<string, CacheEntry> _cache = new();
    private readonly ILogService _logService;

    private class CacheEntry
    {
        public object Value { get; set; }
        public DateTime ExpiresAt { get; set; }
    }

    public InMemoryCacheService(ILogService logService)
    {
        _logService = logService;
    }

    public Task<T?> GetAsync<T>(string key)
    {
        if (_cache.TryGetValue(key, out var entry))
        {
            if (entry.ExpiresAt > DateTime.UtcNow)
            {
                _logService.TrackEvent("CacheHit", new Dictionary<string, object> { { "Key", key } });
                return Task.FromResult((T?)entry.Value);
            }

            // Expired, remove it
            _cache.TryRemove(key, out _);
        }

        _logService.TrackEvent("CacheMiss", new Dictionary<string, object> { { "Key", key } });
        return Task.FromResult(default(T));
    }

    public Task SetAsync<T>(string key, T value, TimeSpan? expiry = null)
    {
        var expiresAt = DateTime.UtcNow.Add(expiry ?? TimeSpan.FromMinutes(5));

        _cache[key] = new CacheEntry
        {
            Value = value!,
            ExpiresAt = expiresAt
        };

        _logService.TrackEvent("CacheSet", new Dictionary<string, object>
        {
            { "Key", key },
            { "ExpiresAt", expiresAt }
        });

        return Task.CompletedTask;
    }

    public Task RemoveAsync(string key)
    {
        _cache.TryRemove(key, out _);
        return Task.CompletedTask;
    }

    public Task ClearAsync()
    {
        _cache.Clear();
        return Task.CompletedTask;
    }
}
```

#### Anti-Patterns (MUST DOCUMENT)
```markdown
## Anti-Patterns to Avoid

1. **Database Access in Services** ❌
   ```csharp
   // WRONG - Services should NEVER access database
   public class ProductService
   {
       private readonly SQLiteAsyncConnection _database; // ❌ NO!
   }

   // CORRECT - Services call APIs, Domain orchestrates with Repositories
   public class GetProducts
   {
       private readonly IProductRepository _repository;
       private readonly IApiService _apiService;

       public async Task<ErrorOr<List<Product>>> ExecuteAsync()
       {
           // Try API first
           var apiResult = await _apiService.GetAsync<List<Product>>("/products");
           if (!apiResult.IsError) return apiResult;

           // Fallback to local database (via Repository)
           return await _repository.GetAllAsync();
       }
   }
   ```

2. **Business Logic in Services** ❌
   ```csharp
   // WRONG - Complex orchestration in service
   public async Task<ErrorOr<Order>> CreateOrderAsync(OrderRequest request)
   {
       var customer = await GetCustomerAsync(request.CustomerId);
       var products = await ValidateProductsAsync(request.Items);
       var pricing = CalculatePricing(products, customer.DiscountLevel);
       var order = new Order { ... }; // Complex business rules
       await SaveOrderAsync(order);
       return order;
   }

   // CORRECT - Services are simple, Domain orchestrates
   public async Task<ErrorOr<Customer>> GetCustomerAsync(string customerId)
   {
       var response = await _httpClient.GetAsync($"/customers/{customerId}");
       // Just handle HTTP concerns, return data
       return ParseResponse<Customer>(response);
   }
   ```

3. **Direct ViewModel Integration** ❌
   ```csharp
   // WRONG - Service knows about ViewModels
   public class NotificationService
   {
       public void NotifyViewModel(BaseViewModel viewModel, string message) { } // ❌
   }

   // CORRECT - Service handles external notification, Domain/ViewModel consume
   public interface INotificationService
   {
       Task<ErrorOr<bool>> SendPushNotificationAsync(string message);
   }
   ```

4. **Mixing Concerns** ❌
   ```csharp
   // WRONG - API service also handles caching and database
   public class ProductService
   {
       private readonly HttpClient _httpClient;
       private readonly ICacheService _cache;
       private readonly IProductRepository _repository; // ❌ Too many concerns
   }

   // CORRECT - Separation of concerns (Domain orchestrates)
   public class GetProducts
   {
       private readonly IApiService _apiService;
       private readonly ICacheService _cacheService;
       private readonly IProductRepository _repository;

       // Domain orchestrates the caching strategy
   }
   ```
```

#### Package Dependencies
```markdown
## Required NuGet Packages

```xml
<!-- HTTP Client -->
<PackageReference Include="Microsoft.Extensions.Http" Version="8.0.0" />
<PackageReference Include="Refit" Version="7.0.0" /> <!-- Optional REST library -->

<!-- Hardware Services -->
<PackageReference Include="Microsoft.Maui.Essentials" Version="8.0.0" />

<!-- Error Handling -->
<PackageReference Include="ErrorOr" Version="1.2.1" />

<!-- Testing -->
<PackageReference Include="JustEat.HttpClientInterception" Version="4.0.0" />
<!-- OR -->
<PackageReference Include="WireMock.Net" Version="1.5.40" />
```
```

#### Testing Patterns
```markdown
## Testing Strategy

### 1. HTTP Service Testing with Interception
```csharp
using JustEat.HttpClientInterception;

public class ApiServiceTests : IDisposable
{
    private readonly HttpRequestInterceptor _httpInterceptor;
    private readonly IApiService _apiService;

    public ApiServiceTests()
    {
        _httpInterceptor = new HttpRequestInterceptor();
        var httpClient = _httpInterceptor.CreateHttpClient();
        _apiService = new ApiService(httpClient, new LogService());
    }

    [Fact]
    public async Task GetAsync_WhenSuccessful_ReturnsData()
    {
        // Arrange
        var expectedProduct = new Product { Id = "123", Name = "Test" };
        _httpInterceptor.RegisterGetResponse("/products/123", expectedProduct);

        // Act
        var result = await _apiService.GetAsync<Product>("/products/123");

        // Assert
        Assert.False(result.IsError);
        Assert.Equal("Test", result.Value.Name);
    }

    [Fact]
    public async Task GetAsync_WhenNetworkError_ReturnsError()
    {
        // Arrange
        _httpInterceptor.RegisterException(new HttpRequestException("Network error"));

        // Act
        var result = await _apiService.GetAsync<Product>("/products/123");

        // Assert
        Assert.True(result.IsError);
        Assert.Equal("Api.NetworkError", result.FirstError.Code);
    }
}
```

### 2. Hardware Service Testing with Mocks
```csharp
public class LocationServiceTests
{
    [Fact]
    public async Task GetCurrentLocationAsync_WhenPermissionDenied_ReturnsError()
    {
        // Arrange
        var mockGeolocation = new Mock<IGeolocation>();
        mockGeolocation
            .Setup(x => x.GetLocationAsync(It.IsAny<GeolocationRequest>()))
            .ThrowsAsync(new PermissionException("Permission denied"));

        var service = new LocationService(mockGeolocation.Object, new LogService());

        // Act
        var result = await service.GetCurrentLocationAsync();

        // Assert
        Assert.True(result.IsError);
        Assert.Equal("Location.PermissionDenied", result.FirstError.Code);
    }
}
```

### 3. Cache Service Testing
```csharp
public class InMemoryCacheServiceTests
{
    [Fact]
    public async Task GetAsync_WhenExpired_ReturnsNull()
    {
        // Arrange
        var cache = new InMemoryCacheService(new LogService());
        await cache.SetAsync("key1", "value1", TimeSpan.FromMilliseconds(10));
        await Task.Delay(20); // Wait for expiration

        // Act
        var result = await cache.GetAsync<string>("key1");

        // Assert
        Assert.Null(result);
    }

    [Fact]
    public async Task SetAsync_ThenGet_ReturnsValue()
    {
        // Arrange
        var cache = new InMemoryCacheService(new LogService());

        // Act
        await cache.SetAsync("key1", "value1");
        var result = await cache.GetAsync<string>("key1");

        // Assert
        Assert.Equal("value1", result);
    }
}
```
```

## Acceptance Criteria

- [x] Agent markdown file created at `installer/global/templates/maui-appshell/agents/maui-service-specialist.md`
- [x] Agent markdown file created at `installer/global/templates/maui-navigationpage/agents/maui-service-specialist.md`
- [x] Both files contain identical content
- [x] Agent follows standard agent format (frontmatter with metadata)
- [x] Core expertise clearly defined for:
  - [x] HTTP API integration patterns
  - [x] Hardware service patterns (GPS, Camera, Sensors)
  - [x] Caching services (in-memory and persistent)
  - [x] Authentication services
- [x] Clear boundary documented: NO database access in services
- [x] ErrorOr pattern usage documented with examples
- [x] Anti-patterns section includes at least 4 examples
- [x] Testing strategies documented for:
  - [x] HTTP mocking
  - [x] Hardware service mocking
  - [x] Cache testing
- [x] Code examples include:
  - [x] Complete HTTP API service with error handling
  - [x] Hardware service (Location) with permissions
  - [x] Cache service with TTL
- [x] Collaboration patterns documented with maui-domain-specialist
- [x] Package dependencies listed (HttpClient, ErrorOr, testing libraries)
- [x] Interface-first approach emphasized
- [x] Files validated to match existing agent format structure

## Implementation Plan

### Phase 1: Research & Analysis
1. Review existing agent files for format consistency
2. Study Service.cs template implementation
3. Review maui-template-architecture.md for service layer design
4. Analyze maui-usecase-specialist.md for collaboration patterns

### Phase 2: Content Creation
1. Create agent frontmatter with metadata
2. Write core expertise section (5 key areas)
3. Document clear boundaries (NO database, NO business logic)
4. Create comprehensive code examples (3 service types)
5. Document anti-patterns with clear examples
6. Write testing strategies with complete examples
7. Document collaboration patterns
8. List required NuGet packages

### Phase 3: Validation & Refinement
1. Validate agent format matches existing agents
2. Verify all examples compile conceptually
3. Ensure anti-patterns are clear and actionable
4. Review testing examples for completeness
5. Cross-check with architecture documentation

### Phase 4: File Creation
1. Create `maui-appshell/agents/maui-service-specialist.md`
2. Create `maui-navigationpage/agents/maui-service-specialist.md` (copy content)
3. Verify both files are identical
4. Run final validation

## Testing Strategy

Since this is documentation-only, testing will focus on:

### Validation Tests
1. **Format Validation**: Verify agent markdown structure matches existing agents
2. **Content Completeness**: Ensure all required sections are present
3. **Example Compilation**: Verify code examples would compile in a MAUI project
4. **Anti-Pattern Coverage**: Verify all critical anti-patterns documented
5. **File Synchronization**: Verify both template files are identical

### Manual Review Checklist
- [ ] Agent format matches existing MAUI agents
- [ ] All code examples use ErrorOr pattern correctly
- [ ] Clear distinction between Services, Repositories, and Domain
- [ ] Testing strategies are practical and implementable
- [ ] Anti-patterns provide clear guidance
- [ ] Package dependencies are complete and version-appropriate
- [ ] Collaboration patterns are clearly explained

## Success Metrics

- Agent file successfully created for both templates
- Content is comprehensive and actionable
- Clear boundaries prevent architectural violations
- Testing strategies are practical and complete
- Code examples demonstrate best practices
- Anti-patterns guide developers away from common mistakes

## Related Work

### Dependencies
- None (standalone agent creation)

### Follow-up Tasks
- **Phase 2.4**: Create maui-repository-specialist agent for database access
- **Phase 2.5**: Update template integration tests
- **Phase 3.0**: Migrate template commands to use new specialist agents

## Notes

- This agent is critical for maintaining architectural boundaries
- Clear separation between Services (external) and Repositories (database) prevents common mistakes
- ErrorOr pattern usage must be consistent across all layers
- Testing strategies should emphasize mocking external dependencies
- Both template variants (AppShell and NavigationPage) use identical service patterns

## Timeline

- **Estimated Effort**: 4 hours
- **Complexity**: Medium (5/10)
- **Review Mode**: QUICK_OPTIONAL (30-second checkpoint)

---

**Created**: 2025-10-12T10:00:00Z
**Phase**: MAUI Template Migration - Phase 2.3
**Epic**: EPIC-MAUI-TEMPLATE-MIGRATION
