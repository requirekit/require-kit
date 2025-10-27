# SOURCE: maui-appshell template (shared)
using ErrorOr;
using {{ProjectName}}.DatabaseServices.Interfaces;
using {{ProjectName}}.Entities;
using {{ProjectName}}.Services.Interfaces;
using Realms;

namespace {{ProjectName}}.DatabaseServices;

/// <summary>
/// Repository implementation for [ENTITY_TYPE] using Realm database
/// Implements the Repository pattern for data access
/// </summary>
public class [ENTITY_TYPE]Repository : I[ENTITY_TYPE]Repository
{
    private readonly ILogService _logService;

    public [ENTITY_TYPE]Repository(ILogService logService)
    {
        _logService = logService;
    }

    /// <summary>
    /// Get entity by ID
    /// </summary>
    public async Task<ErrorOr<[ENTITY_TYPE]>> GetByIdAsync(int id)
    {
        try
        {
            using var realm = Realm.GetInstance();
            
            var entity = realm.Find<[ENTITY_TYPE]>(id);
            
            if (entity == null)
            {
                return Error.NotFound(
                    code: "[ENTITY_TYPE].NotFound",
                    description: $"[ENTITY_TYPE] with ID {id} was not found");
            }

            // Return a detached copy to avoid Realm threading issues
            return realm.ObjectForPrimaryKey<[ENTITY_TYPE]>(id)?.Detach() 
                ?? Error.NotFound(
                    code: "[ENTITY_TYPE].NotFound",
                    description: $"[ENTITY_TYPE] with ID {id} was not found");
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetByIdAsync" },
                { "EntityId", id },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to retrieve [ENTITY_TYPE] from database");
        }
    }

    /// <summary>
    /// Get all entities
    /// </summary>
    public async Task<ErrorOr<IList<[ENTITY_TYPE]>>> GetAllAsync()
    {
        try
        {
            using var realm = Realm.GetInstance();
            
            var entities = realm.All<[ENTITY_TYPE]>()
                .ToList()
                .Select(e => e.Detach())
                .ToList();

            return entities;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetAllAsync" },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to retrieve [ENTITY_TYPE] entities from database");
        }
    }

    /// <summary>
    /// Get entities with filtering
    /// </summary>
    public async Task<ErrorOr<IList<[ENTITY_TYPE]>>> GetWhereAsync(Func<[ENTITY_TYPE], bool> predicate)
    {
        try
        {
            using var realm = Realm.GetInstance();
            
            var entities = realm.All<[ENTITY_TYPE]>()
                .Where(predicate)
                .ToList()
                .Select(e => e.Detach())
                .ToList();

            return entities;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetWhereAsync" },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to retrieve filtered [ENTITY_TYPE] entities from database");
        }
    }

    /// <summary>
    /// Insert new entity
    /// </summary>
    public async Task<ErrorOr<[ENTITY_TYPE]>> InsertAsync([ENTITY_TYPE] entity)
    {
        try
        {
            if (entity == null)
            {
                return Error.Validation(
                    code: "[ENTITY_TYPE].NullEntity",
                    description: "[ENTITY_TYPE] cannot be null");
            }

            using var realm = Realm.GetInstance();
            
            await realm.WriteAsync(() =>
            {
                realm.Add(entity);
            });

            _logService.TrackEvent("[ENTITY_TYPE]Inserted", new Dictionary<string, object>
            {
                { "EntityId", entity.Id }
            });

            return entity.Detach();
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "InsertAsync" },
                { "EntityId", entity?.Id ?? 0 },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to insert [ENTITY_TYPE] into database");
        }
    }

    /// <summary>
    /// Update existing entity
    /// </summary>
    public async Task<ErrorOr<bool>> UpdateAsync([ENTITY_TYPE] entity)
    {
        try
        {
            if (entity == null)
            {
                return Error.Validation(
                    code: "[ENTITY_TYPE].NullEntity",
                    description: "[ENTITY_TYPE] cannot be null");
            }

            using var realm = Realm.GetInstance();
            
            var existingEntity = realm.Find<[ENTITY_TYPE]>(entity.Id);
            if (existingEntity == null)
            {
                return Error.NotFound(
                    code: "[ENTITY_TYPE].NotFound",
                    description: $"[ENTITY_TYPE] with ID {entity.Id} was not found");
            }

            await realm.WriteAsync(() =>
            {
                // Update properties as needed
                // existingEntity.Property = entity.Property;
                realm.Add(entity, update: true);
            });

            _logService.TrackEvent("[ENTITY_TYPE]Updated", new Dictionary<string, object>
            {
                { "EntityId", entity.Id }
            });

            return true;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "UpdateAsync" },
                { "EntityId", entity?.Id ?? 0 },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to update [ENTITY_TYPE] in database");
        }
    }

    /// <summary>
    /// Delete entity by ID
    /// </summary>
    public async Task<ErrorOr<bool>> DeleteAsync(int id)
    {
        try
        {
            using var realm = Realm.GetInstance();
            
            var entity = realm.Find<[ENTITY_TYPE]>(id);
            if (entity == null)
            {
                return Error.NotFound(
                    code: "[ENTITY_TYPE].NotFound",
                    description: $"[ENTITY_TYPE] with ID {id} was not found");
            }

            await realm.WriteAsync(() =>
            {
                realm.Remove(entity);
            });

            _logService.TrackEvent("[ENTITY_TYPE]Deleted", new Dictionary<string, object>
            {
                { "EntityId", id }
            });

            return true;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "DeleteAsync" },
                { "EntityId", id },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to delete [ENTITY_TYPE] from database");
        }
    }

    /// <summary>
    /// Delete entity
    /// </summary>
    public async Task<ErrorOr<bool>> DeleteAsync([ENTITY_TYPE] entity)
    {
        if (entity == null)
        {
            return Error.Validation(
                code: "[ENTITY_TYPE].NullEntity",
                description: "[ENTITY_TYPE] cannot be null");
        }

        return await DeleteAsync(entity.Id);
    }

    /// <summary>
    /// Check if entity exists
    /// </summary>
    public async Task<ErrorOr<bool>> ExistsAsync(int id)
    {
        try
        {
            using var realm = Realm.GetInstance();
            
            var exists = realm.Find<[ENTITY_TYPE]>(id) != null;
            return exists;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "ExistsAsync" },
                { "EntityId", id },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to check [ENTITY_TYPE] existence in database");
        }
    }

    /// <summary>
    /// Get count of entities
    /// </summary>
    public async Task<ErrorOr<int>> GetCountAsync()
    {
        try
        {
            using var realm = Realm.GetInstance();
            
            var count = realm.All<[ENTITY_TYPE]>().Count();
            return count;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetCountAsync" },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to get [ENTITY_TYPE] count from database");
        }
    }

    /// <summary>
    /// Get entities with pagination
    /// </summary>
    public async Task<ErrorOr<IList<[ENTITY_TYPE]>>> GetPagedAsync(int skip, int take)
    {
        try
        {
            if (skip < 0)
            {
                return Error.Validation(
                    code: "[ENTITY_TYPE].InvalidSkip",
                    description: "Skip value cannot be negative");
            }

            if (take <= 0)
            {
                return Error.Validation(
                    code: "[ENTITY_TYPE].InvalidTake",
                    description: "Take value must be greater than zero");
            }

            using var realm = Realm.GetInstance();
            
            var entities = realm.All<[ENTITY_TYPE]>()
                .Skip(skip)
                .Take(take)
                .ToList()
                .Select(e => e.Detach())
                .ToList();

            return entities;
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "GetPagedAsync" },
                { "Skip", skip },
                { "Take", take },
                { "Repository", nameof([ENTITY_TYPE]Repository) }
            });

            return Error.Failure(
                code: "[ENTITY_TYPE].DatabaseError",
                description: "Failed to retrieve paged [ENTITY_TYPE] entities from database");
        }
    }
}

/// <summary>
/// Extension methods for Realm objects
/// </summary>
public static class [ENTITY_TYPE]Extensions
{
    /// <summary>
    /// Create a detached copy of the entity for use outside of Realm context
    /// </summary>
    public static [ENTITY_TYPE] Detach(this [ENTITY_TYPE] entity)
    {
        if (entity == null) return null;

        return new [ENTITY_TYPE]
        {
            Id = entity.Id,
            // Copy other properties as needed
            // Property = entity.Property,
        };
    }
}
