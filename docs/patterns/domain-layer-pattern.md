# Domain Layer Pattern (.NET MAUI)

**Purpose**: Complete guide to implementing verb-based Domain operations with ErrorOr functional error handling in .NET MAUI applications.

**Learn Domain pattern in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Get Started Immediately

```csharp
// 1. Define operation with verb-based naming
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

// 2. Register in DI container (MauiProgram.cs)
builder.Services.AddTransient<GetProducts>();

// 3. Use in ViewModel
public partial class ProductListViewModel : ObservableObject
{
    private readonly GetProducts _getProducts;

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

**That's it!** Domain operations encapsulate business logic with functional error handling.

**Learn More**: See "Core Concepts" below for naming conventions and ErrorOr patterns.

---

## Core Concepts (10 minutes)

### What is the Domain Layer?

The Domain layer contains **business operations** that orchestrate business logic. Each operation:
- Has a **clear verb-based name** that describes the business action
- Returns **ErrorOr<T>** for functional error handling
- Depends on **Repository** (database) or **Service** (external systems) abstractions
- Contains **validation and business rules**

### Naming Convention: Verb-Based Operations

**Pattern**: `{Verb}{Entity}`

**Correct Examples**:
```csharp
GetProducts          // Query products from repository
CreateOrder          // Create new order with validation
UpdateCustomer       // Update customer information
DeleteProduct        // Remove product (soft or hard delete)
CalculateOrderTotal  // Calculate order total with discounts
ValidateInventory    // Validate product availability
ProcessPayment       // Process payment through service
SendNotification     // Send notification via service
```

**Prohibited Naming** (NEVER use these suffixes):
```csharp
// ❌ WRONG - Do NOT use these patterns
GetProductsUseCase    // No "UseCase" suffix
GetProductsEngine     // No "Engine" suffix
GetProductsHandler    // No "Handler" suffix
GetProductsProcessor  // No "Processor" suffix
GetProductsCommand    // No "Command" suffix (except CQRS pattern)
GetProductsQuery      // No "Query" suffix (except CQRS pattern)
```

**Why?** Verb-based names clearly communicate business intent without technical jargon.

### ErrorOr Pattern for Error Handling

Operations return `ErrorOr<T>` instead of throwing exceptions:

```csharp
// Success case - implicit conversion
ErrorOr<Product> result = product;

// Error case - explicit error creation
return Error.NotFound("Product.NotFound", $"Product {id} not found");

// Consuming results - Switch pattern
result.Switch(
    product => HandleSuccess(product),
    errors => HandleErrors(errors)
);
```

**Benefits**:
- Explicit error handling in type system
- No hidden exceptions to catch
- Compiler ensures error cases are handled
- Functional, composable error handling

### Repository vs Service Dependencies

**Use Repository for**:
- Database queries (EF Core, SQLite)
- Local storage operations
- CRUD operations on entities
- Data persistence

```csharp
public class GetProducts
{
    private readonly IProductRepository _repository; // Database access

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}
```

**Use Service for**:
- REST API calls
- External system integrations
- Cloud service operations
- Device hardware access

```csharp
public class ProcessPayment
{
    private readonly IPaymentService _paymentService; // External API

    public async Task<ErrorOr<PaymentResult>> ExecuteAsync(PaymentRequest request)
    {
        return await _paymentService.ProcessAsync(request);
    }
}
```

See [repository-service-split.md](../guides/repository-service-split.md) for detailed guidance.

### Operation Types

#### Query Operations (Read)

Read-only operations that return data without side effects:

```csharp
public class GetProducts
{
    private readonly IProductRepository _repository;

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}
```

**Characteristics**:
- No validation needed (reading is always safe)
- Return collection or single entity
- Idempotent (same result every call)
- No state changes

#### Command Operations (Write)

Operations that modify state with validation and business rules:

```csharp
public class CreateOrder
{
    private readonly IOrderRepository _repository;
    private readonly IPaymentService _paymentService;

    public async Task<ErrorOr<Order>> ExecuteAsync(CreateOrderRequest request)
    {
        // 1. Validate inputs
        var validationResult = ValidateRequest(request);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // 2. Execute business logic
        var paymentResult = await _paymentService.ProcessPaymentAsync(request.Payment);
        if (paymentResult.IsError)
        {
            return paymentResult.Errors;
        }

        // 3. Persist state
        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = request.CustomerId,
            Status = OrderStatus.Confirmed
        };

        return await _repository.CreateAsync(order);
    }

    private ErrorOr<Success> ValidateRequest(CreateOrderRequest request)
    {
        if (request.CustomerId == Guid.Empty)
        {
            return Error.Validation(
                "Order.CustomerId.Required",
                "Customer ID is required"
            );
        }

        if (request.Total <= 0)
        {
            return Error.Validation(
                "Order.Total.Invalid",
                "Total must be greater than 0"
            );
        }

        return Result.Success;
    }
}
```

**Characteristics**:
- Always validate inputs first
- Contain business rules
- Modify state
- Return created/updated entity or Success

**Learn More**: See "Complete Reference" below for advanced patterns and examples.

---

## Complete Reference (30+ minutes)

### File Structure

```
src/
├── Domain/
│   ├── Products/
│   │   ├── GetProducts.cs          # Query operation
│   │   ├── GetProductById.cs       # Query operation
│   │   ├── CreateProduct.cs        # Command operation
│   │   ├── UpdateProduct.cs        # Command operation
│   │   └── DeleteProduct.cs        # Command operation
│   ├── Orders/
│   │   ├── GetOrders.cs
│   │   ├── CreateOrder.cs
│   │   ├── UpdateOrderStatus.cs
│   │   └── CalculateOrderTotal.cs  # Calculation operation
│   └── Repositories/               # Repository interfaces
│       ├── IProductRepository.cs
│       └── IOrderRepository.cs
```

### Operation Template

```csharp
namespace ProjectName.Domain.FeatureName;

/// <summary>
/// {Describe what this operation does in business terms}
/// </summary>
public class {Verb}{Entity}
{
    private readonly I{Entity}Repository _repository;
    // Add other dependencies (repositories, services) as needed

    /// <summary>
    /// Initializes a new instance of {Verb}{Entity}
    /// </summary>
    public {Verb}{Entity}(I{Entity}Repository repository)
    {
        _repository = repository;
    }

    /// <summary>
    /// Executes the operation
    /// </summary>
    /// <param name="parameter">Operation parameter</param>
    /// <returns>Success result or errors</returns>
    public async Task<ErrorOr<{ReturnType}>> ExecuteAsync({ParameterType} parameter)
    {
        // 1. Validate inputs (for command operations)
        var validationResult = ValidateInputs(parameter);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // 2. Execute business logic
        var result = await _repository.MethodAsync(parameter);

        // 3. Return result
        return result;
    }

    private ErrorOr<Success> ValidateInputs({ParameterType} parameter)
    {
        // Validation logic
        if (/* invalid condition */)
        {
            return Error.Validation(
                "{Entity}.{Field}.{ErrorType}",
                "User-friendly error message"
            );
        }

        return Result.Success;
    }
}
```

### ErrorOr Error Types

#### Validation Errors

Use for invalid input data:

```csharp
return Error.Validation(
    "Product.Name.Required",
    "Product name is required"
);

return Error.Validation(
    "Product.Price.Invalid",
    "Price must be greater than 0"
);

return Error.Validation(
    "Product.Name.TooLong",
    "Product name cannot exceed 100 characters"
);
```

#### Not Found Errors

Use when resource doesn't exist:

```csharp
return Error.NotFound(
    "Product.NotFound",
    $"Product with ID {productId} not found"
);

return Error.NotFound(
    "Order.NotFound",
    $"Order {orderId} does not exist"
);
```

#### Conflict Errors

Use for duplicate or conflicting data:

```csharp
return Error.Conflict(
    "Product.Duplicate",
    $"Product with SKU {sku} already exists"
);

return Error.Conflict(
    "Order.AlreadyShipped",
    "Cannot modify order that has already shipped"
);
```

#### Unauthorized Errors

Use when authentication is required:

```csharp
return Error.Unauthorized(
    "User.NotAuthenticated",
    "Authentication required to access this resource"
);
```

#### Forbidden Errors

Use when user lacks permissions:

```csharp
return Error.Forbidden(
    "Order.InsufficientPermissions",
    "You do not have permission to modify this order"
);
```

#### Unexpected Errors

Use for system errors and exceptions:

```csharp
try
{
    var result = await _repository.GetAllAsync();
    return result;
}
catch (Exception ex)
{
    return Error.Unexpected(
        "Product.DatabaseError",
        $"Database error: {ex.Message}"
    );
}
```

### Consuming ErrorOr Results

#### Pattern 1: Switch (Void Return)

Best for ViewModels handling UI updates:

```csharp
var result = await _getProducts.ExecuteAsync();

result.Switch(
    products => {
        Products = new ObservableCollection<Product>(products);
        ErrorMessage = string.Empty;
    },
    errors => {
        ErrorMessage = errors.First().Description;
        Products.Clear();
    }
);
```

#### Pattern 2: Match (With Return Value)

Best for transforming results:

```csharp
var message = result.Match(
    product => $"Product created: {product.Name}",
    errors => $"Error: {errors.First().Description}"
);
```

#### Pattern 3: IsError Check (Imperative Style)

Best for early returns and nested logic:

```csharp
var result = await _getProduct.ExecuteAsync(id);

if (result.IsError)
{
    var firstError = result.FirstError;
    Logger.LogError(firstError.Description);
    return;
}

var product = result.Value;
// Continue processing product
```

#### Pattern 4: Error Type Handling

Handle different error types differently:

```csharp
result.SwitchFirst(
    value => HandleSuccess(value),
    error => error.Type switch
    {
        ErrorType.Validation => ShowValidationError(error.Description),
        ErrorType.NotFound => ShowNotFoundMessage(error.Description),
        ErrorType.Conflict => ShowConflictDialog(error.Description),
        ErrorType.Unauthorized => NavigateToLogin(),
        ErrorType.Forbidden => ShowPermissionDenied(error.Description),
        _ => ShowUnexpectedError(error.Description)
    }
);
```

### Advanced Patterns

#### Pattern 1: Composition with Multiple Dependencies

```csharp
public class CreateOrderWithInventoryCheck
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly IPaymentService _paymentService;
    private readonly INotificationService _notificationService;

    public async Task<ErrorOr<Order>> ExecuteAsync(CreateOrderRequest request)
    {
        // 1. Validate inventory
        var inventoryResult = await ValidateInventoryAsync(request.Items);
        if (inventoryResult.IsError)
        {
            return inventoryResult.Errors;
        }

        // 2. Process payment
        var paymentResult = await _paymentService.ProcessAsync(request.Payment);
        if (paymentResult.IsError)
        {
            return paymentResult.Errors;
        }

        // 3. Create order
        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = request.CustomerId,
            Items = request.Items,
            Total = request.Total,
            Status = OrderStatus.Confirmed
        };

        var orderResult = await _orderRepository.CreateAsync(order);
        if (orderResult.IsError)
        {
            // Rollback payment if order creation fails
            await _paymentService.RefundAsync(paymentResult.Value.TransactionId);
            return orderResult.Errors;
        }

        // 4. Send notification
        await _notificationService.SendOrderConfirmationAsync(order);

        return orderResult;
    }

    private async Task<ErrorOr<Success>> ValidateInventoryAsync(List<OrderItem> items)
    {
        foreach (var item in items)
        {
            var productResult = await _productRepository.GetByIdAsync(item.ProductId);
            if (productResult.IsError)
            {
                return productResult.Errors;
            }

            if (productResult.Value.Stock < item.Quantity)
            {
                return Error.Conflict(
                    "Order.InsufficientStock",
                    $"Insufficient stock for {productResult.Value.Name}"
                );
            }
        }

        return Result.Success;
    }
}
```

#### Pattern 2: Result Chaining

Chain multiple operations together:

```csharp
public class UpdateProductPrice
{
    public async Task<ErrorOr<Product>> ExecuteAsync(Guid productId, decimal newPrice)
    {
        // Get product
        var getResult = await _repository.GetByIdAsync(productId);
        if (getResult.IsError)
        {
            return getResult.Errors;
        }

        var product = getResult.Value;

        // Validate price
        var validationResult = ValidatePrice(newPrice);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // Update price
        product.Price = newPrice;
        product.LastModified = DateTime.UtcNow;

        return await _repository.UpdateAsync(product);
    }

    private ErrorOr<Success> ValidatePrice(decimal price)
    {
        if (price <= 0)
        {
            return Error.Validation(
                "Product.Price.Invalid",
                "Price must be greater than 0"
            );
        }

        if (price > 999999)
        {
            return Error.Validation(
                "Product.Price.TooHigh",
                "Price cannot exceed 999,999"
            );
        }

        return Result.Success;
    }
}
```

#### Pattern 3: Batch Operations

Handle multiple entities with partial success:

```csharp
public class DeleteProducts
{
    public async Task<ErrorOr<BatchResult>> ExecuteAsync(List<Guid> productIds)
    {
        var result = new BatchResult
        {
            TotalAttempted = productIds.Count,
            Succeeded = new List<Guid>(),
            Failed = new List<(Guid Id, Error Error)>()
        };

        foreach (var id in productIds)
        {
            var deleteResult = await _repository.DeleteAsync(id);

            if (deleteResult.IsError)
            {
                result.Failed.Add((id, deleteResult.FirstError));
            }
            else
            {
                result.Succeeded.Add(id);
            }
        }

        // Return error if ALL operations failed
        if (result.Succeeded.Count == 0)
        {
            return Error.Unexpected(
                "Products.DeleteAll.Failed",
                "Failed to delete any products"
            );
        }

        return result;
    }
}

public class BatchResult
{
    public int TotalAttempted { get; set; }
    public List<Guid> Succeeded { get; set; }
    public List<(Guid Id, Error Error)> Failed { get; set; }

    public bool HasPartialFailure => Failed.Any() && Succeeded.Any();
    public bool IsCompleteSuccess => Failed.Count == 0;
}
```

### Testing Domain Operations

#### Unit Test Structure

```csharp
using FluentAssertions;
using NSubstitute;
using Xunit;

namespace ProjectName.Tests.Domain.Products;

public class GetProductsTests
{
    private readonly IProductRepository _repository;
    private readonly GetProducts _sut;

    public GetProductsTests()
    {
        _repository = Substitute.For<IProductRepository>();
        _sut = new GetProducts(_repository);
    }

    [Fact]
    public async Task ExecuteAsync_WhenRepositorySucceeds_ReturnsProducts()
    {
        // Arrange
        var expected = new List<Product>
        {
            new Product { Id = Guid.NewGuid(), Name = "Product 1" },
            new Product { Id = Guid.NewGuid(), Name = "Product 2" }
        };
        _repository.GetAllAsync().Returns(expected);

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Should().HaveCount(2);
        result.Value.Should().BeEquivalentTo(expected);
    }

    [Fact]
    public async Task ExecuteAsync_WhenRepositoryFails_ReturnsError()
    {
        // Arrange
        var error = Error.Unexpected("Product.Database.Error", "Connection failed");
        _repository.GetAllAsync().Returns(error);

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Should().Be(error);
    }
}
```

#### Testing Command Operations with Validation

```csharp
public class CreateProductTests
{
    private readonly IProductRepository _repository;
    private readonly CreateProduct _sut;

    public CreateProductTests()
    {
        _repository = Substitute.For<IProductRepository>();
        _sut = new CreateProduct(_repository);
    }

    [Fact]
    public async Task ExecuteAsync_WithValidRequest_CreatesProduct()
    {
        // Arrange
        var request = new CreateProductRequest
        {
            Name = "Test Product",
            Price = 29.99m,
            Stock = 100
        };

        var expectedProduct = new Product
        {
            Id = Guid.NewGuid(),
            Name = request.Name,
            Price = request.Price,
            Stock = request.Stock
        };

        _repository.CreateAsync(Arg.Any<Product>()).Returns(expectedProduct);

        // Act
        var result = await _sut.ExecuteAsync(request);

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Name.Should().Be(request.Name);
        await _repository.Received(1).CreateAsync(Arg.Any<Product>());
    }

    [Fact]
    public async Task ExecuteAsync_WithEmptyName_ReturnsValidationError()
    {
        // Arrange
        var request = new CreateProductRequest
        {
            Name = "",
            Price = 29.99m,
            Stock = 100
        };

        // Act
        var result = await _sut.ExecuteAsync(request);

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Type.Should().Be(ErrorType.Validation);
        result.FirstError.Code.Should().Be("Product.Name.Required");
        await _repository.DidNotReceive().CreateAsync(Arg.Any<Product>());
    }

    [Fact]
    public async Task ExecuteAsync_WithNegativePrice_ReturnsValidationError()
    {
        // Arrange
        var request = new CreateProductRequest
        {
            Name = "Test Product",
            Price = -10m,
            Stock = 100
        };

        // Act
        var result = await _sut.ExecuteAsync(request);

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Type.Should().Be(ErrorType.Validation);
        result.FirstError.Code.Should().Be("Product.Price.Invalid");
    }

    [Fact]
    public async Task ExecuteAsync_WhenRepositoryFails_ReturnsError()
    {
        // Arrange
        var request = new CreateProductRequest
        {
            Name = "Test Product",
            Price = 29.99m,
            Stock = 100
        };

        var error = Error.Conflict("Product.Duplicate", "Product already exists");
        _repository.CreateAsync(Arg.Any<Product>()).Returns(error);

        // Act
        var result = await _sut.ExecuteAsync(request);

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Should().Be(error);
    }
}
```

### Dependency Injection Configuration

```csharp
// MauiProgram.cs
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();

        // ... MAUI configuration

        // Register repositories (Scoped - per-page lifecycle)
        builder.Services.AddScoped<IProductRepository, ProductRepository>();
        builder.Services.AddScoped<IOrderRepository, OrderRepository>();
        builder.Services.AddScoped<ICustomerRepository, CustomerRepository>();

        // Register services (Singleton - app-wide)
        builder.Services.AddSingleton<IPaymentService, PaymentService>();
        builder.Services.AddSingleton<INotificationService, NotificationService>();
        builder.Services.AddSingleton<IAuthenticationService, AuthenticationService>();

        // Register domain operations (Transient - new instance per request)
        builder.Services.AddTransient<GetProducts>();
        builder.Services.AddTransient<GetProductById>();
        builder.Services.AddTransient<CreateProduct>();
        builder.Services.AddTransient<UpdateProduct>();
        builder.Services.AddTransient<DeleteProduct>();

        builder.Services.AddTransient<GetOrders>();
        builder.Services.AddTransient<CreateOrder>();
        builder.Services.AddTransient<UpdateOrderStatus>();

        // Register ViewModels (Transient - new instance per navigation)
        builder.Services.AddTransient<ProductListViewModel>();
        builder.Services.AddTransient<ProductDetailsViewModel>();
        builder.Services.AddTransient<OrderCreateViewModel>();

        // Register Pages (Transient - new instance per navigation)
        builder.Services.AddTransient<ProductListPage>();
        builder.Services.AddTransient<ProductDetailsPage>();
        builder.Services.AddTransient<OrderCreatePage>();

        return builder.Build();
    }
}
```

**Lifetime Guidelines**:
- **Transient** (`AddTransient`): Domain operations, ViewModels, Pages
  - New instance created every time it's requested
  - Best for stateless operations

- **Scoped** (`AddScoped`): Repositories
  - Single instance per scope (page navigation in MAUI)
  - Shares instance across same page lifecycle

- **Singleton** (`AddSingleton`): Services
  - Single instance for entire application lifetime
  - Use for stateless, thread-safe services

### Integration with ViewModels

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace ProjectName.Presentation.Products;

public partial class ProductListViewModel : ObservableObject
{
    private readonly GetProducts _getProducts;
    private readonly DeleteProduct _deleteProduct;

    [ObservableProperty]
    private ObservableCollection<Product> _products = new();

    [ObservableProperty]
    private bool _isBusy;

    [ObservableProperty]
    private string _errorMessage = string.Empty;

    public ProductListViewModel(
        GetProducts getProducts,
        DeleteProduct deleteProduct)
    {
        _getProducts = getProducts;
        _deleteProduct = deleteProduct;
    }

    [RelayCommand]
    private async Task LoadProductsAsync()
    {
        IsBusy = true;
        ErrorMessage = string.Empty;

        var result = await _getProducts.ExecuteAsync();

        result.Switch(
            products => Products = new ObservableCollection<Product>(products),
            errors => ErrorMessage = errors.First().Description
        );

        IsBusy = false;
    }

    [RelayCommand]
    private async Task DeleteProductAsync(Guid productId)
    {
        IsBusy = true;
        ErrorMessage = string.Empty;

        var result = await _deleteProduct.ExecuteAsync(productId);

        result.Switch(
            _ => {
                Products.Remove(Products.First(p => p.Id == productId));
                ErrorMessage = string.Empty;
            },
            errors => ErrorMessage = errors.First().Description
        );

        IsBusy = false;
    }
}
```

---

## Examples

### Example 1: Simple Query Operation

```csharp
namespace ShoppingApp.Domain.Products;

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

### Example 2: Query with Parameter

```csharp
namespace ShoppingApp.Domain.Products;

public class GetProductById
{
    private readonly IProductRepository _repository;

    public GetProductById(IProductRepository repository)
    {
        _repository = repository;
    }

    public async Task<ErrorOr<Product>> ExecuteAsync(Guid productId)
    {
        if (productId == Guid.Empty)
        {
            return Error.Validation(
                "Product.Id.Invalid",
                "Product ID is required"
            );
        }

        return await _repository.GetByIdAsync(productId);
    }
}
```

### Example 3: Command with Validation

```csharp
namespace ShoppingApp.Domain.Products;

public class CreateProduct
{
    private readonly IProductRepository _repository;

    public CreateProduct(IProductRepository repository)
    {
        _repository = repository;
    }

    public async Task<ErrorOr<Product>> ExecuteAsync(CreateProductRequest request)
    {
        // Validate
        var validationResult = ValidateRequest(request);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // Create entity
        var product = new Product
        {
            Id = Guid.NewGuid(),
            Name = request.Name,
            Description = request.Description,
            Price = request.Price,
            Stock = request.Stock,
            CreatedAt = DateTime.UtcNow
        };

        // Persist
        return await _repository.CreateAsync(product);
    }

    private ErrorOr<Success> ValidateRequest(CreateProductRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Name))
        {
            return Error.Validation(
                "Product.Name.Required",
                "Product name is required"
            );
        }

        if (request.Name.Length > 100)
        {
            return Error.Validation(
                "Product.Name.TooLong",
                "Product name cannot exceed 100 characters"
            );
        }

        if (request.Price <= 0)
        {
            return Error.Validation(
                "Product.Price.Invalid",
                "Price must be greater than 0"
            );
        }

        if (request.Stock < 0)
        {
            return Error.Validation(
                "Product.Stock.Invalid",
                "Stock cannot be negative"
            );
        }

        return Result.Success;
    }
}

public record CreateProductRequest(
    string Name,
    string Description,
    decimal Price,
    int Stock
);
```

### Example 4: Complex Command with External Service

```csharp
namespace ShoppingApp.Domain.Orders;

public class CreateOrder
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly IPaymentService _paymentService;
    private readonly IEmailService _emailService;

    public CreateOrder(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        IPaymentService paymentService,
        IEmailService emailService)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _paymentService = paymentService;
        _emailService = emailService;
    }

    public async Task<ErrorOr<Order>> ExecuteAsync(CreateOrderRequest request)
    {
        // 1. Validate request
        var validationResult = await ValidateRequestAsync(request);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        // 2. Check inventory
        var inventoryResult = await ValidateInventoryAsync(request.Items);
        if (inventoryResult.IsError)
        {
            return inventoryResult.Errors;
        }

        // 3. Process payment
        var paymentResult = await _paymentService.ProcessAsync(request.Payment);
        if (paymentResult.IsError)
        {
            return Error.Unexpected(
                "Order.Payment.Failed",
                $"Payment failed: {paymentResult.FirstError.Description}"
            );
        }

        // 4. Create order
        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = request.CustomerId,
            Items = request.Items,
            Total = CalculateTotal(request.Items),
            Status = OrderStatus.Confirmed,
            CreatedAt = DateTime.UtcNow,
            PaymentTransactionId = paymentResult.Value.TransactionId
        };

        var createResult = await _orderRepository.CreateAsync(order);
        if (createResult.IsError)
        {
            // Rollback payment
            await _paymentService.RefundAsync(paymentResult.Value.TransactionId);
            return createResult.Errors;
        }

        // 5. Send confirmation email
        await _emailService.SendOrderConfirmationAsync(
            request.CustomerEmail,
            createResult.Value
        );

        return createResult;
    }

    private async Task<ErrorOr<Success>> ValidateRequestAsync(CreateOrderRequest request)
    {
        if (request.CustomerId == Guid.Empty)
        {
            return Error.Validation(
                "Order.CustomerId.Required",
                "Customer ID is required"
            );
        }

        if (request.Items == null || request.Items.Count == 0)
        {
            return Error.Validation(
                "Order.Items.Required",
                "Order must contain at least one item"
            );
        }

        return Result.Success;
    }

    private async Task<ErrorOr<Success>> ValidateInventoryAsync(List<OrderItem> items)
    {
        foreach (var item in items)
        {
            var productResult = await _productRepository.GetByIdAsync(item.ProductId);
            if (productResult.IsError)
            {
                return productResult.Errors;
            }

            if (productResult.Value.Stock < item.Quantity)
            {
                return Error.Conflict(
                    "Order.InsufficientStock",
                    $"Insufficient stock for {productResult.Value.Name}. " +
                    $"Available: {productResult.Value.Stock}, Requested: {item.Quantity}"
                );
            }
        }

        return Result.Success;
    }

    private decimal CalculateTotal(List<OrderItem> items)
    {
        return items.Sum(item => item.Price * item.Quantity);
    }
}
```

---

## FAQ

### Q: Why verb-based naming instead of UseCase/Engine/Handler?

**A**: Verb-based names clearly communicate business intent without technical jargon. "GetProducts" is immediately understandable to business stakeholders, while "GetProductsUseCase" introduces unnecessary technical terminology. The pattern scales: "CreateOrder", "UpdateCustomer", "ProcessPayment" - all clear business actions.

### Q: When should I use ErrorOr vs throwing exceptions?

**A**: Use ErrorOr for **expected** error conditions (validation failures, not found, conflicts). Use exceptions only for **unexpected** system errors (out of memory, null reference). ErrorOr makes error handling explicit in the type system, while exceptions hide error paths.

```csharp
// ✅ Good - Use ErrorOr for expected errors
public async Task<ErrorOr<Product>> ExecuteAsync(Guid id)
{
    if (id == Guid.Empty)
    {
        return Error.Validation("Product.Id.Invalid", "ID required");
    }
    // ...
}

// ❌ Bad - Don't throw for expected errors
public async Task<Product> ExecuteAsync(Guid id)
{
    if (id == Guid.Empty)
    {
        throw new ArgumentException("ID required"); // Don't do this
    }
    // ...
}
```

### Q: Should validation be in Domain operations or Repository?

**A**: Validation belongs in **Domain operations**. Repositories should trust their inputs and focus on data access. Domain operations orchestrate business rules and validation before calling repositories.

```csharp
// ✅ Good - Validation in Domain
public class CreateProduct
{
    public async Task<ErrorOr<Product>> ExecuteAsync(CreateProductRequest request)
    {
        // Validate in Domain
        if (string.IsNullOrEmpty(request.Name))
        {
            return Error.Validation("Product.Name.Required", "Name required");
        }

        return await _repository.CreateAsync(product);
    }
}

// ❌ Bad - Validation in Repository
public class ProductRepository
{
    public async Task<ErrorOr<Product>> CreateAsync(Product product)
    {
        // Don't validate in Repository
        if (string.IsNullOrEmpty(product.Name))
        {
            return Error.Validation("Product.Name.Required", "Name required");
        }
        // ...
    }
}
```

### Q: How do I handle multiple validation errors?

**A**: Collect all validation errors and return them together:

```csharp
private ErrorOr<Success> ValidateRequest(CreateProductRequest request)
{
    var errors = new List<Error>();

    if (string.IsNullOrWhiteSpace(request.Name))
    {
        errors.Add(Error.Validation(
            "Product.Name.Required",
            "Product name is required"
        ));
    }

    if (request.Price <= 0)
    {
        errors.Add(Error.Validation(
            "Product.Price.Invalid",
            "Price must be greater than 0"
        ));
    }

    if (request.Stock < 0)
    {
        errors.Add(Error.Validation(
            "Product.Stock.Invalid",
            "Stock cannot be negative"
        ));
    }

    return errors.Any()
        ? errors
        : Result.Success;
}
```

### Q: Should I use async for operations without I/O?

**A**: For consistency, use async even for synchronous operations. This allows easy addition of I/O later without breaking the interface:

```csharp
// ✅ Good - Consistent async interface
public async Task<ErrorOr<decimal>> ExecuteAsync(Order order)
{
    // No I/O, but still async for consistency
    return await Task.FromResult(order.Items.Sum(i => i.Price));
}
```

### Q: How do I test Domain operations?

**A**: Mock the repository/service dependencies using NSubstitute:

```csharp
[Fact]
public async Task ExecuteAsync_WhenValid_CallsRepository()
{
    // Arrange
    var repository = Substitute.For<IProductRepository>();
    var sut = new CreateProduct(repository);
    var request = new CreateProductRequest("Product", "Description", 29.99m, 10);

    // Act
    await sut.ExecuteAsync(request);

    // Assert
    await repository.Received(1).CreateAsync(Arg.Any<Product>());
}
```

See "Testing Domain Operations" section above for complete examples.

---

## Related Documentation

- [MAUI Template Selection Guide](../guides/maui-template-selection.md) - Choose between AppShell and NavigationPage templates
- [Repository vs Service Split](../guides/repository-service-split.md) - When to use Repository vs Service
- [Creating Local Templates](../guides/creating-local-templates.md) - Create custom Domain operation templates
- [ErrorOr Library Documentation](https://github.com/amantinband/error-or) - Complete ErrorOr reference

---

**Last Updated**: 2025-10-15
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
