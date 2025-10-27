# Engine-to-Domain Migration Guide

**Purpose**: Complete guide to migrating from old UseCase/Engine patterns to modern verb-based Domain operations in .NET MAUI applications.

**Learn migration in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Migrate in 4 Steps

```bash
# 1. Identify old patterns (UseCase, Engine, Handler)
grep -r "UseCase\|Engine\|Handler" src/

# 2. Rename files and classes
# Before: GetProductsUseCase.cs
mv src/UseCases/GetProductsUseCase.cs src/Domain/Products/GetProducts.cs

# 3. Update class definition
# Before:
class GetProductsUseCase { ... }

# After:
class GetProducts { ... }

# 4. Update dependency injection
# Before:
builder.Services.AddTransient<GetProductsUseCase>();

# After:
builder.Services.AddTransient<GetProducts>();
```

**That's it!** Rename files, classes, and DI registrations. The internal logic stays the same.

**Learn More**: See "Core Concepts" below for naming patterns and systematic migration approach.

---

## Core Concepts (10 minutes)

### Why Migrate from UseCase/Engine?

**Old Pattern Problems**:
- ❌ Technical jargon confuses business stakeholders
- ❌ Inconsistent naming ("UseCase" vs "Engine" vs "Handler")
- ❌ Adds suffix noise without business value
- ❌ Not intuitive for new team members

**New Pattern Benefits**:
- ✅ Clear business intent ("GetProducts", "CreateOrder")
- ✅ Consistent naming across entire codebase
- ✅ Understandable by business and technical teams
- ✅ Aligns with Domain-Driven Design principles

### Naming Pattern Migration

| Old Pattern | New Pattern | Example |
|-------------|-------------|---------|
| `{Operation}UseCase` | `{Verb}{Entity}` | `GetProductsUseCase` → `GetProducts` |
| `{Operation}Engine` | `{Verb}{Entity}` | `CreateOrderEngine` → `CreateOrder` |
| `{Operation}Handler` | `{Verb}{Entity}` | `UpdateCustomerHandler` → `UpdateCustomer` |
| `{Operation}Processor` | `{Verb}{Entity}` | `ProcessPaymentProcessor` → `ProcessPayment` |
| `{Operation}Command` | `{Verb}{Entity}` | `DeleteProductCommand` → `DeleteProduct` |
| `{Operation}Query` | `{Verb}{Entity}` | `GetOrdersQuery` → `GetOrders` |

**Verb Selection**:
- **Query Operations** (Read): Get, Find, Search, List, Calculate
- **Command Operations** (Write): Create, Update, Delete, Add, Remove, Process, Send

### Directory Structure Migration

**Before** (UseCase pattern):
```
src/
├── UseCases/
│   ├── Products/
│   │   ├── GetProductsUseCase.cs
│   │   ├── CreateProductUseCase.cs
│   │   └── UpdateProductUseCase.cs
│   └── Orders/
│       ├── GetOrdersUseCase.cs
│       └── CreateOrderUseCase.cs
├── Repositories/
└── ViewModels/
```

**After** (Domain pattern):
```
src/
├── Domain/
│   ├── Products/
│   │   ├── GetProducts.cs
│   │   ├── CreateProduct.cs
│   │   └── UpdateProduct.cs
│   ├── Orders/
│   │   ├── GetOrders.cs
│   │   └── CreateOrder.cs
│   └── Repositories/
│       ├── IProductRepository.cs
│       └── IOrderRepository.cs
├── Data/
│   └── Repositories/
│       ├── ProductRepository.cs
│       └── OrderRepository.cs
└── Presentation/
    └── ViewModels/
```

### Migration Checklist

For each operation:

- [ ] Rename file: `{Operation}UseCase.cs` → `{Verb}{Entity}.cs`
- [ ] Move file: `src/UseCases/` → `src/Domain/{Feature}/`
- [ ] Rename class: `{Operation}UseCase` → `{Verb}{Entity}`
- [ ] Update namespace: `ProjectName.UseCases` → `ProjectName.Domain.{Feature}`
- [ ] Update DI registration in `MauiProgram.cs`
- [ ] Update ViewModel injections
- [ ] Update test file names and class names
- [ ] Update documentation and comments
- [ ] Run tests to verify functionality

**Learn More**: See "Complete Reference" below for step-by-step examples and automated migration scripts.

---

## Complete Reference (30+ minutes)

### Migration Strategy

#### Phase 1: Assessment (15 minutes)

**Identify All Operations**:

```bash
# Find all UseCase/Engine/Handler patterns
find src/ -name "*UseCase.cs" -o -name "*Engine.cs" -o -name "*Handler.cs"

# List all matches
grep -r "class.*\(UseCase\|Engine\|Handler\)" src/ --include="*.cs"

# Count operations
grep -rc "UseCase\|Engine\|Handler" src/ | grep -v ":0" | wc -l
```

**Create Migration Inventory**:

```markdown
## Migration Inventory

### Products Feature (5 operations)
- [ ] GetProductsUseCase.cs → GetProducts.cs
- [ ] GetProductByIdUseCase.cs → GetProductById.cs
- [ ] CreateProductUseCase.cs → CreateProduct.cs
- [ ] UpdateProductUseCase.cs → UpdateProduct.cs
- [ ] DeleteProductUseCase.cs → DeleteProduct.cs

### Orders Feature (4 operations)
- [ ] GetOrdersUseCase.cs → GetOrders.cs
- [ ] GetOrderByIdUseCase.cs → GetOrderById.cs
- [ ] CreateOrderUseCase.cs → CreateOrder.cs
- [ ] UpdateOrderStatusUseCase.cs → UpdateOrderStatus.cs

### Customers Feature (3 operations)
- [ ] GetCustomersUseCase.cs → GetCustomers.cs
- [ ] CreateCustomerUseCase.cs → CreateCustomer.cs
- [ ] UpdateCustomerUseCase.cs → UpdateCustomer.cs

**Total**: 12 operations to migrate
**Estimated Time**: 2 hours (10 minutes per operation)
```

#### Phase 2: Incremental Migration (Recommended)

Migrate one feature at a time to minimize risk:

**Week 1**: Products feature (5 operations)
**Week 2**: Orders feature (4 operations)
**Week 3**: Customers feature (3 operations)

#### Phase 3: Big Bang Migration (Alternative)

Migrate all operations at once (higher risk, faster completion):

1. Create migration script
2. Run on dedicated branch
3. Comprehensive testing
4. Merge to main

### Step-by-Step Migration Example

#### Example: Migrate GetProductsUseCase

**Before State**:

```csharp
// File: src/UseCases/Products/GetProductsUseCase.cs
namespace ShoppingApp.UseCases.Products;

public class GetProductsUseCase
{
    private readonly IProductRepository _repository;

    public GetProductsUseCase(IProductRepository repository)
    {
        _repository = repository;
    }

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}

// File: src/Presentation/Products/ProductListViewModel.cs
public partial class ProductListViewModel : ObservableObject
{
    private readonly GetProductsUseCase _getProductsUseCase;

    public ProductListViewModel(GetProductsUseCase getProductsUseCase)
    {
        _getProductsUseCase = getProductsUseCase;
    }

    [RelayCommand]
    private async Task LoadAsync()
    {
        var result = await _getProductsUseCase.ExecuteAsync();
        // ...
    }
}

// File: src/MauiProgram.cs
builder.Services.AddTransient<GetProductsUseCase>();

// File: tests/UseCases/Products/GetProductsUseCaseTests.cs
public class GetProductsUseCaseTests
{
    private readonly GetProductsUseCase _sut;
    // ...
}
```

**Migration Steps**:

**Step 1: Create new Domain directory structure**

```bash
mkdir -p src/Domain/Products
```

**Step 2: Copy and rename file**

```bash
cp src/UseCases/Products/GetProductsUseCase.cs src/Domain/Products/GetProducts.cs
```

**Step 3: Update class definition**

```csharp
// File: src/Domain/Products/GetProducts.cs
namespace ShoppingApp.Domain.Products; // Updated namespace

/// <summary>
/// Gets all products from repository
/// </summary>
public class GetProducts // Renamed class
{
    private readonly IProductRepository _repository;

    public GetProducts(IProductRepository repository) // Updated constructor
    {
        _repository = repository;
    }

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}
```

**Step 4: Update ViewModel**

```csharp
// File: src/Presentation/Products/ProductListViewModel.cs
using ShoppingApp.Domain.Products; // Updated using

public partial class ProductListViewModel : ObservableObject
{
    private readonly GetProducts _getProducts; // Renamed field

    public ProductListViewModel(GetProducts getProducts) // Updated constructor
    {
        _getProducts = getProducts;
    }

    [RelayCommand]
    private async Task LoadAsync()
    {
        var result = await _getProducts.ExecuteAsync(); // Updated call
        // ...
    }
}
```

**Step 5: Update DI registration**

```csharp
// File: src/MauiProgram.cs
using ShoppingApp.Domain.Products; // Updated using

// builder.Services.AddTransient<GetProductsUseCase>(); // Remove old
builder.Services.AddTransient<GetProducts>(); // Add new
```

**Step 6: Update test file**

```bash
mkdir -p tests/Domain/Products
cp tests/UseCases/Products/GetProductsUseCaseTests.cs tests/Domain/Products/GetProductsTests.cs
```

```csharp
// File: tests/Domain/Products/GetProductsTests.cs
using ShoppingApp.Domain.Products; // Updated using

public class GetProductsTests // Renamed test class
{
    private readonly GetProducts _sut; // Renamed field

    public GetProductsTests()
    {
        _repository = Substitute.For<IProductRepository>();
        _sut = new GetProducts(_repository); // Updated instantiation
    }

    [Fact]
    public async Task ExecuteAsync_WhenRepositorySucceeds_ReturnsProducts() // Updated test name
    {
        // ... test implementation (no changes needed)
    }
}
```

**Step 7: Delete old files**

```bash
rm src/UseCases/Products/GetProductsUseCase.cs
rm tests/UseCases/Products/GetProductsUseCaseTests.cs
```

**Step 8: Run tests**

```bash
dotnet test

# Expected: All tests passing
# If failures, check for missed references
```

**Step 9: Commit changes**

```bash
git add src/Domain/Products/GetProducts.cs
git add src/Presentation/Products/ProductListViewModel.cs
git add src/MauiProgram.cs
git add tests/Domain/Products/GetProductsTests.cs
git rm src/UseCases/Products/GetProductsUseCase.cs
git rm tests/UseCases/Products/GetProductsUseCaseTests.cs

git commit -m "refactor: Migrate GetProductsUseCase to GetProducts domain operation

- Rename GetProductsUseCase → GetProducts
- Move src/UseCases/Products → src/Domain/Products
- Update namespace ShoppingApp.UseCases → ShoppingApp.Domain.Products
- Update ViewModel injection
- Update DI registration
- Migrate tests
- All tests passing ✅"
```

### Automated Migration Script

```bash
#!/bin/bash
# File: scripts/migrate-usecase-to-domain.sh

# Usage: ./migrate-usecase-to-domain.sh GetProductsUseCase GetProducts Products

OLD_NAME=$1  # e.g., GetProductsUseCase
NEW_NAME=$2  # e.g., GetProducts
FEATURE=$3   # e.g., Products

echo "Migrating $OLD_NAME → $NEW_NAME (Feature: $FEATURE)"

# 1. Create Domain directory
mkdir -p src/Domain/$FEATURE
mkdir -p tests/Domain/$FEATURE

# 2. Copy files
cp src/UseCases/$FEATURE/${OLD_NAME}.cs src/Domain/$FEATURE/${NEW_NAME}.cs
cp tests/UseCases/$FEATURE/${OLD_NAME}Tests.cs tests/Domain/$FEATURE/${NEW_NAME}Tests.cs

# 3. Update namespace and class name in source file
sed -i '' "s/namespace.*UseCases\.$FEATURE/namespace ShoppingApp.Domain.$FEATURE/" src/Domain/$FEATURE/${NEW_NAME}.cs
sed -i '' "s/class $OLD_NAME/class $NEW_NAME/" src/Domain/$FEATURE/${NEW_NAME}.cs
sed -i '' "s/public $OLD_NAME(/public $NEW_NAME(/" src/Domain/$FEATURE/${NEW_NAME}.cs

# 4. Update namespace and class name in test file
sed -i '' "s/namespace.*Tests\.UseCases\.$FEATURE/namespace ShoppingApp.Tests.Domain.$FEATURE/" tests/Domain/$FEATURE/${NEW_NAME}Tests.cs
sed -i '' "s/using.*UseCases\.$FEATURE/using ShoppingApp.Domain.$FEATURE/" tests/Domain/$FEATURE/${NEW_NAME}Tests.cs
sed -i '' "s/class ${OLD_NAME}Tests/class ${NEW_NAME}Tests/" tests/Domain/$FEATURE/${NEW_NAME}Tests.cs
sed -i '' "s/$OLD_NAME _sut/$NEW_NAME _sut/" tests/Domain/$FEATURE/${NEW_NAME}Tests.cs
sed -i '' "s/new $OLD_NAME(/new $NEW_NAME(/" tests/Domain/$FEATURE/${NEW_NAME}Tests.cs

# 5. Update ViewModels
find src/Presentation -name "*.cs" -exec sed -i '' "s/using.*UseCases\.$FEATURE/using ShoppingApp.Domain.$FEATURE/" {} \;
find src/Presentation -name "*.cs" -exec sed -i '' "s/$OLD_NAME _/${NEW_NAME} _/g" {} \;
find src/Presentation -name "*.cs" -exec sed -i '' "s/$OLD_NAME $OLD_NAME/$NEW_NAME ${NEW_NAME}/g" {} \;

# 6. Update DI registration
sed -i '' "s/using.*UseCases\.$FEATURE/using ShoppingApp.Domain.$FEATURE/" src/MauiProgram.cs
sed -i '' "s/AddTransient<$OLD_NAME>/AddTransient<$NEW_NAME>/" src/MauiProgram.cs

# 7. Run tests
echo "Running tests..."
dotnet test

if [ $? -eq 0 ]; then
    echo "✅ Tests passing. Safe to delete old files."

    # 8. Delete old files
    rm src/UseCases/$FEATURE/${OLD_NAME}.cs
    rm tests/UseCases/$FEATURE/${OLD_NAME}Tests.cs

    # 9. Git operations
    git add src/Domain/$FEATURE/${NEW_NAME}.cs
    git add tests/Domain/$FEATURE/${NEW_NAME}Tests.cs
    git add src/MauiProgram.cs
    git add src/Presentation
    git rm src/UseCases/$FEATURE/${OLD_NAME}.cs
    git rm tests/UseCases/$FEATURE/${OLD_NAME}Tests.cs

    echo "✅ Migration complete. Review changes and commit."
else
    echo "❌ Tests failing. Review changes before proceeding."
    exit 1
fi
```

**Usage**:

```bash
chmod +x scripts/migrate-usecase-to-domain.sh

# Migrate individual operations
./scripts/migrate-usecase-to-domain.sh GetProductsUseCase GetProducts Products
./scripts/migrate-usecase-to-domain.sh CreateOrderUseCase CreateOrder Orders
./scripts/migrate-usecase-to-domain.sh UpdateCustomerUseCase UpdateCustomer Customers
```

### Migration Patterns by Operation Type

#### Pattern 1: Simple Query (No Parameters)

**Before**:
```csharp
public class GetProductsUseCase
{
    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}
```

**After**:
```csharp
public class GetProducts
{
    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}
```

**Changes**: Class name only. Logic unchanged.

#### Pattern 2: Query with Parameter

**Before**:
```csharp
public class GetProductByIdUseCase
{
    public async Task<ErrorOr<Product>> ExecuteAsync(Guid productId)
    {
        return await _repository.GetByIdAsync(productId);
    }
}
```

**After**:
```csharp
public class GetProductById
{
    public async Task<ErrorOr<Product>> ExecuteAsync(Guid productId)
    {
        return await _repository.GetByIdAsync(productId);
    }
}
```

**Changes**: Class name only. Logic unchanged.

#### Pattern 3: Command with Validation

**Before**:
```csharp
public class CreateProductUseCase
{
    public async Task<ErrorOr<Product>> ExecuteAsync(CreateProductRequest request)
    {
        var validationResult = ValidateRequest(request);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        var product = new Product { /* ... */ };
        return await _repository.CreateAsync(product);
    }

    private ErrorOr<Success> ValidateRequest(CreateProductRequest request)
    {
        // Validation logic
    }
}
```

**After**:
```csharp
public class CreateProduct
{
    public async Task<ErrorOr<Product>> ExecuteAsync(CreateProductRequest request)
    {
        var validationResult = ValidateRequest(request);
        if (validationResult.IsError)
        {
            return validationResult.Errors;
        }

        var product = new Product { /* ... */ };
        return await _repository.CreateAsync(product);
    }

    private ErrorOr<Success> ValidateRequest(CreateProductRequest request)
    {
        // Validation logic (unchanged)
    }
}
```

**Changes**: Class name only. Validation logic unchanged.

#### Pattern 4: Complex Command with Multiple Dependencies

**Before**:
```csharp
public class CreateOrderUseCase
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly IPaymentService _paymentService;

    public CreateOrderUseCase(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        IPaymentService paymentService)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _paymentService = paymentService;
    }

    public async Task<ErrorOr<Order>> ExecuteAsync(CreateOrderRequest request)
    {
        // Complex logic with multiple dependencies
    }
}
```

**After**:
```csharp
public class CreateOrder
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly IPaymentService _paymentService;

    public CreateOrder(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        IPaymentService paymentService)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _paymentService = paymentService;
    }

    public async Task<ErrorOr<Order>> ExecuteAsync(CreateOrderRequest request)
    {
        // Complex logic (unchanged)
    }
}
```

**Changes**: Class name and constructor only. Logic unchanged.

### Handling Edge Cases

#### Edge Case 1: Generic UseCase Names

**Before**:
```csharp
public class ProcessPaymentUseCase { ... }
```

**After**:
```csharp
public class ProcessPayment { ... }
```

**Guideline**: Remove "UseCase" suffix. If name is already verb-based, keep it.

#### Edge Case 2: Multiple Responsibilities

**Before**:
```csharp
public class GetAndValidateProductsUseCase
{
    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        var products = await _repository.GetAllAsync();
        // Validate products
        // Filter products
        return products;
    }
}
```

**Refactoring Needed**: Split into focused operations:

**After**:
```csharp
// Get operation
public class GetProducts
{
    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}

// Validate operation
public class ValidateProducts
{
    public async Task<ErrorOr<List<Product>>> ExecuteAsync(List<Product> products)
    {
        // Validation logic
        return validProducts;
    }
}

// ViewModel composes both
public partial class ProductListViewModel : ObservableObject
{
    private readonly GetProducts _getProducts;
    private readonly ValidateProducts _validateProducts;

    [RelayCommand]
    private async Task LoadAsync()
    {
        var getResult = await _getProducts.ExecuteAsync();
        if (getResult.IsError) return;

        var validateResult = await _validateProducts.ExecuteAsync(getResult.Value);
        // ...
    }
}
```

#### Edge Case 3: CQRS Command/Query Suffix

**Before (CQRS pattern)**:
```csharp
public class GetProductsQuery { ... }
public class CreateProductCommand { ... }
```

**After (Domain pattern)**:
```csharp
public class GetProducts { ... }    // Query → Get
public class CreateProduct { ... }  // Command → Create
```

**Guideline**: Remove "Query"/"Command" suffix. Use verb prefix (Get, Create).

**Exception**: If using CQRS library (MediatR), keep suffixes for library conventions.

### Validation and Testing

#### Pre-Migration Test Coverage

```bash
# Check test coverage before migration
dotnet test /p:CollectCoverage=true /p:CoverageReporter=cobertura

# Save baseline coverage
mv coverage.cobertura.xml coverage-baseline.xml
```

#### Post-Migration Test Coverage

```bash
# Check test coverage after migration
dotnet test /p:CollectCoverage=true /p:CoverageReporter=cobertura

# Compare to baseline
diff coverage-baseline.xml coverage.cobertura.xml

# Expected: No coverage loss
```

#### Smoke Testing Checklist

After each migration:

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] App builds successfully
- [ ] App launches without crashes
- [ ] All screens navigate correctly
- [ ] Data loads correctly on all screens
- [ ] Create/Update/Delete operations work
- [ ] No console errors or warnings

#### Regression Testing

Test all features thoroughly:

```markdown
## Regression Test Plan

### Products Feature
- [ ] List all products
- [ ] View product details
- [ ] Create new product
- [ ] Update existing product
- [ ] Delete product

### Orders Feature
- [ ] List all orders
- [ ] Create new order
- [ ] Update order status
- [ ] View order details

### Customers Feature
- [ ] List all customers
- [ ] Create new customer
- [ ] Update customer info
- [ ] View customer details
```

---

## Examples

### Example 1: Migrate Complete Feature (Products)

**Feature Inventory**:
```
Products Feature (5 operations)
- GetProductsUseCase → GetProducts
- GetProductByIdUseCase → GetProductById
- CreateProductUseCase → CreateProduct
- UpdateProductUseCase → UpdateProduct
- DeleteProductUseCase → DeleteProduct
```

**Migration Commands**:
```bash
# Migrate all operations in Products feature
./scripts/migrate-usecase-to-domain.sh GetProductsUseCase GetProducts Products
./scripts/migrate-usecase-to-domain.sh GetProductByIdUseCase GetProductById Products
./scripts/migrate-usecase-to-domain.sh CreateProductUseCase CreateProduct Products
./scripts/migrate-usecase-to-domain.sh UpdateProductUseCase UpdateProduct Products
./scripts/migrate-usecase-to-domain.sh DeleteProductUseCase DeleteProduct Products

# Run full test suite
dotnet test

# Commit feature migration
git commit -m "refactor: Migrate Products feature to Domain pattern

- Migrated 5 operations: Get, GetById, Create, Update, Delete
- All tests passing ✅
- Coverage maintained at 85%"
```

### Example 2: Migrate with Custom Naming

**Before** (non-standard naming):
```csharp
public class ProductFetcherEngine { ... }
public class OrderCreationHandler { ... }
```

**After** (standardized):
```csharp
public class GetProducts { ... }
public class CreateOrder { ... }
```

**Custom Script**:
```bash
# Manual rename for non-standard names
mv src/Engines/ProductFetcherEngine.cs src/Domain/Products/GetProducts.cs

# Update class name manually
sed -i '' "s/class ProductFetcherEngine/class GetProducts/" src/Domain/Products/GetProducts.cs
```

### Example 3: Incremental Migration with Feature Flags

Use feature flags to migrate gradually in production:

```csharp
// MauiProgram.cs
if (Configuration.GetValue<bool>("UseNewDomainPattern"))
{
    // New Domain pattern
    builder.Services.AddTransient<GetProducts>();
    builder.Services.AddTransient<CreateOrder>();
}
else
{
    // Old UseCase pattern (fallback)
    builder.Services.AddTransient<GetProductsUseCase>();
    builder.Services.AddTransient<CreateOrderUseCase>();
}
```

**Benefits**:
- Test in production with small user percentage
- Easy rollback if issues detected
- Gradual confidence building

---

## FAQ

### Q: Do I need to change the internal logic of operations?

**A**: No. Only rename files, classes, and update references. The internal logic (ExecuteAsync implementation) remains identical.

### Q: What if my tests break after migration?

**A**: Common causes:
1. Missed reference in ViewModel (search and replace missed)
2. Missed DI registration in MauiProgram.cs
3. Test class not renamed properly

**Solution**: Use IDE "Find References" to locate all usages before deleting old files.

### Q: Should I migrate all at once or incrementally?

**A**: **Incrementally** (Recommended) - Migrate one feature at a time to minimize risk.

**Exception**: Small apps (<10 operations) can migrate all at once.

### Q: How do I handle third-party code that uses UseCase pattern?

**A**: Leave third-party code unchanged. Wrap it in an adapter:

```csharp
// Your Domain operation (adapter)
public class GetProducts
{
    private readonly ThirdParty.GetProductsUseCase _useCase;

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _useCase.ExecuteAsync();
    }
}
```

### Q: What if my team disagrees on naming?

**A**: Establish naming convention document:

```markdown
## Team Naming Convention

**Domain Operations**: {Verb}{Entity}
- Examples: GetProducts, CreateOrder, UpdateCustomer

**Prohibited Suffixes**: UseCase, Engine, Handler, Processor

**Exception**: CQRS libraries (MediatR) - keep Command/Query suffix
```

Get team buy-in before starting migration.

### Q: How long does migration typically take?

**A**:
- **Simple operation**: 10 minutes
- **Complex operation**: 30 minutes
- **Full feature (5 ops)**: 1-2 hours
- **Entire app (50 ops)**: 1-2 weeks (incremental)

### Q: Can I automate the migration completely?

**A**: 80-90% can be automated with scripts. Manual verification still needed for:
- Complex naming scenarios
- Custom patterns
- Test validation
- Documentation updates

---

## Related Documentation

- [Domain Layer Pattern](../patterns/domain-layer-pattern.md) - Target pattern after migration
- [Creating Local Templates](../guides/creating-local-templates.md) - Create templates with new pattern
- [MAUI Template Selection](../guides/maui-template-selection.md) - Choose base template

---

**Last Updated**: 2025-10-15
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
