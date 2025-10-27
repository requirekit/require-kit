# .NET MAUI NavigationPage Template

A production-ready .NET MAUI template using **NavigationPage** for traditional page-based navigation with MVVM architecture, ErrorOr pattern, and comprehensive testing support.

## Quick Start

### 1. Initialize Project

```bash
# Create new project with this template
agentic-init maui-navigationpage

# Or select interactively
agentic-init
> Select: maui-navigationpage
```

### 2. Setup App Structure

```csharp
// App.xaml.cs
public partial class App : Application
{
    public App()
    {
        InitializeComponent();

        // Set NavigationPage as root
        MainPage = new NavigationPage(new MainPage());
    }
}
```

### 3. Register Navigation Services

```csharp
// MauiProgram.cs
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
    builder.AddNavigators();

    // Register your pages and ViewModels
    builder.Services.AddPageViewModel<HomePage, HomeViewModel>();
    builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();

    return builder.Build();
}
```

### 4. Create Your First Page

```csharp
// ViewModels/HomeViewModel.cs
public class HomeViewModel : ViewModelBase
{
    public HomeViewModel(INavigator navigationService)
        : base(navigationService)
    {
    }

    [RelayCommand]
    private async Task NavigateToProductDetail(string productId)
    {
        await Navigator.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
            new ProductDetailParams { ProductId = productId });
    }
}

// Pages/HomePage.xaml
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="YourApp.Pages.HomePage"
             Title="Home">
    <VerticalStackLayout Padding="20">
        <Button Text="View Product"
                Command="{Binding NavigateToProductDetailCommand}"
                CommandParameter="123" />
    </VerticalStackLayout>
</ContentPage>
```

## Navigation Architecture

### Overview

```
App.xaml.cs
    └─ new NavigationPage(MainPage)
           └─ INavigator (Singleton)
                  ├─ Resolves Pages from DI
                  ├─ Resolves ViewModels from DI
                  ├─ Manages Navigation Stack
                  └─ Handles Parameter Passing
```

### Core Components

#### INavigator

The central navigation abstraction:

```csharp
public interface INavigator
{
    // Navigate without parameters
    Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase;

    // Navigate with parameters
    Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
        where TViewModel : ViewModelBase<TParams>;

    // Navigate back
    Task GoBackAsync();

    // Pop to root
    Task PopToRootAsync();
}
```

**Key Features:**
- Type-safe navigation using ViewModels
- Automatic page resolution via naming conventions
- Parameter passing with type safety
- Exception-based error handling

#### Navigator Implementation

**Convention-Based Resolution:**
- `ProductDetailViewModel` → `ProductDetailPage`
- Namespace: `YourApp.ViewModels` → `YourApp.Pages`

**Resolution Process:**
1. Extract ViewModel type
2. Apply naming convention (ViewModel → Page)
3. Resolve Page from DI container
4. Resolve ViewModel from DI container
5. Bind ViewModel to Page
6. Call lifecycle hooks (OnPrepare, OnInitialize)
7. Push to navigation stack

#### ViewModelBase

Base class for all ViewModels with navigation support:

```csharp
public abstract class ViewModelBase : ObservableObject
{
    protected INavigator Navigator { get; }

    // Lifecycle hooks
    public virtual Task OnInitialize();      // After navigation
    public virtual Task OnAppearing();       // When page appears
    public virtual Task OnDisappearing();    // When page disappears

    // Helper for busy state
    protected sealed class BusyScope : IDisposable
    {
        public BusyScope(ViewModelBase viewModel, string message = "")
    }
}
```

**With Parameters:**
```csharp
public abstract class ViewModelBase<TParams> : ViewModelBase
{
    public virtual void OnPrepare(TParams parameter);  // Before initialization
}
```

## API Reference

### INavigator Methods

#### NavigateToAsync&lt;TViewModel&gt;()

Navigate to a page without parameters.

**Signature:**
```csharp
Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase
```

**Example:**
```csharp
await Navigator.NavigateToAsync<SettingsViewModel>();
```

**Requirements:**
- Page and ViewModel must be registered in DI
- Must follow naming convention: `{Feature}ViewModel` → `{Feature}Page`

**Throws:**
- `InvalidOperationException` if page or ViewModel cannot be resolved

---

#### NavigateToAsync&lt;TViewModel, TParams&gt;(TParams)

Navigate to a page with parameters.

**Signature:**
```csharp
Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
    where TViewModel : ViewModelBase<TParams>
```

**Example:**
```csharp
await Navigator.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
    new ProductDetailParams
    {
        ProductId = "123",
        Source = "ProductList"
    });
```

**Requirements:**
- ViewModel must inherit from `ViewModelBase<TParams>`
- ViewModel must override `OnPrepare(TParams parameter)`
- Parameters cannot be null

**Throws:**
- `ArgumentNullException` if parameters is null
- `InvalidOperationException` if page or ViewModel cannot be resolved

---

#### GoBackAsync()

Navigate back to the previous page.

**Signature:**
```csharp
Task GoBackAsync()
```

**Example:**
```csharp
[RelayCommand]
private async Task Back()
{
    await Navigator.GoBackAsync();
}
```

**Throws:**
- `InvalidOperationException` if navigation stack is empty

---

#### PopToRootAsync()

Pop to the root page of the navigation stack.

**Signature:**
```csharp
Task PopToRootAsync()
```

**Example:**
```csharp
[RelayCommand]
private async Task BackToHome()
{
    await Navigator.PopToRootAsync();
}
```

**Throws:**
- `InvalidOperationException` if navigation stack is empty

## Template Components

### Domain/
Domain models and error types.

**Files:**
- `Entity.cs` - Base entity with ErrorOr support
- `BaseError.cs` - Base error type for ErrorOr pattern

### Repository/
Data access layer with ErrorOr pattern.

**Files:**
- `IRepository.cs` - Repository interface
- `Repository.cs` - Repository implementation
- `RepositoryTests.cs` - xUnit tests

### Service/
Business logic services.

**Files:**
- `IService.cs` - Service interface
- `Service.cs` - Service implementation
- `ServiceTests.cs` - xUnit tests
- `ApiService.cs` - HTTP API service
- `CacheService.cs` - Caching service
- `IUseCase.cs` - UseCase interface
- `SampleUseCase.cs` - Example UseCase

### ViewModel/
MVVM ViewModels with navigation support.

**Files:**
- `ViewModelBase.cs` - Base ViewModel class
- `ViewModel.cs` - Example ViewModel
- `ViewModelTests.cs` - xUnit tests

### Page/
XAML pages with MVVM binding.

**Files:**
- `SampleViewModel.cs` - Example page ViewModel

### Navigation/
NavigationPage-based navigation service.

**Files:**
- `INavigator.cs` - Navigation service interface
- `Navigator.cs` - Navigation service implementation
- `MauiProgram.Navigation.cs` - DI registration extensions

## Examples

### Example 1: Simple List-Detail Navigation

```csharp
// ProductListViewModel.cs
public class ProductListViewModel : ViewModelBase
{
    [ObservableProperty]
    private ObservableCollection<Product> _products;

    [RelayCommand]
    private async Task ViewProduct(Product product)
    {
        await Navigator.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
            new ProductDetailParams { ProductId = product.Id });
    }
}

// ProductDetailViewModel.cs
public class ProductDetailViewModel : ViewModelBase<ProductDetailParams>
{
    private readonly IProductService _productService;
    private string _productId;

    [ObservableProperty]
    private Product? _product;

    public ProductDetailViewModel(
        INavigator navigationService,
        IProductService productService)
        : base(navigationService)
    {
        _productService = productService;
    }

    public override void OnPrepare(ProductDetailParams parameter)
    {
        _productId = parameter.ProductId;
    }

    public override async Task OnInitialize()
    {
        using (new BusyScope(this, "Loading product..."))
        {
            var result = await _productService.GetProductAsync(_productId);

            result.Match(
                Right: product => Product = product,
                Left: error => ShowError(error.Message)
            );
        }
    }
}

// Register in MauiProgram.cs
builder.Services.AddPageViewModel<ProductListPage, ProductListViewModel>();
builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();
```

### Example 2: Multi-Step Wizard

```csharp
// Shared wizard data
public class RegistrationWizardData
{
    public PersonalInfo Personal { get; set; }
    public AddressInfo Address { get; set; }
    public PreferencesInfo Preferences { get; set; }
}

// Step 1: Personal Info
public class PersonalInfoViewModel : ViewModelBase<RegistrationWizardData>
{
    [ObservableProperty]
    private string _firstName;

    [ObservableProperty]
    private string _lastName;

    [RelayCommand]
    private async Task Next()
    {
        WizardData.Personal = new PersonalInfo
        {
            FirstName = FirstName,
            LastName = LastName
        };

        await Navigator.NavigateToAsync<AddressInfoViewModel, RegistrationWizardData>(
            WizardData);
    }
}

// Step 2: Address Info
public class AddressInfoViewModel : ViewModelBase<RegistrationWizardData>
{
    [ObservableProperty]
    private string _street;

    [ObservableProperty]
    private string _city;

    [RelayCommand]
    private async Task Back()
    {
        await Navigator.GoBackAsync();
    }

    [RelayCommand]
    private async Task Next()
    {
        WizardData.Address = new AddressInfo
        {
            Street = Street,
            City = City
        };

        await Navigator.NavigateToAsync<PreferencesViewModel, RegistrationWizardData>(
            WizardData);
    }
}

// Step 3: Preferences
public class PreferencesViewModel : ViewModelBase<RegistrationWizardData>
{
    [RelayCommand]
    private async Task Back()
    {
        await Navigator.GoBackAsync();
    }

    [RelayCommand]
    private async Task Finish()
    {
        // Save registration
        await SaveRegistration(WizardData);

        // Return to root
        await Navigator.PopToRootAsync();
    }
}
```

### Example 3: Modal with Result

```csharp
// Caller ViewModel
public class ProductListViewModel : ViewModelBase
{
    [RelayCommand]
    private async Task FilterProducts()
    {
        // Navigate to filter modal
        await Navigator.NavigateToAsync<FilterViewModel>();

        // Subscribe to result
        WeakReferenceMessenger.Default.Register<FilterAppliedMessage>(this,
            (recipient, message) =>
            {
                ApplyFilter(message.Filter);
                WeakReferenceMessenger.Default.Unregister<FilterAppliedMessage>(this);
            });
    }
}

// Filter Modal ViewModel
public class FilterViewModel : ViewModelBase
{
    [ObservableProperty]
    private FilterOptions _filter;

    [RelayCommand]
    private async Task Apply()
    {
        // Send result
        WeakReferenceMessenger.Default.Send(new FilterAppliedMessage(Filter));

        // Close modal
        await Navigator.GoBackAsync();
    }

    [RelayCommand]
    private async Task Cancel()
    {
        await Navigator.GoBackAsync();
    }
}
```

## Testing

### Unit Testing ViewModels

```csharp
public class ProductDetailViewModelTests
{
    [Fact]
    public async Task OnInitialize_WhenProductExists_LoadsProduct()
    {
        // Arrange
        var mockNavigation = Substitute.For<INavigator>();
        var mockProductService = Substitute.For<IProductService>();

        var expectedProduct = new Product { Id = "123", Name = "Test Product" };
        mockProductService.GetProductAsync("123")
            .Returns(Right<ProductError, Product>(expectedProduct));

        var viewModel = new ProductDetailViewModel(mockNavigation, mockProductService);
        viewModel.OnPrepare(new ProductDetailParams { ProductId = "123" });

        // Act
        await viewModel.OnInitialize();

        // Assert
        Assert.NotNull(viewModel.Product);
        Assert.Equal("Test Product", viewModel.Product.Name);
    }
}
```

### Testing Navigation

```csharp
public class ProductListViewModelTests
{
    [Fact]
    public async Task ViewProductCommand_ShouldNavigateToDetail()
    {
        // Arrange
        var mockNavigation = Substitute.For<INavigator>();
        var viewModel = new ProductListViewModel(mockNavigation);
        var product = new Product { Id = "123" };

        // Act
        await viewModel.ViewProductCommand.ExecuteAsync(product);

        // Assert
        await mockNavigation.Received(1)
            .NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
                Arg.Is<ProductDetailParams>(p => p.ProductId == "123"));
    }
}
```

## Troubleshooting

### Page Not Found Error

**Error:**
```
InvalidOperationException: Page type 'YourApp.Pages.ProductDetailPage' not found.
```

**Solutions:**
1. Check naming convention: `ProductDetailViewModel` must map to `ProductDetailPage`
2. Verify namespace: ViewModels in `*.ViewModels`, Pages in `*.Pages`
3. Ensure page class exists with correct name

### Service Resolution Error

**Error:**
```
InvalidOperationException: Page 'ProductDetailPage' could not be resolved from the service provider.
```

**Solutions:**
1. Register page in MauiProgram.cs:
   ```csharp
   builder.Services.AddTransient<ProductDetailPage>();
   ```
2. Or use helper method:
   ```csharp
   builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();
   ```

### Navigation Not Available Error

**Error:**
```
InvalidOperationException: Navigation is not available. Ensure MainPage is set.
```

**Solutions:**
1. Set MainPage in App.xaml.cs:
   ```csharp
   MainPage = new NavigationPage(new MainPage());
   ```
2. Ensure navigation is called after MainPage is set

## Migration Guide

See [MIGRATION.md](./MIGRATION.md) for detailed guide on migrating from:
- AppShell template
- Xamarin.Forms NavigationPage apps
- Shell-based navigation

## Contributing

This template is part of the Agentecflow project. Contributions welcome!

## License

MIT License - See LICENSE file in repository root.
