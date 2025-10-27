# .NET MAUI Template Architecture

## Overview

This document defines the architecture patterns for .NET MAUI templates in the Agentecflow system. It provides clear separation between global (generic) templates and local (project-specific) templates.

## Template Types

### Global Templates (Repository-Level)

**Location**: `installer/global/templates/`

Two global MAUI templates are available:

1. **maui-appshell**: Modern MAUI with Shell-based navigation (recommended)
2. **maui-navigationpage**: Traditional NavigationPage-based navigation

### Local Templates (Project-Level)

**Location**: `<project>/.claude/templates/`

Projects can define custom templates for organization-specific patterns:
- MyDrive: Uses `Engine` suffix pattern
- Other projects: Can define their own naming conventions

## Architecture Layers

### Domain Layer (Business Logic)

**Purpose**: Contains business rules and orchestration logic

**Pattern**: Verb-based naming, no suffix
- ✅ `GetProducts`
- ✅ `CreateOrder`
- ✅ `UpdateUserProfile`
- ❌ `GetProductsUseCase`
- ❌ `GetProductsEngine`

**Namespace**: `<ProjectName>.Domain`

**Example**:
```csharp
namespace MyApp.Domain;

/// <summary>
/// Retrieves products with caching support
/// </summary>
public class GetProducts
{
    private readonly IProductRepository _repository;
    private readonly IApiService _apiService;
    private readonly ICacheService _cacheService;

    public GetProducts(
        IProductRepository repository,
        IApiService apiService,
        ICacheService cacheService)
    {
        _repository = repository;
        _apiService = apiService;
        _cacheService = cacheService;
    }

    public async Task<ErrorOr<List<Product>>> ExecuteAsync(string? category = null)
    {
        // Try cache first
        var cached = await _cacheService.GetAsync<List<Product>>($"products_{category}");
        if (cached != null) return cached;

        // Try local database
        var localProducts = await _repository.GetByCategoryAsync(category);
        if (localProducts.Any()) return localProducts.ToList();

        // Fallback to API
        var apiResult = await _apiService.GetAsync<List<Product>>($"/products?category={category}");
        if (apiResult.IsError) return apiResult.Errors;

        // Cache and persist
        await _cacheService.SetAsync($"products_{category}", apiResult.Value);
        await _repository.AddRangeAsync(apiResult.Value);

        return apiResult.Value;
    }
}
```

### Data Access Layer

#### Repositories (Database Access)

**Purpose**: Database operations (SQLite, LiteDB, etc.)

**Pattern**: Repository pattern with interface
- Interface: `IProductRepository`
- Implementation: `ProductRepository`

**Namespace**: `<ProjectName>.Data.Repositories`

**Example**:
```csharp
namespace MyApp.Data.Repositories;

public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id);
    Task<IEnumerable<Product>> GetByCategoryAsync(string? category);
    Task<int> AddAsync(Product product);
    Task AddRangeAsync(IEnumerable<Product> products);
    Task UpdateAsync(Product product);
    Task DeleteAsync(int id);
}

public class ProductRepository : IProductRepository
{
    private readonly SQLiteAsyncConnection _database;

    public ProductRepository(SQLiteAsyncConnection database)
    {
        _database = database;
    }

    public async Task<Product?> GetByIdAsync(int id)
    {
        return await _database.Table<Product>()
            .FirstOrDefaultAsync(p => p.Id == id);
    }

    public async Task<IEnumerable<Product>> GetByCategoryAsync(string? category)
    {
        if (string.IsNullOrWhiteSpace(category))
            return await _database.Table<Product>().ToListAsync();

        return await _database.Table<Product>()
            .Where(p => p.Category == category)
            .ToListAsync();
    }

    public async Task<int> AddAsync(Product product)
    {
        return await _database.InsertAsync(product);
    }

    public async Task AddRangeAsync(IEnumerable<Product> products)
    {
        await _database.InsertAllAsync(products);
    }

    public async Task UpdateAsync(Product product)
    {
        await _database.UpdateAsync(product);
    }

    public async Task DeleteAsync(int id)
    {
        await _database.DeleteAsync<Product>(id);
    }
}
```

#### Services (APIs, Hardware, External)

**Purpose**: External system integration

**Pattern**: Service pattern with interface
- Interface: `IApiService`, `ILocationService`, `ICacheService`
- Implementation: `ApiService`, `LocationService`, `CacheService`

**Namespace**: `<ProjectName>.Services`

**Example**:
```csharp
namespace MyApp.Services;

public interface IApiService
{
    Task<ErrorOr<T>> GetAsync<T>(string endpoint);
    Task<ErrorOr<T>> PostAsync<T>(string endpoint, object data);
    Task<ErrorOr<T>> PutAsync<T>(string endpoint, object data);
    Task<ErrorOr<bool>> DeleteAsync(string endpoint);
}

public interface ILocationService
{
    Task<ErrorOr<Location>> GetCurrentLocationAsync();
    Task<bool> IsLocationEnabledAsync();
}

public interface ICacheService
{
    Task<T?> GetAsync<T>(string key);
    Task SetAsync<T>(string key, T value, TimeSpan? expiry = null);
    Task RemoveAsync(string key);
    Task ClearAsync();
}
```

## Complete Layer Interaction Example

```csharp
// Domain Layer: GetProducts
namespace MyApp.Domain;

public class GetProducts
{
    private readonly IProductRepository _repository;  // Database
    private readonly IApiService _apiService;         // External API
    private readonly ICacheService _cacheService;     // Local cache
    private readonly IConnectivityService _connectivity; // Hardware

    public async Task<ErrorOr<List<Product>>> ExecuteAsync(ProductQuery query)
    {
        // 1. Try cache (fast)
        var cacheKey = $"products_{query.Category}_{query.PageIndex}";
        var cached = await _cacheService.GetAsync<List<Product>>(cacheKey);
        if (cached != null) return cached;

        // 2. Try local database (offline support)
        if (!await _connectivity.IsConnectedAsync())
        {
            var localProducts = await _repository.GetByCategoryAsync(query.Category);
            return localProducts.ToList();
        }

        // 3. Fetch from API (online)
        var apiResult = await _apiService.GetAsync<List<Product>>(
            $"/products?category={query.Category}&page={query.PageIndex}");

        if (apiResult.IsError)
        {
            // Fallback to database on API error
            var localProducts = await _repository.GetByCategoryAsync(query.Category);
            if (localProducts.Any()) return localProducts.ToList();
            return apiResult.Errors;
        }

        // 4. Update cache and database
        await _cacheService.SetAsync(cacheKey, apiResult.Value, TimeSpan.FromMinutes(5));
        await _repository.AddRangeAsync(apiResult.Value);

        return apiResult.Value;
    }
}
```

## Navigation Patterns

### AppShell Navigation (maui-appshell)

**Use When**:
- Modern MAUI applications
- Single-level navigation
- Flyout menus and tabs
- Bottom tab bars
- Simple hierarchical navigation

**Example**:
```csharp
// AppShell.xaml.cs
public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();

        Routing.RegisterRoute(nameof(ProductDetailPage), typeof(ProductDetailPage));
        Routing.RegisterRoute(nameof(OrderHistoryPage), typeof(OrderHistoryPage));
    }
}

// ViewModel navigation
await Shell.Current.GoToAsync(nameof(ProductDetailPage),
    new Dictionary<string, object> { { "ProductId", productId } });
```

### NavigationPage Navigation (maui-navigationpage)

**Use When**:
- Complex navigation flows
- Multiple navigation stacks
- Custom navigation behavior
- Legacy XAML Forms migration
- Deep linking requirements

**Example**:
```csharp
// INavigationService.cs
public interface INavigationService
{
    Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase;
    Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
        where TViewModel : ViewModelBase<TParams>;
    Task GoBackAsync();
    Task PopToRootAsync();
}

// ViewModel navigation
await _navigationService.NavigateToAsync<ProductDetailViewModel, ProductParams>(
    new ProductParams { ProductId = productId });
```

## Project Structure

### Global Template Structure
```
maui-appshell/
├── agents/
│   ├── maui-domain-specialist.md      # Domain layer expert
│   ├── maui-repository-specialist.md  # Database access expert
│   ├── maui-service-specialist.md     # External services expert
│   ├── maui-viewmodel-specialist.md   # MVVM expert
│   └── maui-ui-specialist.md          # XAML/UI expert
├── templates/
│   ├── Domain.cs                      # Domain layer template
│   ├── Repository.cs                  # Repository template
│   ├── Service.cs                     # Service template
│   ├── ViewModel.cs                   # ViewModel template
│   └── Page.xaml                      # Page template
├── CLAUDE.md                          # Template guidance
└── manifest.json                      # Template metadata
```

### Local Template Structure (Example: MyDrive)
```
.claude/templates/maui-mydrive/
├── agents/
│   ├── maui-engine-specialist.md      # MyDrive Engine pattern
│   └── [other custom agents]
├── templates/
│   ├── Engine.cs                      # MyDrive Engine template
│   └── [other custom templates]
├── CLAUDE.md                          # MyDrive-specific guidance
└── manifest.json                      # Custom template metadata
```

## Template Priority Resolution

When initializing a project, templates are resolved in this order:

1. **Local project template** (`.claude/templates/<template-name>/`)
2. **Global template** (`~/.agentecflow/templates/<template-name>/`)
3. **Fallback to default** (`~/.agentecflow/templates/default/`)

Example:
```bash
# Uses global template
agentec-init maui-appshell

# Uses local template (if exists in .claude/templates/)
agentec-init maui-mydrive
```

## Creating Local Templates

### Option 1: Start from Global Template
```bash
# Copy global template to project
mkdir -p .claude/templates/maui-custom
cp -r ~/.agentecflow/templates/maui-appshell/* .claude/templates/maui-custom/

# Customize for your project
# Edit .claude/templates/maui-custom/CLAUDE.md
# Edit agents and templates as needed
```

### Option 2: Create from Scratch
```bash
mkdir -p .claude/templates/maui-custom/{agents,templates}

# Create manifest.json
cat > .claude/templates/maui-custom/manifest.json << EOF
{
  "name": "maui-custom",
  "description": "Custom MAUI template for MyProject",
  "version": "1.0.0",
  "base": "maui-appshell",
  "customizations": {
    "domain_pattern": "Engine",
    "namespace_pattern": "MyCompany.MyProject"
  }
}
EOF

# Create custom agents and templates
```

## Best Practices

### Domain Layer
1. ✅ Use verb-based naming (GetProducts, CreateOrder)
2. ✅ Keep business logic in Domain layer
3. ✅ Return `ErrorOr<T>` for functional error handling
4. ✅ Compose Repositories and Services
5. ❌ Don't access database directly from ViewModels
6. ❌ Don't put UI logic in Domain layer

### Repository Layer
1. ✅ Use for database access ONLY
2. ✅ Interface-based design
3. ✅ Return domain models
4. ✅ Handle database-specific errors
5. ❌ Don't call APIs from Repositories
6. ❌ Don't put business logic in Repositories

### Service Layer
1. ✅ Use for external systems (APIs, hardware)
2. ✅ Interface-based design
3. ✅ Return `ErrorOr<T>` for error handling
4. ✅ Handle connectivity and timeouts
5. ❌ Don't access database from Services
6. ❌ Don't put business logic in Services

### ViewModel Layer
1. ✅ Orchestrate Domain layer calls
2. ✅ Manage UI state (loading, error messages)
3. ✅ Use ObservableProperty and RelayCommand
4. ✅ Thin ViewModels - delegate to Domain
5. ❌ Don't put business logic in ViewModels
6. ❌ Don't call Repositories/Services directly

## Migration Guide

### From Engine Pattern to Domain Pattern

**Before** (MyDrive-specific):
```csharp
namespace DeCUK.Mobile.MyDrive.Engines;

public class GetProductsEngine
{
    // Implementation
}
```

**After** (Generic pattern):
```csharp
namespace MyApp.Domain;

public class GetProducts
{
    // Implementation
}
```

### Creating Local Template from Current Project

```bash
# 1. Create local template directory
mkdir -p .claude/templates/maui-mydrive

# 2. Copy current patterns
cp -r installer/global/templates/maui/* .claude/templates/maui-mydrive/

# 3. Update manifest to mark as local
cat > .claude/templates/maui-mydrive/manifest.json << EOF
{
  "name": "maui-mydrive",
  "description": "MyDrive-specific MAUI template with Engine pattern",
  "version": "1.0.0",
  "scope": "local",
  "base": "maui-appshell",
  "customizations": {
    "domain_pattern": "Engine",
    "namespace_pattern": "DeCUK.Mobile.MyDrive"
  }
}
EOF

# 4. Commit to source control
git add .claude/templates/maui-mydrive
git commit -m "Add MyDrive-specific MAUI template"
```

## Comparison: Global vs Local Templates

| Aspect | Global Template | Local Template |
|--------|----------------|----------------|
| **Location** | `~/.agentecflow/templates/` | `.claude/templates/` |
| **Scope** | All projects | Single project |
| **Version Control** | Not in project repo | Committed with project |
| **Customization** | Generic patterns | Project-specific |
| **Naming** | Verb-based (GetProducts) | Custom (Engine, UseCase) |
| **Namespace** | Generic (Domain) | Custom (Engines, UseCases) |
| **Updates** | Via installer | Manual/team decision |

## Examples

### Complete Feature Implementation

**Scenario**: Add "View Product Details" feature

```bash
# 1. Create Domain class
# File: Domain/GetProductDetails.cs
namespace MyApp.Domain;

public class GetProductDetails
{
    private readonly IProductRepository _repository;
    private readonly IApiService _apiService;

    public async Task<ErrorOr<ProductDetails>> ExecuteAsync(int productId)
    {
        // Try local database first
        var product = await _repository.GetByIdAsync(productId);
        if (product != null) return ProductDetails.FromProduct(product);

        // Fallback to API
        var apiResult = await _apiService.GetAsync<ProductDetails>($"/products/{productId}");
        if (apiResult.IsError) return apiResult.Errors;

        // Cache in database
        await _repository.AddAsync(apiResult.Value.ToProduct());
        return apiResult.Value;
    }
}

# 2. Create ViewModel
# File: ViewModels/ProductDetailViewModel.cs
namespace MyApp.ViewModels;

public partial class ProductDetailViewModel : ViewModelBase
{
    private readonly GetProductDetails _getProductDetails;

    [ObservableProperty]
    private ProductDetails? _product;

    [ObservableProperty]
    private bool _isLoading;

    [RelayCommand]
    private async Task LoadProductAsync()
    {
        IsLoading = true;

        var result = await _getProductDetails.ExecuteAsync(ProductId);

        result.Match(
            value => Product = value,
            errors => ShowError(errors)
        );

        IsLoading = false;
    }
}

# 3. Create View
# File: Views/ProductDetailPage.xaml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.Views.ProductDetailPage">
    <VerticalStackLayout>
        <Label Text="{Binding Product.Name}" />
        <Label Text="{Binding Product.Description}" />
        <Label Text="{Binding Product.Price, StringFormat='{0:C}'}" />
    </VerticalStackLayout>
</ContentPage>
```

## Summary

**Key Architectural Decisions**:
1. ✅ **Domain layer**: Verb-based naming, no suffix
2. ✅ **Repositories**: Database access only
3. ✅ **Services**: APIs and hardware only
4. ✅ **ViewModels**: Thin orchestrators
5. ✅ **Two navigation options**: AppShell vs NavigationPage
6. ✅ **Local templates**: Project-specific customizations
7. ✅ **Global templates**: Generic, reusable patterns

This architecture provides clean separation of concerns, testability, and flexibility while maintaining consistency across projects.
