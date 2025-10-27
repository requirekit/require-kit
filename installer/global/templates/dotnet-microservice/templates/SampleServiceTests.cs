using {ServiceName}.API.Domain;
using {ServiceName}.API.Domain.Entities;
using {ServiceName}.API.Models.Dtos;
using {ServiceName}.API.Repositories.Interfaces;
using {ServiceName}.API.Services.Implementations;
using FluentAssertions;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace {ServiceName}.Tests.Unit.Services;

public class {Feature}ServiceTests
{
    private readonly Mock<I{Feature}Repository> _repositoryMock;
    private readonly Mock<ILogger<{Feature}Service>> _loggerMock;
    private readonly {Feature}Service _service;
    
    public {Feature}ServiceTests()
    {
        _repositoryMock = new Mock<I{Feature}Repository>();
        _loggerMock = new Mock<ILogger<{Feature}Service>>();
        _service = new {Feature}Service(_repositoryMock.Object, _loggerMock.Object);
    }
    
    [Fact]
    public async Task Get{Feature}_WhenExists_ReturnsRight()
    {
        // Arrange
        var id = Guid.NewGuid();
        var expected = new {Feature}
        {
            Id = id,
            Name = "Test {Feature}",
            Description = "Test Description",
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };
        
        _repositoryMock
            .Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(expected);
        
        // Act
        var result = await _service.Get{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsRight.Should().BeTrue();
        result.IfRight(response =>
        {
            response.Id.Should().Be(expected.Id);
            response.Name.Should().Be(expected.Name);
            response.Description.Should().Be(expected.Description);
        });
        
        _repositoryMock.Verify(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()), Times.Once);
    }
    
    [Fact]
    public async Task Get{Feature}_WhenNotFound_ReturnsNotFoundError()
    {
        // Arrange
        var id = Guid.NewGuid();
        _repositoryMock
            .Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(({Feature})null);
        
        // Act
        var result = await _service.Get{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsLeft.Should().BeTrue();
        result.IfLeft(error =>
        {
            error.Should().BeOfType<NotFoundError>();
            error.StatusCode.Should().Be(404);
            error.Message.Should().Contain(id.ToString());
        });
    }
    
    [Fact]
    public async Task Get{Feature}_WhenRepositoryThrows_ReturnsServiceError()
    {
        // Arrange
        var id = Guid.NewGuid();
        var exception = new Exception("Database connection failed");
        
        _repositoryMock
            .Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ThrowsAsync(exception);
        
        // Act
        var result = await _service.Get{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsLeft.Should().BeTrue();
        result.IfLeft(error =>
        {
            error.Should().BeOfType<ServiceError>();
            error.StatusCode.Should().Be(500);
            error.Message.Should().Contain("Database connection failed");
        });
    }
    
    [Fact]
    public async Task Create{Feature}_WithValidData_ReturnsRight()
    {
        // Arrange
        var dto = new Create{Feature}Dto
        {
            Name = "New {Feature}",
            Description = "New Description"
        };
        
        _repositoryMock
            .Setup(x => x.GetByNameAsync(dto.Name, It.IsAny<CancellationToken>()))
            .ReturnsAsync(({Feature})null);
        
        _repositoryMock
            .Setup(x => x.CreateAsync(It.IsAny<{Feature}>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((Feature entity, CancellationToken ct) => entity);
        
        // Act
        var result = await _service.Create{Feature}Async(dto, CancellationToken.None);
        
        // Assert
        result.IsRight.Should().BeTrue();
        result.IfRight(response =>
        {
            response.Name.Should().Be(dto.Name);
            response.Description.Should().Be(dto.Description);
            response.Id.Should().NotBeEmpty();
        });
        
        _repositoryMock.Verify(x => x.CreateAsync(It.IsAny<{Feature}>(), It.IsAny<CancellationToken>()), Times.Once);
    }
    
    [Fact]
    public async Task Create{Feature}_WithDuplicateName_ReturnsConflictError()
    {
        // Arrange
        var dto = new Create{Feature}Dto
        {
            Name = "Existing {Feature}",
            Description = "Description"
        };
        
        var existing = new {Feature}
        {
            Id = Guid.NewGuid(),
            Name = dto.Name
        };
        
        _repositoryMock
            .Setup(x => x.GetByNameAsync(dto.Name, It.IsAny<CancellationToken>()))
            .ReturnsAsync(existing);
        
        // Act
        var result = await _service.Create{Feature}Async(dto, CancellationToken.None);
        
        // Assert
        result.IsLeft.Should().BeTrue();
        result.IfLeft(error =>
        {
            error.Should().BeOfType<ConflictError>();
            error.StatusCode.Should().Be(409);
            error.Message.Should().Contain(dto.Name);
        });
        
        _repositoryMock.Verify(x => x.CreateAsync(It.IsAny<{Feature}>(), It.IsAny<CancellationToken>()), Times.Never);
    }
    
    [Fact]
    public async Task Update{Feature}_WhenExists_ReturnsRight()
    {
        // Arrange
        var id = Guid.NewGuid();
        var dto = new Update{Feature}Dto
        {
            Name = "Updated {Feature}",
            Description = "Updated Description"
        };
        
        var existing = new {Feature}
        {
            Id = id,
            Name = "Original {Feature}",
            Description = "Original Description",
            CreatedAt = DateTime.UtcNow.AddDays(-1),
            UpdatedAt = DateTime.UtcNow.AddDays(-1)
        };
        
        _repositoryMock
            .Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(existing);
        
        _repositoryMock
            .Setup(x => x.GetByNameAsync(dto.Name, It.IsAny<CancellationToken>()))
            .ReturnsAsync(({Feature})null);
        
        _repositoryMock
            .Setup(x => x.UpdateAsync(It.IsAny<{Feature}>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((Feature entity, CancellationToken ct) => entity);
        
        // Act
        var result = await _service.Update{Feature}Async(id, dto, CancellationToken.None);
        
        // Assert
        result.IsRight.Should().BeTrue();
        result.IfRight(response =>
        {
            response.Id.Should().Be(id);
            response.Name.Should().Be(dto.Name);
            response.Description.Should().Be(dto.Description);
        });
        
        _repositoryMock.Verify(x => x.UpdateAsync(It.IsAny<{Feature}>(), It.IsAny<CancellationToken>()), Times.Once);
    }
    
    [Fact]
    public async Task Delete{Feature}_WhenExists_ReturnsRight()
    {
        // Arrange
        var id = Guid.NewGuid();
        var existing = new {Feature}
        {
            Id = id,
            Name = "Test {Feature}"
        };
        
        _repositoryMock
            .Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(existing);
        
        _repositoryMock
            .Setup(x => x.DeleteAsync(id, It.IsAny<CancellationToken>()))
            .Returns(Task.CompletedTask);
        
        // Act
        var result = await _service.Delete{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsRight.Should().BeTrue();
        _repositoryMock.Verify(x => x.DeleteAsync(id, It.IsAny<CancellationToken>()), Times.Once);
    }
    
    [Fact]
    public async Task Delete{Feature}_WhenNotFound_ReturnsNotFoundError()
    {
        // Arrange
        var id = Guid.NewGuid();
        _repositoryMock
            .Setup(x => x.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(({Feature})null);
        
        // Act
        var result = await _service.Delete{Feature}Async(id, CancellationToken.None);
        
        // Assert
        result.IsLeft.Should().BeTrue();
        result.IfLeft(error =>
        {
            error.Should().BeOfType<NotFoundError>();
            error.StatusCode.Should().Be(404);
        });
        
        _repositoryMock.Verify(x => x.DeleteAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>()), Times.Never);
    }
}
