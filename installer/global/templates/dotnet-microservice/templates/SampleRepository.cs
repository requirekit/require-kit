using {ServiceName}.API.Domain.Entities;

namespace {ServiceName}.API.Repositories.Interfaces;

/// <summary>
/// Repository interface for {Feature} data access
/// </summary>
public interface I{Feature}Repository
{
    /// <summary>
    /// Get a {Feature} by ID
    /// </summary>
    Task<{Feature}?> GetByIdAsync(Guid id, CancellationToken ct);
    
    /// <summary>
    /// Get a {Feature} by name
    /// </summary>
    Task<{Feature}?> GetByNameAsync(string name, CancellationToken ct);
    
    /// <summary>
    /// Get all {Feature}s
    /// </summary>
    Task<IEnumerable<{Feature}>> GetAllAsync(CancellationToken ct);
    
    /// <summary>
    /// Get paged {Feature}s
    /// </summary>
    Task<(IEnumerable<{Feature}> Items, int TotalCount)> GetPagedAsync(int page, int pageSize, CancellationToken ct);
    
    /// <summary>
    /// Create a new {Feature}
    /// </summary>
    Task<{Feature}> CreateAsync({Feature} entity, CancellationToken ct);
    
    /// <summary>
    /// Update an existing {Feature}
    /// </summary>
    Task<{Feature}> UpdateAsync({Feature} entity, CancellationToken ct);
    
    /// <summary>
    /// Delete a {Feature}
    /// </summary>
    Task DeleteAsync(Guid id, CancellationToken ct);
    
    /// <summary>
    /// Check if a {Feature} exists
    /// </summary>
    Task<bool> ExistsAsync(Guid id, CancellationToken ct);
}

namespace {ServiceName}.API.Repositories.Implementations;

/// <summary>
/// In-memory repository implementation for {Feature} (for testing/demo purposes)
/// Replace with actual database implementation (EF Core, Dapper, etc.)
/// </summary>
public class InMemory{Feature}Repository : I{Feature}Repository
{
    private readonly List<{Feature}> _data = new();
    private readonly ILogger<InMemory{Feature}Repository> _logger;
    
    public InMemory{Feature}Repository(ILogger<InMemory{Feature}Repository> logger)
    {
        _logger = logger;
        
        // Seed with sample data
        SeedData();
    }
    
    public Task<{Feature}?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        var entity = _data.FirstOrDefault(x => x.Id == id);
        return Task.FromResult(entity);
    }
    
    public Task<{Feature}?> GetByNameAsync(string name, CancellationToken ct)
    {
        var entity = _data.FirstOrDefault(x => x.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
        return Task.FromResult(entity);
    }
    
    public Task<IEnumerable<{Feature}>> GetAllAsync(CancellationToken ct)
    {
        return Task.FromResult(_data.AsEnumerable());
    }
    
    public Task<(IEnumerable<{Feature}> Items, int TotalCount)> GetPagedAsync(int page, int pageSize, CancellationToken ct)
    {
        var totalCount = _data.Count;
        var items = _data
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToList();
        
        return Task.FromResult((items.AsEnumerable(), totalCount));
    }
    
    public Task<{Feature}> CreateAsync({Feature} entity, CancellationToken ct)
    {
        _data.Add(entity);
        _logger.LogDebug("Created {Feature} with ID {Id} in repository", entity.Id);
        return Task.FromResult(entity);
    }
    
    public Task<{Feature}> UpdateAsync({Feature} entity, CancellationToken ct)
    {
        var index = _data.FindIndex(x => x.Id == entity.Id);
        if (index >= 0)
        {
            _data[index] = entity;
            _logger.LogDebug("Updated {Feature} with ID {Id} in repository", entity.Id);
        }
        return Task.FromResult(entity);
    }
    
    public Task DeleteAsync(Guid id, CancellationToken ct)
    {
        var index = _data.FindIndex(x => x.Id == id);
        if (index >= 0)
        {
            _data.RemoveAt(index);
            _logger.LogDebug("Deleted {Feature} with ID {Id} from repository", id);
        }
        return Task.CompletedTask;
    }
    
    public Task<bool> ExistsAsync(Guid id, CancellationToken ct)
    {
        var exists = _data.Any(x => x.Id == id);
        return Task.FromResult(exists);
    }
    
    private void SeedData()
    {
        _data.AddRange(new[]
        {
            new {Feature}
            {
                Id = Guid.Parse("11111111-1111-1111-1111-111111111111"),
                Name = "Sample {Feature} 1",
                Description = "This is the first sample {Feature}",
                CreatedAt = DateTime.UtcNow.AddDays(-30),
                UpdatedAt = DateTime.UtcNow.AddDays(-10)
            },
            new {Feature}
            {
                Id = Guid.Parse("22222222-2222-2222-2222-222222222222"),
                Name = "Sample {Feature} 2",
                Description = "This is the second sample {Feature}",
                CreatedAt = DateTime.UtcNow.AddDays(-20),
                UpdatedAt = DateTime.UtcNow.AddDays(-5)
            }
        });
        
        _logger.LogInformation("Seeded {Count} sample {Feature}s", _data.Count);
    }
}
