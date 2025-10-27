# .NET Microservice Template

This template provides a complete .NET 8+ microservice structure using FastEndpoints with functional error handling via the Either monad pattern from LanguageExt.

## Template Structure

```
templates/
├── CLAUDE.md                     # Instructions for Claude Code
├── BaseError.cs                  # Base error types for Either monad
├── EndpointEitherExtensions.cs   # Either monad extensions for endpoints
├── FastEndpointsExtensions.cs    # FastEndpoints configuration
├── OpenTelemetryExtensions.cs    # Observability configuration
├── HealthCheckEndpoint.cs        # Health check endpoints
├── SampleEndpoint.cs             # Example endpoint with CRUD operations
├── SampleService.cs              # Example service with Either pattern
├── SampleRepository.cs           # Example repository pattern
├── SampleValidator.cs            # FluentValidation examples
├── SampleEntity.cs               # Domain entity example
├── SampleRequests.cs             # Request DTOs
├── SampleResponses.cs            # Response DTOs
├── SampleDtos.cs                 # Data transfer objects
├── SampleServiceTests.cs         # Unit test examples
├── SampleIntegrationTests.cs     # Integration test examples
├── ApiFactory.cs                 # Test fixture for integration tests
├── Program.cs                    # Application entry point
├── API.csproj                    # API project file
├── Tests.csproj                  # Test project file
├── appsettings.json             # Configuration file
└── Dockerfile                    # Docker container definition
```

## Usage

### Variable Replacement

The template uses the following placeholder variables that should be replaced:

- `{ServiceName}` - The name of your microservice (e.g., "ProductCatalog", "OrderManagement")
- `{Feature}` - The name of your domain feature (e.g., "Product", "Order", "Customer")
- `{feature}` - Lowercase version of feature name for URLs (e.g., "product", "order")

### Creating a New Microservice

1. Copy the template files to your new project directory
2. Replace all occurrences of `{ServiceName}` with your service name
3. Replace all occurrences of `{Feature}` and `{feature}` with your domain feature name
4. Update the namespaces and folder structure as needed
5. Install the required NuGet packages (see project files)
6. Configure your specific business logic

### Key Patterns

#### Either Monad for Error Handling

```csharp
public async Task<Either<BaseError, Product>> GetProductAsync(Guid id)
{
    return await TryAsync(async () =>
    {
        var product = await _repository.GetByIdAsync(id);
        if (product == null)
            return Left<BaseError, Product>(new NotFoundError($"Product {id} not found"));
        return Right<BaseError, Product>(product);
    })
    .IfFail(ex => Left<BaseError, Product>(new ServiceError(ex.Message)));
}
```

#### FastEndpoints Pattern

```csharp
public class GetProductById : Endpoint<GetProductRequest, ProductResponse>
{
    public override void Configure()
    {
        Get("product/{id}");
        AllowAnonymous();
    }
    
    public override async Task HandleAsync(GetProductRequest req, CancellationToken ct)
    {
        var result = await _service.GetProductAsync(req.Id, ct);
        await this.HandleEitherResultAsync(result,
            async product => await SendOkAsync(product, ct),
            ct);
    }
}
```

#### Structured Logging with OpenTelemetry

```csharp
_logger.LogInformation("Processing order {OrderId} for customer {CustomerId}", 
    orderId, customerId);
```

### Testing

The template includes comprehensive testing patterns:

- **Unit Tests**: Test services and business logic in isolation
- **Integration Tests**: Test full API endpoints with test server
- **Test Fixtures**: Shared test infrastructure and utilities

Run tests with:
```bash
dotnet test
dotnet test --filter Category=Unit
dotnet test --filter Category=Integration
```

### Docker Support

Build and run with Docker:
```bash
docker build -t {servicename}:latest .
docker run -p 8080:8080 {servicename}:latest
```

### Health Checks

The service includes three health check endpoints:

- `/health` - Detailed health check with all dependencies
- `/health/live` - Simple liveness check for Kubernetes
- `/health/ready` - Readiness check for traffic routing

### Configuration

The template uses standard .NET configuration with support for:

- Environment variables
- appsettings.json
- User secrets (development)
- Command line arguments

Key configuration sections:

- `Serilog` - Logging configuration
- `OpenTelemetry` - Observability endpoints
- `Authentication` - JWT/OAuth settings
- `ExternalServices` - External API configurations
- `HealthChecks` - Health check settings

## Best Practices

1. **Always use Either monad** for operations that can fail
2. **Create focused endpoints** - one endpoint per operation
3. **Use structured logging** with correlation IDs
4. **Implement comprehensive health checks**
5. **Add OpenTelemetry instrumentation**
6. **Validate all inputs** using FluentValidation
7. **Handle errors functionally** - avoid exceptions
8. **Write tests first** - TDD approach
9. **Keep endpoints thin** - delegate to services
10. **Document APIs** with OpenAPI/Swagger

## Common Extensions

### Adding Database Support

1. Add Entity Framework Core packages
2. Create DbContext
3. Replace in-memory repository with EF repository
4. Add database health check
5. Configure connection string

### Adding Authentication

1. Uncomment authentication code in Program.cs
2. Configure JWT settings
3. Add authorization policies
4. Update endpoints with appropriate policies

### Adding Message Queue

1. Add MassTransit or similar package
2. Create message contracts
3. Add consumers/publishers
4. Configure message broker
5. Add health checks

## Resources

- [FastEndpoints Documentation](https://fast-endpoints.com)
- [LanguageExt Documentation](https://github.com/louthy/language-ext)
- [OpenTelemetry .NET](https://opentelemetry.io/docs/instrumentation/net/)
- [Serilog Documentation](https://serilog.net)
