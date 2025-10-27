# SOURCE: maui-appshell template (shared)
// Core/Models/BaseError.cs
namespace YourApp.Core.Models;

/// <summary>
/// Base class for all error types in the application
/// </summary>
public abstract class BaseError
{
    public string Message { get; }
    public ErrorType Type { get; }
    public DateTime Timestamp { get; }
    public string? Details { get; }
    
    protected BaseError(string message, ErrorType type = ErrorType.UnknownError, string? details = null)
    {
        Message = message ?? "An error occurred";
        Type = type;
        Details = details;
        Timestamp = DateTime.UtcNow;
    }

    public override string ToString()
    {
        return string.IsNullOrEmpty(Details) 
            ? $"[{Type}] {Message}" 
            : $"[{Type}] {Message} - {Details}";
    }
}

/// <summary>
/// Common error types used throughout the application
/// </summary>
public enum ErrorType
{
    UnknownError,
    ValidationError,
    NotFound,
    Unauthorized,
    Forbidden,
    NetworkError,
    Timeout,
    ServerError,
    ClientError,
    CacheError,
    DatabaseError,
    ConfigurationError,
    BusinessRuleViolation,
    ConcurrencyError,
    Offline
}

/// <summary>
/// Generic application error
/// </summary>
public class AppError : BaseError
{
    public AppError(string message, ErrorType type = ErrorType.UnknownError, string? details = null) 
        : base(message, type, details)
    {
    }
}

/// <summary>
/// Validation error with field-specific information
/// </summary>
public class ValidationError : BaseError
{
    public Dictionary<string, List<string>> FieldErrors { get; }
    
    public ValidationError(string message, Dictionary<string, List<string>>? fieldErrors = null) 
        : base(message, ErrorType.ValidationError)
    {
        FieldErrors = fieldErrors ?? new Dictionary<string, List<string>>();
    }
    
    public ValidationError(Dictionary<string, List<string>> fieldErrors) 
        : base("Validation failed", ErrorType.ValidationError)
    {
        FieldErrors = fieldErrors;
    }
}

/// <summary>
/// API-related errors
/// </summary>
public class ApiError : BaseError
{
    public int? StatusCode { get; }
    public string? ResponseBody { get; }
    
    public ApiError(string message, int? statusCode = null, string? responseBody = null) 
        : base(message, DetermineErrorType(statusCode), responseBody)
    {
        StatusCode = statusCode;
        ResponseBody = responseBody;
    }
    
    private static ErrorType DetermineErrorType(int? statusCode)
    {
        return statusCode switch
        {
            401 => ErrorType.Unauthorized,
            403 => ErrorType.Forbidden,
            404 => ErrorType.NotFound,
            >= 400 and < 500 => ErrorType.ClientError,
            >= 500 => ErrorType.ServerError,
            _ => ErrorType.NetworkError
        };
    }
}

/// <summary>
/// Cache-related errors
/// </summary>
public class CacheError : BaseError
{
    public string? Key { get; }
    
    public CacheError(string message, string? key = null) 
        : base(message, ErrorType.CacheError)
    {
        Key = key;
    }
}

/// <summary>
/// Business logic errors
/// </summary>
public class BusinessError : BaseError
{
    public string? RuleViolated { get; }
    
    public BusinessError(string message, string? ruleViolated = null) 
        : base(message, ErrorType.BusinessRuleViolation)
    {
        RuleViolated = ruleViolated;
    }
}
