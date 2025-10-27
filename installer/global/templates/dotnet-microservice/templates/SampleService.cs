using {ServiceName}.API.Domain;
using {ServiceName}.API.Domain.Entities;
using {ServiceName}.API.Models.Dtos;
using {ServiceName}.API.Models.Responses;
using {ServiceName}.API.Repositories.Interfaces;
using LanguageExt;
using static LanguageExt.Prelude;

namespace {ServiceName}.API.Services.Interfaces;

/// <summary>
/// Service interface for {Feature} operations
/// </summary>
public interface I{Feature}Service
{
    /// <summary>
    /// Get a {Feature} by ID
    /// </summary>
    Task<Either<BaseError, {Feature}Response>> Get{Feature}Async(Guid id, CancellationToken ct);
    
    /// <summary>
    /// Get all {Feature}s with optional filtering
    /// </summary>
    Task<Either<BaseError, List<{Feature}Response>>> GetAll{Feature}sAsync(CancellationToken ct);
    
    /// <summary>
    /// Create a new {Feature}
    /// </summary>
    Task<Either<BaseError, {Feature}Response>> Create{Feature}Async(Create{Feature}Dto dto, CancellationToken ct);
    
    /// <summary>
    /// Update an existing {Feature}
    /// </summary>
    Task<Either<BaseError, {Feature}Response>> Update{Feature}Async(Guid id, Update{Feature}Dto dto, CancellationToken ct);
    
    /// <summary>
    /// Delete a {Feature}
    /// </summary>
    Task<Either<BaseError, Unit>> Delete{Feature}Async(Guid id, CancellationToken ct);
}

namespace {ServiceName}.API.Services.Implementations;

/// <summary>
/// Service implementation for {Feature} operations using functional error handling
/// </summary>
public class {Feature}Service : I{Feature}Service
{
    private readonly I{Feature}Repository _repository;
    private readonly ILogger<{Feature}Service> _logger;
    
    public {Feature}Service(
        I{Feature}Repository repository, 
        ILogger<{Feature}Service> logger)
    {
        _repository = repository;
        _logger = logger;
    }
    
    public async Task<Either<BaseError, {Feature}Response>> Get{Feature}Async(Guid id, CancellationToken ct)
    {
        return await TryAsync(async () =>
        {
            _logger.LogDebug("Retrieving {Feature} with ID: {Id}", id);
            
            var entity = await _repository.GetByIdAsync(id, ct);
            
            if (entity == null)
            {
                _logger.LogWarning("{Feature} with ID {Id} not found", id);
                return Left<BaseError, {Feature}Response>(
                    new NotFoundError($"{Feature} with ID {id} not found", "{Feature}", id.ToString()));
            }
            
            var response = MapToResponse(entity);
            _logger.LogDebug("Successfully retrieved {Feature} with ID: {Id}", id);
            
            return Right<BaseError, {Feature}Response>(response);
        })
        .IfFail(ex =>
        {
            _logger.LogError(ex, "Error retrieving {Feature} with ID {Id}", id);
            return Left<BaseError, {Feature}Response>(
                new ServiceError($"Failed to retrieve {Feature}: {ex.Message}", ex));
        });
    }
    
    public async Task<Either<BaseError, List<{Feature}Response>>> GetAll{Feature}sAsync(CancellationToken ct)
    {
        return await TryAsync(async () =>
        {
            _logger.LogDebug("Retrieving all {Feature}s");
            
            var entities = await _repository.GetAllAsync(ct);
            var responses = entities.Select(MapToResponse).ToList();
            
            _logger.LogDebug("Successfully retrieved {Count} {Feature}s", responses.Count);
            
            return Right<BaseError, List<{Feature}Response>>(responses);
        })
        .IfFail(ex =>
        {
            _logger.LogError(ex, "Error retrieving all {Feature}s");
            return Left<BaseError, List<{Feature}Response>>(
                new ServiceError($"Failed to retrieve {Feature}s: {ex.Message}", ex));
        });
    }
    
    public async Task<Either<BaseError, {Feature}Response>> Create{Feature}Async(Create{Feature}Dto dto, CancellationToken ct)
    {
        return await TryAsync(async () =>
        {
            _logger.LogDebug("Creating new {Feature} with name: {Name}", dto.Name);
            
            // Check for duplicate name
            var existing = await _repository.GetByNameAsync(dto.Name, ct);
            if (existing != null)
            {
                _logger.LogWarning("Attempted to create {Feature} with duplicate name: {Name}", dto.Name);
                return Left<BaseError, {Feature}Response>(
                    new ConflictError($"A {Feature} with name '{dto.Name}' already exists", dto.Name));
            }
            
            // Create entity
            var entity = new {Feature}
            {
                Id = Guid.NewGuid(),
                Name = dto.Name,
                Description = dto.Description,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            
            // Validate business rules
            var validationResult = ValidateBusinessRules(entity);
            if (validationResult.IsLeft)
            {
                return validationResult.Map(_ => default({Feature}Response)!);
            }
            
            // Save to repository
            var created = await _repository.CreateAsync(entity, ct);
            var response = MapToResponse(created);
            
            _logger.LogInformation("Successfully created {Feature} with ID: {Id}", created.Id);
            
            return Right<BaseError, {Feature}Response>(response);
        })
        .IfFail(ex =>
        {
            _logger.LogError(ex, "Error creating {Feature}");
            return Left<BaseError, {Feature}Response>(
                new ServiceError($"Failed to create {Feature}: {ex.Message}", ex));
        });
    }
    
    public async Task<Either<BaseError, {Feature}Response>> Update{Feature}Async(Guid id, Update{Feature}Dto dto, CancellationToken ct)
    {
        return await TryAsync(async () =>
        {
            _logger.LogDebug("Updating {Feature} with ID: {Id}", id);
            
            var entity = await _repository.GetByIdAsync(id, ct);
            
            if (entity == null)
            {
                _logger.LogWarning("{Feature} with ID {Id} not found for update", id);
                return Left<BaseError, {Feature}Response>(
                    new NotFoundError($"{Feature} with ID {id} not found", "{Feature}", id.ToString()));
            }
            
            // Check for duplicate name if name is being changed
            if (dto.Name != entity.Name)
            {
                var existing = await _repository.GetByNameAsync(dto.Name, ct);
                if (existing != null && existing.Id != id)
                {
                    _logger.LogWarning("Attempted to update {Feature} with duplicate name: {Name}", dto.Name);
                    return Left<BaseError, {Feature}Response>(
                        new ConflictError($"A {Feature} with name '{dto.Name}' already exists", dto.Name));
                }
            }
            
            // Update entity
            entity.Name = dto.Name;
            entity.Description = dto.Description;
            entity.UpdatedAt = DateTime.UtcNow;
            
            // Validate business rules
            var validationResult = ValidateBusinessRules(entity);
            if (validationResult.IsLeft)
            {
                return validationResult.Map(_ => default({Feature}Response)!);
            }
            
            // Save to repository
            var updated = await _repository.UpdateAsync(entity, ct);
            var response = MapToResponse(updated);
            
            _logger.LogInformation("Successfully updated {Feature} with ID: {Id}", id);
            
            return Right<BaseError, {Feature}Response>(response);
        })
        .IfFail(ex =>
        {
            _logger.LogError(ex, "Error updating {Feature} with ID {Id}", id);
            return Left<BaseError, {Feature}Response>(
                new ServiceError($"Failed to update {Feature}: {ex.Message}", ex));
        });
    }
    
    public async Task<Either<BaseError, Unit>> Delete{Feature}Async(Guid id, CancellationToken ct)
    {
        return await TryAsync(async () =>
        {
            _logger.LogDebug("Deleting {Feature} with ID: {Id}", id);
            
            var entity = await _repository.GetByIdAsync(id, ct);
            
            if (entity == null)
            {
                _logger.LogWarning("{Feature} with ID {Id} not found for deletion", id);
                return Left<BaseError, Unit>(
                    new NotFoundError($"{Feature} with ID {id} not found", "{Feature}", id.ToString()));
            }
            
            // Check if can be deleted (e.g., no dependent records)
            var canDelete = await CanDelete{Feature}(entity, ct);
            if (canDelete.IsLeft)
            {
                return canDelete;
            }
            
            await _repository.DeleteAsync(id, ct);
            
            _logger.LogInformation("Successfully deleted {Feature} with ID: {Id}", id);
            
            return Right<BaseError, Unit>(Unit.Default);
        })
        .IfFail(ex =>
        {
            _logger.LogError(ex, "Error deleting {Feature} with ID {Id}", id);
            return Left<BaseError, Unit>(
                new ServiceError($"Failed to delete {Feature}: {ex.Message}", ex));
        });
    }
    
    /// <summary>
    /// Validate business rules for a {Feature}
    /// </summary>
    private Either<BaseError, Unit> ValidateBusinessRules({Feature} entity)
    {
        var errors = new Dictionary<string, string[]>();
        
        if (string.IsNullOrWhiteSpace(entity.Name))
        {
            errors["Name"] = new[] { "Name is required" };
        }
        else if (entity.Name.Length > 100)
        {
            errors["Name"] = new[] { "Name must not exceed 100 characters" };
        }
        
        if (!string.IsNullOrEmpty(entity.Description) && entity.Description.Length > 500)
        {
            errors["Description"] = new[] { "Description must not exceed 500 characters" };
        }
        
        if (errors.Any())
        {
            return Left<BaseError, Unit>(
                new ValidationError("Validation failed", errors));
        }
        
        return Right<BaseError, Unit>(Unit.Default);
    }
    
    /// <summary>
    /// Check if a {Feature} can be deleted
    /// </summary>
    private async Task<Either<BaseError, Unit>> CanDelete{Feature}({Feature} entity, CancellationToken ct)
    {
        // TODO: Add checks for dependent records
        // Example: Check if there are related records that would be orphaned
        
        return await Task.FromResult(Right<BaseError, Unit>(Unit.Default));
    }
    
    /// <summary>
    /// Map entity to response DTO
    /// </summary>
    private {Feature}Response MapToResponse({Feature} entity)
    {
        return new {Feature}Response
        {
            Id = entity.Id,
            Name = entity.Name,
            Description = entity.Description,
            CreatedAt = entity.CreatedAt,
            UpdatedAt = entity.UpdatedAt
        };
    }
}
