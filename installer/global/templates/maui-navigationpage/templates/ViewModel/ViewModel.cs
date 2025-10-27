# SOURCE: maui-appshell template (shared)
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using {{ProjectName}}.Navigation;
using {{ProjectName}}.Engines;
using {{ProjectName}}.Services.Interfaces;
using ErrorOr;

namespace {{ProjectName}}.ViewModels;

/// <summary>
/// ViewModel for [FEATURE_NAME] functionality
/// ViewModels should delegate business logic to Engine classes
/// </summary>
public partial class [FEATURE_NAME]ViewModel : ViewModelBase
{
    private readonly [FEATURE_NAME]Engine _engine;
    private readonly ILogService _logService;

    [ObservableProperty]
    private string _title = "[FEATURE_NAME]";

    [ObservableProperty]
    private bool _hasData;

    [ObservableProperty]
    private string _errorMessage = string.Empty;

    public [FEATURE_NAME]ViewModel(
        INavigator navigator,
        [FEATURE_NAME]Engine engine,
        ILogService logService) : base(navigator)
    {
        _engine = engine;
        _logService = logService;
    }

    /// <summary>
    /// Called when the view appears
    /// </summary>
    public override async Task OnViewAppearing()
    {
        await base.OnViewAppearing();
        
        _logService.TrackEvent("[FEATURE_NAME]ViewAppeared");
        
        // Initialize data if needed
        await LoadDataCommand.ExecuteAsync(null);
    }

    /// <summary>
    /// Called when the view disappears
    /// </summary>
    public override async Task OnViewDisappearing()
    {
        _logService.TrackEvent("[FEATURE_NAME]ViewDisappeared");
        
        await base.OnViewDisappearing();
    }

    /// <summary>
    /// Command to load data
    /// </summary>
    [RelayCommand]
    private async Task LoadData()
    {
        try
        {
            IsBusy = true;
            BusyMessage = "Loading data...";
            ErrorMessage = string.Empty;

            // Call engine to get data
            var result = await _engine.Get[ENTITY_TYPE]Async(1); // Example ID

            result.Match(
                onValue: data =>
                {
                    // Handle successful result
                    HasData = true;
                    _logService.TrackEvent("[FEATURE_NAME]DataLoaded");
                },
                onError: errors =>
                {
                    // Handle errors
                    var firstError = errors.First();
                    ErrorMessage = firstError.Description;
                    HasData = false;
                    
                    _logService.TrackEvent("[FEATURE_NAME]DataLoadFailed", new Dictionary<string, object>
                    {
                        { "ErrorCode", firstError.Code },
                        { "ErrorDescription", firstError.Description }
                    });
                });
        }
        catch (Exception ex)
        {
            ErrorMessage = "An unexpected error occurred";
            HasData = false;
            
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "LoadData" },
                { "ViewModel", nameof([FEATURE_NAME]ViewModel) }
            });
        }
        finally
        {
            IsBusy = false;
            BusyMessage = string.Empty;
        }
    }

    /// <summary>
    /// Command to process an action
    /// </summary>
    [RelayCommand]
    private async Task ProcessAction()
    {
        try
        {
            IsBusy = true;
            BusyMessage = "Processing...";
            ErrorMessage = string.Empty;

            // Example: Create entity and process it
            var entity = new [ENTITY_TYPE](); // Initialize with appropriate data
            var result = await _engine.Process[ENTITY_TYPE]Async(entity);

            result.Match(
                onValue: _ =>
                {
                    // Handle success
                    _logService.TrackEvent("[FEATURE_NAME]ActionProcessed");
                    
                    // Navigate or update UI as needed
                    // await Navigator.Navigate<NextViewModel>();
                },
                onError: errors =>
                {
                    // Handle errors
                    var firstError = errors.First();
                    ErrorMessage = firstError.Description;
                    
                    _logService.TrackEvent("[FEATURE_NAME]ActionFailed", new Dictionary<string, object>
                    {
                        { "ErrorCode", firstError.Code },
                        { "ErrorDescription", firstError.Description }
                    });
                });
        }
        catch (Exception ex)
        {
            ErrorMessage = "An unexpected error occurred";
            
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "ProcessAction" },
                { "ViewModel", nameof([FEATURE_NAME]ViewModel) }
            });
        }
        finally
        {
            IsBusy = false;
            BusyMessage = string.Empty;
        }
    }

    /// <summary>
    /// Command to navigate to another view
    /// </summary>
    [RelayCommand]
    private async Task NavigateToDetails()
    {
        try
        {
            _logService.TrackEvent("[FEATURE_NAME]NavigateToDetails");
            
            // Example navigation with parameter
            // await Navigator.Navigate<DetailsViewModel, DetailsParameter>(
            //     new DetailsParameter { Id = selectedId });
            
            // Example simple navigation
            // await Navigator.Navigate<DetailsViewModel>();
        }
        catch (Exception ex)
        {
            _logService.TrackError(ex, new Dictionary<string, object>
            {
                { "Operation", "NavigateToDetails" },
                { "ViewModel", nameof([FEATURE_NAME]ViewModel) }
            });
        }
    }

    /// <summary>
    /// Method to handle errors consistently
    /// </summary>
    private void HandleError(Error error, string operation)
    {
        ErrorMessage = error.Description;
        
        _logService.TrackEvent($"[FEATURE_NAME]{operation}Failed", new Dictionary<string, object>
        {
            { "ErrorCode", error.Code },
            { "ErrorDescription", error.Description },
            { "ErrorType", error.Type.ToString() }
        });
    }
}
