# SOURCE: maui-appshell template (shared)
using {{ProjectName}}.Services;
using {{ProjectName}}.Services.Interfaces;
using ErrorOr;
using System.Net;

namespace {{ProjectName}}.UnitTests.Services;

/// <summary>
/// Unit tests for [SERVICE_NAME]Service
/// Tests focus on service behavior, HTTP interactions, and error handling
/// </summary>
public class [SERVICE_NAME]ServiceTests : IDisposable
{
    private readonly Mock<ILogService> _mockLogService;
    private readonly Mock<HttpMessageHandler> _mockHttpMessageHandler;
    private readonly HttpClient _httpClient;
    private readonly [SERVICE_NAME]Service _service;

    public [SERVICE_NAME]ServiceTests()
    {
        _mockLogService = new Mock<ILogService>();
        _mockHttpMessageHandler = new Mock<HttpMessageHandler>();
        
        _httpClient = new HttpClient(_mockHttpMessageHandler.Object)
        {
            BaseAddress = new Uri("https://api.example.com/")
        };
        
        _service = new [SERVICE_NAME]Service(_mockLogService.Object, _httpClient);
    }

    public void Dispose()
    {
        _httpClient?.Dispose();
    }

    [Fact]
    public async Task GetDataAsync_WithValidParameter_ShouldReturnData()
    {
        // Arrange
        var parameter = "test-parameter";
        var expectedContent = "test-response-data";
        
        SetupHttpResponse(HttpStatusCode.OK, expectedContent);

        // Act
        var result = await _service.GetDataAsync(parameter);

        // Assert
        Assert.True(result.IsError == false);
        Assert.Equal(expectedContent, result.Value);
        
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]GetDataStarted", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]GetDataCompleted", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public async Task GetDataAsync_WithInvalidParameter_ShouldReturnValidationError(string invalidParameter)
    {
        // Act
        var result = await _service.GetDataAsync(invalidParameter);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].InvalidParameter", result.FirstError.Code);
        
        // Should not make HTTP call
        _mockHttpMessageHandler.Verify();
    }

    [Theory]
    [InlineData(HttpStatusCode.BadRequest)]
    [InlineData(HttpStatusCode.Unauthorized)]
    [InlineData(HttpStatusCode.NotFound)]
    [InlineData(HttpStatusCode.InternalServerError)]
    public async Task GetDataAsync_WithHttpError_ShouldReturnFailureError(HttpStatusCode statusCode)
    {
        // Arrange
        SetupHttpResponse(statusCode, "Error response");

        // Act
        var result = await _service.GetDataAsync("test");

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Failure, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].HttpError", result.FirstError.Code);
        Assert.Contains(statusCode.ToString(), result.FirstError.Description);
    }

    [Fact]
    public async Task GetDataAsync_WithHttpRequestException_ShouldReturnNetworkError()
    {
        // Arrange
        _mockHttpMessageHandler.Setup()
            .ThrowsAsync(new HttpRequestException("Network error"));

        // Act
        var result = await _service.GetDataAsync("test");

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Failure, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].NetworkError", result.FirstError.Code);
        
        _mockLogService.Verify(x => x.TrackError(
            It.IsAny<HttpRequestException>(), 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task GetDataAsync_WithTimeout_ShouldReturnTimeoutError()
    {
        // Arrange
        _mockHttpMessageHandler.Setup()
            .ThrowsAsync(new TaskCanceledException("Request timed out"));

        // Act
        var result = await _service.GetDataAsync("test");

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Failure, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].Timeout", result.FirstError.Code);
        
        _mockLogService.Verify(x => x.TrackError(
            It.IsAny<TaskCanceledException>(), 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task ProcessDataAsync_WithValidData_ShouldReturnSuccess()
    {
        // Arrange
        var testData = "valid-data-string";

        // Act
        var result = await _service.ProcessDataAsync(testData);

        // Assert
        Assert.True(result.IsError == false);
        Assert.True(result.Value);
        
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]ProcessDataStarted"), Times.Once);
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]ProcessDataCompleted"), Times.Once);
    }

    [Fact]
    public async Task ProcessDataAsync_WithNullData_ShouldReturnValidationError()
    {
        // Act
        var result = await _service.ProcessDataAsync(null);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].NullData", result.FirstError.Code);
    }

    [Fact]
    public async Task ProcessDataAsync_WithShortData_ShouldReturnValidationError()
    {
        // Arrange
        var shortData = "123"; // Less than 5 characters

        // Act
        var result = await _service.ProcessDataAsync(shortData);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].InvalidDataLength", result.FirstError.Code);
    }

    [Fact]
    public void ValidateData_WithValidString_ShouldReturnSuccess()
    {
        // Arrange
        var validData = "valid123";

        // Act
        var result = _service.ValidateData(validData);

        // Assert
        Assert.True(result.IsError == false);
        Assert.True(result.Value);
        
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]ValidateDataStarted"), Times.Once);
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]ValidateDataCompleted", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void ValidateData_WithNullOrEmpty_ShouldReturnValidationError(string invalidData)
    {
        // Act
        var result = _service.ValidateData(invalidData);

        // Assert
        Assert.True(result.IsError);
        Assert.Equal(ErrorType.Validation, result.FirstError.Type);
        Assert.Equal("[SERVICE_NAME].EmptyValue", result.FirstError.Code);
    }

    [Fact]
    public void ValidateData_WithTooShortString_ShouldReturnValidationError()
    {
        // Arrange
        var shortData = "ab"; // Less than 3 characters

        // Act
        var result = _service.ValidateData(shortData);

        // Assert
        Assert.True(result.IsError);
        Assert.Contains(result.Errors, e => e.Code == "[SERVICE_NAME].TooShort");
    }

    [Fact]
    public void ValidateData_WithTooLongString_ShouldReturnValidationError()
    {
        // Arrange
        var longData = new string('a', 101); // More than 100 characters

        // Act
        var result = _service.ValidateData(longData);

        // Assert
        Assert.True(result.IsError);
        Assert.Contains(result.Errors, e => e.Code == "[SERVICE_NAME].TooLong");
    }

    [Fact]
    public void ValidateData_WithInvalidCharacters_ShouldReturnValidationError()
    {
        // Arrange
        var invalidData = "test@123"; // Contains special character

        // Act
        var result = _service.ValidateData(invalidData);

        // Assert
        Assert.True(result.IsError);
        Assert.Contains(result.Errors, e => e.Code == "[SERVICE_NAME].InvalidCharacters");
    }

    [Fact]
    public void ValidateData_WithMultipleErrors_ShouldReturnAllErrors()
    {
        // Arrange
        var invalidData = "a@"; // Too short AND has invalid characters

        // Act
        var result = _service.ValidateData(invalidData);

        // Assert
        Assert.True(result.IsError);
        Assert.True(result.Errors.Count >= 2);
        Assert.Contains(result.Errors, e => e.Code == "[SERVICE_NAME].TooShort");
        Assert.Contains(result.Errors, e => e.Code == "[SERVICE_NAME].InvalidCharacters");
    }

    [Fact]
    public async Task GetConfigurationAsync_ShouldReturnConfiguration()
    {
        // Act
        var result = await _service.GetConfigurationAsync();

        // Assert
        Assert.True(result.IsError == false);
        Assert.NotEmpty(result.Value);
        Assert.Contains("Setting1", result.Value.Keys);
        Assert.Contains("Setting2", result.Value.Keys);
        Assert.Contains("Setting3", result.Value.Keys);
        
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]GetConfigurationStarted"), Times.Once);
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]GetConfigurationCompleted", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task GetDataAsync_ShouldLogCorrectEventData()
    {
        // Arrange
        var parameter = "test-param";
        SetupHttpResponse(HttpStatusCode.OK, "response");

        // Act
        await _service.GetDataAsync(parameter);

        // Assert
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]GetDataStarted", 
            It.Is<Dictionary<string, object>>(d => 
                d.ContainsKey("Parameter") && d["Parameter"].ToString() == parameter)), Times.Once);
        
        _mockLogService.Verify(x => x.TrackEvent("[SERVICE_NAME]GetDataCompleted", 
            It.Is<Dictionary<string, object>>(d => 
                d.ContainsKey("Parameter") && 
                d.ContainsKey("ResponseLength"))), Times.Once);
    }

    private void SetupHttpResponse(HttpStatusCode statusCode, string content)
    {
        var response = new HttpResponseMessage(statusCode)
        {
            Content = new StringContent(content)
        };

        _mockHttpMessageHandler.Setup()
            .ReturnsAsync(response);
    }
}

// Extension method to make HttpMessageHandler mocking easier
public static class HttpMessageHandlerExtensions
{
    public static Mock<HttpMessageHandler> Setup(this Mock<HttpMessageHandler> mock)
    {
        return mock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>());
    }

    public static void ThrowsAsync<T>(this Mock<HttpMessageHandler> mock, T exception) where T : Exception
    {
        mock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ThrowsAsync(exception);
    }

    public static void ReturnsAsync(this Mock<HttpMessageHandler> mock, HttpResponseMessage response)
    {
        mock.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(response);
    }
}
