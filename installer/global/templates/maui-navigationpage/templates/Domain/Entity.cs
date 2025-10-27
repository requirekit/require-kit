# SOURCE: maui-appshell template (shared)
using Realms;

namespace {{ProjectName}}.Entities;

/// <summary>
/// Entity class for [ENTITY_NAME]
/// Entities represent data models that map to database tables
/// </summary>
public partial class [ENTITY_TYPE] : RealmObject
{
    /// <summary>
    /// Primary key identifier
    /// </summary>
    [PrimaryKey]
    public int Id { get; set; }

    /// <summary>
    /// Example string property
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Example nullable string property
    /// </summary>
    public string? Description { get; set; }

    /// <summary>
    /// Example datetime property
    /// </summary>
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;

    /// <summary>
    /// Example datetime property that can be null
    /// </summary>
    public DateTimeOffset? UpdatedAt { get; set; }

    /// <summary>
    /// Example boolean property
    /// </summary>
    public bool IsActive { get; set; } = true;

    /// <summary>
    /// Example integer property
    /// </summary>
    public int Count { get; set; }

    /// <summary>
    /// Example decimal property for monetary values
    /// </summary>
    public decimal Amount { get; set; }

    /// <summary>
    /// Example enum property (stored as int in Realm)
    /// </summary>
    public [ENTITY_TYPE]Status Status { get; set; } = [ENTITY_TYPE]Status.Pending;

    /// <summary>
    /// Example list property for related data
    /// </summary>
    public IList<string> Tags { get; } = new List<string>();

    /// <summary>
    /// Example relationship to another entity
    /// </summary>
    public [RELATED_ENTITY]? Related[RELATED_ENTITY] { get; set; }

    /// <summary>
    /// Example computed property (not stored in database)
    /// </summary>
    [Ignored]
    public bool IsNew => CreatedAt > DateTimeOffset.UtcNow.AddDays(-1);

    /// <summary>
    /// Example computed property for display
    /// </summary>
    [Ignored]
    public string DisplayName => string.IsNullOrWhiteSpace(Name) ? "Unnamed" : Name;

    /// <summary>
    /// Method to update the entity
    /// </summary>
    public void Update(string name, string? description = null, bool? isActive = null)
    {
        Name = name;
        
        if (description != null)
            Description = description;
        
        if (isActive.HasValue)
            IsActive = isActive.Value;
        
        UpdatedAt = DateTimeOffset.UtcNow;
    }

    /// <summary>
    /// Method to mark as inactive
    /// </summary>
    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTimeOffset.UtcNow;
    }

    /// <summary>
    /// Method to mark as active
    /// </summary>
    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTimeOffset.UtcNow;
    }

    /// <summary>
    /// Method to change status
    /// </summary>
    public void ChangeStatus([ENTITY_TYPE]Status newStatus)
    {
        Status = newStatus;
        UpdatedAt = DateTimeOffset.UtcNow;
    }

    /// <summary>
    /// Method to add a tag
    /// </summary>
    public void AddTag(string tag)
    {
        if (!string.IsNullOrWhiteSpace(tag) && !Tags.Contains(tag))
        {
            Tags.Add(tag);
            UpdatedAt = DateTimeOffset.UtcNow;
        }
    }

    /// <summary>
    /// Method to remove a tag
    /// </summary>
    public void RemoveTag(string tag)
    {
        if (Tags.Remove(tag))
        {
            UpdatedAt = DateTimeOffset.UtcNow;
        }
    }

    /// <summary>
    /// Method to clear all tags
    /// </summary>
    public void ClearTags()
    {
        if (Tags.Count > 0)
        {
            Tags.Clear();
            UpdatedAt = DateTimeOffset.UtcNow;
        }
    }
}

/// <summary>
/// Status enumeration for [ENTITY_TYPE]
/// </summary>
public enum [ENTITY_TYPE]Status
{
    Pending = 0,
    InProgress = 1,
    Completed = 2,
    Cancelled = 3,
    Failed = 4
}
