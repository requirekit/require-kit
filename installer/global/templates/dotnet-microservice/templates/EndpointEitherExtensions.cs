using {ServiceName}.API.Domain;
using {ServiceName}.API.Infrastructure.OpenTelemetry;
using FastEndpoints;
using LanguageExt;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using System.Diagnostics;

namespace {ServiceName}.API.Infrastructure.Extensions;

/// <summary>
/// Extension methods for handling Either monad results in FastEndpoints
/// </summary>
public static class EndpointEitherExtensions
{
    /// <summary>
    /// Handle Either result for endpoints with request and response
    /// </summary>
    public static async Task HandleEitherResultAsync<TRequest, TResponse, TError, TSuccess>(
        this Endpoint<TRequest, TResponse> endpoint,
        Either<TError, TSuccess> result,
        Func<TSuccess, Task> successHandler,
        CancellationToken ct
    )
        where TRequest : notnull
        where TError : BaseError
    {
        try
        {
            await result.Match(
                Right: async success =>
                {
                    try
                    {
                        await successHandler(success);
                    }
                    catch (Exception ex)
                    {
                        var context = new LoggingContext
                        {
                            Exception = ex,
                            Message = "Error in success handler",
                            HttpContext = endpoint.HttpContext,
                            ErrorType = "SuccessHandlerException",
                            StatusCode = StatusCodes.Status500InternalServerError,
                            CorrelationId = Activity.Current?.Id ?? endpoint.HttpContext?.TraceIdentifier
                        };
                        
                        endpoint.Logger.LogAggregatedError(context);
                        
                        endpoint.AddError($"Error processing response: {ex.Message}");
                        if (endpoint.HttpContext != null)
                        {
                            await endpoint.HttpContext.Response.SendErrorsAsync(
                                endpoint.ValidationFailures,
                                StatusCodes.Status500InternalServerError,
                                null,
                                ct);
                        }
                    }
                },
                Left: async error =>
                {
                    await endpoint.HandleErrorAsync(error, ct);
                }
            );
        }
        catch (Exception ex)
        {
            var context = new LoggingContext
            {
                Exception = ex,
                Message = "Unhandled exception in HandleEitherAsync",
                HttpContext = endpoint.HttpContext,
                ErrorType = "UnhandledException",
                StatusCode = StatusCodes.Status500InternalServerError
            };
            
            endpoint.Logger.LogAggregatedError(context);
                
            endpoint.AddError($"An unexpected error occurred: {ex.Message}");
            if (endpoint.HttpContext != null)
            {
                await endpoint.HttpContext.Response.SendErrorsAsync(
                    endpoint.ValidationFailures,
                    StatusCodes.Status500InternalServerError,
                    null,
                    ct);
            }
        }
    }
    
    /// <summary>
    /// Handle Either result for endpoints without request
    /// </summary>
    public static async Task HandleEitherResultAsync<TResponse, TError, TSuccess>(
        this EndpointWithoutRequest<TResponse> endpoint,
        Either<TError, TSuccess> result,
        Func<TSuccess, Task> successHandler,
        CancellationToken ct
    )
        where TError : BaseError
    {
        try
        {
            await result.Match(
                Right: async success =>
                {
                    try
                    {
                        await successHandler(success);
                    }
                    catch (Exception ex)
                    {
                        var context = new LoggingContext
                        {
                            Exception = ex,
                            Message = "Error in success handler",
                            HttpContext = endpoint.HttpContext,
                            ErrorType = "SuccessHandlerException",
                            StatusCode = StatusCodes.Status500InternalServerError,
                            CorrelationId = Activity.Current?.Id ?? endpoint.HttpContext?.TraceIdentifier
                        };
                        
                        endpoint.Logger.LogAggregatedError(context);
                            
                        endpoint.AddError($"Error processing response: {ex.Message}");
                        if (endpoint.HttpContext != null)
                        {
                            await endpoint.HttpContext.Response.SendErrorsAsync(
                                endpoint.ValidationFailures,
                                StatusCodes.Status500InternalServerError,
                                null,
                                ct);
                        }
                    }
                },
                Left: async error =>
                {
                    await endpoint.HandleErrorAsync(error, ct);
                }
            );
        }
        catch (Exception ex)
        {
            var context = new LoggingContext
            {
                Exception = ex,
                Message = "Unhandled exception in HandleEitherAsync",
                HttpContext = endpoint.HttpContext,
                ErrorType = "UnhandledException",
                StatusCode = StatusCodes.Status500InternalServerError
            };
            
            endpoint.Logger.LogAggregatedError(context);
                
            endpoint.AddError($"An unexpected error occurred: {ex.Message}");
            if (endpoint.HttpContext != null)
            {
                await endpoint.HttpContext.Response.SendErrorsAsync(
                    endpoint.ValidationFailures,
                    StatusCodes.Status500InternalServerError,
                    null,
                    ct);
            }
        }
    }

    /// <summary>
    /// Handle error response for endpoints with request
    /// </summary>
    public static async Task HandleErrorAsync<TRequest, TResponse, TError>(
        this Endpoint<TRequest, TResponse> endpoint,
        TError error,
        CancellationToken ct
    )
        where TRequest : notnull
        where TError : BaseError
    {
        try
        {
            // Get exception from error if available
            Exception? exception = null;
            if (error is ServiceError serviceError)
            {
                exception = serviceError.Exception;
            }
            
            // Use the aggregated logging approach for domain errors
            endpoint.Logger.LogApiError(
                error,
                endpoint.HttpContext,
                exception);
            
            // Add the error message to the endpoint's validation failures
            endpoint.AddError(error.Message);
            
            // Add error details if available
            if (error.Details != null)
            {
                foreach (var detail in error.Details)
                {
                    endpoint.HttpContext?.Items.Add($"error.{detail.Key}", detail.Value);
                }
            }
            
            var statusCode = error.StatusCode;

            if (endpoint.HttpContext != null)
            {
                await endpoint.HttpContext.Response.SendErrorsAsync(
                    endpoint.ValidationFailures,
                    statusCode,
                    null,
                    ct);
            }
        }
        catch (Exception ex)
        {
            var context = new LoggingContext
            {
                Exception = ex,
                Message = "Failed to send error response",
                HttpContext = endpoint.HttpContext,
                ErrorType = "ErrorResponseFailure",
                StatusCode = StatusCodes.Status500InternalServerError,
                AdditionalData = new Dictionary<string, object>
                {
                    ["ErrorMessage"] = error.Message
                }
            };
            
            endpoint.Logger.LogAggregatedError(context);
                
            if (endpoint.HttpContext != null)
            {
                await HandleErrorWithFallbackAsync(
                    endpoint.HttpContext, 
                    endpoint.Logger, 
                    StatusCodes.Status500InternalServerError, 
                    "Failed to process error response", 
                    ct);
            }
        }
    }
    
    /// <summary>
    /// Handle error response for endpoints without request
    /// </summary>
    public static async Task HandleErrorAsync<TResponse, TError>(
        this EndpointWithoutRequest<TResponse> endpoint,
        TError error,
        CancellationToken ct
    )
        where TError : BaseError
    {
        try
        {
            // Get exception from error if available
            Exception? exception = null;
            if (error is ServiceError serviceError)
            {
                exception = serviceError.Exception;
            }
            
            // Use the aggregated logging approach for domain errors
            endpoint.Logger.LogApiError(
                error,
                endpoint.HttpContext,
                exception);
        
            // Add the error message to the endpoint's validation failures
            endpoint.AddError(error.Message);
            
            // Add error details if available
            if (error.Details != null)
            {
                foreach (var detail in error.Details)
                {
                    endpoint.HttpContext?.Items.Add($"error.{detail.Key}", detail.Value);
                }
            }
        
            var statusCode = error.StatusCode;
        
            if (endpoint.HttpContext != null)
            {
                await endpoint.HttpContext.Response.SendErrorsAsync(
                    endpoint.ValidationFailures,
                    statusCode,
                    null,
                    ct);
            }
        }
        catch (Exception ex)
        {
            var context = new LoggingContext
            {
                Exception = ex,
                Message = "Failed to send error response",
                HttpContext = endpoint.HttpContext,
                ErrorType = "ErrorResponseFailure",
                StatusCode = StatusCodes.Status500InternalServerError,
                AdditionalData = new Dictionary<string, object>
                {
                    ["ErrorMessage"] = error.Message
                }
            };
            
            endpoint.Logger.LogAggregatedError(context);
                
            if (endpoint.HttpContext != null)
            {
                await HandleErrorWithFallbackAsync(
                    endpoint.HttpContext, 
                    endpoint.Logger, 
                    StatusCodes.Status500InternalServerError, 
                    "Failed to process error response", 
                    ct);
            }
        }
    }

    /// <summary>
    /// Fallback error handler when primary error handling fails
    /// </summary>
    private static async Task HandleErrorWithFallbackAsync(
        HttpContext httpContext,
        ILogger logger,
        int statusCode,
        string message,
        CancellationToken ct
    )
    {
        try
        {
            httpContext.Response.StatusCode = statusCode;
            await httpContext.Response.WriteAsync(message, ct);
        }
        catch (Exception fallbackEx)
        {
            var context = new LoggingContext
            {
                Exception = fallbackEx,
                Message = "Failed to send fallback error response",
                HttpContext = httpContext,
                ErrorType = "FallbackResponseFailure",
                StatusCode = statusCode
            };
            
            logger.LogAggregatedError(context);
        }
    }
}
