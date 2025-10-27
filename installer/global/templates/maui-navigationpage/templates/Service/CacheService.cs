# SOURCE: maui-appshell template (shared)
// Services/Implementations/CacheService.cs
using System.Text.Json;
using YourApp.Services.Interfaces;
using Microsoft.Maui.Storage;

namespace YourApp.Services.Implementations;

/// <summary>
/// Service for caching data with both in-memory and persistent storage
/// </summary>
public class CacheService : ICacheService
{
    private readonly Dictionary<string, CacheEntry> _memoryCache = new();
    private readonly IPreferences _preferences;
    private readonly IFileSystem _fileSystem;
    private readonly ILogger<CacheService> _logger;
    private readonly JsonSerializerOptions _jsonOptions;
    private readonly SemaphoreSlim _cacheLock = new(1, 1);

    public CacheService(IPreferences preferences, IFileSystem fileSystem, ILogger<CacheService> logger)
    {
        _preferences = preferences;
        _fileSystem = fileSystem;
        _logger = logger;
        
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
    }

    /// <summary>
    /// Get cached data
    /// </summary>
    public async Task<T?> GetAsync<T>(string key)
    {
        await _cacheLock.WaitAsync();
        try
        {
            // Check memory cache first
            if (_memoryCache.TryGetValue(key, out var entry))
            {
                if (entry.ExpiresAt > DateTime.UtcNow)
                {
                    _logger.LogDebug("Cache hit (memory) for key: {Key}", key);
                    return (T)entry.Value;
                }
                
                _memoryCache.Remove(key);
            }

            // Check persistent cache
            var persistentData = await GetFromPersistentCacheAsync<T>(key);
            if (persistentData != null)
            {
                // Add to memory cache for faster access
                _memoryCache[key] = new CacheEntry(persistentData, DateTime.UtcNow.AddMinutes(5));
                _logger.LogDebug("Cache hit (persistent) for key: {Key}", key);
                return persistentData;
            }

            _logger.LogDebug("Cache miss for key: {Key}", key);
            return default;
        }
        finally
        {
            _cacheLock.Release();
        }
    }

    /// <summary>
    /// Set cached data
    /// </summary>
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null)
    {
        await _cacheLock.WaitAsync();
        try
        {
            var expiresAt = expiry.HasValue 
                ? DateTime.UtcNow.Add(expiry.Value) 
                : DateTime.UtcNow.AddHours(1); // Default 1 hour expiry

            // Add to memory cache
            _memoryCache[key] = new CacheEntry(value!, expiresAt);
            
            // Persist if expiry is more than 5 minutes
            if (!expiry.HasValue || expiry.Value.TotalMinutes > 5)
            {
                await SaveToPersistentCacheAsync(key, value, expiresAt);
            }
            
            _logger.LogDebug("Cached data for key: {Key}, expires at: {ExpiresAt}", key, expiresAt);
        }
        finally
        {
            _cacheLock.Release();
        }
    }

    /// <summary>
    /// Remove cached data
    /// </summary>
    public async Task RemoveAsync(string key)
    {
        await _cacheLock.WaitAsync();
        try
        {
            _memoryCache.Remove(key);
            await RemoveFromPersistentCacheAsync(key);
            
            _logger.LogDebug("Removed cache for key: {Key}", key);
        }
        finally
        {
            _cacheLock.Release();
        }
    }

    /// <summary>
    /// Clear all cached data
    /// </summary>
    public async Task ClearAsync()
    {
        await _cacheLock.WaitAsync();
        try
        {
            _memoryCache.Clear();
            await ClearPersistentCacheAsync();
            
            _logger.LogInformation("Cleared all cache");
        }
        finally
        {
            _cacheLock.Release();
        }
    }

    /// <summary>
    /// Get cache statistics
    /// </summary>
    public async Task<CacheStatistics> GetStatisticsAsync()
    {
        await _cacheLock.WaitAsync();
        try
        {
            var stats = new CacheStatistics
            {
                MemoryEntries = _memoryCache.Count,
                MemorySize = EstimateMemorySize(),
                PersistentEntries = await CountPersistentEntriesAsync(),
                PersistentSize = await GetPersistentSizeAsync()
            };
            
            return stats;
        }
        finally
        {
            _cacheLock.Release();
        }
    }

    private async Task<T?> GetFromPersistentCacheAsync<T>(string key)
    {
        try
        {
            var fileName = GetCacheFileName(key);
            var filePath = Path.Combine(_fileSystem.CacheDirectory, fileName);
            
            if (!File.Exists(filePath))
                return default;

            var json = await File.ReadAllTextAsync(filePath);
            var wrapper = JsonSerializer.Deserialize<CacheWrapper<T>>(json, _jsonOptions);
            
            if (wrapper?.ExpiresAt > DateTime.UtcNow)
            {
                return wrapper.Data;
            }
            
            // Clean up expired file
            File.Delete(filePath);
            return default;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error reading from persistent cache for key: {Key}", key);
            return default;
        }
    }

    private async Task SaveToPersistentCacheAsync<T>(string key, T value, DateTime expiresAt)
    {
        try
        {
            var fileName = GetCacheFileName(key);
            var filePath = Path.Combine(_fileSystem.CacheDirectory, fileName);
            
            var wrapper = new CacheWrapper<T>
            {
                Data = value,
                ExpiresAt = expiresAt
            };
            
            var json = JsonSerializer.Serialize(wrapper, _jsonOptions);
            await File.WriteAllTextAsync(filePath, json);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error saving to persistent cache for key: {Key}", key);
        }
    }

    private async Task RemoveFromPersistentCacheAsync(string key)
    {
        try
        {
            var fileName = GetCacheFileName(key);
            var filePath = Path.Combine(_fileSystem.CacheDirectory, fileName);
            
            if (File.Exists(filePath))
            {
                File.Delete(filePath);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error removing from persistent cache for key: {Key}", key);
        }
    }

    private async Task ClearPersistentCacheAsync()
    {
        try
        {
            var cacheFiles = Directory.GetFiles(_fileSystem.CacheDirectory, "cache_*.json");
            foreach (var file in cacheFiles)
            {
                File.Delete(file);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error clearing persistent cache");
        }
    }

    private async Task<int> CountPersistentEntriesAsync()
    {
        try
        {
            var cacheFiles = Directory.GetFiles(_fileSystem.CacheDirectory, "cache_*.json");
            return cacheFiles.Length;
        }
        catch
        {
            return 0;
        }
    }

    private async Task<long> GetPersistentSizeAsync()
    {
        try
        {
            var cacheFiles = Directory.GetFiles(_fileSystem.CacheDirectory, "cache_*.json");
            long totalSize = 0;
            
            foreach (var file in cacheFiles)
            {
                var fileInfo = new FileInfo(file);
                totalSize += fileInfo.Length;
            }
            
            return totalSize;
        }
        catch
        {
            return 0;
        }
    }

    private long EstimateMemorySize()
    {
        // Rough estimation - in production, use proper memory profiling
        return _memoryCache.Count * 1024; // Assume 1KB average per entry
    }

    private string GetCacheFileName(string key)
    {
        // Create a safe filename from the cache key
        var safeKey = key.Replace("/", "_").Replace("\\", "_").Replace(":", "_");
        return $"cache_{safeKey}.json";
    }

    private record CacheEntry(object Value, DateTime ExpiresAt);
    
    private class CacheWrapper<T>
    {
        public T? Data { get; set; }
        public DateTime ExpiresAt { get; set; }
    }
}

/// <summary>
/// Cache statistics
/// </summary>
public class CacheStatistics
{
    public int MemoryEntries { get; set; }
    public long MemorySize { get; set; }
    public int PersistentEntries { get; set; }
    public long PersistentSize { get; set; }
    
    public string FormattedMemorySize => FormatBytes(MemorySize);
    public string FormattedPersistentSize => FormatBytes(PersistentSize);
    
    private string FormatBytes(long bytes)
    {
        string[] sizes = { "B", "KB", "MB", "GB" };
        int order = 0;
        double size = bytes;
        
        while (size >= 1024 && order < sizes.Length - 1)
        {
            order++;
            size /= 1024;
        }
        
        return $"{size:0.##} {sizes[order]}";
    }
}

/// <summary>
/// Interface for cache service
/// </summary>
public interface ICacheService
{
    Task<T?> GetAsync<T>(string key);
    Task SetAsync<T>(string key, T value, TimeSpan? expiry = null);
    Task RemoveAsync(string key);
    Task ClearAsync();
    Task<CacheStatistics> GetStatisticsAsync();
}
