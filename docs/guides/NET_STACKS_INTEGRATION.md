# .NET Stack Integration for AI Engineer

## Overview

This document describes the integration of .NET-based technology stacks into the AI Engineer system, including:
- **.NET Microservice** - FastEndpoints-based microservices with functional error handling
- **.NET MAUI** - Cross-platform mobile applications with MVVM and UseCases

## Stack Features

### .NET Microservice Stack

#### Core Technologies
- **Framework**: .NET 8.0+ with FastEndpoints (REPR pattern)
- **Functional Programming**: LanguageExt for Either monad error handling
- **Testing**: xUnit with FluentAssertions and integration testing
- **Observability**: OpenTelemetry with Serilog structured logging
- **API Documentation**: OpenAPI/Swagger via FastEndpoints.Swagger

#### Key Patterns
1. **Either Monad Pattern**: All service operations return `Either<Error, Success>`
2. **REPR Pattern**: Request-Endpoint-Response architecture
3. **Clean Architecture**: Domain-driven design with clear layer separation
4. **Outside-In TDD**: Integration tests drive development

#### Project Structure
```
ServiceName.API/
├── Domain/           # Domain entities and errors
├── Endpoints/        # FastEndpoints implementations
├── Services/         # Business logic with Either monad
├── Repositories/     # Data access layer
├── Infrastructure/   # Cross-cutting concerns
├── Models/          # DTOs and view models
└── Validators/      # FluentValidation validators

ServiceName.Tests/
├── Unit/            # Unit tests for services
├── Integration/     # API integration tests
└── Fixtures/        # Test infrastructure
```

### .NET MAUI Stack

#### Core Technologies
- **Framework**: .NET MAUI 8.0 for cross-platform mobile
- **MVVM**: CommunityToolkit.Mvvm for data binding
- **Functional Programming**: LanguageExt for error handling
- **Testing**: xUnit with Outside-In TDD approach
- **HTTP Testing**: JustEat.HttpClientInterception or WireMock

#### Key Patterns
1. **UseCase Pattern**: All business logic in single-responsibility use cases
2. **Either Monad**: Functional error handling throughout
3. **Outside-In TDD**: Test from ViewModel through to mocked APIs
4. **Cache-Aside Pattern**: Strategic caching at UseCase level

#### Project Structure
```
AppName/
├── Core/            # Domain models and interfaces
├── UseCases/        # Business logic implementations
├── Services/        # Infrastructure services
├── ViewModels/      # MVVM view models
├── Views/           # XAML pages and controls
├── Configuration/   # App settings and config
└── Tests/
    ├── Integration/ # Feature tests
    └── Fixtures/    # Test infrastructure
```

## Installation

### Prerequisites
- .NET SDK 8.0 or later
- Visual Studio 2022 or JetBrains Rider
- For MAUI: Platform-specific SDKs (Android, iOS, Windows)

### Using the Templates

1. **Initialize a .NET Microservice Project**:
```bash
agentecflow init dotnet-microservice
cd your-service
dotnet restore
dotnet build
```

2. **Initialize a .NET MAUI Project**:
```bash
agentecflow init maui
cd your-app
dotnet restore
dotnet build
```

## Development Workflow

### .NET Microservice Development

1. **Create an Endpoint**:
```bash
# In Claude Code
/create-endpoint GetProductById
```

2. **Create a Service**:
```bash
/create-service ProductService
```

3. **Run Tests**:
```bash
dotnet test
dotnet test --filter Category=Unit
dotnet test --filter Category=Integration
```

4. **Run the Service**:
```bash
dotnet run --project ServiceName.API
```

### .NET MAUI Development

1. **Create a Page and ViewModel**:
```bash
# In Claude Code
/create-page ProductDetail
```

2. **Create a UseCase**:
```bash
/create-usecase GetProductDetails
```

3. **Run Tests**:
```bash
dotnet test --filter Category=Integration
```

4. **Run the App**:
```bash
# Android
dotnet run --framework net8.0-android

# iOS
dotnet run --framework net8.0-ios

# Windows
dotnet run --framework net8.0-windows
```

## Testing Strategy

### .NET Microservice Testing

#### Unit Tests
```csharp
[Fact]
public async Task GetProduct_WhenExists_ReturnsRight()
{
    // Arrange
    var product = new Product { Id = Guid.NewGuid() };
    _repositoryMock.Setup(x => x.GetByIdAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>()))
        .ReturnsAsync(product);
    
    // Act
    var result = await _service.GetProductAsync(product.Id, CancellationToken.None);
    
    // Assert
    result.IsRight.Should().BeTrue();
    result.IfRight(p => p.Should().Be(product));
}
```

#### Integration Tests
```csharp
[Fact]
public async Task GetProduct_ReturnsOk()
{
    // Arrange
    var productId = Guid.NewGuid();
    _factory.SeedProduct(productId);
    
    // Act
    var response = await _client.GetAsync($"/api/v1/products/{productId}");
    
    // Assert
    response.StatusCode.Should().Be(HttpStatusCode.OK);
}
```

### .NET MAUI Testing (Outside-In TDD)

```csharp
[Fact]
public async Task LoadProduct_WhenApiReturnsProduct_DisplaysProductDetails()
{
    // Arrange - Mock HTTP response
    _httpInterceptor.RegisterGetResponse("/products/123", new Product { Name = "Test" });
    var viewModel = _fixture.GetViewModel<ProductViewModel>();
    
    // Act - Execute ViewModel command as user would
    await viewModel.LoadProductCommand.ExecuteAsync(null);
    
    // Assert - Verify complete behavior
    viewModel.Product.Should().NotBeNull();
    viewModel.Product.Name.Should().Be("Test");
    viewModel.HasError.Should().BeFalse();
}
```

## Quality Gates

Both stacks enforce quality gates:

### Code Coverage
- Microservices: ≥90% coverage
- MAUI Apps: ≥80% coverage

### Complexity
- Maximum cyclomatic complexity: 10
- Maximum file length: 500 lines (microservices), 300 lines (MAUI)

### Performance
- Microservices: P95 response time <200ms
- MAUI: Page load <500ms, 60fps scrolling

## Best Practices

### .NET Microservice Best Practices
1. **Always use Either monad** - No exceptions in business logic
2. **One endpoint per operation** - Follow REPR pattern
3. **Structured logging** - Use correlation IDs throughout
4. **Health checks** - Implement for all dependencies
5. **OpenTelemetry** - Full observability stack

### .NET MAUI Best Practices
1. **UseCases for business logic** - ViewModels only orchestrate
2. **Functional error handling** - Use Either throughout
3. **Outside-In TDD** - Test user behavior, not implementation
4. **Cache strategically** - Balance performance with freshness
5. **Loading states** - Always provide user feedback

## Migration from Existing Projects

### Converting to Either Monad Pattern
```csharp
// Before (traditional try-catch)
public async Task<Product> GetProductAsync(Guid id)
{
    try
    {
        var product = await _repository.GetByIdAsync(id);
        if (product == null)
            throw new NotFoundException("Product not found");
        return product;
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error getting product");
        throw;
    }
}

// After (Either monad)
public async Task<Either<BaseError, Product>> GetProductAsync(Guid id, CancellationToken ct)
{
    return await TryAsync(async () =>
    {
        var product = await _repository.GetByIdAsync(id, ct);
        if (product == null)
            return Left<BaseError, Product>(new NotFoundError($"Product {id} not found"));
        return Right<BaseError, Product>(product);
    })
    .IfFail(ex => Left<BaseError, Product>(new ServiceError(ex.Message)));
}
```

## Troubleshooting

### Common Issues

1. **NuGet Package Conflicts**
   - Solution: Ensure all packages target .NET 8.0
   - Use `dotnet list package --outdated` to check versions

2. **Either Monad Compilation Errors**
   - Solution: Add `using static LanguageExt.Prelude;`
   - Ensure LanguageExt.Core package is installed

3. **MAUI Platform-Specific Issues**
   - Android: Check minimum API level (21+)
   - iOS: Ensure Xcode is installed and updated
   - Windows: Check Windows SDK version

4. **Test Discovery Issues**
   - Solution: Clean and rebuild solution
   - Ensure test project references are correct

## Resources

### Documentation
- [FastEndpoints Documentation](https://fast-endpoints.com)
- [LanguageExt Documentation](https://github.com/louthy/language-ext)
- [.NET MAUI Documentation](https://docs.microsoft.com/dotnet/maui)
- [CommunityToolkit.Mvvm](https://learn.microsoft.com/dotnet/communitytoolkit/mvvm/)

### Example Projects
- Microservice: See `installer/global/templates/dotnet-microservice/`
- MAUI: See `installer/global/templates/maui/`

### Learning Resources
- [Functional Programming in C#](https://docs.microsoft.com/dotnet/csharp/programming-guide/concepts/functional-programming/)
- [Outside-In TDD](https://outsidein.dev/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## Contributing

When adding new features to the .NET stacks:

1. Follow the established patterns (Either monad, REPR, UseCase)
2. Add comprehensive tests (unit and integration)
3. Update templates in `.claude/stacks/[stack]/templates/`
4. Document new patterns in the stack's CLAUDE.md file
5. Ensure quality gates pass

## License

MIT - See LICENSE file for details
