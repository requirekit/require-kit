using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;

namespace {ServiceName}.API.Models.Requests;

/// <summary>
/// Request model for getting a {Feature} by ID
/// </summary>
public class Get{Feature}Request
{
    [Required]
    [FromRoute]
    public Guid Id { get; set; }
}

/// <summary>
/// Request model for creating a new {Feature}
/// </summary>
public class Create{Feature}Request
{
    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; } = string.Empty;
    
    [StringLength(500)]
    public string? Description { get; set; }
}

/// <summary>
/// Request model for updating an existing {Feature}
/// </summary>
public class Update{Feature}Request
{
    [Required]
    [FromRoute]
    public Guid Id { get; set; }
    
    [Required]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; } = string.Empty;
    
    [StringLength(500)]
    public string? Description { get; set; }
}

/// <summary>
/// Request model for deleting a {Feature}
/// </summary>
public class Delete{Feature}Request
{
    [Required]
    [FromRoute]
    public Guid Id { get; set; }
}

/// <summary>
/// Request model for paginated queries
/// </summary>
public class PagedRequest
{
    [FromQuery]
    public int Page { get; set; } = 1;
    
    [FromQuery]
    public int PageSize { get; set; } = 20;
    
    [FromQuery]
    public string? SortBy { get; set; }
    
    [FromQuery]
    public bool SortDescending { get; set; } = false;
}
