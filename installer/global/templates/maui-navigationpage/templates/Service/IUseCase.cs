# SOURCE: maui-appshell template (shared)
// Core/Interfaces/IEngine.cs
using ErrorOr;

namespace {{ProjectName}}.Core.Interfaces;

/// <summary>
/// Base interface for all Engine classes that contain business logic
/// Following the template conventions
/// </summary>
public interface IEngine
{
    // Marker interface - engines can define their own methods without constraints
}

/// <summary>
/// Generic interface for engines that execute operations and return results
/// Teams can choose to implement this or define their own method signatures
/// </summary>
public interface IEngine<TResult>
{
    /// <summary>
    /// Executes the engine logic and returns a result
    /// Method name and parameters can be customized per engine
    /// </summary>
    Task<ErrorOr<TResult>> ExecuteAsync();
}

/// <summary>
/// Generic interface for engines that take input parameters
/// </summary>
public interface IEngine<TInput, TResult>
{
    /// <summary>
    /// Executes the engine logic with input and returns a result
    /// </summary>
    Task<ErrorOr<TResult>> ExecuteAsync(TInput input);
}

/// <summary>
/// Interface for engines that perform operations without return values (commands)
/// </summary>
public interface ICommandEngine
{
    /// <summary>
    /// Executes the command operation
    /// </summary>
    Task<ErrorOr<Success>> ExecuteAsync();
}

/// <summary>
/// Interface for engines that perform operations with input but no return value
/// </summary>
public interface ICommandEngine<TInput>
{
    /// <summary>
    /// Executes the command operation with input
    /// </summary>
    Task<ErrorOr<Success>> ExecuteAsync(TInput input);
}
