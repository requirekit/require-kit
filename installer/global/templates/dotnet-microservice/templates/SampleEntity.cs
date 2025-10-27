namespace {ServiceName}.API.Domain.Entities;

/// <summary>
/// Domain entity for {Feature}
/// </summary>
public class {Feature}
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    
    // Add additional properties as needed
    // public string Status { get; set; } = "Active";
    // public string CreatedBy { get; set; } = string.Empty;
    // public string UpdatedBy { get; set; } = string.Empty;
}
