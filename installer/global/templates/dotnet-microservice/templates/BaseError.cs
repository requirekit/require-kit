using Microsoft.AspNetCore.Http;

namespace {ServiceName}.API.Domain;

/// <summary>
/// Base error type for functional error handling using Either monad
/// </summary>
public abstract record BaseError(string Message)
{
    /// <summary>
    /// HTTP status code associated with this error type
    /// </summary>
    public virtual int StatusCode => StatusCodes.Status500InternalServerError;
    
    /// <summary>
    /// Optional error code for client consumption
    /// </summary>
    public virtual string? ErrorCode => null;
    
    /// <summary>
    /// Optional additional details about the error
    /// </summary>
    public virtual Dictionary<string, object>? Details => null;
}

/// <summary>
/// Validation error - typically from input validation
/// </summary>
public record ValidationError(string Message, Dictionary<string, string[]>? ValidationErrors = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status400BadRequest;
    public override string ErrorCode => "VALIDATION_ERROR";
    public override Dictionary<string, object>? Details => 
        ValidationErrors != null ? new Dictionary<string, object> { ["errors"] = ValidationErrors } : null;
}

/// <summary>
/// Resource not found error
/// </summary>
public record NotFoundError(string Message, string? ResourceType = null, string? ResourceId = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status404NotFound;
    public override string ErrorCode => "NOT_FOUND";
    public override Dictionary<string, object>? Details => 
        ResourceType != null || ResourceId != null 
            ? new Dictionary<string, object> 
              { 
                  ["resourceType"] = ResourceType ?? "Unknown",
                  ["resourceId"] = ResourceId ?? "Unknown"
              } 
            : null;
}

/// <summary>
/// Authentication error - user not authenticated
/// </summary>
public record UnauthorizedError(string Message) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status401Unauthorized;
    public override string ErrorCode => "UNAUTHORIZED";
}

/// <summary>
/// Authorization error - user lacks required permissions
/// </summary>
public record ForbiddenError(string Message, string? RequiredPermission = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status403Forbidden;
    public override string ErrorCode => "FORBIDDEN";
    public override Dictionary<string, object>? Details => 
        RequiredPermission != null 
            ? new Dictionary<string, object> { ["requiredPermission"] = RequiredPermission } 
            : null;
}

/// <summary>
/// Conflict error - operation conflicts with current state
/// </summary>
public record ConflictError(string Message, string? ConflictingResource = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status409Conflict;
    public override string ErrorCode => "CONFLICT";
    public override Dictionary<string, object>? Details => 
        ConflictingResource != null 
            ? new Dictionary<string, object> { ["conflictingResource"] = ConflictingResource } 
            : null;
}

/// <summary>
/// Internal service error
/// </summary>
public record ServiceError(string Message, Exception? Exception = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status500InternalServerError;
    public override string ErrorCode => "INTERNAL_ERROR";
}

/// <summary>
/// External service error - dependency failure
/// </summary>
public record ExternalServiceError(string Message, string? ServiceName = null, int? HttpStatusCode = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status502BadGateway;
    public override string ErrorCode => "EXTERNAL_SERVICE_ERROR";
    public override Dictionary<string, object>? Details => 
        ServiceName != null || HttpStatusCode != null 
            ? new Dictionary<string, object> 
              { 
                  ["service"] = ServiceName ?? "Unknown",
                  ["statusCode"] = HttpStatusCode ?? 0
              } 
            : null;
}

/// <summary>
/// Service unavailable error - temporary unavailability
/// </summary>
public record ServiceUnavailableError(string Message, TimeSpan? RetryAfter = null) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status503ServiceUnavailable;
    public override string ErrorCode => "SERVICE_UNAVAILABLE";
    public override Dictionary<string, object>? Details => 
        RetryAfter != null 
            ? new Dictionary<string, object> { ["retryAfterSeconds"] = RetryAfter.Value.TotalSeconds } 
            : null;
}

/// <summary>
/// Timeout error - operation timed out
/// </summary>
public record TimeoutError(string Message, int TimeoutSeconds = 30) : BaseError(Message)
{
    public override int StatusCode => StatusCodes.Status408RequestTimeout;
    public override string ErrorCode => "TIMEOUT";
    public override Dictionary<string, object>? Details => 
        new Dictionary<string, object> { ["timeoutSeconds"] = TimeoutSeconds };
}
