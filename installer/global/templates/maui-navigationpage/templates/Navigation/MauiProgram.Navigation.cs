using {{ProjectName}}.Navigation;
using {{ProjectName}}.ViewModels;
using {{ProjectName}}.Pages;

namespace {{ProjectName}};

/// <summary>
/// Extension methods for registering navigation services in MauiProgram.
/// </summary>
public static class MauiProgramNavigationExtensions
{
    /// <summary>
    /// Add navigation services to the application.
    /// Registers INavigator as a Singleton.
    /// </summary>
    /// <param name="builder">The MauiAppBuilder instance.</param>
    /// <returns>The MauiAppBuilder for method chaining.</returns>
    public static MauiAppBuilder AddNavigationServices(this MauiAppBuilder builder)
    {
        // Register Navigator as Singleton
        builder.Services.AddSingleton<INavigator, Navigator>();

        // Example: Register Pages and ViewModels
        // Uncomment and modify as needed for your application

        // Example: Home Page
        // builder.Services.AddTransient<HomePage>();
        // builder.Services.AddTransient<HomeViewModel>();

        // Example: Product Detail Page with Parameters
        // builder.Services.AddTransient<ProductDetailPage>();
        // builder.Services.AddTransient<ProductDetailViewModel>();

        // Example: Settings Page
        // builder.Services.AddTransient<SettingsPage>();
        // builder.Services.AddTransient<SettingsViewModel>();

        return builder;
    }

    /// <summary>
    /// Example helper method to register a Page-ViewModel pair.
    /// </summary>
    /// <typeparam name="TPage">The Page type.</typeparam>
    /// <typeparam name="TViewModel">The ViewModel type.</typeparam>
    /// <param name="services">The service collection.</param>
    /// <returns>The service collection for method chaining.</returns>
    public static IServiceCollection AddPageViewModel<TPage, TViewModel>(this IServiceCollection services)
        where TPage : Page
        where TViewModel : ViewModelBase
    {
        services.AddTransient<TPage>();
        services.AddTransient<TViewModel>();
        return services;
    }
}
