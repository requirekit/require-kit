namespace {ServiceName}.API.Models.Dtos;

/// <summary>
/// DTO for creating a {Feature}
/// </summary>
public class Create{Feature}Dto
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
}

/// <summary>
/// DTO for updating a {Feature}
/// </summary>
public class Update{Feature}Dto
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
}

/// <summary>
/// DTO for {Feature} filters
/// </summary>
public class {Feature}FilterDto
{
    public string? SearchTerm { get; set; }
    public DateTime? CreatedAfter { get; set; }
    public DateTime? CreatedBefore { get; set; }
    public string? Status { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 20;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; } = false;
}
