using FastEndpoints;
using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace {ServiceName}.API.Endpoints.Health;

/// <summary>
/// Health check endpoint for monitoring service health
/// </summary>
public class HealthCheck : EndpointWithoutRequest<HealthCheckResponse>
{
    private readonly IHealthCheckService _healthCheckService;
    private readonly ILogger<HealthCheck> _logger;
    
    public HealthCheck(IHealthCheckService healthCheckService, ILogger<HealthCheck> logger)
    {
        _healthCheckService = healthCheckService;
        _logger = logger;
    }
    
    public override void Configure()
    {
        Get("/health");
        AllowAnonymous();
        
        Description(b => b
            .Produces<HealthCheckResponse>(200, "application/json")
            .Produces<HealthCheckResponse>(503, "application/json")
            .WithName("HealthCheck")
            .WithDisplayName("Health Check")
            .WithDescription("Returns the health status of the service and its dependencies.")
            .WithSummary("Health Check")
            .WithTags("Health"));
    }
    
    public override async Task HandleAsync(CancellationToken ct)
    {
        var healthReport = await _healthCheckService.CheckHealthAsync(
            predicate: _ => true,
            cancellationToken: ct);
        
        var response = new HealthCheckResponse
        {
            Status = healthReport.Status.ToString(),
            TotalDuration = healthReport.TotalDuration.TotalMilliseconds,
            Checks = healthReport.Entries.Select(x => new HealthCheckItem
            {
                Name = x.Key,
                Status = x.Value.Status.ToString(),
                Description = x.Value.Description,
                Duration = x.Value.Duration.TotalMilliseconds,
                Tags = x.Value.Tags?.ToList() ?? new List<string>(),
                Data = x.Value.Data?.ToDictionary(d => d.Key, d => d.Value?.ToString() ?? string.Empty)
            }).ToList()
        };
        
        var statusCode = healthReport.Status == HealthStatus.Healthy ? 200 : 503;
        
        if (healthReport.Status != HealthStatus.Healthy)
        {
            _logger.LogWarning("Health check failed: {Status}", healthReport.Status);
        }
        
        await SendAsync(response, statusCode, ct);
    }
}

/// <summary>
/// Liveness probe endpoint for Kubernetes
/// </summary>
public class LivenessCheck : EndpointWithoutRequest<LivenessResponse>
{
    public override void Configure()
    {
        Get("/health/live");
        AllowAnonymous();
        
        Description(b => b
            .Produces<LivenessResponse>(200)
            .WithName("LivenessCheck")
            .WithDisplayName("Liveness Check")
            .WithDescription("Simple liveness check for container orchestration.")
            .WithSummary("Liveness Check")
            .WithTags("Health"));
    }
    
    public override async Task HandleAsync(CancellationToken ct)
    {
        await SendOkAsync(new LivenessResponse { Status = "Alive" }, ct);
    }
}

/// <summary>
/// Readiness probe endpoint for Kubernetes
/// </summary>
public class ReadinessCheck : EndpointWithoutRequest<ReadinessResponse>
{
    private readonly IHealthCheckService _healthCheckService;
    
    public ReadinessCheck(IHealthCheckService healthCheckService)
    {
        _healthCheckService = healthCheckService;
    }
    
    public override void Configure()
    {
        Get("/health/ready");
        AllowAnonymous();
        
        Description(b => b
            .Produces<ReadinessResponse>(200)
            .Produces<ReadinessResponse>(503)
            .WithName("ReadinessCheck")
            .WithDisplayName("Readiness Check")
            .WithDescription("Checks if the service is ready to accept traffic.")
            .WithSummary("Readiness Check")
            .WithTags("Health"));
    }
    
    public override async Task HandleAsync(CancellationToken ct)
    {
        var healthReport = await _healthCheckService.CheckHealthAsync(
            predicate: check => check.Tags.Contains("ready"),
            cancellationToken: ct);
        
        var response = new ReadinessResponse
        {
            Status = healthReport.Status == HealthStatus.Healthy ? "Ready" : "NotReady",
            Checks = healthReport.Entries
                .Where(x => x.Value.Status != HealthStatus.Healthy)
                .Select(x => x.Key)
                .ToList()
        };
        
        var statusCode = healthReport.Status == HealthStatus.Healthy ? 200 : 503;
        await SendAsync(response, statusCode, ct);
    }
}

// Response models
public class HealthCheckResponse
{
    public string Status { get; set; } = "Healthy";
    public double TotalDuration { get; set; }
    public List<HealthCheckItem> Checks { get; set; } = new();
}

public class HealthCheckItem
{
    public string Name { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string? Description { get; set; }
    public double Duration { get; set; }
    public List<string> Tags { get; set; } = new();
    public Dictionary<string, string>? Data { get; set; }
}

public class LivenessResponse
{
    public string Status { get; set; } = string.Empty;
}

public class ReadinessResponse
{
    public string Status { get; set; } = string.Empty;
    public List<string> Checks { get; set; } = new();
}
