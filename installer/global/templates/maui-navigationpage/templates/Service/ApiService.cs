# SOURCE: maui-appshell template (shared)
// Services/Implementations/ApiService.cs
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using YourApp.Core.Functional;
using YourApp.Core.Models;
using YourApp.Services.Interfaces;

namespace YourApp.Services.Implementations;

/// <summary>
/// Service for making API calls with error handling
/// </summary>
public class ApiService : IApiService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ApiService> _logger;
    private readonly JsonSerializerOptions _jsonOptions;
    private readonly ApiConfiguration _configuration;

    public ApiService(HttpClient httpClient, ApiConfiguration configuration, ILogger<ApiService> logger)
    {
        _httpClient = httpClient;
        _configuration = configuration;
        _logger = logger;
        
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };

        ConfigureHttpClient();
    }

    private void ConfigureHttpClient()
    {
        _httpClient.BaseAddress = new Uri(_configuration.BaseUrl);
        _httpClient.DefaultRequestHeaders.Accept.Clear();
        _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        
        if (_configuration.Timeout.HasValue)
        {
            _httpClient.Timeout = _configuration.Timeout.Value;
        }
    }

    /// <summary>
    /// Makes a GET request to the API
    /// </summary>
    public async Task<Either<ApiError, T>> GetAsync<T>(string endpoint, CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("GET request to {Endpoint}", endpoint);
            
            var response = await _httpClient.GetAsync(endpoint, cancellationToken);
            
            return await HandleResponse<T>(response);
        }
        catch (TaskCanceledException)
        {
            _logger.LogError("Request to {Endpoint} timed out", endpoint);
            return new ApiError("Request timed out", null);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Network error for {Endpoint}", endpoint);
            return new ApiError($"Network error: {ex.Message}", null);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error for {Endpoint}", endpoint);
            return new ApiError($"Unexpected error: {ex.Message}", null);
        }
    }

    /// <summary>
    /// Makes a POST request to the API
    /// </summary>
    public async Task<Either<ApiError, TResponse>> PostAsync<TRequest, TResponse>(
        string endpoint, 
        TRequest data, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("POST request to {Endpoint}", endpoint);
            
            var json = JsonSerializer.Serialize(data, _jsonOptions);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            
            var response = await _httpClient.PostAsync(endpoint, content, cancellationToken);
            
            return await HandleResponse<TResponse>(response);
        }
        catch (TaskCanceledException)
        {
            _logger.LogError("Request to {Endpoint} timed out", endpoint);
            return new ApiError("Request timed out", null);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Network error for {Endpoint}", endpoint);
            return new ApiError($"Network error: {ex.Message}", null);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error for {Endpoint}", endpoint);
            return new ApiError($"Unexpected error: {ex.Message}", null);
        }
    }

    /// <summary>
    /// Makes a PUT request to the API
    /// </summary>
    public async Task<Either<ApiError, TResponse>> PutAsync<TRequest, TResponse>(
        string endpoint, 
        TRequest data, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("PUT request to {Endpoint}", endpoint);
            
            var json = JsonSerializer.Serialize(data, _jsonOptions);
            var content = new StringContent(json, Encoding.UTF8, "application/json");
            
            var response = await _httpClient.PutAsync(endpoint, content, cancellationToken);
            
            return await HandleResponse<TResponse>(response);
        }
        catch (TaskCanceledException)
        {
            _logger.LogError("Request to {Endpoint} timed out", endpoint);
            return new ApiError("Request timed out", null);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Network error for {Endpoint}", endpoint);
            return new ApiError($"Network error: {ex.Message}", null);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error for {Endpoint}", endpoint);
            return new ApiError($"Unexpected error: {ex.Message}", null);
        }
    }

    /// <summary>
    /// Makes a DELETE request to the API
    /// </summary>
    public async Task<Either<ApiError, Unit>> DeleteAsync(string endpoint, CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("DELETE request to {Endpoint}", endpoint);
            
            var response = await _httpClient.DeleteAsync(endpoint, cancellationToken);
            
            if (response.IsSuccessStatusCode)
            {
                return Unit.Default;
            }

            var error = await GetErrorMessage(response);
            _logger.LogError("DELETE request failed: {StatusCode} - {Error}", response.StatusCode, error);
            return new ApiError(error, (int)response.StatusCode);
        }
        catch (TaskCanceledException)
        {
            _logger.LogError("Request to {Endpoint} timed out", endpoint);
            return new ApiError("Request timed out", null);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Network error for {Endpoint}", endpoint);
            return new ApiError($"Network error: {ex.Message}", null);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error for {Endpoint}", endpoint);
            return new ApiError($"Unexpected error: {ex.Message}", null);
        }
    }

    /// <summary>
    /// Sets the authentication token
    /// </summary>
    public void SetAuthToken(string token)
    {
        _httpClient.DefaultRequestHeaders.Authorization = 
            new AuthenticationHeaderValue("Bearer", token);
    }

    /// <summary>
    /// Clears the authentication token
    /// </summary>
    public void ClearAuthToken()
    {
        _httpClient.DefaultRequestHeaders.Authorization = null;
    }

    private async Task<Either<ApiError, T>> HandleResponse<T>(HttpResponseMessage response)
    {
        if (response.IsSuccessStatusCode)
        {
            var json = await response.Content.ReadAsStringAsync();
            
            if (string.IsNullOrWhiteSpace(json))
            {
                return default(T)!;
            }

            try
            {
                var data = JsonSerializer.Deserialize<T>(json, _jsonOptions);
                return data!;
            }
            catch (JsonException ex)
            {
                _logger.LogError(ex, "Failed to deserialize response");
                return new ApiError("Invalid response format", (int)response.StatusCode, json);
            }
        }

        var error = await GetErrorMessage(response);
        _logger.LogError("Request failed: {StatusCode} - {Error}", response.StatusCode, error);
        
        return new ApiError(error, (int)response.StatusCode, await response.Content.ReadAsStringAsync());
    }

    private async Task<string> GetErrorMessage(HttpResponseMessage response)
    {
        try
        {
            var errorContent = await response.Content.ReadAsStringAsync();
            
            if (!string.IsNullOrWhiteSpace(errorContent))
            {
                var errorObj = JsonSerializer.Deserialize<Dictionary<string, object>>(errorContent, _jsonOptions);
                
                if (errorObj?.TryGetValue("error", out var error) == true)
                {
                    return error.ToString() ?? GetDefaultErrorMessage(response.StatusCode);
                }
                
                if (errorObj?.TryGetValue("message", out var message) == true)
                {
                    return message.ToString() ?? GetDefaultErrorMessage(response.StatusCode);
                }
            }
        }
        catch
        {
            // If we can't parse the error, use default message
        }

        return GetDefaultErrorMessage(response.StatusCode);
    }

    private string GetDefaultErrorMessage(System.Net.HttpStatusCode statusCode)
    {
        return statusCode switch
        {
            System.Net.HttpStatusCode.BadRequest => "Invalid request",
            System.Net.HttpStatusCode.Unauthorized => "Authentication required",
            System.Net.HttpStatusCode.Forbidden => "Access denied",
            System.Net.HttpStatusCode.NotFound => "Resource not found",
            System.Net.HttpStatusCode.InternalServerError => "Server error occurred",
            System.Net.HttpStatusCode.ServiceUnavailable => "Service is unavailable",
            _ => $"Request failed with status {statusCode}"
        };
    }
}

/// <summary>
/// API configuration
/// </summary>
public class ApiConfiguration
{
    public string BaseUrl { get; set; } = "https://api.example.com";
    public TimeSpan? Timeout { get; set; } = TimeSpan.FromSeconds(30);
    public Dictionary<string, string> DefaultHeaders { get; set; } = new();
}
