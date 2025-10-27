using {ServiceName}.API.Infrastructure.Extensions;
using {ServiceName}.API.Repositories.Implementations;
using {ServiceName}.API.Repositories.Interfaces;
using {ServiceName}.API.Services.Implementations;
using {ServiceName}.API.Services.Interfaces;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Serilog;
using Serilog.Events;

// Configure Serilog early
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
    Log.Information("Starting {ServiceName} API");
    
    var builder = WebApplication.CreateBuilder(args);
    
    // Configure Serilog from configuration
    builder.Host.UseSerilog((context, services, configuration) => configuration
        .ReadFrom.Configuration(context.Configuration)
        .ReadFrom.Services(services)
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.WithEnvironmentName()
        .Enrich.WithProperty("Service", "{ServiceName}")
        .WriteTo.Console(
            outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {SourceContext} {Message:lj} {Properties:j}{NewLine}{Exception}")
        .WriteTo.OpenTelemetry(options =>
        {
            options.Endpoint = context.Configuration["OpenTelemetry:LogsEndpoint"] ?? 
                               context.Configuration["OpenTelemetry:Endpoint"] ?? 
                               "http://localhost:4317";
            options.ResourceAttributes = new Dictionary<string, object>
            {
                ["service.name"] = "{ServiceName}",
                ["service.version"] = "1.0.0"
            };
        }));
    
    // Add services to the container
    ConfigureServices(builder.Services, builder.Configuration);
    
    var app = builder.Build();
    
    // Configure the HTTP request pipeline
    ConfigurePipeline(app);
    
    await app.RunAsync();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    await Log.CloseAndFlushAsync();
}

void ConfigureServices(IServiceCollection services, IConfiguration configuration)
{
    // Add FastEndpoints
    services.AddFastendpointsServices(configuration);
    
    // Add OpenTelemetry
    services.AddOpenTelemetryServices(configuration, "{ServiceName}");
    
    // Add Health Checks
    services.AddHealthChecks()
        .AddCheck("self", () => HealthCheckResult.Healthy(), tags: new[] { "ready" });
    
    // TODO: Add external service health checks
    // Example:
    // .AddUrlGroup(new Uri(configuration["ExternalServices:ApiUrl"]), "external-api", tags: new[] { "ready" })
    // .AddSqlServer(connectionString, name: "database", tags: new[] { "ready" })
    // .AddRedis(redisConnection, name: "cache", tags: new[] { "ready" });
    
    // Add Authentication if needed
    // services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    //     .AddJwtBearer(options =>
    //     {
    //         options.Authority = configuration["Authentication:Authority"];
    //         options.Audience = configuration["Authentication:Audience"];
    //         options.RequireHttpsMetadata = false; // Set to true in production
    //     });
    
    // Add Authorization if needed
    // services.AddAuthorization(options =>
    // {
    //     options.AddPolicy("RequireAuthenticatedUser", policy =>
    //         policy.RequireAuthenticatedUser());
    // });
    
    // Add HTTP clients
    services.AddHttpClient();
    
    // Register domain services
    services.AddScoped<I{Feature}Service, {Feature}Service>();
    
    // Register repositories
    // TODO: Replace with actual database implementation
    services.AddSingleton<I{Feature}Repository, InMemory{Feature}Repository>();
    
    // Add CORS if needed
    services.AddCors(options =>
    {
        options.AddPolicy("AllowSpecificOrigins", policy =>
        {
            policy
                .WithOrigins(configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() ?? new[] { "http://localhost:3000" })
                .AllowAnyHeader()
                .AllowAnyMethod()
                .AllowCredentials();
        });
    });
    
    // Add response compression
    services.AddResponseCompression(options =>
    {
        options.EnableForHttps = true;
    });
}

void ConfigurePipeline(WebApplication app)
{
    // Enable Serilog request logging
    app.UseSerilogRequestLogging(options =>
    {
        options.MessageTemplate = "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
        options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
        {
            diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
            diagnosticContext.Set("RequestScheme", httpContext.Request.Scheme);
            diagnosticContext.Set("UserAgent", httpContext.Request.Headers.UserAgent.ToString());
            diagnosticContext.Set("RemoteIpAddress", httpContext.Connection.RemoteIpAddress?.ToString());
        };
    });
    
    // Add OpenTelemetry middleware
    app.UseOpenTelemetry();
    
    // Use CORS
    app.UseCors("AllowSpecificOrigins");
    
    // Use response compression
    app.UseResponseCompression();
    
    // Configure API with FastEndpoints
    app.UseApiConfiguration(app.Environment, "{ServiceName}", "v1");
    
    // Map health check endpoints (using minimal APIs for simplicity)
    app.MapHealthChecks("/health", new HealthCheckOptions
    {
        ResponseWriter = async (context, report) =>
        {
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsJsonAsync(new
            {
                status = report.Status.ToString(),
                checks = report.Entries.Select(x => new
                {
                    name = x.Key,
                    status = x.Value.Status.ToString(),
                    description = x.Value.Description,
                    duration = x.Value.Duration.TotalMilliseconds
                })
            });
        }
    });
    
    app.MapHealthChecks("/health/live", new HealthCheckOptions
    {
        Predicate = _ => false // Don't run any checks, just return healthy
    });
    
    app.MapHealthChecks("/health/ready", new HealthCheckOptions
    {
        Predicate = check => check.Tags.Contains("ready")
    });
    
    // Add a minimal API endpoint for service info
    app.MapGet("/", () => new
    {
        service = "{ServiceName}",
        version = "1.0.0",
        status = "running",
        timestamp = DateTime.UtcNow
    }).AllowAnonymous();
}
