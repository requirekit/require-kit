# SOURCE: maui-appshell template (shared)
// Engines/GetProductsEngine.cs
using ErrorOr;
using {{ProjectName}}.Core.Interfaces;
using {{ProjectName}}.Models;
using {{ProjectName}}.Services.Interfaces;

namespace {{ProjectName}}.Engines;

/// <summary>
/// Interface for the GetProducts engine
/// </summary>
public interface IGetProductsEngine
{
    Task<ErrorOr<List<Product>>> GetProductsAsync();
    Task<ErrorOr<List<Product>>> GetProductsByCategoryAsync(string category);
}

/// <summary>
/// Engine for retrieving products with caching support using ErrorOr pattern
/// Demonstrates the Engine pattern with flexible method naming
/// </summary>
public class GetProductsEngine : IGetProductsEngine
{
    private readonly IApiService _apiService;
    private readonly ICacheService _cacheService;
    private readonly IConnectivityService _connectivityService;
    private readonly ILogger<GetProductsEngine> _logger;
    
    private const string CacheKey = "products_list";
    private static readonly TimeSpan CacheExpiry = TimeSpan.FromMinutes(5);

    public GetProductsEngine(
        IApiService apiService,
        ICacheService cacheService,
        IConnectivityService connectivityService,
        ILogger<GetProductsEngine> logger)
    {
        _apiService = apiService;
        _cacheService = cacheService;
        _connectivityService = connectivityService;
        _logger = logger;
    }

    public async Task<ErrorOr<List<Product>>> GetProductsAsync()
    {
        try
        {
            // Check connectivity first
            if (!_connectivityService.IsConnected)
            {
                _logger.LogInformation("Device is offline, attempting to load from cache");
                return await LoadFromCacheOrError();
            }

            // Try to get from cache first
            var cachedProducts = await _cacheService.GetAsync<List<Product>>(CacheKey);
            
            if (cachedProducts != null && cachedProducts.Any())
            {
                _logger.LogInformation("Returning {Count} products from cache", cachedProducts.Count);
                
                // Refresh cache in background if it's getting old
                _ = RefreshCacheInBackground();
                
                return cachedProducts;
            }

            return await FetchFromApiAndCache();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error in GetProductsEngine");
            return Error.Failure("GetProducts.UnexpectedError", "Failed to load products");
        }
    }

    public async Task<ErrorOr<List<Product>>> GetProductsByCategoryAsync(string category)
    {
        if (string.IsNullOrWhiteSpace(category))
        {
            return Error.Validation("GetProducts.InvalidCategory", "Category cannot be empty");
        }

        var allProductsResult = await GetProductsAsync();
        
        if (allProductsResult.IsError)
        {
            return allProductsResult.Errors;
        }

        var filteredProducts = allProductsResult.Value
            .Where(p => p.Category?.Equals(category, StringComparison.OrdinalIgnoreCase) == true)
            .ToList();

        return filteredProducts;
    }

    private async Task<ErrorOr<List<Product>>> LoadFromCacheOrError()
    {
        var cachedProducts = await _cacheService.GetAsync<List<Product>>(CacheKey);
        
        if (cachedProducts != null && cachedProducts.Any())
        {
            _logger.LogInformation("Returning {Count} products from cache (offline mode)", cachedProducts.Count);
            return cachedProducts;
        }

        return Error.Failure("GetProducts.Offline", "No offline data available. Please connect to the internet to load products.");
    }

    private async Task<ErrorOr<List<Product>>> FetchFromApiAndCache()
    {
        _logger.LogInformation("Fetching products from API");
        
        var apiResult = await _apiService.GetAsync<ProductsResponse>("/api/products");
        
        if (apiResult.IsError)
        {
            _logger.LogError("API error: {Errors}", string.Join(", ", apiResult.Errors));
            
            // Try to return cached data even if expired
            return await LoadFromCacheOrError();
        }

        var products = apiResult.Value?.Products ?? new List<Product>();
        
        if (products.Any())
        {
            // Cache the results
            await _cacheService.SetAsync(CacheKey, products, CacheExpiry);
            _logger.LogInformation("Cached {Count} products", products.Count);
        }
        
        return products;
    }

    private async Task RefreshCacheInBackground()
    {
        try
        {
            _logger.LogInformation("Refreshing cache in background");
            var apiResult = await _apiService.GetAsync<ProductsResponse>("/api/products");
            
            if (apiResult.IsError)
            {
                _logger.LogWarning("Background cache refresh failed: {Errors}", string.Join(", ", apiResult.Errors));
                return;
            }

            if (apiResult.Value?.Products != null && apiResult.Value.Products.Any())
            {
                await _cacheService.SetAsync(CacheKey, apiResult.Value.Products, CacheExpiry);
                _logger.LogInformation("Background cache refresh completed");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during background cache refresh");
        }
    }
}

/// <summary>
/// Create Product engine demonstrating validation with ErrorOr
/// Shows flexible method naming - not constrained to ExecuteAsync
/// </summary>
public class CreateProductEngine : IEngine<CreateProductRequest, Product>
{
    private readonly IApiService _apiService;
    private readonly ILogger<CreateProductEngine> _logger;

    public CreateProductEngine(IApiService apiService, ILogger<CreateProductEngine> logger)
    {
        _apiService = apiService;
        _logger = logger;
    }

    // Traditional ExecuteAsync method if you prefer
    public async Task<ErrorOr<Product>> ExecuteAsync(CreateProductRequest input)
    {
        return await CreateProductAsync(input);
    }

    // Or custom method name for better semantics
    public async Task<ErrorOr<Product>> CreateProductAsync(CreateProductRequest request)
    {
        // Validate input
        var validation = ValidateInput(request);
        if (validation.IsError)
        {
            return validation.Errors;
        }

        _logger.LogInformation("Creating product: {Name}", request.Name);
        
        var result = await _apiService.PostAsync<CreateProductRequest, Product>("/api/products", request);
        
        if (result.IsError)
        {
            _logger.LogError("Failed to create product: {Errors}", string.Join(", ", result.Errors));
            return result.Errors;
        }

        _logger.LogInformation("Product created successfully: {Id}", result.Value.Id);
        return result.Value;
    }

    private ErrorOr<Success> ValidateInput(CreateProductRequest input)
    {
        var errors = new List<Error>();

        if (string.IsNullOrWhiteSpace(input.Name))
            errors.Add(Error.Validation("CreateProduct.NameRequired", "Product name is required"));
        
        if (input.Name?.Length > 100)
            errors.Add(Error.Validation("CreateProduct.NameTooLong", "Product name must be 100 characters or less"));
        
        if (input.Price <= 0)
            errors.Add(Error.Validation("CreateProduct.InvalidPrice", "Product price must be greater than zero"));
        
        if (input.Price > 1_000_000)
            errors.Add(Error.Validation("CreateProduct.PriceTooHigh", "Product price cannot exceed 1,000,000"));

        return errors.Any() ? errors : Result.Success;
    }
}

/// <summary>
/// Response model for products API
/// </summary>
public class ProductsResponse
{
    public List<Product> Products { get; set; } = new();
    public int TotalCount { get; set; }
    public DateTime LastUpdated { get; set; }
}

/// <summary>
/// Request model for creating a product
/// </summary>
public class CreateProductRequest
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public string? Category { get; set; }
}
