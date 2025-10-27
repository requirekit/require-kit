using {{ProjectName}}.ViewModels;

namespace {{ProjectName}}.Navigation;

/// <summary>
/// Navigator implementation using convention-based page resolution.
/// Conventions:
/// - ViewModel: {Feature}ViewModel
/// - Page: {Feature}Page
/// Example: ProductViewModel -> ProductPage
/// </summary>
public class Navigator : INavigator
{
    private readonly IServiceProvider _serviceProvider;
    private INavigation Navigation => Application.Current?.MainPage?.Navigation
        ?? throw new InvalidOperationException("Navigation is not available. Ensure MainPage is set.");

    public Navigator(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider ?? throw new ArgumentNullException(nameof(serviceProvider));
    }

    /// <inheritdoc />
    public async Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase
    {
        var page = ResolvePage<TViewModel>();
        var viewModel = ResolveViewModel<TViewModel>();

        page.BindingContext = viewModel;
        await Navigation.PushAsync(page);
    }

    /// <inheritdoc />
    public async Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
        where TViewModel : ViewModelBase<TParams>
    {
        if (parameters == null)
            throw new ArgumentNullException(nameof(parameters));

        var page = ResolvePage<TViewModel>();
        var viewModel = ResolveViewModel<TViewModel, TParams>();

        // Initialize ViewModel with parameters
        viewModel.OnPrepare(parameters);

        page.BindingContext = viewModel;
        await Navigation.PushAsync(page);

        // Call initialization hook
        await viewModel.OnInitialize();
    }

    /// <inheritdoc />
    public async Task GoBackAsync()
    {
        if (Navigation.NavigationStack.Count <= 1)
            throw new InvalidOperationException("Cannot navigate back from root page.");

        await Navigation.PopAsync();
    }

    /// <inheritdoc />
    public async Task PopToRootAsync()
    {
        if (Navigation.NavigationStack.Count == 0)
            throw new InvalidOperationException("Navigation stack is empty.");

        await Navigation.PopToRootAsync();
    }

    /// <summary>
    /// Resolve a Page from the service provider using convention-based naming.
    /// </summary>
    /// <typeparam name="TViewModel">The ViewModel type.</typeparam>
    /// <returns>The resolved Page instance.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when the page cannot be resolved.
    /// </exception>
    private Page ResolvePage<TViewModel>() where TViewModel : ViewModelBase
    {
        var viewModelName = typeof(TViewModel).Name;

        // Convention: ProductViewModel -> ProductPage
        var pageName = viewModelName.Replace("ViewModel", "Page");
        var pageTypeName = $"{typeof(TViewModel).Namespace?.Replace(".ViewModels", ".Pages")}.{pageName}";

        // Try to find the page type
        var pageType = AppDomain.CurrentDomain.GetAssemblies()
            .SelectMany(a => a.GetTypes())
            .FirstOrDefault(t => t.FullName == pageTypeName && t.IsSubclassOf(typeof(Page)));

        if (pageType == null)
        {
            throw new InvalidOperationException(
                $"Page type '{pageTypeName}' not found. " +
                $"Ensure the page follows the convention: {viewModelName} -> {pageName}. " +
                $"Expected namespace: {typeof(TViewModel).Namespace?.Replace(".ViewModels", ".Pages")}");
        }

        // Resolve page from DI container
        var page = _serviceProvider.GetService(pageType) as Page;

        if (page == null)
        {
            throw new InvalidOperationException(
                $"Page '{pageName}' could not be resolved from the service provider. " +
                $"Ensure it is registered in MauiProgram.cs using services.AddTransient<{pageName}>();");
        }

        return page;
    }

    /// <summary>
    /// Resolve a ViewModel from the service provider.
    /// </summary>
    /// <typeparam name="TViewModel">The ViewModel type.</typeparam>
    /// <returns>The resolved ViewModel instance.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when the ViewModel cannot be resolved.
    /// </exception>
    private TViewModel ResolveViewModel<TViewModel>() where TViewModel : ViewModelBase
    {
        var viewModel = _serviceProvider.GetService<TViewModel>();

        if (viewModel == null)
        {
            throw new InvalidOperationException(
                $"ViewModel '{typeof(TViewModel).Name}' could not be resolved from the service provider. " +
                $"Ensure it is registered in MauiProgram.cs using services.AddTransient<{typeof(TViewModel).Name}>();");
        }

        return viewModel;
    }

    /// <summary>
    /// Resolve a parameterized ViewModel from the service provider.
    /// </summary>
    /// <typeparam name="TViewModel">The ViewModel type.</typeparam>
    /// <typeparam name="TParams">The parameter type.</typeparam>
    /// <returns>The resolved ViewModel instance.</returns>
    /// <exception cref="InvalidOperationException">
    /// Thrown when the ViewModel cannot be resolved.
    /// </exception>
    private TViewModel ResolveViewModel<TViewModel, TParams>()
        where TViewModel : ViewModelBase<TParams>
    {
        var viewModel = _serviceProvider.GetService<TViewModel>();

        if (viewModel == null)
        {
            throw new InvalidOperationException(
                $"ViewModel '{typeof(TViewModel).Name}' could not be resolved from the service provider. " +
                $"Ensure it is registered in MauiProgram.cs using services.AddTransient<{typeof(TViewModel).Name}>();");
        }

        return viewModel;
    }
}
