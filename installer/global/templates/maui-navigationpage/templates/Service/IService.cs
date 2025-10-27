# SOURCE: maui-appshell template (shared)
using ErrorOr;

namespace {{ProjectName}}.Services.Interfaces;

/// <summary>
/// Service interface for [SERVICE_NAME] functionality
/// Services handle external integrations and cross-cutting concerns
/// </summary>
public interface I[SERVICE_NAME]Service
{
    /// <summary>
    /// Example service method with ErrorOr return type
    /// </summary>
    /// <param name="parameter">Input parameter</param>
    /// <returns>ErrorOr containing the result or errors</returns>
    Task<ErrorOr<string>> GetDataAsync(string parameter);

    /// <summary>
    /// Example service method for processing
    /// </summary>
    /// <param name="data">Data to process</param>
    /// <returns>ErrorOr containing success result or errors</returns>
    Task<ErrorOr<bool>> ProcessDataAsync(object data);

    /// <summary>
    /// Example synchronous service method
    /// </summary>
    /// <param name="value">Value to validate</param>
    /// <returns>ErrorOr containing validation result or errors</returns>
    ErrorOr<bool> ValidateData(string value);

    /// <summary>
    /// Example method for configuration
    /// </summary>
    /// <returns>ErrorOr containing configuration or errors</returns>
    Task<ErrorOr<Dictionary<string, object>>> GetConfigurationAsync();
}
