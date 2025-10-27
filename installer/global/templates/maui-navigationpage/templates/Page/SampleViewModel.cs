# SOURCE: maui-appshell template (shared)
// ViewModels/SampleViewModel.cs
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using {{ProjectName}}.Navigation;
using {{ProjectName}}.Engines;
using {{ProjectName}}.Models;
using ErrorOr;

namespace {{ProjectName}}.ViewModels;

/// <summary>
/// Sample ViewModel demonstrating template conventions:
/// - Inherits from ViewModelBase with INavigator
/// - Uses Engine pattern for business logic
/// - Uses ErrorOr for functional error handling
/// - Follows MVVM patterns with CommunityToolkit.Mvvm
/// </summary>
public partial class SampleViewModel : ViewModelBase
{
    private readonly IGetProductsEngine _getProductsEngine;
    private readonly ILogger<SampleViewModel> _logger;

    [ObservableProperty]
    private string _title = "Sample Page";

    [ObservableProperty]
    private bool _isLoading;

    [ObservableProperty]
    private bool _hasError;

    [ObservableProperty]
    private string _errorMessage = string.Empty;

    [ObservableProperty]
    private List<Product> _products = new();

    [ObservableProperty]
    private Product? _selectedProduct;

    [ObservableProperty]
    private string _searchText = string.Empty;

    public SampleViewModel(
        INavigator navigator,
        IGetProductsEngine getProductsEngine,
        ILogger<SampleViewModel> logger) : base(navigator)
    {
        _getProductsEngine = getProductsEngine;
        _logger = logger;
    }

    public override async Task OnViewAppearing()
    {
        await base.OnViewAppearing();
        
        // Load data when the view appears
        await LoadProductsCommand.ExecuteAsync(null);
    }

    [RelayCommand]
    private async Task LoadProducts()
    {
        using var busyScope = new BusyScope(this, "Loading products...");
        
        try
        {
            HasError = false;
            ErrorMessage = string.Empty;

            _logger.LogInformation("Loading products");

            var result = await _getProductsEngine.GetProductsAsync();

            result.Match(
                onValue: products =>
                {
                    Products = products;
                    _logger.LogInformation("Loaded {Count} products successfully", products.Count);
                },
                onError: errors =>
                {
                    var errorMessage = string.Join("; ", errors.Select(e => e.Description));
                    _logger.LogError("Failed to load products: {Errors}", errorMessage);
                    
                    HasError = true;
                    ErrorMessage = GetUserFriendlyErrorMessage(errors);
                }
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error loading products");
            HasError = true;
            ErrorMessage = "An unexpected error occurred. Please try again.";
        }
    }

    [RelayCommand]
    private async Task SearchProducts()
    {
        if (string.IsNullOrWhiteSpace(SearchText))
        {
            await LoadProductsCommand.ExecuteAsync(null);
            return;
        }

        using var busyScope = new BusyScope(this, "Searching...");

        try
        {
            HasError = false;
            ErrorMessage = string.Empty;

            _logger.LogInformation("Searching products with term: {SearchText}", SearchText);

            var result = await _getProductsEngine.GetProductsByCategoryAsync(SearchText);

            result.Match(
                onValue: products =>
                {
                    Products = products;
                    _logger.LogInformation("Found {Count} products for search term '{SearchText}'", 
                        products.Count, SearchText);
                },
                onError: errors =>
                {
                    var errorMessage = string.Join("; ", errors.Select(e => e.Description));
                    _logger.LogError("Failed to search products: {Errors}", errorMessage);
                    
                    HasError = true;
                    ErrorMessage = GetUserFriendlyErrorMessage(errors);
                }
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error searching products");
            HasError = true;
            ErrorMessage = "An unexpected error occurred. Please try again.";
        }
    }

    [RelayCommand]
    private async Task SelectProduct(Product? product)
    {
        if (product == null) return;

        SelectedProduct = product;
        _logger.LogInformation("Product selected: {ProductName}", product.Name);

        // Navigate to product detail page
        await Navigator.Navigate<ProductDetailViewModel, Product>(product);
    }

    [RelayCommand]
    private async Task RefreshProducts()
    {
        // Clear current data and reload
        Products.Clear();
        await LoadProductsCommand.ExecuteAsync(null);
    }

    [RelayCommand]
    private void ClearError()
    {
        HasError = false;
        ErrorMessage = string.Empty;
    }

    [RelayCommand]
    private async Task GoBack()
    {
        try
        {
            await Navigator.Close(this);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to navigate back");
        }
    }

    private string GetUserFriendlyErrorMessage(List<e> errors)
    {
        // Convert technical errors to user-friendly messages
        if (errors.Any(e => e.Code.Contains("Offline")))
            return "You're offline. Please check your connection and try again.";

        if (errors.Any(e => e.Code.Contains("Network")))
            return "Network error. Please check your connection.";

        if (errors.Any(e => e.Code.Contains("Unauthorized")))
            return "You need to log in again to continue.";

        if (errors.Any(e => e.Code.Contains("Validation")))
            return "Please check your input and try again.";

        // Default to first error message
        return errors.FirstOrDefault()?.Description ?? "An error occurred. Please try again.";
    }

    /// <summary>
    /// Example of a method that could be called when text changes
    /// Shows reactive programming patterns
    /// </summary>
    partial void OnSearchTextChanged(string value)
    {
        // You could add debouncing here if needed
        // For now, just log the change
        _logger.LogDebug("Search text changed to: {SearchText}", value);
    }

    /// <summary>
    /// Example of validation that runs when SelectedProduct changes
    /// </summary>
    partial void OnSelectedProductChanged(Product? value)
    {
        if (value != null)
        {
            _logger.LogDebug("Selected product changed to: {ProductName}", value.Name);
        }
    }
}

/// <summary>
/// Sample ViewModel that accepts parameters
/// Demonstrates the generic ViewModelBase<T> pattern
/// </summary>
public partial class ProductDetailViewModel : ViewModelBase<Product>, IViewModel<Product>
{
    [ObservableProperty]
    private Product? _product;

    [ObservableProperty]
    private string _title = "Product Details";

    public ProductDetailViewModel(INavigator navigator) : base(navigator)
    {
    }

    public override void OnPrepare(Product parameter)
    {
        base.OnPrepare(parameter);
        Product = parameter;
        Title = $"Product: {parameter.Name}";
    }

    [RelayCommand]
    private async Task SaveProduct()
    {
        if (Product == null) return;

        using var busyScope = new BusyScope(this, "Saving product...");

        // Here you would call an engine to save the product
        // await _saveProductEngine.SaveAsync(Product);

        await Navigator.Close(this);
    }

    [RelayCommand]
    private async Task Cancel()
    {
        await Navigator.Close(this);
    }
}

/// <summary>
/// Sample product model
/// </summary>
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public string? Category { get; set; }
    public DateTime CreatedAt { get; set; }
    public bool IsActive { get; set; } = true;
}
