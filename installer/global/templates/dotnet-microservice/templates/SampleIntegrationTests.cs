using {ServiceName}.API.Models.Requests;
using {ServiceName}.API.Models.Responses;
using {ServiceName}.Tests.Integration.Fixtures;
using FluentAssertions;
using Microsoft.AspNetCore.Http;
using System.Net;
using System.Net.Http.Json;
using Xunit;

namespace {ServiceName}.Tests.Integration.Endpoints;

[Collection("Api")]
public class {Feature}EndpointTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;
    private readonly HttpClient _client;
    
    public {Feature}EndpointTests(ApiFactory factory)
    {
        _factory = factory;
        _client = _factory.CreateClient();
    }
    
    [Fact]
    public async Task Get{Feature}_WhenExists_ReturnsOk()
    {
        // Arrange
        var id = Guid.Parse("11111111-1111-1111-1111-111111111111"); // Seeded data ID
        
        // Act
        var response = await _client.GetAsync($"/api/v1/{feature}/{id}");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var content = await response.Content.ReadFromJsonAsync<{Feature}Response>();
        content.Should().NotBeNull();
        content!.Id.Should().Be(id);
        content.Name.Should().Be("Sample {Feature} 1");
    }
    
    [Fact]
    public async Task Get{Feature}_WhenNotFound_Returns404()
    {
        // Arrange
        var id = Guid.NewGuid();
        
        // Act
        var response = await _client.GetAsync($"/api/v1/{feature}/{id}");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
        
        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails!.Status.Should().Be(404);
        problemDetails.Detail.Should().Contain(id.ToString());
    }
    
    [Fact]
    public async Task Create{Feature}_WithValidData_Returns201()
    {
        // Arrange
        var request = new Create{Feature}Request
        {
            Name = $"Test {Feature} {Guid.NewGuid()}",
            Description = "Test Description"
        };
        
        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/{feature}", request);
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        response.Headers.Location.Should().NotBeNull();
        
        var content = await response.Content.ReadFromJsonAsync<{Feature}Response>();
        content.Should().NotBeNull();
        content!.Name.Should().Be(request.Name);
        content.Description.Should().Be(request.Description);
        content.Id.Should().NotBeEmpty();
    }
    
    [Fact]
    public async Task Create{Feature}_WithInvalidData_Returns400()
    {
        // Arrange
        var request = new Create{Feature}Request
        {
            Name = "", // Invalid: empty name
            Description = "Test Description"
        };
        
        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/{feature}", request);
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
        
        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails!.Status.Should().Be(400);
    }
    
    [Fact]
    public async Task Create{Feature}_WithDuplicateName_Returns409()
    {
        // Arrange
        var request = new Create{Feature}Request
        {
            Name = "Sample {Feature} 1", // Duplicate name from seeded data
            Description = "Test Description"
        };
        
        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/{feature}", request);
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Conflict);
        
        var problemDetails = await response.Content.ReadFromJsonAsync<ProblemDetails>();
        problemDetails.Should().NotBeNull();
        problemDetails!.Status.Should().Be(409);
        problemDetails.Detail.Should().Contain("already exists");
    }
    
    [Fact]
    public async Task Update{Feature}_WhenExists_ReturnsOk()
    {
        // Arrange
        var id = Guid.Parse("11111111-1111-1111-1111-111111111111");
        var request = new Update{Feature}Request
        {
            Id = id,
            Name = $"Updated {Feature} {Guid.NewGuid()}",
            Description = "Updated Description"
        };
        
        // Act
        var response = await _client.PutAsJsonAsync($"/api/v1/{feature}/{id}", request);
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var content = await response.Content.ReadFromJsonAsync<{Feature}Response>();
        content.Should().NotBeNull();
        content!.Id.Should().Be(id);
        content.Name.Should().Be(request.Name);
        content.Description.Should().Be(request.Description);
    }
    
    [Fact]
    public async Task Update{Feature}_WhenNotFound_Returns404()
    {
        // Arrange
        var id = Guid.NewGuid();
        var request = new Update{Feature}Request
        {
            Id = id,
            Name = "Updated {Feature}",
            Description = "Updated Description"
        };
        
        // Act
        var response = await _client.PutAsJsonAsync($"/api/v1/{feature}/{id}", request);
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
    
    [Fact]
    public async Task Delete{Feature}_WhenExists_Returns204()
    {
        // Arrange
        // First create a {feature} to delete
        var createRequest = new Create{Feature}Request
        {
            Name = $"To Delete {Guid.NewGuid()}",
            Description = "Will be deleted"
        };
        
        var createResponse = await _client.PostAsJsonAsync("/api/v1/{feature}", createRequest);
        var created = await createResponse.Content.ReadFromJsonAsync<{Feature}Response>();
        
        // Act
        var deleteResponse = await _client.DeleteAsync($"/api/v1/{feature}/{created!.Id}");
        
        // Assert
        deleteResponse.StatusCode.Should().Be(HttpStatusCode.NoContent);
        
        // Verify it's deleted
        var getResponse = await _client.GetAsync($"/api/v1/{feature}/{created.Id}");
        getResponse.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
    
    [Fact]
    public async Task Delete{Feature}_WhenNotFound_Returns404()
    {
        // Arrange
        var id = Guid.NewGuid();
        
        // Act
        var response = await _client.DeleteAsync($"/api/v1/{feature}/{id}");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
    
    [Fact]
    public async Task GetAll{Feature}s_ReturnsOk()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/{feature}");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var content = await response.Content.ReadFromJsonAsync<List<{Feature}Response>>();
        content.Should().NotBeNull();
        content!.Should().HaveCountGreaterThan(0);
    }
}
