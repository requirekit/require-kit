using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Logs;

namespace {ServiceName}.API.Infrastructure.Extensions;

/// <summary>
/// Extension methods for configuring OpenTelemetry
/// </summary>
public static class OpenTelemetryExtensions
{
    /// <summary>
    /// Add OpenTelemetry tracing, metrics, and logging
    /// </summary>
    public static IServiceCollection AddOpenTelemetryServices(
        this IServiceCollection services,
        IConfiguration configuration,
        string serviceName = "{ServiceName}")
    {
        var otlpEndpoint = configuration["OpenTelemetry:Endpoint"] ?? "http://localhost:4317";
        
        // Configure OpenTelemetry
        services.AddOpenTelemetry()
            .ConfigureResource(resource => resource
                .AddService(serviceName: serviceName, serviceVersion: "1.0.0")
                .AddAttributes(new Dictionary<string, object>
                {
                    ["environment"] = configuration["Environment"] ?? "Development",
                    ["deployment.environment"] = configuration["Environment"] ?? "Development"
                }))
            .WithTracing(tracing =>
            {
                tracing
                    .AddAspNetCoreInstrumentation(options =>
                    {
                        options.RecordException = true;
                        options.Filter = (httpContext) =>
                        {
                            // Don't trace health checks
                            return !httpContext.Request.Path.StartsWithSegments("/health");
                        };
                    })
                    .AddHttpClientInstrumentation(options =>
                    {
                        options.RecordException = true;
                        options.SetHttpFlavor = true;
                    })
                    .AddSource(serviceName)
                    .SetSampler(new AlwaysOnSampler());
                
                // Add OTLP exporter if configured
                if (!string.IsNullOrEmpty(otlpEndpoint))
                {
                    tracing.AddOtlpExporter(options =>
                    {
                        options.Endpoint = new Uri(otlpEndpoint);
                        options.Protocol = OpenTelemetry.Exporter.OtlpExportProtocol.Grpc;
                    });
                }
                
                // Add console exporter in development
                if (configuration["Environment"] == "Development")
                {
                    tracing.AddConsoleExporter();
                }
            })
            .WithMetrics(metrics =>
            {
                metrics
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddRuntimeInstrumentation()
                    .AddProcessInstrumentation()
                    .AddMeter(serviceName);
                
                // Add Prometheus exporter for scraping
                metrics.AddPrometheusExporter();
                
                // Add OTLP exporter if configured
                if (!string.IsNullOrEmpty(otlpEndpoint))
                {
                    metrics.AddOtlpExporter(options =>
                    {
                        options.Endpoint = new Uri(otlpEndpoint);
                        options.Protocol = OpenTelemetry.Exporter.OtlpExportProtocol.Grpc;
                    });
                }
                
                // Add console exporter in development
                if (configuration["Environment"] == "Development")
                {
                    metrics.AddConsoleExporter();
                }
            });
        
        return services;
    }
    
    /// <summary>
    /// Configure OpenTelemetry middleware
    /// </summary>
    public static IApplicationBuilder UseOpenTelemetry(this IApplicationBuilder app)
    {
        // Add Prometheus scraping endpoint
        app.UseOpenTelemetryPrometheusScrapingEndpoint();
        
        return app;
    }
}

/// <summary>
/// Logging context for structured logging
/// </summary>
public class LoggingContext
{
    public Exception? Exception { get; set; }
    public string Message { get; set; } = string.Empty;
    public HttpContext? HttpContext { get; set; }
    public string? ErrorType { get; set; }
    public int? StatusCode { get; set; }
    public string? CorrelationId { get; set; }
    public Dictionary<string, object>? AdditionalData { get; set; }
}

/// <summary>
/// Extension methods for structured logging
/// </summary>
public static class LoggingExtensions
{
    /// <summary>
    /// Log an API error with structured context
    /// </summary>
    public static void LogApiError(
        this ILogger logger,
        BaseError error,
        HttpContext? httpContext = null,
        Exception? exception = null)
    {
        using (logger.BeginScope(new Dictionary<string, object>
        {
            ["ErrorType"] = error.GetType().Name,
            ["StatusCode"] = error.StatusCode,
            ["CorrelationId"] = httpContext?.TraceIdentifier ?? Guid.NewGuid().ToString()
        }))
        {
            if (exception != null)
            {
                logger.LogError(exception, "API Error: {ErrorMessage}", error.Message);
            }
            else
            {
                logger.LogError("API Error: {ErrorMessage}", error.Message);
            }
        }
    }
    
    /// <summary>
    /// Log an aggregated error with full context
    /// </summary>
    public static void LogAggregatedError(this ILogger logger, LoggingContext context)
    {
        var scope = new Dictionary<string, object>
        {
            ["CorrelationId"] = context.CorrelationId ?? context.HttpContext?.TraceIdentifier ?? Guid.NewGuid().ToString(),
            ["ErrorType"] = context.ErrorType ?? "UnknownError",
            ["StatusCode"] = context.StatusCode ?? 500
        };
        
        if (context.HttpContext != null)
        {
            scope["RequestPath"] = context.HttpContext.Request.Path.ToString();
            scope["RequestMethod"] = context.HttpContext.Request.Method;
            scope["UserAgent"] = context.HttpContext.Request.Headers.UserAgent.ToString();
        }
        
        if (context.AdditionalData != null)
        {
            foreach (var kvp in context.AdditionalData)
            {
                scope[kvp.Key] = kvp.Value;
            }
        }
        
        using (logger.BeginScope(scope))
        {
            if (context.Exception != null)
            {
                logger.LogError(context.Exception, "{Message}", context.Message);
            }
            else
            {
                logger.LogError("{Message}", context.Message);
            }
        }
    }
}
