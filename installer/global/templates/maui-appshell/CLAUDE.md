# .NET MAUI AppShell Template - Claude Code Guidance

## Template Overview

This template provides a complete .NET MAUI architecture using AppShell navigation, verb-based Domain operations, Repository/Service split, and ErrorOr functional error handling.

## Architecture Patterns

### 1. Domain Pattern (Verb-Based Operations)

**Philosophy**: Domain operations are named after business actions, NOT technical patterns.

**Naming Convention**: `{Verb}{Entity}`

**Examples**:
- `GetProducts` - Query products from repository
- `CreateOrder` - Create new order with validation
- `UpdateCustomer` - Update customer information
- `DeleteProduct` - Remove product (soft or hard delete)

**PROHIBITED Naming**:
- ~~GetProductsUseCase~~ - No "UseCase" suffix
- ~~GetProductsEngine~~ - No "Engine" suffix
- ~~GetProductsHandler~~ - No "Handler" suffix
- ~~GetProductsProcessor~~ - No "Processor" suffix

**Structure**:
```csharp
namespace {{ProjectName}}.Domain.{{Feature}};

public class {{Verb}}{{Entity}}
{
    private readonly I{{Entity}}Repository _repository;

    public {{Verb}}{{Entity}}(I{{Entity}}Repository repository)
    {
        _repository = repository;
    }

    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync({{Parameters}})
    {
        // 1. Validate inputs
        var validationResult = ValidateInputs(parameters);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // 2. Execute business logic
        var result = await _repository.MethodAsync(parameters);

        // 3. Return ErrorOr result
        return result;
    }
}
```

**Usage in ViewModels**:
```csharp
public class ProductListViewModel : ObservableObject
{
    private readonly GetProducts _getProducts;

    [RelayCommand]
    private async Task LoadProductsAsync()
    {
        var result = await _getProducts.ExecuteAsync();

        result.Switch(
            products => Products = new ObservableCollection<Product>(products),
            errors => ShowError(errors)
        );
    }
}
```

### 2. Repository Pattern (Database Access)

**Purpose**: Abstract database access behind interfaces.

**Naming Convention**: `I{Entity}Repository` / `{Entity}Repository`

**Interface Structure**:
```csharp
namespace {{ProjectName}}.Domain.Repositories;

public interface I{{Entity}}Repository
{
    Task<ErrorOr<List<{{Entity}}>>> GetAllAsync();
    Task<ErrorOr<{{Entity}}>> GetByIdAsync(Guid id);
    Task<ErrorOr<{{Entity}}>> CreateAsync({{Entity}} entity);
    Task<ErrorOr<{{Entity}}>> UpdateAsync({{Entity}} entity);
    Task<ErrorOr<Deleted>> DeleteAsync(Guid id);
}
```

**Implementation Structure**:
```csharp
namespace {{ProjectName}}.Data.Repositories;

public class {{Entity}}Repository : I{{Entity}}Repository
{
    private readonly DbContext _context;

    public {{Entity}}Repository(DbContext context)
    {
        _context = context;
    }

    public async Task<ErrorOr<List<{{Entity}}>>> GetAllAsync()
    {
        try
        {
            var entities = await _context.{{Entity}}s.ToListAsync();
            return entities;
        }
        catch (Exception ex)
        {
            return Error.Unexpected("{{Entity}}.GetAll.Failed", ex.Message);
        }
    }
}
```

**When to Use Repositories**:
- Database queries (EF Core, SQLite, etc.)
- Local storage access
- Data persistence operations
- CRUD operations on entities

**When NOT to Use Repositories**:
- API calls (use Services)
- File system operations (use Services)
- External integrations (use Services)

### 3. Service Pattern (External Integrations)

**Purpose**: Abstract external system integrations behind interfaces.

**Naming Convention**: `I{Purpose}Service` / `{Purpose}Service`

**Interface Structure**:
```csharp
namespace {{ProjectName}}.Domain.Services;

public interface I{{Purpose}}Service
{
    Task<ErrorOr<{{ReturnType}}>> {{Method}}Async({{Parameters}});
}
```

**Implementation Structure**:
```csharp
namespace {{ProjectName}}.Infrastructure.Services;

public class {{Purpose}}Service : I{{Purpose}}Service
{
    private readonly HttpClient _httpClient;

    public {{Purpose}}Service(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<ErrorOr<{{ReturnType}}>> {{Method}}Async({{Parameters}})
    {
        try
        {
            var response = await _httpClient.GetAsync(endpoint);

            if (!response.IsSuccessStatusCode)
            {
                return Error.Unexpected(
                    "{{Purpose}}.{{Method}}.Failed",
                    $"Status: {response.StatusCode}"
                );
            }

            var result = await response.Content.ReadFromJsonAsync<{{ReturnType}}>();
            return result ?? Error.NotFound("{{Purpose}}.{{Method}}.NotFound", "No data");
        }
        catch (Exception ex)
        {
            return Error.Unexpected("{{Purpose}}.{{Method}}.Exception", ex.Message);
        }
    }
}
```

**When to Use Services**:
- REST API calls
- Authentication/authorization
- Third-party SDK integrations
- Cloud service operations
- File system operations
- Device hardware access

**When NOT to Use Services**:
- Database operations (use Repositories)
- In-memory data manipulation (use Domain)

### 4. ErrorOr Pattern (Functional Error Handling)

**Library**: `ErrorOr` 2.0+

**Philosophy**: Operations return `ErrorOr<T>` instead of throwing exceptions.

**Creating Success Results**:
```csharp
// Implicit conversion
ErrorOr<Product> result = product;

// Explicit creation
return ErrorOr<Product>.From(product);
```

**Creating Error Results**:
```csharp
// Validation error
return Error.Validation("Product.Name.Required", "Product name is required");

// Not found error
return Error.NotFound("Product.NotFound", $"Product {id} not found");

// Conflict error
return Error.Conflict("Product.Duplicate", "Product already exists");

// Unexpected error
return Error.Unexpected("Product.DatabaseError", ex.Message);
```

**Consuming ErrorOr Results**:
```csharp
// Pattern 1: Switch (void return)
result.Switch(
    value => Console.WriteLine(value),
    errors => Console.WriteLine(errors.First().Description)
);

// Pattern 2: Match (with return value)
var message = result.Match(
    value => $"Success: {value}",
    errors => $"Error: {errors.First().Description}"
);

// Pattern 3: IsError check
if (result.IsError)
{
    var firstError = result.FirstError;
    Console.WriteLine(firstError.Description);
    return;
}

var value = result.Value;
```

**Error Types**:
- `Error.Validation()` - Invalid input data
- `Error.NotFound()` - Resource not found
- `Error.Conflict()` - Duplicate or conflicting data
- `Error.Unauthorized()` - Authentication required
- `Error.Forbidden()` - Insufficient permissions
- `Error.Unexpected()` - Unexpected system errors

### 5. MVVM Pattern with CommunityToolkit.Mvvm

**ViewModel Structure**:
```csharp
namespace {{ProjectName}}.Presentation.{{Feature}};

public partial class {{Feature}}ViewModel : ObservableObject
{
    private readonly {{DomainOperation}} _operation;

    [ObservableProperty]
    private ObservableCollection<{{Entity}}> _items = new();

    [ObservableProperty]
    private bool _isBusy;

    [ObservableProperty]
    private string _errorMessage = string.Empty;

    public {{Feature}}ViewModel({{DomainOperation}} operation)
    {
        _operation = operation;
    }

    [RelayCommand]
    private async Task LoadAsync()
    {
        IsBusy = true;
        ErrorMessage = string.Empty;

        var result = await _operation.ExecuteAsync();

        result.Switch(
            items => Items = new ObservableCollection<{{Entity}}>(items),
            errors => ErrorMessage = errors.First().Description
        );

        IsBusy = false;
    }
}
```

**Page Structure**:
```xaml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="{{ProjectName}}.Presentation.{{Feature}}.{{Feature}}Page"
             Title="{{Title}}">

    <Grid RowDefinitions="Auto,*">
        <!-- Busy indicator -->
        <ActivityIndicator Grid.Row="0" IsRunning="{Binding IsBusy}" />

        <!-- Error message -->
        <Label Grid.Row="0"
               Text="{Binding ErrorMessage}"
               IsVisible="{Binding ErrorMessage, Converter={StaticResource IsNotNullOrEmptyConverter}}"
               TextColor="Red" />

        <!-- Content -->
        <CollectionView Grid.Row="1" ItemsSource="{Binding Items}">
            <CollectionView.ItemTemplate>
                <DataTemplate>
                    <!-- Item template -->
                </DataTemplate>
            </CollectionView.ItemTemplate>
        </CollectionView>
    </Grid>
</ContentPage>
```

### 6. AppShell Navigation

**AppShell.xaml Structure**:
```xaml
<Shell xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
       xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
       xmlns:pages="clr-namespace:{{ProjectName}}.Presentation"
       x:Class="{{ProjectName}}.AppShell">

    <!-- Flyout menu -->
    <FlyoutItem Title="Home" Icon="home.png">
        <ShellContent ContentTemplate="{DataTemplate pages:HomePage}" />
    </FlyoutItem>

    <FlyoutItem Title="Products" Icon="products.png">
        <ShellContent ContentTemplate="{DataTemplate pages:ProductListPage}" />
    </FlyoutItem>
</Shell>
```

**Route Registration** (AppShell.xaml.cs):
```csharp
public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();

        // Register routes for navigation
        Routing.RegisterRoute("product-details", typeof(ProductDetailsPage));
        Routing.RegisterRoute("product-edit", typeof(ProductEditPage));
    }
}
```

**Navigation from ViewModels**:
```csharp
// Navigate to registered route
await Shell.Current.GoToAsync("product-details");

// Navigate with parameters
await Shell.Current.GoToAsync($"product-details?id={productId}");

// Navigate back
await Shell.Current.GoToAsync("..");

// Navigate to root
await Shell.Current.GoToAsync("//");
```

**Receiving Navigation Parameters**:
```csharp
[QueryProperty(nameof(ProductId), "id")]
public partial class ProductDetailsViewModel : ObservableObject
{
    private Guid _productId;

    public Guid ProductId
    {
        get => _productId;
        set
        {
            _productId = value;
            LoadProductAsync(value);
        }
    }
}
```

### 7. Dependency Injection Configuration

**MauiProgram.cs**:
```csharp
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();

        builder
            .UseMauiApp<App>()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            });

        // Register repositories
        builder.Services.AddScoped<IProductRepository, ProductRepository>();
        builder.Services.AddScoped<IOrderRepository, OrderRepository>();

        // Register services
        builder.Services.AddSingleton<IAuthenticationService, AuthenticationService>();
        builder.Services.AddSingleton<IPaymentService, PaymentService>();

        // Register domain operations
        builder.Services.AddTransient<GetProducts>();
        builder.Services.AddTransient<CreateOrder>();
        builder.Services.AddTransient<UpdateCustomer>();

        // Register ViewModels
        builder.Services.AddTransient<ProductListViewModel>();
        builder.Services.AddTransient<ProductDetailsViewModel>();
        builder.Services.AddTransient<OrderCreateViewModel>();

        // Register Pages
        builder.Services.AddTransient<ProductListPage>();
        builder.Services.AddTransient<ProductDetailsPage>();
        builder.Services.AddTransient<OrderCreatePage>();

        return builder.Build();
    }
}
```

**Lifetime Recommendations**:
- **Transient** (`AddTransient`): Domain operations, ViewModels, Pages (new instance per request)
- **Scoped** (`AddScoped`): Repositories (per-page lifecycle)
- **Singleton** (`AddSingleton`): Services, NavigationService (single instance app-wide)

## Testing Strategy

### Outside-In TDD Approach

1. **Write Acceptance Test** (ViewModel test)
2. **Run test** (should fail)
3. **Implement Domain Operation** (with unit tests)
4. **Implement Repository/Service** (with unit tests)
5. **Wire up ViewModel**
6. **Run acceptance test** (should pass)

### Domain Operation Tests

```csharp
namespace {{ProjectName}}.Tests.Domain;

public class {{Verb}}{{Entity}}Tests
{
    private readonly I{{Entity}}Repository _repository;
    private readonly {{Verb}}{{Entity}} _sut;

    public {{Verb}}{{Entity}}Tests()
    {
        _repository = Substitute.For<I{{Entity}}Repository>();
        _sut = new {{Verb}}{{Entity}}(_repository);
    }

    [Fact]
    public async Task ExecuteAsync_WhenRepositorySucceeds_ReturnsSuccess()
    {
        // Arrange
        var expected = new List<{{Entity}}> { new {{Entity}}() };
        _repository.GetAllAsync().Returns(expected);

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Should().BeEquivalentTo(expected);
    }

    [Fact]
    public async Task ExecuteAsync_WhenRepositoryFails_ReturnsError()
    {
        // Arrange
        var error = Error.Unexpected("Test.Error", "Test error");
        _repository.GetAllAsync().Returns(error);

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Should().Be(error);
    }
}
```

### Repository Tests

```csharp
namespace {{ProjectName}}.Tests.Repositories;

public class {{Entity}}RepositoryTests
{
    private readonly DbContext _context;
    private readonly {{Entity}}Repository _sut;

    public {{Entity}}RepositoryTests()
    {
        var options = new DbContextOptionsBuilder<DbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new DbContext(options);
        _sut = new {{Entity}}Repository(_context);
    }

    [Fact]
    public async Task GetAllAsync_WhenEntitiesExist_ReturnsEntities()
    {
        // Arrange
        var entities = new List<{{Entity}}>
        {
            new {{Entity}} { Id = Guid.NewGuid(), Name = "Test 1" },
            new {{Entity}} { Id = Guid.NewGuid(), Name = "Test 2" }
        };
        _context.{{Entity}}s.AddRange(entities);
        await _context.SaveChangesAsync();

        // Act
        var result = await _sut.GetAllAsync();

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Should().HaveCount(2);
    }
}
```

### Service Tests

```csharp
namespace {{ProjectName}}.Tests.Services;

public class {{Purpose}}ServiceTests
{
    private readonly HttpClient _httpClient;
    private readonly {{Purpose}}Service _sut;

    public {{Purpose}}ServiceTests()
    {
        var handler = new MockHttpMessageHandler();
        _httpClient = new HttpClient(handler);
        _sut = new {{Purpose}}Service(_httpClient);
    }

    [Fact]
    public async Task {{Method}}Async_WhenApiSucceeds_ReturnsSuccess()
    {
        // Arrange
        var expected = new {{ReturnType}} { /* ... */ };
        SetupHttpResponse(HttpStatusCode.OK, expected);

        // Act
        var result = await _sut.{{Method}}Async(parameters);

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Should().BeEquivalentTo(expected);
    }

    [Fact]
    public async Task {{Method}}Async_WhenApiFails_ReturnsError()
    {
        // Arrange
        SetupHttpResponse(HttpStatusCode.InternalServerError, null);

        // Act
        var result = await _sut.{{Method}}Async(parameters);

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Type.Should().Be(ErrorType.Unexpected);
    }
}
```

## Quality Gates

### Required Quality Gates
1. All tests passing (100%)
2. ErrorOr used for all fallible operations
3. Interfaces for all repositories and services
4. Verb-based domain operation naming (no UseCase/Engine suffixes)
5. AppShell routing configured correctly
6. Dependency injection configured in MauiProgram.cs

### Recommended Quality Gates
1. 80%+ line coverage
2. 75%+ branch coverage
3. No code duplication (DRY principle)
4. SOLID principles followed

## Common Patterns and Examples

### Pattern 1: Query Operation (Read)

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

### Pattern 2: Command Operation (Write)

```csharp
public class CreateOrder
{
    private readonly IOrderRepository _repository;
    private readonly IPaymentService _paymentService;

    public CreateOrder(
        IOrderRepository repository,
        IPaymentService paymentService)
    {
        _repository = repository;
        _paymentService = paymentService;
    }

    public async Task<ErrorOr<Order>> ExecuteAsync(CreateOrderRequest request)
    {
        // 1. Validate
        var validationResult = ValidateRequest(request);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // 2. Process payment
        var paymentResult = await _paymentService.ProcessPaymentAsync(request.PaymentDetails);
        if (paymentResult.IsError)
        {
            return paymentResult.Errors;
        }

        // 3. Create order
        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = request.CustomerId,
            Total = request.Total,
            Status = OrderStatus.Confirmed
        };

        return await _repository.CreateAsync(order);
    }

    private ErrorOr<Success> ValidateRequest(CreateOrderRequest request)
    {
        if (request.CustomerId == Guid.Empty)
        {
            return Error.Validation("Order.CustomerId.Required", "Customer ID is required");
        }

        if (request.Total <= 0)
        {
            return Error.Validation("Order.Total.Invalid", "Total must be greater than 0");
        }

        return Result.Success;
    }
}
```

### Pattern 3: Navigation Service

```csharp
public interface INavigationService
{
    Task NavigateToAsync(string route);
    Task NavigateToAsync(string route, Dictionary<string, object> parameters);
    Task GoBackAsync();
}

public class NavigationService : INavigationService
{
    public async Task NavigateToAsync(string route)
    {
        await Shell.Current.GoToAsync(route);
    }

    public async Task NavigateToAsync(string route, Dictionary<string, object> parameters)
    {
        var queryString = string.Join("&", parameters.Select(p => $"{p.Key}={p.Value}"));
        await Shell.Current.GoToAsync($"{route}?{queryString}");
    }

    public async Task GoBackAsync()
    {
        await Shell.Current.GoToAsync("..");
    }
}
```

## Template Placeholder Reference

When generating code from templates, use these placeholders:

- `{{ProjectName}}` - Root project name
- `{{RootNamespace}}` - Root namespace
- `{{FeatureName}}` - Feature/module name
- `{{Entity}}` - Entity/model name
- `{{Verb}}` - Action verb (Get, Create, Update, Delete)
- `{{OperationName}}` - Complete operation name (e.g., GetProducts)
- `{{ReturnType}}` - Return type of operation
- `{{Parameters}}` - Method parameters
- `{{RepositoryName}}` - Repository name
- `{{ServiceName}}` - Service name
- `{{Purpose}}` - Service purpose/responsibility

## Troubleshooting

### ErrorOr Not Found
```bash
dotnet add package ErrorOr --version 2.0.0
```

### CommunityToolkit.Mvvm Not Found
```bash
dotnet add package CommunityToolkit.Mvvm
```

### Navigation Not Working
1. Ensure routes registered in AppShell.xaml.cs
2. Check route names match exactly
3. Verify pages registered in DI container

### Dependency Injection Issues
1. Verify all dependencies registered in MauiProgram.cs
2. Check constructor injection matches registered types
3. Ensure interfaces match implementations

## Best Practices Summary

1. **Domain Operations**: Use verb-based naming, return ErrorOr, inject interfaces
2. **Repositories**: Database access only, return ErrorOr, implement interfaces
3. **Services**: External integrations only, return ErrorOr, implement interfaces
4. **ViewModels**: Inject domain operations, handle ErrorOr results, use CommunityToolkit.Mvvm
5. **Navigation**: Use AppShell routing, register routes, use NavigationService
6. **Dependency Injection**: Register all dependencies, use appropriate lifetimes
7. **Testing**: Outside-In TDD, mock interfaces with NSubstitute, verify ErrorOr behavior
8. **Error Handling**: Use ErrorOr for all fallible operations, provide descriptive error messages

## Additional Resources

- [.NET MAUI Documentation](https://learn.microsoft.com/en-us/dotnet/maui/)
- [ErrorOr Library](https://github.com/amantinband/error-or)
- [CommunityToolkit.Mvvm](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/)
- [AppShell Navigation](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/)
- [Dependency Injection in .NET MAUI](https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/dependency-injection)
