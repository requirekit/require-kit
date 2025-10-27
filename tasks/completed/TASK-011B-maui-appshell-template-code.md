---
id: TASK-011B
title: Create maui-appshell template code files (Domain, Repository, Service)
status: completed
created: 2025-10-12T10:45:00Z
updated: 2025-10-13T09:15:00Z
completed: 2025-10-13T09:15:00Z
assignee: Claude
priority: high
tags: [maui-template, architecture, phase-1.2, domain-pattern, appshell]
requirements: []
bdd_scenarios: []
parent_task: null
dependencies: []
blocks: []
related_tasks: []
complexity_evaluation:
  score: 7
  level: complex
  review_mode: FULL_REQUIRED
  factor_scores:
    - factor: file_complexity
      score: 3
      max_score: 3
      justification: 10+ interdependent template files to create
    - factor: pattern_familiarity
      score: 1
      max_score: 2
      justification: Using familiar MAUI patterns with ErrorOr
    - factor: risk_level
      score: 2
      max_score: 3
      justification: Templates affect all future MAUI development
    - factor: dependencies
      score: 1
      max_score: 2
      justification: Depends on architecture documentation
completion_summary:
  architectural_review_score: 88
  quality_improvements:
    - Fixed command-operation.cs.template syntax error
    - Removed ArgumentNullException from repository (trust DI)
    - Added viewmodel-test.cs.template (354 lines)
    - Enhanced repository with 4 new methods (GetWhereAsync, ExistsAsync, GetCountAsync, GetPagedAsync)
    - Updated manifest.json with changelog
    - Created TEMPLATE-ENHANCEMENTS.md documentation
  templates_created: 14
  documentation_complete: true
  all_acceptance_criteria_met: true
---

# Task: Create maui-appshell template code files (Domain, Repository, Service)

## Business Context

**Problem**: The MAUI template currently lacks complete code templates following the Domain pattern architecture. Developers need comprehensive, production-ready templates that demonstrate:
- Verb-based Domain naming (no suffix)
- Clear separation: Repository (DB) vs Service (API/hardware)
- ErrorOr functional error handling throughout
- MVVM pattern with CommunityToolkit
- AppShell-based navigation
- Outside-In TDD testing approach

**Solution**: Create complete template files for maui-appshell that follow the architecture defined in `docs/shared/maui-template-architecture.md`. These templates will serve as the foundation for all MAUI AppShell-based projects.

**Business Value**:
- **Consistency**: All MAUI projects follow the same architectural patterns
- **Productivity**: Developers start with production-ready code structure
- **Quality**: Built-in ErrorOr error handling and comprehensive testing
- **Maintainability**: Clear layer separation (Domain, Repository, Service)
- **Onboarding**: New developers learn patterns through templates

## Description

Create all code template files for the maui-appshell global template following the Domain pattern architecture. Templates must be generic, reusable, and include placeholders for customization.

### Template Files to Create

**Location**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui-appshell/templates/`

#### Domain Layer
1. **Domain.cs** - Business logic class with verb-based naming
   - Orchestrates Repository and Service calls
   - Returns `ErrorOr<T>` for error handling
   - Includes caching and offline support patterns
   - XML documentation with examples

#### Data Access Layer
2. **IRepository.cs** - Repository interface (database access)
   - CRUD operations for database entities
   - No business logic
   - Returns domain models

3. **Repository.cs** - Repository implementation
   - SQLite database access
   - Database-specific error handling
   - Async/await patterns

#### External Systems Layer
4. **IService.cs** - Service interface (APIs, hardware)
   - HTTP client operations
   - Hardware access (location, camera, etc.)
   - External system integration

5. **Service.cs** - Service implementation
   - API client with retry logic
   - Timeout handling
   - Returns `ErrorOr<T>`

#### Presentation Layer
6. **ViewModel.cs** - MVVM ViewModel
   - CommunityToolkit ObservableProperty and RelayCommand
   - Calls Domain layer (not Repository/Service directly)
   - UI state management (loading, errors)
   - Thin orchestration only

7. **Page.xaml** - XAML ContentPage
   - Data binding to ViewModel
   - Modern MAUI controls
   - Responsive layout

8. **Page.xaml.cs** - Code-behind (minimal)
   - InitializeComponent only
   - No business logic

#### Application Shell
9. **AppShell.xaml** - Shell navigation structure
   - FlyoutItem and TabBar configuration
   - Route registration
   - Navigation structure

10. **AppShell.xaml.cs** - AppShell code-behind
    - Route registration in constructor
    - Navigation setup

11. **MauiProgram.cs** - Dependency injection setup
    - Service registration (AddSingleton, AddTransient)
    - Database initialization
    - Platform-specific services

#### Test Templates
12. **DomainTests.cs** - Domain layer unit tests
    - Mock Repository and Service dependencies
    - Test business logic in isolation
    - ErrorOr result testing

13. **RepositoryTests.cs** - Repository integration tests
    - In-memory database testing
    - CRUD operation validation
    - Error handling tests

14. **ServiceTests.cs** - Service integration tests
    - HttpClient mocking
    - API response testing
    - Error and timeout handling

15. **ViewModelTests.cs** - ViewModel unit tests
    - Mock Domain dependencies
    - Command execution testing
    - Property change notification tests

## Acceptance Criteria

### Phase 1: Domain and Data Access Templates

- [ ] **Domain.cs Template Created**
  - [ ] Verb-based naming pattern (e.g., `GetProducts`, `CreateOrder`)
  - [ ] No suffix (not `GetProductsUseCase` or `GetProductsEngine`)
  - [ ] Constructor with IRepository, IService, ICacheService dependencies
  - [ ] `ExecuteAsync()` method returning `ErrorOr<T>`
  - [ ] Multi-tier data access pattern:
    1. Try cache first (fast)
    2. Try local database (offline support)
    3. Fallback to API (online)
    4. Update cache and database on success
  - [ ] Comprehensive XML documentation
  - [ ] Placeholders for customization ({{FeatureName}}, {{EntityName}}, etc.)

- [ ] **IRepository.cs Template Created**
  - [ ] Interface with CRUD operations
  - [ ] Async methods (GetByIdAsync, GetAllAsync, AddAsync, UpdateAsync, DeleteAsync)
  - [ ] Returns domain models (not DTOs)
  - [ ] XML documentation
  - [ ] Generic entity placeholders

- [ ] **Repository.cs Template Created**
  - [ ] Implements IRepository interface
  - [ ] SQLiteAsyncConnection dependency
  - [ ] Database-specific error handling
  - [ ] Async/await patterns
  - [ ] No business logic
  - [ ] XML documentation

- [ ] **IService.cs Template Created**
  - [ ] Interface for external system access
  - [ ] API client methods (GetAsync, PostAsync, PutAsync, DeleteAsync)
  - [ ] Returns `ErrorOr<T>`
  - [ ] Generic endpoint placeholders
  - [ ] XML documentation

- [ ] **Service.cs Template Created**
  - [ ] Implements IService interface
  - [ ] HttpClient dependency
  - [ ] Retry logic with exponential backoff
  - [ ] Timeout handling
  - [ ] Error to ErrorOr conversion
  - [ ] XML documentation

### Phase 2: Presentation Layer Templates

- [ ] **ViewModel.cs Template Created**
  - [ ] Inherits from `ViewModelBase` or `ObservableObject`
  - [ ] [ObservableProperty] for bindable properties
  - [ ] [RelayCommand] for commands
  - [ ] Calls Domain layer (not Repository/Service directly)
  - [ ] UI state properties (IsLoading, ErrorMessage, etc.)
  - [ ] Async command patterns
  - [ ] Error handling with ErrorOr.Match()
  - [ ] XML documentation

- [ ] **Page.xaml Template Created**
  - [ ] ContentPage with BindingContext
  - [ ] Data binding examples
  - [ ] Modern MAUI controls (CollectionView, Button, Entry, etc.)
  - [ ] Loading and error state UI
  - [ ] Responsive layout (VerticalStackLayout, Grid)
  - [ ] Accessibility labels
  - [ ] Placeholder content

- [ ] **Page.xaml.cs Template Created**
  - [ ] Minimal code-behind
  - [ ] InitializeComponent only
  - [ ] Optional: Query parameter handling
  - [ ] No business logic

### Phase 3: Application Structure Templates

- [ ] **AppShell.xaml Template Created**
  - [ ] Shell with FlyoutItem examples
  - [ ] TabBar configuration
  - [ ] ShellContent for pages
  - [ ] Navigation structure example
  - [ ] Placeholder routes

- [ ] **AppShell.xaml.cs Template Created**
  - [ ] Constructor with route registration
  - [ ] Routing.RegisterRoute() examples
  - [ ] Navigation setup
  - [ ] XML documentation

- [ ] **MauiProgram.cs Template Created**
  - [ ] CreateMauiApp() method
  - [ ] UseMauiApp() configuration
  - [ ] Dependency injection examples:
    - [ ] AddSingleton for Repositories
    - [ ] AddSingleton for Services
    - [ ] AddTransient for Domain classes
    - [ ] AddTransient for ViewModels
  - [ ] Database initialization
  - [ ] Platform-specific service registration
  - [ ] XML documentation

### Phase 4: Test Templates

- [ ] **DomainTests.cs Template Created**
  - [ ] xUnit test class
  - [ ] Mock IRepository and IService using NSubstitute
  - [ ] Test successful execution path
  - [ ] Test error handling from Repository
  - [ ] Test error handling from Service
  - [ ] Test caching behavior
  - [ ] Test offline fallback logic
  - [ ] Arrange-Act-Assert pattern
  - [ ] XML documentation

- [ ] **RepositoryTests.cs Template Created**
  - [ ] xUnit test class
  - [ ] In-memory SQLite database setup
  - [ ] Test CRUD operations
  - [ ] Test query filtering
  - [ ] Test error scenarios
  - [ ] Setup/teardown with database disposal
  - [ ] XML documentation

- [ ] **ServiceTests.cs Template Created**
  - [ ] xUnit test class
  - [ ] Mock HttpMessageHandler for API testing
  - [ ] Test successful API calls
  - [ ] Test error responses (404, 500, etc.)
  - [ ] Test timeout scenarios
  - [ ] Test retry logic
  - [ ] XML documentation

- [ ] **ViewModelTests.cs Template Created**
  - [ ] xUnit test class
  - [ ] Mock Domain dependencies
  - [ ] Test command execution
  - [ ] Test property change notifications
  - [ ] Test loading state management
  - [ ] Test error message handling
  - [ ] XML documentation

### Phase 5: Template Quality and Documentation

- [ ] **All Templates Use Consistent Placeholders**
  - [ ] {{ProjectName}} - Project namespace
  - [ ] {{FeatureName}} - Feature name (e.g., Products, Orders)
  - [ ] {{EntityName}} - Domain entity (e.g., Product, Order)
  - [ ] {{DomainAction}} - Verb action (e.g., Get, Create, Update, Delete)
  - [ ] {{RepositoryName}} - Repository name
  - [ ] {{ServiceName}} - Service name

- [ ] **ErrorOr Pattern Used Throughout**
  - [ ] All Domain methods return `ErrorOr<T>`
  - [ ] All Service methods return `ErrorOr<T>`
  - [ ] ViewModels use ErrorOr.Match() for result handling
  - [ ] Consistent error types (NotFound, Validation, Unexpected, etc.)

- [ ] **XML Documentation Complete**
  - [ ] All public classes documented
  - [ ] All public methods documented
  - [ ] All interfaces documented
  - [ ] Example usage included in documentation
  - [ ] Parameter descriptions
  - [ ] Return value descriptions

- [ ] **Template Files Compile Successfully**
  - [ ] No syntax errors
  - [ ] All using statements present
  - [ ] Correct namespace structure
  - [ ] Platform-appropriate code

- [ ] **Templates Follow Architecture Document**
  - [ ] Domain layer: verb-based naming, no suffix
  - [ ] Repository layer: database access only
  - [ ] Service layer: APIs and hardware only
  - [ ] ViewModel layer: thin orchestrators
  - [ ] Clean separation of concerns
  - [ ] No direct Repository/Service calls from ViewModels

## Technical Specifications

### Namespace Structure

```csharp
{{ProjectName}}
├── Domain                    // Business logic
├── Data
│   └── Repositories         // Database access
├── Services                 // APIs, hardware
├── ViewModels               // MVVM ViewModels
├── Views                    // XAML pages
└── Tests
    ├── Unit                 // Domain and ViewModel tests
    └── Integration          // Repository and Service tests
```

### Dependency Flow

```
ViewModel
    └─> Domain
           ├─> Repository (database)
           ├─> Service (APIs, hardware)
           └─> CacheService (local cache)
```

**Key Rules**:
- ✅ ViewModels call Domain layer ONLY
- ❌ ViewModels NEVER call Repository or Service directly
- ✅ Domain layer orchestrates Repository and Service
- ❌ Repository and Service NEVER call each other

### ErrorOr Pattern Examples

```csharp
// Domain layer
public async Task<ErrorOr<Product>> ExecuteAsync(int productId)
{
    var result = await _repository.GetByIdAsync(productId);
    if (result == null)
        return Error.NotFound("Product.NotFound", $"Product {productId} not found");

    return result;
}

// ViewModel layer
[RelayCommand]
private async Task LoadProductAsync()
{
    IsLoading = true;

    var result = await _getProduct.ExecuteAsync(ProductId);

    result.Match(
        value => Product = value,
        errors => ErrorMessage = errors.First().Description
    );

    IsLoading = false;
}
```

### Template Placeholder Conventions

```csharp
// Class naming
public class {{DomainAction}}{{FeatureName}}  // Example: GetProducts, CreateOrder
public interface I{{EntityName}}Repository     // Example: IProductRepository
public class {{EntityName}}Repository          // Example: ProductRepository

// Namespace
namespace {{ProjectName}}.Domain;
namespace {{ProjectName}}.Data.Repositories;
namespace {{ProjectName}}.Services;

// Method naming
Task<ErrorOr<{{EntityName}}>> ExecuteAsync({{EntityName}}Query query);
Task<{{EntityName}}?> GetByIdAsync(int id);
Task<ErrorOr<{{EntityName}}>> GetAsync<{{EntityName}}>(string endpoint);
```

### Testing Pattern Examples

```csharp
// Domain test with mocks
[Fact]
public async Task ExecuteAsync_WhenProductExists_ReturnsProduct()
{
    // Arrange
    var mockRepository = Substitute.For<IProductRepository>();
    var mockService = Substitute.For<IApiService>();
    var getProducts = new GetProducts(mockRepository, mockService);

    var expectedProduct = new Product { Id = 1, Name = "Test" };
    mockRepository.GetByIdAsync(1).Returns(expectedProduct);

    // Act
    var result = await getProducts.ExecuteAsync(1);

    // Assert
    result.IsError.Should().BeFalse();
    result.Value.Should().BeEquivalentTo(expectedProduct);
}

// Repository test with in-memory database
[Fact]
public async Task AddAsync_WhenProductValid_InsertsProduct()
{
    // Arrange
    var connection = new SQLiteAsyncConnection(":memory:");
    await connection.CreateTableAsync<Product>();
    var repository = new ProductRepository(connection);

    var product = new Product { Name = "Test", Price = 10.99m };

    // Act
    var id = await repository.AddAsync(product);

    // Assert
    id.Should().BeGreaterThan(0);
    var retrieved = await repository.GetByIdAsync(id);
    retrieved.Should().NotBeNull();
    retrieved!.Name.Should().Be("Test");
}
```

## Implementation Strategy

### Day 1: Domain and Data Access (6 hours)

**Morning (3 hours)**:
1. Create Domain.cs template with multi-tier data access pattern
2. Create IRepository.cs and Repository.cs templates
3. Create IService.cs and Service.cs templates
4. Add comprehensive XML documentation

**Afternoon (3 hours)**:
1. Create DomainTests.cs template with mocking examples
2. Create RepositoryTests.cs template with in-memory database
3. Create ServiceTests.cs template with HttpClient mocking
4. Verify templates compile

### Day 2: Presentation Layer (6 hours)

**Morning (3 hours)**:
1. Create ViewModel.cs template with CommunityToolkit patterns
2. Create Page.xaml template with data binding
3. Create Page.xaml.cs template (minimal)
4. Create ViewModelTests.cs template

**Afternoon (3 hours)**:
1. Create AppShell.xaml template with navigation
2. Create AppShell.xaml.cs template with route registration
3. Create MauiProgram.cs template with DI setup
4. Verify all templates compile together

### Day 3: Testing and Polish (4 hours)

**Morning (2 hours)**:
1. Test all templates compile successfully
2. Verify placeholder consistency
3. Verify ErrorOr pattern usage
4. Test template generation with sample values

**Afternoon (2 hours)**:
1. Review against architecture document
2. Add missing XML documentation
3. Create template usage examples
4. Final quality check

**Total Estimated Time**: 2-3 days (16 hours)

## Success Metrics

### Template Quality (Day 1-3)

**Compilation**:
- All templates compile without errors: Target 100%
- No missing using statements: Target 0 errors
- Correct namespace structure: Target 100%

**Architecture Compliance**:
- Domain layer follows verb-based naming: Target 100%
- Repository only accesses database: Target 100%
- Service only accesses external systems: Target 100%
- ViewModels only call Domain layer: Target 100%
- ErrorOr pattern used consistently: Target 100%

**Documentation Quality**:
- All public classes documented: Target 100%
- All public methods documented: Target 100%
- Example usage included: Target 100%
- Placeholder documentation clear: Target 100%

### Developer Experience (Week 1-4)

**Usability**:
- Developers can generate code from templates: Target 95%+
- Templates follow expected patterns: Survey (target 4.5/5)
- Placeholders are intuitive: Survey (target 4.5/5)
- Error messages are clear: Survey (target 4/5)

**Productivity**:
- Time saved vs manual coding: Target 50%+ reduction
- Errors in generated code: Target <5%
- Need for template modifications: Target <20%

## Risks and Mitigations

### Risk 1: Template Complexity (Medium Probability, Medium Impact)

**Risk**: Templates are too complex, developers don't understand patterns

**Mitigations**:
- Comprehensive XML documentation with examples
- Simple, clear placeholder names
- Follow established MAUI patterns
- Include usage examples in CLAUDE.md

### Risk 2: Platform-Specific Issues (Low Probability, High Impact)

**Risk**: Templates don't work on all platforms (iOS, Android, Windows, macOS)

**Mitigations**:
- Use cross-platform MAUI APIs only
- Platform-specific code in conditional compilation
- Test on multiple platforms
- Document platform limitations

### Risk 3: Outdated Dependencies (Low Probability, Medium Impact)

**Risk**: Templates use outdated NuGet packages or MAUI versions

**Mitigations**:
- Use current stable MAUI version (.NET 8)
- Document required package versions
- Include version placeholders
- Regular template updates

### Risk 4: Incomplete Error Handling (Low Probability, High Impact)

**Risk**: ErrorOr pattern not applied consistently

**Mitigations**:
- Review all return types
- Test error scenarios in test templates
- Document ErrorOr usage patterns
- Provide ErrorOr examples

## Dependencies

### Internal Dependencies

**Required Completions**:
- ✅ `docs/shared/maui-template-architecture.md` (architecture guide exists)
- ✅ Existing MAUI template structure (installer/global/templates/maui/)

**Optional Enhancements**:
- maui-appshell agents (can be created after templates)
- Template generation automation

### External Dependencies

**Required NuGet Packages** (documented in templates):
- Microsoft.Maui.Controls (≥8.0.0)
- CommunityToolkit.Mvvm (≥8.2.0)
- ErrorOr (≥2.0.0)
- SQLite-net-pcl (≥1.9.0)
- xUnit (≥2.6.0)
- NSubstitute (≥5.1.0)
- FluentAssertions (≥6.12.0)

**System Requirements**:
- .NET 8.0 SDK
- MAUI workload installed
- Platform SDKs (iOS, Android, Windows)

## Related Documents

- **Architecture Guide**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/shared/maui-template-architecture.md`
- **Existing MAUI Template**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui/`
- **MAUI Template CLAUDE.md**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui/CLAUDE.md`

## Future Enhancements (Not in Scope)

### Enhancement 1: Template Generator CLI
Command-line tool to generate code from templates:
- Interactive prompt for placeholders
- Automatic file generation
- Namespace resolution

### Enhancement 2: Additional Templates
- LoginPage template
- ListPage with search/filter
- DetailPage with edit mode
- SettingsPage template

### Enhancement 3: Blazor Hybrid Templates
Templates for Blazor Hybrid MAUI apps:
- Razor component templates
- Interop patterns
- State management

### Enhancement 4: Platform-Specific Templates
Templates for platform-specific code:
- iOS handlers
- Android services
- Windows-specific features

## Conclusion

This task creates comprehensive, production-ready code templates for the maui-appshell global template. These templates will serve as the foundation for all MAUI AppShell-based projects, ensuring consistency, quality, and productivity across the organization.

**Key Benefits**:
- ✅ Consistent architecture across all MAUI projects
- ✅ Production-ready code structure from day one
- ✅ Built-in error handling with ErrorOr pattern
- ✅ Comprehensive testing examples
- ✅ Clear separation of concerns (Domain, Repository, Service)
- ✅ Developer productivity boost (50%+ faster development)

**Status**: Ready for implementation
**Risk Level**: MEDIUM (complex but well-documented)
**Estimated ROI**: HIGH (affects all future MAUI development)

---

**Next Steps**: Begin Phase 1 implementation (Domain and Data Access templates)
