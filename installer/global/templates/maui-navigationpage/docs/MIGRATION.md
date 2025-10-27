# Migration Guide: AppShell to NavigationPage

This guide helps you migrate from the **maui-appshell** template to the **maui-navigationpage** template.

## Why Migrate?

Consider migrating from AppShell to NavigationPage if:

- Your app has simple linear navigation without tabs or flyout
- You need more explicit control over the navigation stack
- You're primarily using modal navigation patterns
- AppShell's routing complexity is unnecessary for your use case
- You're migrating from Xamarin.Forms NavigationPage apps

**Do NOT migrate if:**
- Your app uses tabbed navigation (multiple top-level sections)
- You have flyout/drawer navigation
- You rely on URL-based routing and deep linking
- Your navigation structure is complex and hierarchical

## High-Level Changes

| Component | AppShell | NavigationPage |
|-----------|----------|----------------|
| Root Page | `AppShell` | `NavigationPage` |
| Navigation Interface | `INavigator` | `INavigator` |
| Navigation Method | `GoToAsync(route)` | `NavigateToAsync<TViewModel>()` |
| Parameter Passing | Query parameters | Type-safe parameter objects |
| Route Definition | Shell routes in XAML | Convention-based resolution |
| DI Registration | Route registration | Page/ViewModel registration |

## Step-by-Step Migration

### Step 1: Update App.xaml.cs

**Before (AppShell):**
```csharp
public partial class App : Application
{
    public App()
    {
        InitializeComponent();

        MainPage = new AppShell();
    }
}
```

**After (NavigationPage):**
```csharp
public partial class App : Application
{
    public App()
    {
        InitializeComponent();

        MainPage = new NavigationPage(new MainPage());
    }
}
```

### Step 2: Update MauiProgram.cs

**Before (AppShell):**
```csharp
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    builder
        .UseMauiApp<App>()
        .ConfigureFonts(fonts =>
        {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
        });

    // Register services, ViewModels
    builder.Services.AddSingleton<INavigator, Navigator>();
    builder.Services.AddTransient<ProductDetailViewModel>();

    return builder.Build();
}
```

**After (NavigationPage):**
```csharp
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    builder
        .UseMauiApp<App>()
        .ConfigureFonts(fonts =>
        {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
        });

    // Add navigation services
    builder.AddNavigationServices();

    // Register Pages and ViewModels
    builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();

    return builder.Build();
}
```

### Step 3: Update ViewModelBase

**Before (AppShell):**
```csharp
public abstract class ViewModelBase : ObservableObject
{
    protected INavigator Navigator { get; }

    protected ViewModelBase(INavigator navigator)
    {
        Navigator = navigator;
    }
}
```

**After (NavigationPage):**
```csharp
public abstract class ViewModelBase : ObservableObject
{
    protected INavigator Navigator { get; }

    protected ViewModelBase(INavigator navigator)
    {
        NavigationService = navigationService;
    }
}
```

### Step 4: Update Navigation Calls

**Before (AppShell):**
```csharp
// Simple navigation
await Navigator.GoToAsync("///ProductDetail");

// With parameters
await Navigator.GoToAsync($"///ProductDetail?productId={productId}");

// With navigation parameters
var parameters = new Dictionary<string, object>
{
    { "productId", productId }
};
await Navigator.GoToAsync("///ProductDetail", parameters);
```

**After (NavigationPage):**
```csharp
// Simple navigation
await Navigator.NavigateToAsync<ProductDetailViewModel>();

// With parameters
await Navigator.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
    new ProductDetailParams { ProductId = productId });
```

### Step 5: Update Parameter Handling

**Before (AppShell):**
```csharp
public class ProductDetailViewModel : ViewModelBase, IQueryAttributable
{
    private string _productId;

    public void ApplyQueryAttributes(IDictionary<string, object> query)
    {
        if (query.ContainsKey("productId"))
        {
            _productId = query["productId"].ToString();
            Task.Run(async () => await LoadProduct(_productId));
        }
    }
}
```

**After (NavigationPage):**
```csharp
public class ProductDetailParams
{
    public string ProductId { get; set; }
}

public class ProductDetailViewModel : ViewModelBase<ProductDetailParams>
{
    private string _productId;

    public override void OnPrepare(ProductDetailParams parameter)
    {
        _productId = parameter.ProductId;
    }

    public override async Task OnInitialize()
    {
        await LoadProduct(_productId);
    }
}
```

### Step 6: Remove AppShell Routes

**Before (AppShell.xaml):**
```xml
<Shell xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
       xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
       x:Class="YourApp.AppShell">

    <ShellContent Title="Home"
                  ContentTemplate="{DataTemplate local:HomePage}"
                  Route="Home" />

    <ShellContent Title="ProductDetail"
                  ContentTemplate="{DataTemplate local:ProductDetailPage}"
                  Route="ProductDetail" />
</Shell>
```

**After:**
- Delete AppShell.xaml and AppShell.xaml.cs files
- Routes are no longer needed (convention-based resolution)

### Step 7: Update Back Navigation

**Before (AppShell):**
```csharp
// Go back
await Navigator.GoToAsync("..");

// Go to root
await Navigator.GoToAsync("///Home");
```

**After (NavigationPage):**
```csharp
// Go back
await Navigator.GoBackAsync();

// Go to root
await Navigator.PopToRootAsync();
```

## API Mapping Table

| AppShell API | NavigationPage API | Notes |
|--------------|-------------------|-------|
| `GoToAsync(route)` | `NavigateToAsync<TViewModel>()` | Type-safe navigation |
| `GoToAsync(route, params)` | `NavigateToAsync<TViewModel, TParams>(params)` | Type-safe parameters |
| `GoToAsync("..")` | `GoBackAsync()` | Back navigation |
| `GoToAsync("//Root")` | `PopToRootAsync()` | Navigate to root |
| `IQueryAttributable` | `ViewModelBase<TParams>` | Parameter handling |
| `ApplyQueryAttributes()` | `OnPrepare(TParams)` | Receive parameters |
| Shell routes | Convention-based | No route registration needed |

## Common Migration Pitfalls

### 1. Forgetting to Register Pages

**Problem:**
```csharp
// Only registered ViewModel
builder.Services.AddTransient<ProductDetailViewModel>();
```

**Solution:**
```csharp
// Register both Page and ViewModel
builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();
```

### 2. Wrong Namespace Convention

**Problem:**
```csharp
// ViewModel in Pages namespace
namespace YourApp.Pages
{
    public class ProductDetailViewModel : ViewModelBase { }
}
```

**Solution:**
```csharp
// ViewModel in ViewModels namespace
namespace YourApp.ViewModels
{
    public class ProductDetailViewModel : ViewModelBase { }
}
```

### 3. Not Updating ViewModel Constructor

**Problem:**
```csharp
// Still using INavigator
public ProductDetailViewModel(INavigator navigator)
    : base(navigator) { }
```

**Solution:**
```csharp
// Use INavigator
public ProductDetailViewModel(INavigator navigator)
    : base(navigationService) { }
```

### 4. Mixing Navigation Approaches

**Problem:**
```csharp
// Using both old and new navigation
await Shell.Current.GoToAsync("ProductDetail");  // Old
await Navigator.NavigateToAsync<ProductDetailViewModel>();  // New
```

**Solution:**
```csharp
// Always use NavigationService
await Navigator.NavigateToAsync<ProductDetailViewModel>();
```

## Before and After Examples

### Example 1: List-Detail Navigation

**Before (AppShell):**
```csharp
// AppShell.xaml
<ShellContent Route="ProductList" ContentTemplate="{DataTemplate local:ProductListPage}" />
<ShellContent Route="ProductDetail" ContentTemplate="{DataTemplate local:ProductDetailPage}" />

// ProductListViewModel.cs
[RelayCommand]
private async Task ViewProduct(string productId)
{
    await Navigator.GoToAsync($"ProductDetail?productId={productId}");
}

// ProductDetailViewModel.cs
public class ProductDetailViewModel : ViewModelBase, IQueryAttributable
{
    public void ApplyQueryAttributes(IDictionary<string, object> query)
    {
        if (query.ContainsKey("productId"))
        {
            var productId = query["productId"].ToString();
            Task.Run(async () => await LoadProduct(productId));
        }
    }
}
```

**After (NavigationPage):**
```csharp
// No routes needed

// MauiProgram.cs
builder.Services.AddPageViewModel<ProductListPage, ProductListViewModel>();
builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();

// ProductListViewModel.cs
[RelayCommand]
private async Task ViewProduct(string productId)
{
    await Navigator.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
        new ProductDetailParams { ProductId = productId });
}

// ProductDetailViewModel.cs
public class ProductDetailViewModel : ViewModelBase<ProductDetailParams>
{
    public override void OnPrepare(ProductDetailParams parameter)
    {
        _productId = parameter.ProductId;
    }

    public override async Task OnInitialize()
    {
        await LoadProduct(_productId);
    }
}
```

### Example 2: Modal Navigation

**Before (AppShell):**
```csharp
// Navigate to modal
await Navigator.GoToAsync("FilterModal", new Dictionary<string, object>
{
    { "currentFilter", CurrentFilter }
});

// Go back
await Navigator.GoToAsync("..");
```

**After (NavigationPage):**
```csharp
// Navigate to modal
await Navigator.NavigateToAsync<FilterViewModel, FilterParams>(
    new FilterParams { CurrentFilter = CurrentFilter });

// Go back
await Navigator.GoBackAsync();
```

## Testing Migration

### Before (AppShell)

```csharp
[Fact]
public async Task ViewProduct_ShouldNavigateToDetail()
{
    // Arrange
    var mockNavigator = Substitute.For<INavigator>();
    var viewModel = new ProductListViewModel(mockNavigator);

    // Act
    await viewModel.ViewProductCommand.ExecuteAsync("123");

    // Assert
    await mockNavigator.Received(1).GoToAsync(Arg.Is<string>(s => s.Contains("productId=123")));
}
```

### After (NavigationPage)

```csharp
[Fact]
public async Task ViewProduct_ShouldNavigateToDetail()
{
    // Arrange
    var mockNavigation = Substitute.For<INavigator>();
    var viewModel = new ProductListViewModel(mockNavigation);

    // Act
    await viewModel.ViewProductCommand.ExecuteAsync("123");

    // Assert
    await mockNavigation.Received(1)
        .NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
            Arg.Is<ProductDetailParams>(p => p.ProductId == "123"));
}
```

## Rollback Plan

If you need to rollback:

1. Restore App.xaml.cs to use AppShell
2. Restore AppShell.xaml and AppShell.xaml.cs files
3. Change ViewModelBase constructor back to `INavigator`
4. Replace `NavigateToAsync` calls with `GoToAsync`
5. Restore IQueryAttributable implementations
6. Update MauiProgram.cs to register INavigator

## Getting Help

- Review CLAUDE.md for NavigationPage patterns
- Review README.md for API reference
- Check examples in the template
- File an issue at: https://github.com/agentecflow/ai-engineer/issues

## Checklist

Use this checklist to ensure complete migration:

- [ ] Updated App.xaml.cs to use NavigationPage
- [ ] Updated MauiProgram.cs to call AddNavigationServices()
- [ ] Registered all Pages and ViewModels
- [ ] Changed ViewModelBase constructor to use INavigator
- [ ] Replaced all GoToAsync calls with NavigateToAsync
- [ ] Converted query parameters to parameter objects
- [ ] Removed AppShell.xaml and routes
- [ ] Updated all ViewModels to use OnPrepare/OnInitialize
- [ ] Updated unit tests to mock INavigator
- [ ] Tested all navigation flows
- [ ] Verified back navigation works
- [ ] Verified parameter passing works
- [ ] Updated documentation

## Timeline Estimate

| Project Size | Estimated Time |
|-------------|----------------|
| Small (1-5 pages) | 2-4 hours |
| Medium (6-15 pages) | 1-2 days |
| Large (16+ pages) | 3-5 days |

The migration is straightforward but requires careful attention to ensure all navigation paths are updated correctly.
