using {{ProjectName}}.ViewModels;

namespace {{ProjectName}}.Navigation;

/// <summary>
/// Navigator interface for type-safe page navigation.
/// </summary>
public interface INavigator
{
    /// <summary>
    /// Navigate to a page associated with the specified ViewModel.
    /// </summary>
    /// <typeparam name="TViewModel">The ViewModel type to navigate to.</typeparam>
    /// <returns>A task representing the asynchronous navigation operation.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when the page for the specified ViewModel cannot be resolved.
    /// </exception>
    Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase;

    /// <summary>
    /// Navigate to a page associated with the specified ViewModel, passing parameters.
    /// </summary>
    /// <typeparam name="TViewModel">The ViewModel type to navigate to.</typeparam>
    /// <typeparam name="TParams">The type of parameters to pass.</typeparam>
    /// <param name="parameters">The parameters to pass to the ViewModel.</param>
    /// <returns>A task representing the asynchronous navigation operation.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when the page for the specified ViewModel cannot be resolved.
    /// </exception>
    Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
        where TViewModel : ViewModelBase<TParams>;

    /// <summary>
    /// Navigate back to the previous page in the navigation stack.
    /// </summary>
    /// <returns>A task representing the asynchronous navigation operation.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when navigation stack is empty or navigation fails.
    /// </exception>
    Task GoBackAsync();

    /// <summary>
    /// Pop to the root page of the navigation stack.
    /// </summary>
    /// <returns>A task representing the asynchronous navigation operation.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when navigation fails.
    /// </exception>
    Task PopToRootAsync();
}
