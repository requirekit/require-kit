# .NET Microservice Project Context for Claude Code

This is a .NET 8+ microservice project using FastEndpoints with functional error handling via the Either monad pattern from LanguageExt.

## Technology Stack
- **Framework**: .NET 8.0+ with FastEndpoints (not traditional ASP.NET Controllers)
- **Architecture**: REPR Pattern (Request-Endpoint-Response) with Domain-Driven Design
- **Error Handling**: Either Monad via LanguageExt library
- **Testing**: xUnit with FluentAssertions
- **API Documentation**: OpenAPI/Swagger via FastEndpoints.Swagger
- **Observability**: OpenTelemetry with Serilog structured logging
- **Authentication**: JWT Bearer tokens (Keycloak-ready)
- **Validation**: FluentValidation via FastEndpoints
- **HTTP Client**: Typed clients with Polly resilience
- **Health Checks**: ASP.NET Core Health Checks

## Project Structure

### API Project Structure
```
{ServiceName}.API/
├── .claude/              # Agentic Flow configuration
├── Program.cs            # Application entry point with DI setup
├── appsettings.json      # Configuration
├── Domain/
│   ├── BaseError.cs     # Base error type for Either monad
│   ├── DomainErrors.cs  # Specific error types
│   ├── Entities/        # Domain entities
│   └── ValueObjects/    # Domain value objects
├── Endpoints/
│   ├── Health/
│   │   └── HealthCheck.cs
│   └── {Feature}/
│       ├── Create{Feature}.cs
│       ├── Get{Feature}.cs
│       ├── Update{Feature}.cs
│       └── Delete{Feature}.cs
├── Services/
│   ├── Interfaces/
│   │   └── I{Service}.cs
│   └── Implementations/
│       └── {Service}.cs
├── Repositories/
│   ├── Interfaces/
│   │   └── I{Repository}.cs
│   └── Implementations/
│       └── {Repository}.cs
├── Infrastructure/
│   ├── Extensions/
│   │   ├── EndpointEitherExtensions.cs
│   │   ├── FastEndpointsExtensions.cs
│   │   └── OpenTelemetryExtensions.cs
│   ├── Authentication/
│   │   └── AuthenticationExtensions.cs
│   ├── HttpClients/
│   │   └── Typed HTTP clients
│   └── Middleware/
│       └── Custom middleware
├── Models/
│   ├── Requests/        # Request DTOs
│   ├── Responses/       # Response DTOs
│   └── Dtos/           # Data transfer objects
├── Validators/
│   └── {Feature}Validator.cs
└── Dockerfile

{ServiceName}.Tests/
├── Unit/
│   ├── Services/
│   ├── Repositories/
│   └── Validators/
├── Integration/
│   ├── Endpoints/
│   └── Fixtures/
│       └── ApiFactory.cs
└── TestHelpers/
    └── HttpTestHelpers.cs
```

## Development Standards

### FastEndpoints Pattern
```csharp
public class Get{Feature}ById : Endpoint<Get{Feature}Request, Get{Feature}Response>
{
    private readonly I{Feature}Service _service;
    private readonly ILogger<Get{Feature}ById> _logger;
    
    public Get{Feature}ById(I{Feature}Service service, ILogger<Get{Feature}ById> logger)
    {
        _service = service;
        _logger = logger;
    }
    
    public override void Configure()
    {
        Get("{resource}/{id}");
        AllowAnonymous(); // or Policies("PolicyName")
        
        Description(b => b
            .Produces<Get{Feature}Response>(200)
            .ProducesProblem(404)
            .ProducesProblem(500)
            .WithName("Get{Feature}")
            .WithTags("{Feature}"));
    }
    
    public override async Task HandleAsync(Get{Feature}Request req, CancellationToken ct)
    {
        var result = await _service.Get{Feature}Async(req.Id, ct);
        
        await this.HandleEitherResultAsync(
            result,
            async response => await SendOkAsync(response, ct),
            ct
        );
    }
}
```

### Service Pattern with Either Monad
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

public interface I{Feature}Service
{
    Task<Either<BaseError, {Feature}>> Get{Feature}Async(Guid id, CancellationToken ct);
    Task<Either<BaseError, {Feature}>> Create{Feature}Async(Create{Feature}Dto dto, CancellationToken ct);
    Task<Either<BaseError, {Feature}>> Update{Feature}Async(Guid id, Update{Feature}Dto dto, CancellationToken ct);
    Task<Either<BaseError, Unit>> Delete{Feature}Async(Guid id, CancellationToken ct);
}

public class {Feature}Service : I{Feature}Service
{
    private readonly I{Feature}Repository _repository;
    private readonly ILogger<{Feature}Service> _logger;
    
    public {Feature}Service(I{Feature}Repository repository, ILogger<{Feature}Service> logger)
    {
        _repository = repository;
        _logger = logger;
    }
    
    public async Task<Either<BaseError, {Feature}>> Get{Feature}Async(Guid id, CancellationToken ct)
    {
        return await TryAsync(async () =>
        {
            var entity = await _repository.GetByIdAsync(id, ct);
            
            if (entity == null)
            {
                return Left<BaseError, {Feature}>(
                    new NotFoundError($"{Feature} with ID {id} not found"));
            }
            
            return Right<BaseError, {Feature}>(entity);
        })
        .IfFail(ex =>
        {
            _logger.LogError(ex, "Error retrieving {Feature} with ID {Id}", id);
            return Left<BaseError, {Feature}>(
                new ServiceError($"Failed to retrieve {Feature}: {ex.Message}"));
        });
    }
}
```

### Domain Errors
```csharp
using Microsoft.AspNetCore.Http;

public abstract record BaseError(string Message)
{
    public virtual int StatusCode => StatusCodes.Status500InternalServerError;
}

public record ValidationError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status400BadRequest;
}

public record NotFoundError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status404NotFound;
}

public record UnauthorizedError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status401Unauthorized;
}

public record ForbiddenError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status403Forbidden;
}

public record ConflictError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status409Conflict;
}

public record ServiceError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status500InternalServerError;
}

public record ExternalServiceError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status502BadGateway;
}
```

### Either Extensions for Endpoints
```csharp
public static class EndpointEitherExtensions
{
    public static async Task HandleEitherResultAsync<TRequest, TResponse, TError, TSuccess>(
        this Endpoint<TRequest, TResponse> endpoint,
        Either<TError, TSuccess> result,
        Func<TSuccess, Task> successHandler,
        CancellationToken ct
    )
        where TRequest : notnull
        where TError : BaseError
    {
        await result.Match(
            Right: async success =>
            {
                try
                {
                    await successHandler(success);
                }
                catch (Exception ex)
                {
                    endpoint.Logger.LogError(ex, "Error in success handler");
                    endpoint.AddError($"Error processing response: {ex.Message}");
                    await endpoint.HttpContext.Response.SendErrorsAsync(
                        endpoint.ValidationFailures,
                        StatusCodes.Status500InternalServerError,
                        null,
                        ct);
                }
            },
            Left: async error =>
            {
                await endpoint.HandleErrorAsync(error, ct);
            }
        );
    }
    
    public static async Task HandleErrorAsync<TRequest, TResponse, TError>(
        this Endpoint<TRequest, TResponse> endpoint,
        TError error,
        CancellationToken ct
    )
        where TRequest : notnull
        where TError : BaseError
    {
        endpoint.Logger.LogError("Domain error occurred: {ErrorMessage}", error.Message);
        endpoint.AddError(error.Message);
        
        await endpoint.HttpContext.Response.SendErrorsAsync(
            endpoint.ValidationFailures,
            error.StatusCode,
            null,
            ct);
    }
}
```

### Validation Pattern
```csharp
public class Create{Feature}Validator : Validator<Create{Feature}Request>
{
    public Create{Feature}Validator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters");
        
        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Invalid email format");
        
        RuleFor(x => x.Value)
            .GreaterThan(0).WithMessage("Value must be greater than zero");
    }
}
```

## NuGet Packages Required

```xml
<!-- Core packages -->
<PackageReference Include="FastEndpoints" Version="6.2.0" />
<PackageReference Include="FastEndpoints.Swagger" Version="6.2.0" />
<PackageReference Include="LanguageExt.Core" Version="4.4.9" />

<!-- Authentication -->
<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.14" />

<!-- Observability -->
<PackageReference Include="OpenTelemetry" Version="1.11.2" />
<PackageReference Include="OpenTelemetry.Exporter.OpenTelemetryProtocol" Version="1.11.2" />
<PackageReference Include="OpenTelemetry.Extensions.Hosting" Version="1.11.2" />
<PackageReference Include="OpenTelemetry.Instrumentation.AspNetCore" Version="1.11.1" />
<PackageReference Include="OpenTelemetry.Instrumentation.Http" Version="1.11.1" />
<PackageReference Include="Serilog.AspNetCore" Version="9.0.0" />
<PackageReference Include="Serilog.Sinks.Console" Version="6.0.0" />
<PackageReference Include="Serilog.Sinks.OpenTelemetry" Version="4.1.1" />

<!-- Health Checks -->
<PackageReference Include="AspNetCore.HealthChecks.Uris" Version="9.0.0" />

<!-- HTTP Resilience -->
<PackageReference Include="Microsoft.Extensions.Http.Polly" Version="8.0.0" />

<!-- Testing packages -->
<PackageReference Include="xunit" Version="2.6.1" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.5.3" />
<PackageReference Include="FluentAssertions" Version="6.12.0" />
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
<PackageReference Include="Moq" Version="4.20.0" />
```

## Testing Patterns

### Integration Testing
```csharp
public class {Feature}EndpointTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    private readonly HttpClient _client;
    
    public {Feature}EndpointTests(ApiFactory factory)
    {
        _factory = factory;
        _client = _factory.CreateClient();
    }
    
    [Fact]
    public async Task Get{Feature}_WhenExists_ReturnsOk()
    {
        // Arrange
        var id = Guid.NewGuid();
        _factory.Seed{Feature}(id);
        
        // Act
        var response = await _client.GetAsync($"/api/v1/{feature}/{id}");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var content = await response.Content.ReadFromJsonAsync<{Feature}Response>();
        content.Should().NotBeNull();
        content.Id.Should().Be(id);
    }
    
    [Fact]
    public async Task Get{Feature}_WhenNotFound_Returns404()
    {
        // Act
        var response = await _client.GetAsync($"/api/v1/{feature}/{Guid.NewGuid()}");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails.Status.Should().Be(404);
    }
}
```

### Unit Testing Services
```csharp
public class {Feature}ServiceTests
{
    private readonly Mock<I{Feature}Repository> _repositoryMock;
    private readonly {Feature}Service _service;
    
    public {Feature}ServiceTests()
    {
        _repositoryMock = new Mock<I{Feature}Repository>();
        var logger = new Mock<ILogger<{Feature}Service>>();
        _service = new {Feature}Service(_repositoryMock.Object, logger.Object);
    }
    
    [Fact]
    public async Task Get{Feature}_WhenExists_ReturnsRight()
    {
        // Arrange
        var id = Guid.NewGuid();
        var expected = new {Feature} { Id = id, Name = "Test" };
        _repositoryMock.Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(expected);
        
        // Act
        var result = await _service.Get{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsRight.Should().BeTrue();
        result.IfRight(entity => entity.Should().Be(expected));
    }
    
    [Fact]
    public async Task Get{Feature}_WhenNotFound_ReturnsLeft()
    {
        // Arrange
        var id = Guid.NewGuid();
        _repositoryMock.Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(({Feature})null);
        
        // Act
        var result = await _service.Get{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsLeft.Should().BeTrue();
        result.IfLeft(error =>
        {
            error.Should().BeOfType<NotFoundError>();
            error.StatusCode.Should().Be(404);
        });
    }
}
```

## Program.cs Configuration

```csharp
using Serilog;
using {ServiceName}.API.Infrastructure.Extensions;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
builder.Host.UseSerilog((context, config) =>
{
    config.ReadFrom.Configuration(context.Configuration);
});

// Add services
builder.Services.AddFastendpointsServices(builder.Configuration);
builder.Services.AddOpenTelemetryServices(builder.Configuration);
builder.Services.AddHealthChecks();
builder.Services.AddAuthentication(builder.Configuration);

// Register domain services
builder.Services.AddScoped<I{Feature}Service, {Feature}Service>();
builder.Services.AddScoped<I{Feature}Repository, {Feature}Repository>();

// Add HTTP clients
builder.Services.AddHttpClient<IExternalApiClient, ExternalApiClient>()
    .AddPolicyHandler(GetRetryPolicy())
    .AddPolicyHandler(GetCircuitBreakerPolicy());

var app = builder.Build();

// Configure pipeline
app.UseApiConfiguration(app.Environment, "{ServiceName}", "v1");
app.MapHealthChecks("/health");

app.Run();
```

## Available Commands

### Development
```bash
# Build and run
dotnet build
dotnet run

# Watch mode
dotnet watch run

# Testing
dotnet test                          # Run all tests
dotnet test --filter Category=Unit   # Run unit tests only
dotnet test --filter Category=Integration  # Run integration tests only
dotnet test --collect:"XPlat Code Coverage"  # Generate coverage report

# Code Quality
dotnet format                        # Format code
dotnet analyzers                     # Run analyzers
```

## Microservice-Specific Commands

### Endpoint Generation
Use `/create-endpoint {Feature}{Action}` to generate:
- Endpoint class with Either pattern
- Request/Response DTOs
- Validator
- Integration test
- Service method stub

### Service Generation
Use `/create-service {Service}Name` to generate:
- Service interface
- Service implementation with Either pattern
- Repository interface
- Unit tests
- DI registration

### Domain Entity Generation
Use `/create-entity {Entity}Name` to generate:
- Domain entity
- Value objects
- Domain errors
- Repository interface

## OpenTelemetry Configuration

```csharp
public static class OpenTelemetryExtensions
{
    public static IServiceCollection AddOpenTelemetryServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddOpenTelemetry()
            .WithTracing(builder =>
            {
                builder
                    .SetResourceBuilder(ResourceBuilder.CreateDefault()
                        .AddService("{ServiceName}"))
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddOtlpExporter(options =>
                    {
                        options.Endpoint = new Uri(configuration["OpenTelemetry:Endpoint"]);
                    });
            })
            .WithMetrics(builder =>
            {
                builder
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddPrometheusExporter();
            });
        
        return services;
    }
}
```

## Health Checks

```csharp
public class HealthCheck : EndpointWithoutRequest<HealthCheckResponse>
{
    private readonly IHealthCheckService _healthCheckService;
    
    public HealthCheck(IHealthCheckService healthCheckService)
    {
        _healthCheckService = healthCheckService;
    }
    
    public override void Configure()
    {
        Get("/health");
        AllowAnonymous();
    }
    
    public override async Task HandleAsync(CancellationToken ct)
    {
        var health = await _healthCheckService.CheckHealthAsync();
        
        var response = new HealthCheckResponse
        {
            Status = health.Status.ToString(),
            Checks = health.Entries.Select(x => new HealthCheckItem
            {
                Name = x.Key,
                Status = x.Value.Status.ToString(),
                Description = x.Value.Description
            }).ToList()
        };
        
        await SendOkAsync(response, ct);
    }
}
```

## Configuration Management

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    }
  },
  "OpenTelemetry": {
    "Endpoint": "http://localhost:4317"
  },
  "Authentication": {
    "Authority": "https://keycloak.example.com/realms/your-realm",
    "Audience": "your-audience"
  },
  "ExternalServices": {
    "ApiBaseUrl": "https://api.example.com",
    "Timeout": 30
  }
}
```

## Performance Requirements
- API response time < 200ms (P95)
- Database query time < 50ms
- Memory usage < 512MB
- Support 1000 concurrent connections
- Circuit breaker triggers after 5 consecutive failures

## Security Requirements
- JWT authentication for protected endpoints
- Input validation on all endpoints
- SQL injection prevention via parameterized queries
- Rate limiting per client
- CORS configuration for allowed origins
- Secrets management via configuration providers

## Best Practices
1. **Always use Either monad** for operations that can fail
2. **Create focused endpoints** - one endpoint per operation
3. **Use structured logging** with correlation IDs
4. **Implement health checks** for all external dependencies
5. **Add OpenTelemetry** instrumentation for observability
6. **Validate all inputs** using FluentValidation
7. **Handle errors functionally** - avoid throwing exceptions
8. **Use typed HTTP clients** with resilience policies
9. **Keep endpoints thin** - delegate to services
10. **Test behavior, not implementation** - focus on contracts

## Common Patterns

### Pagination
```csharp
public class GetPagedRequest
{
    [FromQuery] public int Page { get; set; } = 1;
    [FromQuery] public int PageSize { get; set; } = 20;
}

public class PagedResponse<T>
{
    public List<T> Data { get; set; }
    public int TotalCount { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
}
```

### Caching
```csharp
public async Task<Either<BaseError, T>> GetWithCacheAsync<T>(
    string key,
    Func<Task<T>> factory,
    TimeSpan? expiry = null)
{
    return await TryAsync(async () =>
    {
        if (_cache.TryGetValue(key, out T cached))
            return cached;
        
        var value = await factory();
        _cache.Set(key, value, expiry ?? TimeSpan.FromMinutes(5));
        return value;
    })
    .ToEither(ex => new ServiceError($"Cache operation failed: {ex.Message}"));
}
```

### Audit Logging
```csharp
public class AuditMiddleware
{
    public async Task InvokeAsync(HttpContext context)
    {
        var userId = context.User?.FindFirst("sub")?.Value;
        
        using (LogContext.PushProperty("UserId", userId))
        using (LogContext.PushProperty("CorrelationId", context.TraceIdentifier))
        {
            await _next(context);
        }
    }
}
```

## Resources
- [FastEndpoints Documentation](https://fast-endpoints.com)
- [LanguageExt Documentation](https://github.com/louthy/language-ext)
- [OpenTelemetry .NET](https://opentelemetry.io/docs/instrumentation/net/)
- [Serilog Documentation](https://serilog.net)
