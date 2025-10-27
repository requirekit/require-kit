# SOURCE: maui-appshell template (shared)
using {{ProjectName}}.ViewModels;
using {{ProjectName}}.Engines;
using {{ProjectName}}.Services.Interfaces;
using Microsoft.Extensions.Logging;

namespace {{ProjectName}}.UnitTests.ViewModels;

/// <summary>
/// Unit tests for [FEATURE_NAME]ViewModel
/// Tests focus on ViewModel behavior and Engine integration using mocks
/// </summary>
public class [FEATURE_NAME]ViewModelTests
{
    private readonly Mock<[FEATURE_NAME]Engine> _mockEngine;
    private readonly Mock<INavigator> _mockNavigator;
    private readonly Mock<ILogService> _mockLogService;
    private readonly [FEATURE_NAME]ViewModel _viewModel;

    public [FEATURE_NAME]ViewModelTests()
    {
        _mockEngine = new Mock<[FEATURE_NAME]Engine>();
        _mockNavigator = new Mock<INavigator>();
        _mockLogService = new Mock<ILogService>();
        
        _viewModel = new [FEATURE_NAME]ViewModel(
            _mockNavigator.Object,
            _mockEngine.Object,
            _mockLogService.Object);
    }

    [Fact]
    public async Task OnViewAppearing_ShouldTrackEvent_AndLoadData()
    {
        // Arrange
        var expectedEntity = new [ENTITY_TYPE] { Id = 1, Name = "Test" };
        _mockEngine.Setup(x => x.Get[ENTITY_TYPE]Async(It.IsAny<int>()))
                  .ReturnsAsync(expectedEntity);

        // Act
        await _viewModel.OnViewAppearing();

        // Assert
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]ViewAppeared"), Times.Once);
        _mockEngine.Verify(x => x.Get[ENTITY_TYPE]Async(It.IsAny<int>()), Times.Once);
        
        Assert.True(_viewModel.HasData);
        Assert.Empty(_viewModel.ErrorMessage);
    }

    [Fact]
    public async Task LoadDataCommand_WithValidData_ShouldSetHasDataTrue()
    {
        // Arrange
        var expectedEntity = new [ENTITY_TYPE] { Id = 1, Name = "Test Entity" };
        _mockEngine.Setup(x => x.Get[ENTITY_TYPE]Async(It.IsAny<int>()))
                  .ReturnsAsync(expectedEntity);

        // Act
        await _viewModel.LoadDataCommand.ExecuteAsync(null);

        // Assert
        Assert.True(_viewModel.HasData);
        Assert.Empty(_viewModel.ErrorMessage);
        Assert.False(_viewModel.IsBusy);
        
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]DataLoaded"), Times.Once);
    }

    [Fact]
    public async Task LoadDataCommand_WithEngineError_ShouldSetErrorMessage()
    {
        // Arrange
        var expectedError = Error.NotFound("Entity not found");
        _mockEngine.Setup(x => x.Get[ENTITY_TYPE]Async(It.IsAny<int>()))
                  .ReturnsAsync(expectedError);

        // Act
        await _viewModel.LoadDataCommand.ExecuteAsync(null);

        // Assert
        Assert.False(_viewModel.HasData);
        Assert.Equal("Entity not found", _viewModel.ErrorMessage);
        Assert.False(_viewModel.IsBusy);
        
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]DataLoadFailed", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task LoadDataCommand_WithException_ShouldHandleGracefully()
    {
        // Arrange
        _mockEngine.Setup(x => x.Get[ENTITY_TYPE]Async(It.IsAny<int>()))
                  .ThrowsAsync(new Exception("Test exception"));

        // Act
        await _viewModel.LoadDataCommand.ExecuteAsync(null);

        // Assert
        Assert.False(_viewModel.HasData);
        Assert.Equal("An unexpected error occurred", _viewModel.ErrorMessage);
        Assert.False(_viewModel.IsBusy);
        
        _mockLogService.Verify(x => x.TrackError(
            It.IsAny<Exception>(), 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task ProcessActionCommand_WithValidEntity_ShouldSucceed()
    {
        // Arrange
        _mockEngine.Setup(x => x.Process[ENTITY_TYPE]Async(It.IsAny<[ENTITY_TYPE]>()))
                  .ReturnsAsync(true);

        // Act
        await _viewModel.ProcessActionCommand.ExecuteAsync(null);

        // Assert
        Assert.Empty(_viewModel.ErrorMessage);
        Assert.False(_viewModel.IsBusy);
        
        _mockEngine.Verify(x => x.Process[ENTITY_TYPE]Async(It.IsAny<[ENTITY_TYPE]>()), Times.Once);
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]ActionProcessed"), Times.Once);
    }

    [Fact]
    public async Task ProcessActionCommand_WithValidationError_ShouldSetErrorMessage()
    {
        // Arrange
        var validationError = Error.Validation("Invalid data");
        _mockEngine.Setup(x => x.Process[ENTITY_TYPE]Async(It.IsAny<[ENTITY_TYPE]>()))
                  .ReturnsAsync(validationError);

        // Act
        await _viewModel.ProcessActionCommand.ExecuteAsync(null);

        // Assert
        Assert.Equal("Invalid data", _viewModel.ErrorMessage);
        Assert.False(_viewModel.IsBusy);
        
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]ActionFailed", 
            It.IsAny<Dictionary<string, object>>()), Times.Once);
    }

    [Fact]
    public async Task ProcessActionCommand_ShouldSetBusyStateDuringExecution()
    {
        // Arrange
        var tcs = new TaskCompletionSource<ErrorOr<bool>>();
        _mockEngine.Setup(x => x.Process[ENTITY_TYPE]Async(It.IsAny<[ENTITY_TYPE]>()))
                  .Returns(tcs.Task);

        // Act
        var task = _viewModel.ProcessActionCommand.ExecuteAsync(null);
        
        // Assert - Should be busy during execution
        Assert.True(_viewModel.IsBusy);
        Assert.Equal("Processing...", _viewModel.BusyMessage);
        
        // Complete the task
        tcs.SetResult(true);
        await task;
        
        // Assert - Should not be busy after completion
        Assert.False(_viewModel.IsBusy);
        Assert.Empty(_viewModel.BusyMessage);
    }

    [Fact]
    public async Task NavigateToDetailsCommand_ShouldTrackEvent()
    {
        // Act
        await _viewModel.NavigateToDetailsCommand.ExecuteAsync(null);

        // Assert
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]NavigateToDetails"), Times.Once);
    }

    [Fact]
    public async Task OnViewDisappearing_ShouldTrackEvent()
    {
        // Act
        await _viewModel.OnViewDisappearing();

        // Assert
        _mockLogService.Verify(x => x.TrackEvent("[FEATURE_NAME]ViewDisappeared"), Times.Once);
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public void HasData_PropertyChanged_ShouldNotifyObservers(bool hasData)
    {
        // Arrange
        var propertyChangedEventArgs = new List<string>();
        _viewModel.PropertyChanged += (sender, e) => propertyChangedEventArgs.Add(e.PropertyName);

        // Act
        _viewModel.HasData = hasData;

        // Assert
        Assert.Contains(nameof(_viewModel.HasData), propertyChangedEventArgs);
    }

    [Fact]
    public void Title_DefaultValue_ShouldBeCorrect()
    {
        // Assert
        Assert.Equal("[FEATURE_NAME]", _viewModel.Title);
    }
}
