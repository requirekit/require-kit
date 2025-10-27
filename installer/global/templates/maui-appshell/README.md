# .NET MAUI AppShell Template

## Overview

This template provides a complete .NET MAUI architecture using:
- **AppShell Navigation**: Shell-based routing with flyout menu
- **Domain Pattern**: Verb-based operations (GetProducts, CreateOrder) with clear business intent
- **Repository Pattern**: Interface-based database access abstraction
- **Service Pattern**: Interface-based external system integration
- **ErrorOr Pattern**: Functional error handling (no exceptions)
- **MVVM Pattern**: CommunityToolkit.Mvvm for presentation logic
- **Dependency Injection**: Microsoft.Extensions.DependencyInjection

## Architecture

### Layer Structure

```
Domain Layer
├── Operations (GetProducts, CreateOrder, etc.)
├── Repositories (IProductRepository, IOrderRepository)
└── Services (IAuthenticationService, IPaymentService)

Data Layer
└── Repositories (ProductRepository, OrderRepository)

Infrastructure Layer
└── Services (AuthenticationService, PaymentService)

Presentation Layer
├── Pages (ProductListPage, OrderDetailsPage)
└── ViewModels (ProductListViewModel, OrderDetailsViewModel)
```

### Naming Conventions

**Domain Operations**: `{Verb}{Entity}`
- Examples: `GetProducts`, `CreateOrder`, `UpdateCustomer`
- Prohibited: ~~GetProductsUseCase~~, ~~GetProductsEngine~~, ~~GetProductsHandler~~

**Repositories**: `I{Entity}Repository` / `{Entity}Repository`
- Examples: `IProductRepository` / `ProductRepository`

**Services**: `I{Purpose}Service` / `{Purpose}Service`
- Examples: `IAuthenticationService` / `AuthenticationService`

**Presentation**: `{Feature}Page` / `{Feature}ViewModel`
- Examples: `ProductListPage` / `ProductListViewModel`

## Files Included

### Configuration Files (3)
- `manifest.json` - Template metadata and architecture definition
- `settings.json` - Naming conventions and layer configuration
- `CLAUDE.md` - Comprehensive guidance for Claude Code

### Code Templates (13)

**Domain (2)**
- `domain/query-operation.cs.template` - Read-only operations
- `domain/command-operation.cs.template` - Write operations with validation

**Repository (2)**
- `repository/repository-interface.cs.template` - Repository contract
- `repository/repository-implementation.cs.template` - EF Core implementation

**Service (2)**
- `service/service-interface.cs.template` - Service contract
- `service/service-implementation.cs.template` - HTTP client implementation

**Presentation (4)**
- `presentation/page.xaml.template` - MAUI page markup
- `presentation/page.xaml.cs.template` - Page code-behind
- `presentation/viewmodel.cs.template` - ViewModel with commands
- `presentation/navigation-service.cs.template` - Navigation abstraction

**Testing (3)**
- `testing/domain-test.cs.template` - Domain operation tests
- `testing/repository-test.cs.template` - Repository tests (in-memory DB)
- `testing/service-test.cs.template` - Service tests (mocked HttpClient)

### Agent Specifications (3)
- `agents/maui-appshell-domain-specialist.md` - Domain operation expert
- `agents/maui-appshell-repository-specialist.md` - Repository pattern expert
- `agents/maui-appshell-service-specialist.md` - Service integration expert

## Template Placeholders

### Project-Level
- `{{ProjectName}}` - Root project name
- `{{RootNamespace}}` - Root namespace

### Feature-Level
- `{{FeatureName}}` - Feature/module name
- `{{Entity}}` - Entity/model name
- `{{Verb}}` - Action verb (Get, Create, Update, Delete)

### Operation-Level
- `{{OperationName}}` - Complete operation name
- `{{ReturnType}}` - Return type of operation
- `{{Parameters}}` - Method parameters
- `{{RequestType}}` - Request object type

### Repository-Level
- `{{RepositoryName}}` - Repository name
- `{{RepositoryMethod}}` - Repository method name
- `{{DbContextName}}` - DbContext class name

### Service-Level
- `{{ServiceName}}` - Service name
- `{{Purpose}}` - Service purpose/responsibility
- `{{Endpoint}}` - API endpoint URL

### Presentation-Level
- `{{PageName}}` - Page class name
- `{{ViewModelName}}` - ViewModel class name
- `{{PageTitle}}` - Page display title
- `{{ItemType}}` - Collection item type

## Prerequisites

### Required SDK/Workload
```bash
dotnet --version  # Requires .NET 8.0+
dotnet workload install maui
```

### Required NuGet Packages
```xml
<PackageReference Include="ErrorOr" Version="2.0.0" />
<PackageReference Include="CommunityToolkit.Mvvm" Version="8.2.0" />
<PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="8.0.0" />

<!-- Testing -->
<PackageReference Include="xunit" Version="2.6.0" />
<PackageReference Include="FluentAssertions" Version="6.12.0" />
<PackageReference Include="NSubstitute" Version="5.1.0" />
```

## Quality Gates

### Required
- All tests passing (100%)
- ErrorOr used for all fallible operations
- Interfaces for all repositories and services
- Verb-based domain operation naming (no UseCase/Engine suffixes)
- AppShell routing configured correctly
- Dependency injection configured in MauiProgram.cs

### Recommended
- 80%+ line coverage
- 75%+ branch coverage
- No code duplication (DRY principle)
- SOLID principles followed

## Quick Start

### 1. Create Domain Operation
```csharp
public class GetProducts
{
    private readonly IProductRepository _repository;

    public GetProducts(IProductRepository repository)
    {
        _repository = repository;
    }

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}
```

### 2. Create Repository
```csharp
public interface IProductRepository
{
    Task<ErrorOr<List<Product>>> GetAllAsync();
}

public class ProductRepository : IProductRepository
{
    private readonly AppDbContext _context;

    public async Task<ErrorOr<List<Product>>> GetAllAsync()
    {
        var products = await _context.Products.AsNoTracking().ToListAsync();
        return products;
    }
}
```

### 3. Create ViewModel
```csharp
public partial class ProductListViewModel : ObservableObject
{
    private readonly GetProducts _getProducts;

    [ObservableProperty]
    private ObservableCollection<Product> _products = new();

    [RelayCommand]
    private async Task LoadAsync()
    {
        var result = await _getProducts.ExecuteAsync();
        result.Switch(
            products => Products = new ObservableCollection<Product>(products),
            errors => ErrorMessage = errors.First().Description
        );
    }
}
```

### 4. Register Dependencies
```csharp
// MauiProgram.cs
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddTransient<GetProducts>();
builder.Services.AddTransient<ProductListViewModel>();
builder.Services.AddTransient<ProductListPage>();
```

### 5. Configure AppShell Navigation
```csharp
// AppShell.xaml.cs
Routing.RegisterRoute("product-details", typeof(ProductDetailsPage));

// Navigate
await Shell.Current.GoToAsync("product-details");
```

## Testing Strategy

### Outside-In TDD
1. Write ViewModel test (acceptance test)
2. Write Domain operation test
3. Write Repository/Service test
4. Implement code to pass tests

### Example Test
```csharp
public class GetProductsTests
{
    [Fact]
    public async Task ExecuteAsync_WhenRepositorySucceeds_ReturnsProducts()
    {
        // Arrange
        var repository = Substitute.For<IProductRepository>();
        var products = new List<Product> { new Product() };
        repository.GetAllAsync().Returns(products);
        var sut = new GetProducts(repository);

        // Act
        var result = await sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Should().BeEquivalentTo(products);
    }
}
```

## Architectural Principles

### SOLID Compliance
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes substitutable for base types
- **Interface Segregation**: Many specific interfaces over one general interface
- **Dependency Inversion**: Depend on abstractions, not concretions

### DRY Principle
- No code duplication
- Extract common patterns
- Reusable templates and components

### YAGNI Principle
- Implement only what's required
- No speculative features
- Keep it simple

## Error Handling

### ErrorOr Pattern
All operations return `ErrorOr<TValue>` instead of throwing exceptions.

**Success**:
```csharp
ErrorOr<Product> result = product;
```

**Error**:
```csharp
return Error.NotFound("Product.NotFound", "Product not found");
return Error.Validation("Product.Name.Required", "Name is required");
return Error.Unexpected("Product.Database.Error", ex.Message);
```

**Consumption**:
```csharp
result.Switch(
    value => HandleSuccess(value),
    errors => HandleErrors(errors)
);
```

## Additional Resources

- [.NET MAUI Documentation](https://learn.microsoft.com/en-us/dotnet/maui/)
- [ErrorOr Library](https://github.com/amantinband/error-or)
- [CommunityToolkit.Mvvm](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/)
- [AppShell Navigation](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/)

## Version

- **Version**: 1.0.0
- **Created**: 2025-10-12
- **Last Updated**: 2025-10-12
- **Author**: Agentecflow System

## License

This template is part of the Agentecflow system and follows the same licensing terms as the parent project.
