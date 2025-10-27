# SOURCE: maui-appshell template (shared, adapted for NavigationPage)
// ViewModels/ViewModelBase.cs
using CommunityToolkit.Mvvm.ComponentModel;
using {{ProjectName}}.Navigation;

namespace {{ProjectName}}.ViewModels;

public abstract partial class ViewModelBase : ObservableObject
{
    [ObservableProperty] private string _busyMessage = string.Empty;

    [ObservableProperty] private bool _isBusy;

    protected INavigator Navigator { get; }

    protected ViewModelBase(INavigator navigator)
    {
        Navigator = navigator ?? throw new ArgumentNullException(nameof(navigator));
    }

    /// <summary>
    /// Called to initialize the view model after construction.
    /// </summary>
    public virtual Task OnInitialize()
    {
        return Task.CompletedTask;
    }

    /// <summary>
    /// Called when the page appears.
    /// </summary>
    public virtual Task OnAppearing()
    {
        return Task.CompletedTask;
    }

    /// <summary>
    /// Called when the page disappears.
    /// </summary>
    public virtual Task OnDisappearing()
    {
        return Task.CompletedTask;
    }

    /// <summary>
    /// Helper class for managing busy state with proper disposal
    /// </summary>
    protected sealed class BusyScope : IDisposable
    {
        private readonly ViewModelBase _viewModel;

        public BusyScope(ViewModelBase viewModel, string message = "")
        {
            _viewModel = viewModel;
            _viewModel.IsBusy = true;
            _viewModel.BusyMessage = message;
        }

        public void Dispose()
        {
            _viewModel.IsBusy = false;
            _viewModel.BusyMessage = string.Empty;
        }
    }
}

/// <summary>
/// Base class for ViewModels that accept navigation parameters.
/// </summary>
/// <typeparam name="TParams">The type of navigation parameters.</typeparam>
public abstract class ViewModelBase<TParams> : ViewModelBase
{
    protected ViewModelBase(INavigator navigator) : base(navigator)
    {
    }

    /// <summary>
    /// Called before initialization when the ViewModel is provided with parameters from the caller.
    /// </summary>
    /// <param name="parameter">The navigation parameters.</param>
    public virtual void OnPrepare(TParams parameter)
    {
    }
}
