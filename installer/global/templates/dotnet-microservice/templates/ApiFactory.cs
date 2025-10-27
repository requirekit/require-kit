using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace {ServiceName}.Tests.Integration.Fixtures;

/// <summary>
/// Factory for creating test server instances for integration testing
/// </summary>
public class ApiFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureTestServices(services =>
        {
            // Remove production services and replace with test doubles if needed
            // Example: Replace database with in-memory database
            // var descriptor = services.SingleOrDefault(
            //     d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            // if (descriptor != null)
            // {
            //     services.Remove(descriptor);
            // }
            // services.AddDbContext<AppDbContext>(options =>
            // {
            //     options.UseInMemoryDatabase("TestDb");
            // });
            
            // Configure test authentication if needed
            // services.AddAuthentication("Test")
            //     .AddScheme<TestAuthenticationSchemeOptions, TestAuthenticationHandler>(
            //         "Test", options => { });
        });
        
        builder.ConfigureServices(services =>
        {
            // Add any test-specific services
            services.AddSingleton<IHostLifetime, NoOpHostLifetime>();
        });
        
        builder.UseEnvironment("Test");
        
        // Suppress logs during testing unless debugging
        builder.ConfigureLogging((context, logging) =>
        {
            logging.ClearProviders();
            if (Environment.GetEnvironmentVariable("SHOW_TEST_LOGS") == "true")
            {
                logging.AddConsole();
                logging.SetMinimumLevel(LogLevel.Debug);
            }
        });
    }
    
    /// <summary>
    /// Create an authenticated HTTP client for testing
    /// </summary>
    public HttpClient CreateAuthenticatedClient(string userId = "test-user", string[] roles = null)
    {
        var client = WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                // Configure test authentication
                // services.Configure<TestAuthenticationOptions>(options =>
                // {
                //     options.UserId = userId;
                //     options.Roles = roles ?? new[] { "User" };
                // });
            });
        }).CreateClient();
        
        // Add authentication header if needed
        // client.DefaultRequestHeaders.Authorization = 
        //     new System.Net.Http.Headers.AuthenticationHeaderValue("Test");
        
        return client;
    }
}

/// <summary>
/// No-op host lifetime for testing to prevent application shutdown
/// </summary>
public class NoOpHostLifetime : IHostLifetime
{
    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
    public Task WaitForStartAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}

/// <summary>
/// Collection definition for shared test context
/// </summary>
[CollectionDefinition("Api")]
public class ApiCollectionFixture : ICollectionFixture<ApiFactory>
{
    // This class has no code, and is never created.
    // Its purpose is to be the place to apply [CollectionDefinition]
    // and all the ICollectionFixture<> interfaces.
}
