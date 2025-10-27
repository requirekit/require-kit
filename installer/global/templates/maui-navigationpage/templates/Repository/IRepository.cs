# SOURCE: maui-appshell template (shared)
using ErrorOr;
using {{ProjectName}}.Entities;

namespace {{ProjectName}}.DatabaseServices.Interfaces;

/// <summary>
/// Repository interface for [ENTITY_TYPE] data access
/// Repositories are renamed from DataServices and handle data persistence
/// </summary>
public interface I[ENTITY_TYPE]Repository
{
    /// <summary>
    /// Get entity by ID
    /// </summary>
    /// <param name="id">Entity identifier</param>
    /// <returns>ErrorOr containing the entity or errors</returns>
    Task<ErrorOr<[ENTITY_TYPE]>> GetByIdAsync(int id);

    /// <summary>
    /// Get all entities
    /// </summary>
    /// <returns>ErrorOr containing the list of entities or errors</returns>
    Task<ErrorOr<IList<[ENTITY_TYPE]>>> GetAllAsync();

    /// <summary>
    /// Get entities with filtering
    /// </summary>
    /// <param name="predicate">Filter predicate</param>
    /// <returns>ErrorOr containing the filtered entities or errors</returns>
    Task<ErrorOr<IList<[ENTITY_TYPE]>>> GetWhereAsync(Func<[ENTITY_TYPE], bool> predicate);

    /// <summary>
    /// Insert new entity
    /// </summary>
    /// <param name="entity">Entity to insert</param>
    /// <returns>ErrorOr containing the inserted entity or errors</returns>
    Task<ErrorOr<[ENTITY_TYPE]>> InsertAsync([ENTITY_TYPE] entity);

    /// <summary>
    /// Update existing entity
    /// </summary>
    /// <param name="entity">Entity to update</param>
    /// <returns>ErrorOr containing success result or errors</returns>
    Task<ErrorOr<bool>> UpdateAsync([ENTITY_TYPE] entity);

    /// <summary>
    /// Delete entity by ID
    /// </summary>
    /// <param name="id">Entity identifier</param>
    /// <returns>ErrorOr containing success result or errors</returns>
    Task<ErrorOr<bool>> DeleteAsync(int id);

    /// <summary>
    /// Delete entity
    /// </summary>
    /// <param name="entity">Entity to delete</param>
    /// <returns>ErrorOr containing success result or errors</returns>
    Task<ErrorOr<bool>> DeleteAsync([ENTITY_TYPE] entity);

    /// <summary>
    /// Check if entity exists
    /// </summary>
    /// <param name="id">Entity identifier</param>
    /// <returns>ErrorOr containing existence result or errors</returns>
    Task<ErrorOr<bool>> ExistsAsync(int id);

    /// <summary>
    /// Get count of entities
    /// </summary>
    /// <returns>ErrorOr containing the count or errors</returns>
    Task<ErrorOr<int>> GetCountAsync();

    /// <summary>
    /// Get entities with pagination
    /// </summary>
    /// <param name="skip">Number of entities to skip</param>
    /// <param name="take">Number of entities to take</param>
    /// <returns>ErrorOr containing the paged entities or errors</returns>
    Task<ErrorOr<IList<[ENTITY_TYPE]>>> GetPagedAsync(int skip, int take);
}
