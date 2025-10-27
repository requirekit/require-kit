# SOURCE: maui-appshell template (shared)
using {{ProjectName}}.DatabaseServices;
using {{ProjectName}}.Entities;
using {{ProjectName}}.Services.Interfaces;
using ErrorOr;
using Realms;

namespace {{ProjectName}}.UnitTests.DatabaseServices;

/// <summary>
/// Unit tests for [ENTITY_TYPE]Repository
/// Tests focus on data access patterns and error handling
/// Note: These tests use an in-memory Realm database for isolation
/// </summary>
public class [ENTITY_TYPE]RepositoryTests : IDisposable
{
    private readonly Realm _realm;
    private readonly Mock<ILogService> _mockLogService;
    private readonly [ENTITY_TYPE]Repository _repository;

    public [ENTITY_TYPE]RepositoryTests()
    {
        // Create in-memory Realm for testing
        var config = new RealmConfiguration($"test_{Guid.NewGuid()}.realm")
        {
            IsReadOnly = false,
            ShouldDeleteIfMigrationNeeded = true
        };
        
        _realm = Realm.GetInstance(config);
        _mockLogService = new Mock<ILogService>();
        _repository = new [ENTITY_TYPE]Repository(_mockLogService.Object);
    }

    public void Dispose()
    {
        _realm?.Dispose();
    }

    [Fact]
    public async Task GetByIdAsync_WithExistingEntity_ShouldReturnEntity()
    {
        // Arrange
        var entity = new [ENTITY_TYPE] { Id = 1, Name = "Test Entity" };
        await _realm.WriteAsync(() => _realm.Add(entity));

        // Act
        var result = await _repository.GetByIdAsync(1);

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(entity.Id, result.Value.Id);
        Assert.Equal(entity.Name, result.Value.Name);
    }

    [Fact]
    public async Task GetByIdAsync_WithNonExistentEntity_ShouldReturnNotFoundError()
    {
        // Act
        var result = await _repository.GetByIdAsync(999);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.NotFound, result.FirstError.Type);
        Assert.Equal("[ENTITY_TYPE].NotFound", result.FirstError.Code);
        Assert.Contains("999", result.FirstError.Description);
    }

    [Fact]
    public async Task GetAllAsync_WithMultipleEntities_ShouldReturnAllEntities()
    {
        // Arrange
        var entities = new[]
        {
            new [ENTITY_TYPE] { Id = 1, Name = "Entity 1" },
            new [ENTITY_TYPE] { Id = 2, Name = "Entity 2" },
            new [ENTITY_TYPE] { Id = 3, Name = "Entity 3" }
        };

        await _realm.WriteAsync(() =>
        {
            foreach (var entity in entities)
                _realm.Add(entity);
        });

        // Act
        var result = await _repository.GetAllAsync();

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(3, result.Value.Count);
        Assert.Contains(result.Value, e => e.Name == "Entity 1");
        Assert.Contains(result.Value, e => e.Name == "Entity 2");
        Assert.Contains(result.Value, e => e.Name == "Entity 3");
    }

    [Fact]
    public async Task GetAllAsync_WithNoEntities_ShouldReturnEmptyList()
    {
        // Act
        var result = await _repository.GetAllAsync();

        // Assert
        Assert.True(result.IsError == false);
        Assert.Empty(result.Value);
    }

    [Fact]
    public async Task InsertAsync_WithValidEntity_ShouldInsertSuccessfully()
    {
        // Arrange
        var entity = new [ENTITY_TYPE] { Id = 1, Name = "New Entity" };

        // Act
        var result = await _repository.InsertAsync(entity);

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(entity.Id, result.Value.Id);
        Assert.Equal(entity.Name, result.Value.Name);

        // Verify entity exists in database
        var storedEntity = _realm.Find<[ENTITY_TYPE]>(1);
        Assert.NotNull(storedEntity);
        Assert.Equal("New Entity", storedEntity.Name);

        _mockLogService.Verify(x => x.TrackEvent("[ENTITY_TYPE]Inserted", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task InsertAsync_WithNullEntity_ShouldReturnValidationError()
    {
        // Act
        var result = await _repository.InsertAsync(null);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
        Assert.Equal("[ENTITY_TYPE].NullEntity", result.FirstError.Code);
    }

    [Fact]
    public async Task UpdateAsync_WithExistingEntity_ShouldUpdateSuccessfully()
    {
        // Arrange
        var originalEntity = new [ENTITY_TYPE] { Id = 1, Name = "Original Name" };
        await _realm.WriteAsync(() => _realm.Add(originalEntity));

        var updatedEntity = new [ENTITY_TYPE] { Id = 1, Name = "Updated Name" };

        // Act
        var result = await _repository.UpdateAsync(updatedEntity);

        // Assert
        Assert.True(result.IsError == false);
        Assert.True(result.Value);

        // Verify entity was updated
        var storedEntity = _realm.Find<[ENTITY_TYPE]>(1);
        Assert.NotNull(storedEntity);
        Assert.Equal("Updated Name", storedEntity.Name);

        _mockLogService.Verify(x => x.TrackEvent("[ENTITY_TYPE]Updated", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task UpdateAsync_WithNonExistentEntity_ShouldReturnNotFoundError()
    {
        // Arrange
        var entity = new [ENTITY_TYPE] { Id = 999, Name = "Non-existent" };

        // Act
        var result = await _repository.UpdateAsync(entity);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.NotFound, result.FirstError.Type);
        Assert.Equal("[ENTITY_TYPE].NotFound", result.FirstError.Code);
    }

    [Fact]
    public async Task UpdateAsync_WithNullEntity_ShouldReturnValidationError()
    {
        // Act
        var result = await _repository.UpdateAsync(null);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
        Assert.Equal("[ENTITY_TYPE].NullEntity", result.FirstError.Code);
    }

    [Fact]
    public async Task DeleteAsync_WithExistingEntity_ShouldDeleteSuccessfully()
    {
        // Arrange
        var entity = new [ENTITY_TYPE] { Id = 1, Name = "To Delete" };
        await _realm.WriteAsync(() => _realm.Add(entity));

        // Act
        var result = await _repository.DeleteAsync(1);

        // Assert
        Assert.True(result.IsError == false);
        Assert.True(result.Value);

        // Verify entity was deleted
        var deletedEntity = _realm.Find<[ENTITY_TYPE]>(1);
        Assert.Null(deletedEntity);

        _mockLogService.Verify(x => x.TrackEvent("[ENTITY_TYPE]Deleted", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task DeleteAsync_WithNonExistentEntity_ShouldReturnNotFoundError()
    {
        // Act
        var result = await _repository.DeleteAsync(999);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.NotFound, result.FirstError.Type);
        Assert.Equal("[ENTITY_TYPE].NotFound", result.FirstError.Code);
    }

    [Fact]
    public async Task ExistsAsync_WithExistingEntity_ShouldReturnTrue()
    {
        // Arrange
        var entity = new [ENTITY_TYPE] { Id = 1, Name = "Existing Entity" };
        await _realm.WriteAsync(() => _realm.Add(entity));

        // Act
        var result = await _repository.ExistsAsync(1);

        // Assert
        Assert.True(result.IsError == false);
        Assert.True(result.Value);
    }

    [Fact]
    public async Task ExistsAsync_WithNonExistentEntity_ShouldReturnFalse()
    {
        // Act
        var result = await _repository.ExistsAsync(999);

        // Assert
        Assert.True(result.IsError == false);
        Assert.False(result.Value);
    }

    [Fact]
    public async Task GetCountAsync_WithMultipleEntities_ShouldReturnCorrectCount()
    {
        // Arrange
        var entities = new[]
        {
            new [ENTITY_TYPE] { Id = 1, Name = "Entity 1" },
            new [ENTITY_TYPE] { Id = 2, Name = "Entity 2" },
            new [ENTITY_TYPE] { Id = 3, Name = "Entity 3" }
        };

        await _realm.WriteAsync(() =>
        {
            foreach (var entity in entities)
                _realm.Add(entity);
        });

        // Act
        var result = await _repository.GetCountAsync();

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(3, result.Value);
    }

    [Fact]
    public async Task GetCountAsync_WithNoEntities_ShouldReturnZero()
    {
        // Act
        var result = await _repository.GetCountAsync();

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(0, result.Value);
    }

    [Fact]
    public async Task GetPagedAsync_WithValidParameters_ShouldReturnCorrectPage()
    {
        // Arrange
        var entities = Enumerable.Range(1, 10)
            .Select(i => new [ENTITY_TYPE] { Id = i, Name = $"Entity {i}" })
            .ToArray();

        await _realm.WriteAsync(() =>
        {
            foreach (var entity in entities)
                _realm.Add(entity);
        });

        // Act
        var result = await _repository.GetPagedAsync(skip: 2, take: 3);

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(3, result.Value.Count);
        
        // Should get entities 3, 4, 5 (0-based indexing: skip 2, take 3)
        Assert.Contains(result.Value, e => e.Id == 3);
        Assert.Contains(result.Value, e => e.Id == 4);
        Assert.Contains(result.Value, e => e.Id == 5);
    }

    [Theory]
    [InlineData(-1, 5)]
    [InlineData(0, 0)]
    [InlineData(0, -1)]
    public async Task GetPagedAsync_WithInvalidParameters_ShouldReturnValidationError(int skip, int take)
    {
        // Act
        var result = await _repository.GetPagedAsync(skip, take);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
    }

    [Fact]
    public async Task GetWhereAsync_WithPredicate_ShouldReturnFilteredEntities()
    {
        // Arrange
        var entities = new[]
        {
            new [ENTITY_TYPE] { Id = 1, Name = "Active Entity", IsActive = true },
            new [ENTITY_TYPE] { Id = 2, Name = "Inactive Entity", IsActive = false },
            new [ENTITY_TYPE] { Id = 3, Name = "Another Active", IsActive = true }
        };

        await _realm.WriteAsync(() =>
        {
            foreach (var entity in entities)
                _realm.Add(entity);
        });

        // Act
        var result = await _repository.GetWhereAsync(e => e.IsActive);

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(2, result.Value.Count);
        Assert.All(result.Value, e => Assert.True(e.IsActive));
    }
}
