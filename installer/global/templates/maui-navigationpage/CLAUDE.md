# .NET MAUI NavigationPage Template - Claude Code Context

## Template Overview

This template provides a .NET MAUI project structure using **NavigationPage** for traditional page-based navigation. Use this template when you need:

- Simple page-to-page navigation without complex hierarchies
- Modal-heavy workflows (wizards, multi-step forms)
- Direct migration from Xamarin.Forms NavigationPage apps
- Full control over navigation stack management

## When to Use NavigationPage vs AppShell

### Use NavigationPage When:
- Your app has simple linear navigation flows
- You need extensive modal navigation patterns
- You're migrating from Xamarin.Forms NavigationPage
- You want explicit control over the navigation stack
- Your app doesn't require tabbed or flyout navigation

### Use AppShell When:
- Your app has tabbed navigation (multiple top-level sections)
- You need flyout/drawer navigation
- You want URL-based routing
- Your app has complex navigation hierarchies
- You need deep linking and navigation state management

## Navigation Architecture

### Core Components

#### 1. INavigator Interface
```csharp
public interface INavigator
{
    // Navigate to page without parameters
    Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase;

    // Navigate to page with parameters
    Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
        where TViewModel : ViewModelBase<TParams>;

    // Navigate back
    Task GoBackAsync();

    // Pop to root
    Task PopToRootAsync();
}
```

#### 2. NavigationService Implementation
- **Convention-Based Resolution**: Automatically resolves pages from ViewModels
  - `ProductViewModel` → `ProductPage`
  - Namespace: `*.ViewModels` → `*.Pages`
- **Dependency Injection**: All pages and ViewModels resolved from DI container
- **Parameter Passing**: Type-safe parameter passing to ViewModels
- **Lifecycle Hooks**: Calls `OnPrepare()` and `OnInitialize()` automatically

#### 3. ViewModelBase
```csharp
// Base class without parameters
public abstract class ViewModelBase : ObservableObject
{
    protected INavigator Navigator { get; }

    public virtual Task OnInitialize() { }
    public virtual Task OnAppearing() { }
    public virtual Task OnDisappearing() { }
}

// Base class with parameters
public abstract class ViewModelBase<TParams> : ViewModelBase
{
    public virtual void OnPrepare(TParams parameter) { }
}
```

### Navigation Patterns

#### Pattern 1: Simple Navigation (No Parameters)
```csharp
// In any ViewModel
[RelayCommand]
private async Task NavigateToSettings()
{
    await NavigationService.NavigateToAsync<SettingsViewModel>();
}
```

**Registration Required:**
```csharp
// MauiProgram.cs
builder.Services.AddPageViewModel<SettingsPage, SettingsViewModel>();
```

#### Pattern 2: Navigation with Parameters
```csharp
// Define parameter class
public class ProductDetailParams
{
    public string ProductId { get; set; }
    public string Source { get; set; }
}

// Navigate with parameters
[RelayCommand]
private async Task ViewProductDetail(string productId)
{
    await NavigationService.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
        new ProductDetailParams
        {
            ProductId = productId,
            Source = "ProductList"
        });
}

// In ProductDetailViewModel
public class ProductDetailViewModel : ViewModelBase<ProductDetailParams>
{
    private string _productId;

    public override void OnPrepare(ProductDetailParams parameter)
    {
        _productId = parameter.ProductId;
        // Parameters are available here, before OnInitialize
    }

    public override async Task OnInitialize()
    {
        // Load data using the productId
        await LoadProduct(_productId);
    }
}
```

#### Pattern 3: Modal Navigation
```csharp
// Push modal page
[RelayCommand]
private async Task ShowFilterModal()
{
    await NavigationService.NavigateToAsync<FilterViewModel>();
}

// Close modal
[RelayCommand]
private async Task CloseModal()
{
    await NavigationService.GoBackAsync();
}
```

#### Pattern 4: Navigation with Result
```csharp
// Caller ViewModel
[RelayCommand]
private async Task SelectProduct()
{
    // Navigate to product selection page
    await NavigationService.NavigateToAsync<ProductSelectionViewModel>();

    // When user returns, check for result in MessagingCenter or event
    MessagingCenter.Subscribe<ProductSelectionViewModel, Product>(this, "ProductSelected",
        (sender, product) =>
        {
            SelectedProduct = product;
            MessagingCenter.Unsubscribe<ProductSelectionViewModel, Product>(this, "ProductSelected");
        });
}

// Product Selection ViewModel
[RelayCommand]
private async Task SelectProduct(Product product)
{
    // Send result back
    MessagingCenter.Send(this, "ProductSelected", product);

    // Navigate back
    await NavigationService.GoBackAsync();
}
```

## Code Generation Guidelines

### When Generating Page/ViewModel Pairs

1. **Always create both Page and ViewModel**:
   ```
   ProductDetailPage.xaml
   ProductDetailPage.xaml.cs
   ProductDetailViewModel.cs
   ```

2. **Follow naming conventions strictly**:
   - ViewModel: `{Feature}ViewModel`
   - Page: `{Feature}Page`
   - Namespace: `*.ViewModels` and `*.Pages`

3. **Register in MauiProgram.cs**:
   ```csharp
   builder.Services.AddPageViewModel<ProductDetailPage, ProductDetailViewModel>();
   ```

4. **Always inject INavigator into ViewModels**:
   ```csharp
   public class ProductDetailViewModel : ViewModelBase
   {
       public ProductDetailViewModel(INavigator navigator)
           : base(navigator)
       {
       }
   }
   ```

### When Generating Navigation Code

1. **Use type-safe navigation**:
   ```csharp
   // GOOD
   await Navigator.NavigateToAsync<ProductDetailViewModel>();

   // BAD - avoid string-based navigation
   await Navigation.PushAsync(new ProductDetailPage());
   ```

2. **Always handle navigation exceptions**:
   ```csharp
   try
   {
       await NavigationService.NavigateToAsync<ProductDetailViewModel>();
   }
   catch (InvalidOperationException ex)
   {
       // Log error and show user feedback
       await ShowError("Navigation failed", ex.Message);
   }
   ```

3. **Use parameters for type safety**:
   ```csharp
   // GOOD - type-safe parameters
   await NavigationService.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
       new ProductDetailParams { ProductId = "123" });

   // BAD - avoid using ViewModelBase properties directly
   var viewModel = new ProductDetailViewModel();
   viewModel.ProductId = "123";  // Don't do this
   ```

## Testing Requirements

### Navigation Testing
```csharp
[Fact]
public async Task NavigateToProductDetail_ShouldCallNavigationService()
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

### Page Registration Testing
```csharp
[Fact]
public void MauiProgram_ShouldRegisterAllPages()
{
    // Arrange
    var builder = MauiApp.CreateBuilder();
    builder.AddNavigationServices();
    var app = builder.Build();

    // Act & Assert
    Assert.NotNull(app.Services.GetService<ProductDetailPage>());
    Assert.NotNull(app.Services.GetService<ProductDetailViewModel>());
}
```

### ViewModel Lifecycle Testing
```csharp
[Fact]
public async Task OnPrepare_ShouldReceiveParameters()
{
    // Arrange
    var mockNavigation = Substitute.For<INavigator>();
    var viewModel = new ProductDetailViewModel(mockNavigation);
    var parameters = new ProductDetailParams { ProductId = "123" };

    // Act
    viewModel.OnPrepare(parameters);
    await viewModel.OnInitialize();

    // Assert
    Assert.Equal("123", viewModel.ProductId);
}
```

## Common Scenarios

### Scenario 1: Wizard/Multi-Step Form
```csharp
// Step 1
public class PersonalInfoViewModel : ViewModelBase<WizardParams>
{
    [RelayCommand]
    private async Task Next()
    {
        // Save step data
        WizardParams.PersonalInfo = /* collected data */;

        // Navigate to next step
        await NavigationService.NavigateToAsync<AddressInfoViewModel, WizardParams>(
            WizardParams);
    }
}

// Step 2
public class AddressInfoViewModel : ViewModelBase<WizardParams>
{
    [RelayCommand]
    private async Task Back()
    {
        await NavigationService.GoBackAsync();
    }

    [RelayCommand]
    private async Task Finish()
    {
        // Save all wizard data
        await SaveWizardData(WizardParams);

        // Return to root
        await NavigationService.PopToRootAsync();
    }
}
```

### Scenario 2: Conditional Navigation
```csharp
[RelayCommand]
private async Task NavigateBasedOnRole()
{
    if (User.IsAdmin)
    {
        await NavigationService.NavigateToAsync<AdminDashboardViewModel>();
    }
    else if (User.IsManager)
    {
        await NavigationService.NavigateToAsync<ManagerDashboardViewModel>();
    }
    else
    {
        await NavigationService.NavigateToAsync<UserDashboardViewModel>();
    }
}
```

### Scenario 3: Deep Navigation
```csharp
[RelayCommand]
private async Task NavigateToProductReview(string productId, string reviewId)
{
    // Navigate through multiple levels
    await NavigationService.NavigateToAsync<ProductDetailViewModel, ProductDetailParams>(
        new ProductDetailParams { ProductId = productId });

    await NavigationService.NavigateToAsync<ReviewDetailViewModel, ReviewDetailParams>(
        new ReviewDetailParams { ReviewId = reviewId });
}
```

## Error Handling

### Common Navigation Errors

1. **Page Not Found**
   - Error: `Page type 'YourApp.Pages.ProductDetailPage' not found`
   - Solution: Ensure page follows naming convention and exists in correct namespace

2. **Service Not Registered**
   - Error: `Page 'ProductDetailPage' could not be resolved from the service provider`
   - Solution: Add registration in MauiProgram.cs:
     ```csharp
     builder.Services.AddTransient<ProductDetailPage>();
     ```

3. **Navigation Not Available**
   - Error: `Navigation is not available. Ensure MainPage is set.`
   - Solution: Ensure App.xaml.cs sets MainPage:
     ```csharp
     MainPage = new NavigationPage(new MainPage());
     ```

## Best Practices

1. **Always use INavigator**: Never use `Navigation.PushAsync()` directly
2. **Register all pages in MauiProgram**: Use the AddPageViewModel helper
3. **Use parameters for type safety**: Avoid passing data through static properties
4. **Handle navigation exceptions**: Always wrap navigation in try-catch
5. **Test navigation logic**: Mock INavigator in unit tests
6. **Follow naming conventions**: {Feature}ViewModel → {Feature}Page
7. **Use lifecycle hooks**: OnPrepare for parameters, OnInitialize for async loading
8. **Keep navigation logic in ViewModels**: Don't navigate from code-behind

## Migration from AppShell

If migrating from the maui-appshell template:

1. Replace Shell-based navigation with `INavigator` in ViewModels
2. Replace `Shell.Current.GoToAsync()` with `Navigator.NavigateToAsync()`
3. Remove Shell routes and route parameters
4. Update parameter passing from route parameters to type-safe parameter objects
5. Replace `MainPage = new AppShell()` with `MainPage = new NavigationPage(new MainPage())`

See MIGRATION.md for detailed migration guide.

## Resources

- [.NET MAUI NavigationPage Documentation](https://learn.microsoft.com/dotnet/maui/user-interface/pages/navigationpage)
- [MAUI Navigation Patterns](https://learn.microsoft.com/dotnet/maui/fundamentals/navigation)
- Template GitHub: [agentecflow/ai-engineer](https://github.com/agentecflow/ai-engineer)
