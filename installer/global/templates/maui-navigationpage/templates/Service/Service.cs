# SOURCE: maui-appshell template (shared)
using ErrorOr;
using {{ProjectName}}.Services.Interfaces;

namespace {{ProjectName}}.Services;

/// <summary>
/// Service implementation for [SERVICE_NAME] functionality
/// Services handle external integrations and cross-cutting concerns
/// </summary>
public class [SERVICE_NAME]Service : I[SERVICE_NAME]Service
{
    private readonly ILogService _logService;
    private readonly HttpClient _httpClient;

    public [SERVICE_NAME]Service(
        ILogService logService,
        HttpClient httpClient)
    {
        _logService = logService;
        _httpClient = httpClient;
    }

    /// <summary>
    /// Example service method with ErrorOr return type
    /// </summary>
    public async Task<ErrorOr<string>> GetDataAsync(string parameter)
    {
        try
        {
            _logService.TrackEvent("[SERVICE_NAME]GetDataStarted", new Dictionary<string, object>
            {
                { "Parameter", parameter }
            });

            if (string.IsNullOrWhiteSpace(parameter))
            {
                return Error.Validation(
                    code: "[SERVICE_NAME].InvalidParameter",
                    description: "Parameter cannot be null or empty");
            }

            // Example HTTP call
            var response = await _httpClient.GetAsync($"/api/data/{parameter}");
            
            if (!response.IsSuccessStatusCode)
            {
                return Error.Failure(
                    code: "[SERVICE_NAME].HttpError",
                    description: $"HTTP request failed with status: {response.StatusCode}");
            }

            var content = await response.Content.ReadAsStringAsync();
            
            _logService.TrackEvent("[SERVICE_NAME]GetDataCompleted", new Dictionary<string, object>
            {
                { "Parameter", parameter },
                { "ResponseLength", content.Length }
            });

            return content;
        }
        catch (HttpRequestException ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetDataAsync" },
                { "Parameter", parameter },
                { "Service", nameof([SERVICE_NAME]Service) }
            });

            return Error.Failure(
                code: "[SERVICE_NAME].NetworkError",
                description: "Network error occurred while fetching data");
        }
        catch (TaskCanceledException ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetDataAsync" },
                { "Parameter", parameter },
                { "Service", nameof([SERVICE_NAME]Service) }
            });

            return Error.Failure(
                code: "[SERVICE_NAME].Timeout",
                description: "Request timed out");
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetDataAsync" },
                { "Parameter", parameter },
                { "Service", nameof([SERVICE_NAME]Service) }
            });

            return Error.Failure(
                code: "[SERVICE_NAME].UnexpectedError",
                description: "An unexpected error occurred");
        }
    }

    /// <summary>
    /// Example service method for processing
    /// </summary>
    public async Task<ErrorOr<bool>> ProcessDataAsync(object data)
    {
        try
        {
            _logService.TrackEvent("[SERVICE_NAME]ProcessDataStarted");

            if (data == null)
            {
                return Error.Validation(
                    code: "[SERVICE_NAME].NullData",
                    description: "Data cannot be null");
            }

            // Simulate processing
            await Task.Delay(100);

            // Example validation
            if (data.ToString()?.Length < 5)
            {
                return Error.Validation(
                    code: "[SERVICE_NAME].InvalidDataLength",
                    description: "Data must be at least 5 characters long");
            }

            _logService.TrackEvent("[SERVICE_NAME]ProcessDataCompleted");

            return true;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "ProcessDataAsync" },
                { "Service", nameof([SERVICE_NAME]Service) }
            });

            return Error.Failure(
                code: "[SERVICE_NAME].ProcessingError",
                description: "Failed to process data");
        }
    }

    /// <summary>
    /// Example synchronous service method
    /// </summary>
    public ErrorOr<bool> ValidateData(string value)
    {
        try
        {
            _logService.TrackEvent("[SERVICE_NAME]ValidateDataStarted");

            if (string.IsNullOrWhiteSpace(value))
            {
                return Error.Validation(
                    code: "[SERVICE_NAME].EmptyValue",
                    description: "Value cannot be null or empty");
            }

            // Example validation rules
            var errors = new List<e>();

            if (value.Length < 3)
            {
                errors.Add(Error.Validation(
                    code: "[SERVICE_NAME].TooShort",
                    description: "Value must be at least 3 characters long"));
            }

            if (value.Length > 100)
            {
                errors.Add(Error.Validation(
                    code: "[SERVICE_NAME].TooLong",
                    description: "Value cannot be longer than 100 characters"));
            }

            if (!value.All(char.IsLetterOrDigit))
            {
                errors.Add(Error.Validation(
                    code: "[SERVICE_NAME].InvalidCharacters",
                    description: "Value can only contain letters and digits"));
            }

            if (errors.Count > 0)
            {
                return errors;
            }

            _logService.TrackEvent("[SERVICE_NAME]ValidateDataCompleted", new Dictionary<string, object>
            {
                { "IsValid", true }
            });

            return true;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "ValidateData" },
                { "Service", nameof([SERVICE_NAME]Service) }
            });

            return Error.Failure(
                code: "[SERVICE_NAME].ValidationError",
                description: "Failed to validate data");
        }
    }

    /// <summary>
    /// Example method for configuration
    /// </summary>
    public async Task<ErrorOr<Dictionary<string, object>>> GetConfigurationAsync()
    {
        try
        {
            _logService.TrackEvent("[SERVICE_NAME]GetConfigurationStarted");

            // Example configuration retrieval
            var config = new Dictionary<string, object>
            {
                { "Setting1", "Value1" },
                { "Setting2", 42 },
                { "Setting3", true }
            };

            // Simulate async operation
            await Task.Delay(50);

            _logService.TrackEvent("[SERVICE_NAME]GetConfigurationCompleted", new Dictionary<string, object>
            {
                { "ConfigurationKeys", config.Count }
            });

            return config;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetConfigurationAsync" },
                { "Service", nameof([SERVICE_NAME]Service) }
            });

            return Error.Failure(
                code: "[SERVICE_NAME].ConfigurationError",
                description: "Failed to retrieve configuration");
        }
    }
}
