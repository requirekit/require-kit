using FastEndpoints;
using FastEndpoints.Swagger;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.Infrastructure;
using NJsonSchema.Generation;

namespace {ServiceName}.API.Infrastructure.Extensions;

/// <summary>
/// Extension methods for configuring FastEndpoints
/// </summary>
public static class FastEndpointsExtensions
{
    /// <summary>
    /// Add FastEndpoints services with Swagger documentation
    /// </summary>
    public static IServiceCollection AddFastendpointsServices(
        this IServiceCollection services, 
        IConfiguration configuration,
        Action<JsonSchemaGeneratorSettings>? configureSchemaSettings = null)
    {
        // Register core services
        services.AddFastEndpoints()
            .SwaggerDocument(o =>
            {
                o.DocumentSettings = s =>
                {
                    s.Title = "{ServiceName} API";
                    s.Version = "v1";
                    s.Description = "API for {ServiceName} microservice";
                    
                    // Use short schema names (removes namespace)
                    o.ShortSchemaNames = true;
                    
                    // Configure schema settings
                    s.SchemaSettings.GenerateKnownTypes = false;
                    s.SchemaSettings.GenerateEnumMappingDescription = false;
                    
                    // Allow custom configuration
                    configureSchemaSettings?.Invoke(s.SchemaSettings);
                };
                
                o.EndpointFilter = endpoint => 
                    !endpoint.EndpointTags?.Contains("exclude-from-docs") ?? true;
            })
            .AddEndpointsApiExplorer();
        
        // Add ProblemDetails factory
        services.AddSingleton<ProblemDetailsFactory, CustomProblemDetailsFactory>();
        
        return services;
    }
    
    /// <summary>
    /// Configure API middleware pipeline
    /// </summary>
    public static IApplicationBuilder UseApiConfiguration(
        this IApplicationBuilder app,
        IWebHostEnvironment environment,
        string serviceName,
        string apiVersion = "v1")
    {
        var safeServiceName = serviceName.ToLowerInvariant().Trim();
        
        // Configure FastEndpoints
        app.UseFastEndpoints(c => 
        {
            c.Endpoints.RoutePrefix = $"api/{apiVersion}";
            c.Serializer.Options.PropertyNamingPolicy = System.Text.Json.JsonNamingPolicy.CamelCase;
            
            // Configure error responses
            c.Errors.ResponseBuilder = (failures, ctx, statusCode) => 
            {
                var problemFactory = ctx.RequestServices.GetRequiredService<ProblemDetailsFactory>();
                var problemDetails = problemFactory.CreateProblemDetails(
                    ctx,
                    statusCode,
                    detail: string.Join("; ", failures.Select(f => f.ErrorMessage)),
                    type: GetProblemTypeFromStatusCode(statusCode, safeServiceName),
                    instance: ctx.Request.Path
                );
                
                // Add custom properties
                problemDetails.Extensions["timestamp"] = DateTimeOffset.UtcNow;
                if (ctx.TraceIdentifier != null)
                {
                    problemDetails.Extensions["traceId"] = ctx.TraceIdentifier;
                }
                
                return problemDetails;
            };
            
            // Configure global endpoint options
            c.Endpoints.Configurator = endpoint =>
            {
                endpoint.Options(x => x
                    .WithTags("api")
                    .Produces<ProblemDetails>(400)
                    .Produces<ProblemDetails>(401)
                    .Produces<ProblemDetails>(403)
                    .Produces<ProblemDetails>(500));
            };
        });
        
        // Configure exception handling
        app.UseExceptionHandler(errorApp =>
        {
            errorApp.Run(async context =>
            {
                var problemFactory = context.RequestServices.GetRequiredService<ProblemDetailsFactory>();
                var problemDetails = problemFactory.CreateProblemDetails(
                    context, 
                    500, 
                    "An unexpected error occurred");
                
                context.Response.ContentType = "application/problem+json";
                context.Response.StatusCode = 500;
                await context.Response.WriteAsJsonAsync(problemDetails);
            });
        });

        // Environment-specific configuration
        if (environment.IsDevelopment())
        {
            ConfigureDevelopment(app, safeServiceName);
        }
        else
        {
            ConfigureProduction(app);
        }
        
        // Authorization middleware (if using authentication)
        // app.UseAuthorization();
        
        return app;
    }
     
    private static string GetProblemTypeFromStatusCode(int statusCode, string serviceName)
    {
        var safeServiceName = serviceName.ToLowerInvariant();
        return statusCode switch
        {
            StatusCodes.Status400BadRequest => $"https://{safeServiceName}.example.com/errors/bad-request",
            StatusCodes.Status401Unauthorized => $"https://{safeServiceName}.example.com/errors/unauthorized",
            StatusCodes.Status403Forbidden => $"https://{safeServiceName}.example.com/errors/forbidden",
            StatusCodes.Status404NotFound => $"https://{safeServiceName}.example.com/errors/not-found",
            StatusCodes.Status409Conflict => $"https://{safeServiceName}.example.com/errors/conflict",
            StatusCodes.Status422UnprocessableEntity => $"https://{safeServiceName}.example.com/errors/validation",
            StatusCodes.Status500InternalServerError => $"https://{safeServiceName}.example.com/errors/server-error",
            StatusCodes.Status502BadGateway => $"https://{safeServiceName}.example.com/errors/bad-gateway",
            StatusCodes.Status503ServiceUnavailable => $"https://{safeServiceName}.example.com/errors/service-unavailable",
            _ => $"https://{safeServiceName}.example.com/errors/status-{statusCode}"
        };
    }
    
    private static void ConfigureDevelopment(IApplicationBuilder app, string serviceName)
    {
        // Enable Swagger UI
        app.UseOpenApi();
        app.UseSwaggerGen();
        app.UseSwaggerUi(settings =>
        {
            settings.DocExpansion = "list";
            settings.DefaultModelsExpandDepth = -1;
            settings.DocumentTitle = $"{serviceName} API";
            settings.Path = "/swagger";
        });
    }
    
    private static void ConfigureProduction(IApplicationBuilder app)
    {
        // Enable HTTPS redirection
        app.UseHttpsRedirection();
        
        // Enable authentication if configured
        // app.UseAuthentication();
        
        // Optionally enable Swagger in production with authentication
        // app.UseOpenApi();
        // app.UseSwaggerGen();
    }
}

/// <summary>
/// Custom ProblemDetails factory
/// </summary>
public class CustomProblemDetailsFactory : ProblemDetailsFactory
{
    public override Microsoft.AspNetCore.Mvc.ProblemDetails CreateProblemDetails(
        HttpContext httpContext,
        int? statusCode = null,
        string? title = null,
        string? type = null,
        string? detail = null,
        string? instance = null)
    {
        statusCode ??= 500;
        
        var problemDetails = new Microsoft.AspNetCore.Mvc.ProblemDetails
        {
            Status = statusCode,
            Title = title ?? GetDefaultTitle(statusCode.Value),
            Type = type ?? $"https://httpstatuses.com/{statusCode}",
            Detail = detail,
            Instance = instance ?? httpContext.Request.Path
        };
        
        return problemDetails;
    }
    
    public override Microsoft.AspNetCore.Mvc.ValidationProblemDetails CreateValidationProblemDetails(
        HttpContext httpContext,
        ModelStateDictionary modelStateDictionary,
        int? statusCode = null,
        string? title = null,
        string? type = null,
        string? detail = null,
        string? instance = null)
    {
        throw new NotImplementedException("Use FastEndpoints validation instead");
    }
    
    private static string GetDefaultTitle(int statusCode)
    {
        return statusCode switch
        {
            400 => "Bad Request",
            401 => "Unauthorized",
            403 => "Forbidden",
            404 => "Not Found",
            409 => "Conflict",
            422 => "Unprocessable Entity",
            500 => "Internal Server Error",
            502 => "Bad Gateway",
            503 => "Service Unavailable",
            _ => "Error"
        };
    }
}
