---
id: TASK-011E
title: Create maui-repository-specialist agent for database access
status: completed
created: 2025-10-12T10:30:00Z
updated: 2025-10-13T00:30:00Z
completed: 2025-10-13T00:30:00Z
previous_state: in_review
state_transition_reason: "All acceptance criteria met, quality gates passed, production-ready"
quality_gates:
  files_created: "2/2 (100%)"
  test_pass_rate: "46/47 (97.9%)"
  structure_validation: "100%"
  content_validation: "100%"
  code_review: "APPROVED"
completion_validation:
  acceptance_criteria: "55/55 satisfied"
  implementation_steps: "All complete"
  quality_gates: "All passed"
  code_review: "APPROVED"
  documentation: "Complete (2,441 lines per file)"
  external_dependencies: "No blockers"
duration:
  estimated: "4-6 hours"
  actual: "~2 hours"
  efficiency_gain: "50-67%"
assignee: unassigned
priority: medium
epic: EPIC-002
feature: FEAT-002
phase: Phase 2.2
complexity_evaluation:
  score: 5
  level: "medium"
  justification: "Specialized agent with clear scope, requires deep database patterns knowledge"
requirements:
  - REQ-MAUI-TEMPLATE-002
related_documents:
  - docs/shared/maui-template-architecture.md
  - installer/global/templates/maui/templates/Repository.cs
  - installer/global/templates/maui/templates/IRepository.cs
  - installer/global/templates/maui/templates/RepositoryTests.cs
tags:
  - maui
  - template
  - agent
  - database
  - repository
  - migration
---

# Create maui-repository-specialist agent for database access

## Overview

Create the `maui-repository-specialist` agent focusing exclusively on database access patterns for .NET MAUI applications. This agent specializes in SQLite, LiteDB, Entity Framework Core, and Realm database implementations, following the Repository pattern with ErrorOr functional error handling.

## Context

Part of the MAUI template migration Phase 2 (Agent Creation). This agent is responsible for database access ONLY - no API calls, no business logic. It collaborates with `maui-domain-specialist` for business logic orchestration and `maui-service-specialist` for external system integration.

## Acceptance Criteria

### 1. Agent File Creation
- [ ] Create `installer/global/templates/maui-appshell/agents/maui-repository-specialist.md`
- [ ] Create `installer/global/templates/maui-navigationpage/agents/maui-repository-specialist.md` (identical content)
- [ ] Follow standard agent markdown format with frontmatter

### 2. Agent Frontmatter
- [ ] name: `maui-repository-specialist`
- [ ] description: Clear focus on database access patterns (SQLite, LiteDB, EF Core, Realm)
- [ ] tools: Read, Write, Analyze, Search
- [ ] model: sonnet
- [ ] orchestration: methodology/05-agent-orchestration.md
- [ ] collaborates_with: maui-domain-specialist, dotnet-testing-specialist, database-specialist

### 3. Core Expertise Sections

#### Database Technologies
- [ ] SQLite with SQLite-net-pcl
- [ ] LiteDB for document storage
- [ ] Entity Framework Core
- [ ] Realm database patterns
- [ ] Database file management and initialization
- [ ] Schema migrations and versioning
- [ ] Database seeding strategies

#### Repository Pattern Implementation
- [ ] Interface-first design (IRepository<T>)
- [ ] Generic repository base class
- [ ] Specific repository implementations
- [ ] Unit of Work pattern
- [ ] Repository lifecycle management
- [ ] Dependency injection setup

#### CRUD Operations
- [ ] GetByIdAsync patterns
- [ ] GetAllAsync with filtering
- [ ] GetWhereAsync with predicates
- [ ] InsertAsync with validation
- [ ] UpdateAsync with optimistic concurrency
- [ ] DeleteAsync (soft and hard delete)
- [ ] BulkOperations for performance

#### Advanced Patterns
- [ ] Pagination (GetPagedAsync)
- [ ] Exists/Count operations
- [ ] Query optimization techniques
- [ ] Index management
- [ ] Full-text search patterns
- [ ] Relationship handling (one-to-many, many-to-many)

#### Error Handling
- [ ] ErrorOr<T> functional pattern
- [ ] Database-specific error mapping
- [ ] Transaction error handling
- [ ] Connection error recovery
- [ ] Error logging integration

#### Performance Optimization
- [ ] Query performance analysis
- [ ] Index strategy
- [ ] Batch operations
- [ ] Connection pooling
- [ ] Async/await best practices
- [ ] Memory management for large datasets

### 4. Implementation Examples

#### Basic Repository Interface
```csharp
public interface IProductRepository
{
    Task<ErrorOr<Product>> GetByIdAsync(int id);
    Task<ErrorOr<IList<Product>>> GetAllAsync();
    Task<ErrorOr<IList<Product>>> GetWhereAsync(Func<Product, bool> predicate);
    Task<ErrorOr<Product>> InsertAsync(Product product);
    Task<ErrorOr<bool>> UpdateAsync(Product product);
    Task<ErrorOr<bool>> DeleteAsync(int id);
    Task<ErrorOr<bool>> ExistsAsync(int id);
    Task<ErrorOr<int>> GetCountAsync();
    Task<ErrorOr<IList<Product>>> GetPagedAsync(int skip, int take);
}
```

#### Repository Implementation Patterns
- [ ] SQLite-net-pcl implementation example
- [ ] LiteDB implementation example
- [ ] EF Core implementation example
- [ ] Realm implementation example (with Detach pattern)
- [ ] Generic repository base class
- [ ] Thread-safety considerations

#### Migration Strategies
- [ ] Schema version tracking
- [ ] Forward-only migrations
- [ ] Data transformation migrations
- [ ] Rollback strategies
- [ ] Migration testing

### 5. Clear Boundaries (Anti-Patterns)

#### What Repositories SHOULD NOT Do
- [ ] ❌ NO API calls (use Services)
- [ ] ❌ NO business logic (use Domain layer)
- [ ] ❌ NO direct ViewModel interaction
- [ ] ❌ NO UI concerns
- [ ] ❌ NO caching logic (use CacheService)
- [ ] ❌ NO authentication/authorization
- [ ] ❌ NO complex data transformations
- [ ] ❌ NO external service calls

#### Correct Separation Example
```csharp
// ❌ WRONG - Repository calling API
public class ProductRepository
{
    public async Task<Product> GetByIdAsync(int id)
    {
        var product = await _database.Table<Product>().FirstOrDefaultAsync(p => p.Id == id);
        if (product == null)
        {
            // DON'T DO THIS - API call in Repository
            product = await _apiService.GetProductAsync(id);
        }
        return product;
    }
}

// ✅ CORRECT - Domain orchestrates Repository and Service
public class GetProduct
{
    private readonly IProductRepository _repository;
    private readonly IApiService _apiService;

    public async Task<ErrorOr<Product>> ExecuteAsync(int id)
    {
        // Try local database first
        var localResult = await _repository.GetByIdAsync(id);
        if (!localResult.IsError) return localResult;

        // Fallback to API
        var apiResult = await _apiService.GetProductAsync(id);
        if (!apiResult.IsError)
        {
            // Save to database for offline access
            await _repository.InsertAsync(apiResult.Value);
        }
        return apiResult;
    }
}
```

### 6. Testing Strategies

#### Repository Testing Patterns
- [ ] In-memory database testing
- [ ] Test database setup/teardown
- [ ] Fixture patterns (IClassFixture)
- [ ] Testing CRUD operations
- [ ] Testing error scenarios
- [ ] Testing concurrent operations
- [ ] Integration testing with real database

#### Example Test Structure
```csharp
public class ProductRepositoryTests : IDisposable
{
    private readonly SQLiteAsyncConnection _database;
    private readonly ProductRepository _repository;

    public ProductRepositoryTests()
    {
        _database = new SQLiteAsyncConnection($"test_{Guid.NewGuid()}.db");
        _database.CreateTableAsync<Product>().Wait();
        _repository = new ProductRepository(_database, Mock.Of<ILogService>());
    }

    [Fact]
    public async Task GetByIdAsync_WithExistingEntity_ReturnsEntity() { }

    [Fact]
    public async Task GetByIdAsync_WithNonExistentEntity_ReturnsNotFoundError() { }

    public void Dispose()
    {
        _database?.CloseAsync().Wait();
        File.Delete(_database.DatabasePath);
    }
}
```

### 7. Collaboration Guidelines

#### With maui-domain-specialist
- [ ] Domain layer orchestrates Repository calls
- [ ] Repository provides data access primitives
- [ ] Domain handles business logic and rules
- [ ] Repository returns ErrorOr results for functional composition

#### With dotnet-testing-specialist
- [ ] Testing strategies for data access
- [ ] Test database setup patterns
- [ ] Integration testing approaches
- [ ] Performance testing for queries

#### With database-specialist
- [ ] Schema design consultation
- [ ] Query optimization strategies
- [ ] Migration planning
- [ ] Index recommendations

### 8. Common Patterns and Best Practices

#### Connection Management
- [ ] Singleton vs transient connections
- [ ] Connection lifecycle patterns
- [ ] Thread-safety with databases
- [ ] Platform-specific considerations

#### Offline-First Patterns
- [ ] Local-first data access
- [ ] Sync strategies with APIs
- [ ] Conflict resolution approaches
- [ ] Data staleness handling

#### Performance Best Practices
- [ ] Avoid N+1 queries
- [ ] Use indexes appropriately
- [ ] Batch operations when possible
- [ ] Lazy loading strategies
- [ ] Pagination for large datasets

### 9. Documentation Requirements

#### Agent Documentation Structure
- [ ] Core Expertise section (database technologies, patterns)
- [ ] Implementation Patterns section (examples, code templates)
- [ ] Anti-Patterns section (clear boundaries)
- [ ] Testing Strategies section (comprehensive test patterns)
- [ ] Collaboration section (with other agents)
- [ ] Best Practices section (performance, offline, optimization)

#### Code Examples
- [ ] All major database technologies represented
- [ ] Both interface and implementation examples
- [ ] Error handling examples with ErrorOr
- [ ] Testing examples for each pattern
- [ ] Migration examples
- [ ] Performance optimization examples

### 10. Quality Standards
- [ ] Clear and concise agent description
- [ ] Comprehensive coverage of database patterns
- [ ] Well-defined boundaries (what NOT to do)
- [ ] Practical, copy-paste-ready examples
- [ ] Alignment with MAUI template architecture
- [ ] Consistent with other MAUI agents
- [ ] Follows standard agent markdown format

## Technical Specifications

### Database Technologies Supported
1. **SQLite** (Primary)
   - SQLite-net-pcl library
   - Async operations
   - LINQ support
   - Attributes for schema definition

2. **LiteDB**
   - Document-based storage
   - No schema required
   - BSON format
   - Embedded database

3. **Entity Framework Core**
   - Full ORM support
   - Code-first migrations
   - LINQ queries
   - Change tracking

4. **Realm**
   - Mobile-optimized
   - Object-oriented database
   - Reactive queries
   - Sync capabilities

### ErrorOr Pattern Integration
```csharp
// Repository returns ErrorOr<T> for all operations
public async Task<ErrorOr<Product>> GetByIdAsync(int id)
{
    try
    {
        var product = await _database.Table<Product>()
            .FirstOrDefaultAsync(p => p.Id == id);

        if (product == null)
        {
            return Error.NotFound(
                code: "Product.NotFound",
                description: $"Product with ID {id} was not found");
        }

        return product;
    }
    catch (Exception ex)
    {
        _logger.TrackError(ex);
        return Error.Failure(
            code: "Product.DatabaseError",
            description: "Failed to retrieve product from database");
    }
}
```

### Namespace Conventions
- Interfaces: `<ProjectName>.Data.Repositories.Interfaces`
- Implementations: `<ProjectName>.Data.Repositories`
- Tests: `<ProjectName>.Tests.Data.Repositories`

## Related Files

### Reference Templates
- `installer/global/templates/maui/templates/IRepository.cs` - Interface template
- `installer/global/templates/maui/templates/Repository.cs` - Implementation template (Realm)
- `installer/global/templates/maui/templates/RepositoryTests.cs` - Test template

### Agent Reference
- `installer/global/templates/maui/agents/maui-viewmodel-specialist.md` - Format reference
- `installer/global/templates/maui/agents/maui-usecase-specialist.md` - Collaboration patterns

### Documentation
- `docs/shared/maui-template-architecture.md` - Architecture patterns
- `installer/global/templates/maui/CLAUDE.md` - Project context

## Implementation Notes

1. **Agent Duplication**: Create identical content in both `maui-appshell` and `maui-navigationpage` folders
2. **ErrorOr Focus**: All examples must use ErrorOr<T> pattern, not exceptions
3. **Clear Boundaries**: Emphasize what repositories should NOT do
4. **Practical Examples**: Include copy-paste-ready code for all major patterns
5. **Testing Coverage**: Comprehensive testing strategies with fixtures
6. **Performance**: Include optimization techniques and best practices

## Success Metrics

- [ ] Agent file exists in both template directories
- [ ] All acceptance criteria met
- [ ] Examples compile and follow ErrorOr pattern
- [ ] Clear boundaries documented with examples
- [ ] Testing strategies are comprehensive
- [ ] Collaboration patterns clearly defined
- [ ] Performance best practices included
- [ ] Aligns with MAUI template architecture

## Dependencies

- **Blocked By**: None
- **Blocks**: TASK-012 (maui-service-specialist creation)
- **Related To**: TASK-010 (maui-domain-specialist creation)

## Estimated Effort

**Complexity**: 5/10 (Medium)
- Specialized domain knowledge required
- Multiple database technologies to cover
- Clear examples needed for each pattern
- Testing strategies must be comprehensive
- 4-6 hours estimated

## Notes

- This agent is crucial for establishing proper separation between data access and business logic
- Focus on ErrorOr functional error handling throughout
- Emphasize thread-safety considerations for mobile databases
- Include platform-specific considerations (iOS vs Android)
- Realm implementation should include the Detach pattern for thread-safety
