# Creating Local Templates

**Purpose**: Complete guide to creating custom .NET MAUI templates for team-specific patterns and conventions.

**Learn local templates in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Create a Custom Template in 4 Steps

```bash
# 1. Copy existing template as starting point
cp -r installer/global/templates/maui-appshell installer/local/templates/mycompany-maui

# 2. Edit manifest.json
vim installer/local/templates/mycompany-maui/manifest.json

# Update name, description:
{
  "name": "mycompany-maui",
  "description": "My Company's customized MAUI template with company patterns"
}

# 3. Customize code templates
# Edit files in templates/ directory:
# - Add company-specific patterns
# - Customize naming conventions
# - Add company libraries

# 4. Use your custom template
agentic-init mycompany-maui
```

**That's it!** Your custom template is ready for team use.

**Learn More**: See "Core Concepts" below for template structure and customization options.

---

## Core Concepts (10 minutes)

### Template Directory Structure

```
installer/local/templates/mycompany-maui/
├── manifest.json               # Template metadata and configuration
├── settings.json               # Naming conventions and layer config
├── CLAUDE.md                   # Claude Code guidance document
├── README.md                   # Human-readable template documentation
├── templates/                  # Code generation templates
│   ├── domain/
│   │   ├── query-operation.cs.template
│   │   └── command-operation.cs.template
│   ├── repository/
│   │   ├── repository-interface.cs.template
│   │   └── repository-implementation.cs.template
│   ├── service/
│   │   ├── service-interface.cs.template
│   │   └── service-implementation.cs.template
│   ├── presentation/
│   │   ├── page.xaml.template
│   │   ├── page.xaml.cs.template
│   │   └── viewmodel.cs.template
│   └── testing/
│       ├── domain-test.cs.template
│       ├── repository-test.cs.template
│       └── service-test.cs.template
└── agents/                     # Stack-specific AI agents (optional)
    ├── mycompany-domain-specialist.md
    └── mycompany-test-specialist.md
```

### Template Placeholders

All templates support these placeholders:

**Project-Level**:
- `{{ProjectName}}` - Root project name (e.g., "ShoppingApp")
- `{{RootNamespace}}` - Root namespace (e.g., "ShoppingApp")
- `{{CompanyName}}` - Your company name (custom)

**Feature-Level**:
- `{{FeatureName}}` - Feature/module name (e.g., "Products")
- `{{Entity}}` - Entity/model name (e.g., "Product")
- `{{Verb}}` - Action verb (e.g., "Get", "Create", "Update")

**Operation-Level**:
- `{{OperationName}}` - Complete operation name (e.g., "GetProducts")
- `{{ReturnType}}` - Return type (e.g., "List<Product>", "Product")
- `{{Parameters}}` - Method parameters
- `{{RequestType}}` - Request object type

### Customization Areas

#### 1. Naming Conventions

Customize naming in `settings.json`:

```json
{
  "naming": {
    "domain_operations": "{Verb}{Entity}",
    "repositories": "I{Entity}Repository",
    "services": "I{Purpose}Service",
    "viewmodels": "{Feature}ViewModel",
    "pages": "{Feature}Page"
  },
  "prohibited_suffixes": [
    "UseCase",
    "Engine",
    "Handler",
    "Processor"
  ]
}
```

#### 2. Company-Specific Patterns

Add company patterns to code templates:

```csharp
// templates/domain/query-operation.cs.template
namespace {{CompanyName}}.{{ProjectName}}.Domain.{{FeatureName}};

/// <summary>
/// {{OperationName}} - {{CompanyName}} standard domain operation
/// Complies with {{CompanyName}} Architecture Guidelines v2.0
/// </summary>
public class {{OperationName}}
{
    // Your company's standard logging
    private readonly ILogger<{{OperationName}}> _logger;
    private readonly I{{Entity}}Repository _repository;

    // Your company's standard constructor pattern
    public {{OperationName}}(
        ILogger<{{OperationName}}> logger,
        I{{Entity}}Repository repository)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
    }

    // Your company's standard method pattern
    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync()
    {
        _logger.LogInformation("Executing {{OperationName}}");

        try
        {
            var result = await _repository.GetAllAsync();

            _logger.LogInformation(
                "{{OperationName}} completed successfully. Records: {Count}",
                result.IsError ? 0 : result.Value.Count
            );

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "{{OperationName}} failed");
            return Error.Unexpected(
                "{{OperationName}}.Failed",
                ex.Message
            );
        }
    }
}
```

#### 3. Company Libraries

Include company-specific NuGet packages in README.md:

```markdown
## Required Company Packages

```xml
<PackageReference Include="MyCompany.Logging" Version="2.1.0" />
<PackageReference Include="MyCompany.ErrorHandling" Version="1.5.0" />
<PackageReference Include="MyCompany.Security" Version="3.0.0" />
```
```

#### 4. Quality Gates

Customize quality gates in `manifest.json`:

```json
{
  "quality_gates": {
    "required": [
      "All tests passing",
      "MyCompany.Security scan passing",
      "90%+ line coverage (company standard)",
      "Code review by senior developer"
    ],
    "recommended": [
      "Performance benchmarks recorded",
      "Documentation updated in Confluence"
    ]
  }
}
```

### Local vs Global Templates

**Global Templates** (`installer/global/templates/`):
- Shipped with Agentecflow
- Technology-agnostic best practices
- Updated with Agentecflow releases
- DO NOT modify (changes lost on upgrade)

**Local Templates** (`installer/local/templates/`):
- Created by your team
- Company-specific patterns
- Customized to your standards
- Preserved during Agentecflow upgrades

**Override Behavior**: Local templates with same name override global templates.

**Learn More**: See "Complete Reference" below for advanced customization and examples.

---

## Complete Reference (30+ minutes)

### Manifest.json Structure

```json
{
  "name": "mycompany-maui-appshell",
  "version": "1.0.0",
  "description": "MyCompany .NET MAUI template with AppShell, Domain pattern, and company standards",
  "template_type": "technology-stack",
  "technology": "dotnet-maui",
  "company": "MyCompany",
  "architecture": {
    "patterns": [
      "Repository Pattern (MyCompany standard)",
      "Service Pattern (MyCompany standard)",
      "Domain Pattern (verb-based operations)",
      "ErrorOr Pattern (functional error handling)",
      "MVVM Pattern",
      "Dependency Injection Pattern"
    ],
    "layers": [
      {
        "name": "Domain",
        "description": "Business operations with MyCompany logging and security",
        "patterns": ["Domain Pattern", "ErrorOr Pattern", "MyCompany Logging"],
        "naming": "{Verb}{Entity}"
      },
      {
        "name": "Repository",
        "description": "Database access with MyCompany ORM patterns",
        "patterns": ["Repository Pattern", "MyCompany ORM"],
        "naming": "I{Entity}Repository / {Entity}Repository"
      },
      {
        "name": "Service",
        "description": "External integrations with MyCompany API standards",
        "patterns": ["Service Pattern", "MyCompany API Client"],
        "naming": "I{Purpose}Service / {Purpose}Service"
      },
      {
        "name": "Presentation",
        "description": "MVVM with MyCompany UI guidelines",
        "patterns": ["MVVM Pattern", "MyCompany UI Framework"],
        "naming": "{Feature}Page / {Feature}ViewModel"
      }
    ],
    "error_handling": {
      "library": "ErrorOr + MyCompany.ErrorHandling",
      "version": "2.0+ (ErrorOr), 1.5.0 (MyCompany)",
      "pattern": "ErrorOr<TValue> with company error tracking"
    }
  },
  "templates": {
    "domain": [
      "domain/query-operation.cs.template",
      "domain/command-operation.cs.template"
    ],
    "repository": [
      "repository/repository-interface.cs.template",
      "repository/repository-implementation.cs.template"
    ],
    "service": [
      "service/service-interface.cs.template",
      "service/service-implementation.cs.template"
    ],
    "presentation": [
      "presentation/page.xaml.template",
      "presentation/page.xaml.cs.template",
      "presentation/viewmodel.cs.template"
    ],
    "testing": [
      "testing/domain-test.cs.template",
      "testing/repository-test.cs.template",
      "testing/service-test.cs.template"
    ]
  },
  "agents": [
    "mycompany-domain-specialist.md",
    "mycompany-security-specialist.md"
  ],
  "testing": {
    "framework": "xUnit + MyCompany.Testing",
    "mocking": "NSubstitute",
    "assertions": "FluentAssertions",
    "strategy": "Outside-In TDD with company test harness",
    "coverage_target": {
      "line": 90,
      "branch": 85
    }
  },
  "quality_gates": {
    "required": [
      "All tests passing",
      "90%+ line coverage (company standard)",
      "85%+ branch coverage",
      "MyCompany.Security scan passing",
      "Code review completed"
    ],
    "recommended": [
      "Performance benchmarks documented",
      "API documentation generated",
      "Confluence page updated"
    ]
  },
  "prerequisites": {
    "sdk": ".NET 8.0+",
    "workload": "dotnet workload install maui",
    "packages": [
      "ErrorOr (2.0+)",
      "CommunityToolkit.Mvvm",
      "MyCompany.Logging (2.1.0)",
      "MyCompany.ErrorHandling (1.5.0)",
      "MyCompany.Security (3.0.0)"
    ],
    "tools": [
      "MyCompany CLI tools",
      "MyCompany Security Scanner"
    ]
  },
  "created": "2025-10-15",
  "last_updated": "2025-10-15",
  "author": "MyCompany Platform Team",
  "contact": "platform-team@mycompany.com"
}
```

### Settings.json Structure

```json
{
  "naming": {
    "domain_operations": "{Verb}{Entity}",
    "repositories": "I{Entity}Repository / {Entity}Repository",
    "services": "I{Purpose}Service / {Purpose}Service",
    "viewmodels": "{Feature}ViewModel",
    "pages": "{Feature}Page",
    "tests": "{ClassName}Tests"
  },
  "prohibited_suffixes": [
    "UseCase",
    "Engine",
    "Handler",
    "Processor",
    "Command",
    "Query"
  ],
  "layers": {
    "domain": {
      "path": "src/Domain",
      "namespace": "{ProjectName}.Domain",
      "dependencies": ["Domain.Repositories", "Domain.Services"]
    },
    "data": {
      "path": "src/Data",
      "namespace": "{ProjectName}.Data",
      "dependencies": ["Domain.Repositories"]
    },
    "infrastructure": {
      "path": "src/Infrastructure",
      "namespace": "{ProjectName}.Infrastructure",
      "dependencies": ["Domain.Services"]
    },
    "presentation": {
      "path": "src/Presentation",
      "namespace": "{ProjectName}.Presentation",
      "dependencies": ["Domain"]
    }
  },
  "company_standards": {
    "logging": {
      "library": "MyCompany.Logging",
      "version": "2.1.0",
      "required_in": ["Domain", "Repository", "Service"]
    },
    "security": {
      "library": "MyCompany.Security",
      "version": "3.0.0",
      "required_in": ["Service", "Domain"]
    },
    "error_handling": {
      "library": "MyCompany.ErrorHandling",
      "version": "1.5.0",
      "required_in": ["Domain", "Repository", "Service"]
    }
  }
}
```

### Code Template Examples

#### Company-Specific Domain Operation Template

```csharp
// templates/domain/query-operation.cs.template
using ErrorOr;
using MyCompany.Logging;
using MyCompany.ErrorHandling;

namespace {{CompanyName}}.{{ProjectName}}.Domain.{{FeatureName}};

/// <summary>
/// {{OperationName}} domain operation
/// </summary>
/// <remarks>
/// Complies with {{CompanyName}} Architecture Guidelines v2.0
/// See: https://wiki.mycompany.com/architecture/domain-operations
/// </remarks>
public class {{OperationName}}
{
    private readonly ICompanyLogger<{{OperationName}}> _logger;
    private readonly I{{Entity}}Repository _repository;
    private readonly ICompanyErrorTracker _errorTracker;

    public {{OperationName}}(
        ICompanyLogger<{{OperationName}}> logger,
        I{{Entity}}Repository repository,
        ICompanyErrorTracker errorTracker)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _errorTracker = errorTracker ?? throw new ArgumentNullException(nameof(errorTracker));
    }

    /// <summary>
    /// Executes the {{OperationName}} operation
    /// </summary>
    /// <returns>Success result with {{ReturnType}} or error details</returns>
    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync()
    {
        using var _ = _logger.BeginScope("{{OperationName}}");

        _logger.LogInformation("Starting {{OperationName}} execution");

        try
        {
            var result = await _repository.GetAllAsync();

            if (result.IsError)
            {
                _logger.LogWarning(
                    "{{OperationName}} returned error: {ErrorCode}",
                    result.FirstError.Code
                );

                // Track error in company error tracking system
                await _errorTracker.TrackAsync(
                    operation: "{{OperationName}}",
                    error: result.FirstError,
                    context: new { timestamp = DateTime.UtcNow }
                );

                return result.Errors;
            }

            _logger.LogInformation(
                "{{OperationName}} completed successfully. Records: {Count}",
                result.Value.Count
            );

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "{{OperationName}} failed with exception");

            // Track exception in company error tracking system
            await _errorTracker.TrackExceptionAsync(
                operation: "{{OperationName}}",
                exception: ex
            );

            return Error.Unexpected(
                "{{Entity}}.{{OperationName}}.Failed",
                $"Operation failed: {ex.Message}"
            );
        }
    }
}
```

#### Company-Specific Repository Template

```csharp
// templates/repository/repository-implementation.cs.template
using ErrorOr;
using Microsoft.EntityFrameworkCore;
using MyCompany.Logging;
using MyCompany.ORM;

namespace {{CompanyName}}.{{ProjectName}}.Data.Repositories;

/// <summary>
/// {{Entity}}Repository implementation using MyCompany ORM patterns
/// </summary>
public class {{Entity}}Repository : CompanyRepositoryBase<{{Entity}}>, I{{Entity}}Repository
{
    private readonly ICompanyLogger<{{Entity}}Repository> _logger;
    private readonly CompanyDbContext _context;

    public {{Entity}}Repository(
        ICompanyLogger<{{Entity}}Repository> logger,
        CompanyDbContext context) : base(context)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _context = context ?? throw new ArgumentNullException(nameof(context));
    }

    public async Task<ErrorOr<List<{{Entity}}>>> GetAllAsync()
    {
        using var _ = _logger.BeginScope("GetAllAsync");

        try
        {
            _logger.LogDebug("Fetching all {{Entity}} records");

            var entities = await _context.{{Entity}}s
                .AsNoTracking()
                .OrderByDescending(e => e.CreatedAt)
                .ToListAsync();

            _logger.LogInformation("Retrieved {Count} {{Entity}} records", entities.Count);

            return entities;
        }
        catch (DbUpdateException ex)
        {
            _logger.LogError(ex, "Database error retrieving {{Entity}} records");
            return Error.Unexpected(
                "{{Entity}}.Database.Error",
                $"Database error: {ex.Message}"
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error retrieving {{Entity}} records");
            return Error.Unexpected(
                "{{Entity}}.GetAll.Failed",
                $"Failed to retrieve records: {ex.Message}"
            );
        }
    }

    public async Task<ErrorOr<{{Entity}}>> GetByIdAsync(Guid id)
    {
        using var _ = _logger.BeginScope("GetByIdAsync", new { id });

        try
        {
            _logger.LogDebug("Fetching {{Entity}} with ID: {Id}", id);

            var entity = await _context.{{Entity}}s
                .AsNoTracking()
                .FirstOrDefaultAsync(e => e.Id == id);

            if (entity == null)
            {
                _logger.LogWarning("{{Entity}} not found with ID: {Id}", id);
                return Error.NotFound(
                    "{{Entity}}.NotFound",
                    $"{{Entity}} with ID {id} not found"
                );
            }

            _logger.LogInformation("Retrieved {{Entity}} with ID: {Id}", id);

            return entity;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving {{Entity}} with ID: {Id}", id);
            return Error.Unexpected(
                "{{Entity}}.GetById.Failed",
                $"Failed to retrieve {{Entity}}: {ex.Message}"
            );
        }
    }
}
```

#### Company-Specific ViewModel Template

```csharp
// templates/presentation/viewmodel.cs.template
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using MyCompany.MAUI.ViewModels;
using MyCompany.Logging;

namespace {{CompanyName}}.{{ProjectName}}.Presentation.{{FeatureName}};

/// <summary>
/// {{ViewModelName}} - View model following MyCompany MVVM patterns
/// </summary>
public partial class {{ViewModelName}} : CompanyViewModelBase
{
    private readonly ICompanyLogger<{{ViewModelName}}> _logger;
    private readonly {{OperationName}} _operation;

    [ObservableProperty]
    private ObservableCollection<{{Entity}}> _items = new();

    [ObservableProperty]
    private bool _isBusy;

    [ObservableProperty]
    private string _errorMessage = string.Empty;

    public {{ViewModelName}}(
        ICompanyLogger<{{ViewModelName}}> logger,
        {{OperationName}} operation)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _operation = operation ?? throw new ArgumentNullException(nameof(operation));
    }

    public override async Task OnAppearingAsync()
    {
        await base.OnAppearingAsync();
        await LoadItemsAsync();
    }

    [RelayCommand]
    private async Task LoadItemsAsync()
    {
        using var _ = _logger.BeginScope("LoadItemsAsync");

        if (IsBusy)
        {
            _logger.LogDebug("Load already in progress, skipping");
            return;
        }

        IsBusy = true;
        ErrorMessage = string.Empty;

        try
        {
            _logger.LogInformation("Loading {{Entity}} items");

            var result = await _operation.ExecuteAsync();

            result.Switch(
                items =>
                {
                    Items = new ObservableCollection<{{Entity}}>(items);
                    _logger.LogInformation("Loaded {Count} items", items.Count);
                },
                errors =>
                {
                    ErrorMessage = errors.First().Description;
                    _logger.LogWarning("Failed to load items: {ErrorCode}", errors.First().Code);
                }
            );
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error loading items");
            ErrorMessage = "An unexpected error occurred. Please try again.";
        }
        finally
        {
            IsBusy = false;
        }
    }

    [RelayCommand]
    private async Task RefreshAsync()
    {
        await LoadItemsAsync();
    }
}
```

### Custom AI Agent Specifications

Create company-specific AI agents in `agents/` directory:

```markdown
<!-- agents/mycompany-domain-specialist.md -->
# MyCompany Domain Specialist Agent

## Role
Expert in MyCompany's domain operation patterns, logging standards, and error handling practices.

## Expertise
- MyCompany Architecture Guidelines v2.0
- Domain-Driven Design principles
- ErrorOr pattern with MyCompany.ErrorHandling
- MyCompany.Logging integration
- Security best practices per MyCompany standards

## Constraints
1. **ALWAYS use ICompanyLogger<T>** for logging (not ILogger<T>)
2. **ALWAYS inject ICompanyErrorTracker** for error tracking
3. **ALWAYS follow naming**: {Verb}{Entity} (no UseCase/Engine suffix)
4. **ALWAYS return ErrorOr<T>** for fallible operations
5. **ALWAYS include XML documentation** with company wiki links

## Code Generation Rules

### Domain Operation Template
```csharp
public class {Verb}{Entity}
{
    private readonly ICompanyLogger<{Verb}{Entity}> _logger;
    private readonly I{Entity}Repository _repository;
    private readonly ICompanyErrorTracker _errorTracker;

    // Constructor with null checks
    // ExecuteAsync with logging scope
    // Error tracking on failures
    // XML documentation
}
```

### Logging Pattern
```csharp
using var _ = _logger.BeginScope("{OperationName}");
_logger.LogInformation("Starting {OperationName}");
// ... operation logic
_logger.LogInformation("{OperationName} completed");
```

### Error Tracking Pattern
```csharp
await _errorTracker.TrackAsync(
    operation: "{OperationName}",
    error: result.FirstError,
    context: new { /* relevant context */ }
);
```

## Quality Standards
- 90%+ line coverage (company standard)
- All operations logged with scopes
- All errors tracked in error tracking system
- XML documentation with wiki links
- Security review for sensitive operations

## References
- [MyCompany Architecture Guidelines](https://wiki.mycompany.com/architecture)
- [Domain Operations Standard](https://wiki.mycompany.com/architecture/domain-operations)
- [Logging Standard](https://wiki.mycompany.com/architecture/logging)
- [Error Handling Standard](https://wiki.mycompany.com/architecture/error-handling)
```

### Testing Template with Company Standards

```csharp
// templates/testing/domain-test.cs.template
using FluentAssertions;
using NSubstitute;
using Xunit;
using MyCompany.Testing;

namespace {{CompanyName}}.{{ProjectName}}.Tests.Domain.{{FeatureName}};

/// <summary>
/// Tests for {{OperationName}}
/// </summary>
/// <remarks>
/// Follows MyCompany Testing Guidelines v1.5
/// See: https://wiki.mycompany.com/testing/domain-tests
/// </remarks>
[Collection("Domain Tests")]
public class {{OperationName}}Tests : CompanyTestBase
{
    private readonly ICompanyLogger<{{OperationName}}> _logger;
    private readonly I{{Entity}}Repository _repository;
    private readonly ICompanyErrorTracker _errorTracker;
    private readonly {{OperationName}} _sut;

    public {{OperationName}}Tests()
    {
        _logger = CreateMockLogger<{{OperationName}}>();
        _repository = Substitute.For<I{{Entity}}Repository>();
        _errorTracker = CreateMockErrorTracker();
        _sut = new {{OperationName}}(_logger, _repository, _errorTracker);
    }

    [Fact]
    [Trait("Category", "Unit")]
    [Trait("Priority", "P0")]
    public async Task ExecuteAsync_WhenRepositorySucceeds_ReturnsSuccess()
    {
        // Arrange
        var expected = CreateTestData<List<{{Entity}}>>();
        _repository.GetAllAsync().Returns(expected);

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeFalse();
        result.Value.Should().BeEquivalentTo(expected);

        // Verify logging (company standard)
        VerifyLoggingScope(_logger, "{{OperationName}}");
        VerifyLogMessage(_logger, LogLevel.Information, "Starting {{OperationName}}");
        VerifyLogMessage(_logger, LogLevel.Information, "completed successfully");
    }

    [Fact]
    [Trait("Category", "Unit")]
    [Trait("Priority", "P0")]
    public async Task ExecuteAsync_WhenRepositoryFails_ReturnsError()
    {
        // Arrange
        var error = Error.Unexpected("Test.Error", "Test error");
        _repository.GetAllAsync().Returns(error);

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Should().Be(error);

        // Verify error tracking (company standard)
        await _errorTracker.Received(1).TrackAsync(
            operation: "{{OperationName}}",
            error: Arg.Any<Error>(),
            context: Arg.Any<object>()
        );
    }

    [Fact]
    [Trait("Category", "Unit")]
    [Trait("Priority", "P1")]
    public async Task ExecuteAsync_WhenExceptionThrown_TracksError()
    {
        // Arrange
        _repository.GetAllAsync().Returns(Task.FromException<ErrorOr<List<{{Entity}}>>>(
            new InvalidOperationException("Test exception")
        ));

        // Act
        var result = await _sut.ExecuteAsync();

        // Assert
        result.IsError.Should().BeTrue();
        result.FirstError.Type.Should().Be(ErrorType.Unexpected);

        // Verify exception tracking (company standard)
        await _errorTracker.Received(1).TrackExceptionAsync(
            operation: "{{OperationName}}",
            exception: Arg.Any<Exception>()
        );
    }
}
```

### Distribution and Versioning

#### Version Control

```bash
# Add local templates to git
git add installer/local/templates/mycompany-maui/
git commit -m "feat: Add MyCompany MAUI template v1.0.0"
git tag mycompany-maui-v1.0.0
git push origin main --tags
```

#### Changelog Management

```json
// manifest.json
{
  "changelog": [
    {
      "version": "1.1.0",
      "date": "2025-10-20",
      "changes": [
        "Added MyCompany.Security v3.1.0 integration",
        "Updated logging patterns to use structured logging",
        "Added performance monitoring to all operations"
      ]
    },
    {
      "version": "1.0.0",
      "date": "2025-10-15",
      "changes": [
        "Initial release",
        "Company-specific Domain, Repository, Service patterns",
        "Integrated MyCompany logging, error tracking, security"
      ]
    }
  ]
}
```

#### Team Distribution

**Option 1: Git Repository** (Recommended)
```bash
# Team members clone and pull updates
git clone https://github.com/mycompany/agentecflow-templates.git installer/local/templates/
cd installer/local/templates/
git pull origin main
```

**Option 2: Package Distribution**
```bash
# Create tarball
cd installer/local/templates/
tar -czf mycompany-maui-v1.0.0.tar.gz mycompany-maui/

# Distribute via internal package manager or network share
# Team members extract
tar -xzf mycompany-maui-v1.0.0.tar.gz -C installer/local/templates/
```

**Option 3: Template Registry** (Enterprise)
```bash
# Publish to internal template registry
agentic template publish installer/local/templates/mycompany-maui

# Team members install
agentic template install mycompany-maui@1.0.0
```

---

## Examples

### Example 1: Add Company Logging Standard

**Step 1**: Edit domain operation template

```csharp
// templates/domain/query-operation.cs.template

// Add company logging
using MyCompany.Logging;

public class {{OperationName}}
{
    private readonly ICompanyLogger<{{OperationName}}> _logger;

    public {{OperationName}}(ICompanyLogger<{{OperationName}}> logger, ...)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync()
    {
        using var _ = _logger.BeginScope("{{OperationName}}");
        _logger.LogInformation("Executing {{OperationName}}");

        // ... operation logic

        _logger.LogInformation("{{OperationName}} completed");
    }
}
```

**Step 2**: Update manifest.json prerequisites

```json
{
  "prerequisites": {
    "packages": [
      "MyCompany.Logging (2.1.0)"
    ]
  }
}
```

**Step 3**: Document in CLAUDE.md

```markdown
## Company Standards

### Logging
All domain operations MUST use `ICompanyLogger<T>`:
- Begin scope at method start
- Log information at operation start and completion
- Log warnings for error results
- Log errors for exceptions
```

### Example 2: Add Company Security Patterns

**Step 1**: Create security decorator template

```csharp
// templates/domain/secured-operation.cs.template
using MyCompany.Security;

[RequirePermission("{{Entity}}.Read")]
public class {{OperationName}}
{
    private readonly ISecurityContext _securityContext;
    private readonly I{{Entity}}Repository _repository;

    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync()
    {
        // Check permissions
        if (!await _securityContext.HasPermissionAsync("{{Entity}}.Read"))
        {
            return Error.Forbidden(
                "{{Entity}}.Forbidden",
                "Insufficient permissions to read {{Entity}}"
            );
        }

        // ... operation logic
    }
}
```

**Step 2**: Update manifest.json

```json
{
  "templates": {
    "domain": [
      "domain/query-operation.cs.template",
      "domain/secured-operation.cs.template"
    ]
  },
  "prerequisites": {
    "packages": [
      "MyCompany.Security (3.0.0)"
    ]
  }
}
```

### Example 3: Add Company API Client Pattern

**Step 1**: Create API service template

```csharp
// templates/service/api-service-implementation.cs.template
using MyCompany.ApiClient;

public class {{ServiceName}} : CompanyApiServiceBase, I{{ServiceName}}
{
    private readonly ICompanyLogger<{{ServiceName}}> _logger;
    private readonly ICompanyApiClient _apiClient;

    public {{ServiceName}}(
        ICompanyLogger<{{ServiceName}}> logger,
        ICompanyApiClient apiClient) : base(apiClient)
    {
        _logger = logger;
        _apiClient = apiClient;
    }

    public async Task<ErrorOr<{{ReturnType}}>> {{MethodName}}Async({{Parameters}})
    {
        using var _ = _logger.BeginScope("{{MethodName}}Async");

        try
        {
            // Use company API client with built-in auth, retry, circuit breaker
            var response = await _apiClient.GetAsync<{{ReturnType}}>(
                endpoint: "{{Endpoint}}",
                options: new CompanyApiOptions
                {
                    Timeout = TimeSpan.FromSeconds(30),
                    RetryCount = 3,
                    CacheEnabled = true
                }
            );

            return response.MapToErrorOr();
        }
        catch (CompanyApiException ex)
        {
            _logger.LogError(ex, "API call failed: {{MethodName}}");
            return Error.Unexpected(
                "{{ServiceName}}.{{MethodName}}.Failed",
                ex.Message
            );
        }
    }
}
```

**Step 2**: Update prerequisites

```json
{
  "prerequisites": {
    "packages": [
      "MyCompany.ApiClient (4.2.0)"
    ]
  }
}
```

---

## FAQ

### Q: Should I modify global templates or create local templates?

**A**: ALWAYS create local templates. Never modify global templates - your changes will be lost during Agentecflow upgrades.

```bash
# ✅ Good - Create local template
cp -r installer/global/templates/maui-appshell installer/local/templates/mycompany-maui

# ❌ Bad - Modify global template (changes lost on upgrade)
vim installer/global/templates/maui-appshell/templates/domain/query-operation.cs.template
```

### Q: How do I share templates with my team?

**A**: Three options:
1. **Git Repository** (Recommended) - Version control and easy updates
2. **Package Distribution** - Tarball via internal package manager
3. **Template Registry** - Enterprise internal template registry

See "Distribution and Versioning" section above.

### Q: Can I override specific files in global templates?

**A**: Yes. Local templates with matching names override global templates on a file-by-file basis:

```
Local:  installer/local/templates/maui-appshell/templates/domain/query-operation.cs.template
Global: installer/global/templates/maui-appshell/templates/domain/query-operation.cs.template

Result: Local version used (overrides global)
```

### Q: How do I version my templates?

**A**: Use semantic versioning in `manifest.json` and git tags:

```json
{
  "version": "1.2.3",
  "changelog": [
    {
      "version": "1.2.3",
      "date": "2025-10-15",
      "changes": ["Bug fixes", "Updated dependencies"]
    }
  ]
}
```

```bash
git tag mycompany-maui-v1.2.3
git push origin main --tags
```

### Q: Can I create templates for other stacks (React, Python)?

**A**: Yes! Follow the same structure:

```bash
# Create React template
cp -r installer/global/templates/react installer/local/templates/mycompany-react

# Create Python template
cp -r installer/global/templates/python installer/local/templates/mycompany-python
```

Update `manifest.json` with appropriate `technology` value.

### Q: How do I test my templates before distributing?

**A**: Create a test project:

```bash
# Create project from your template
agentic-init mycompany-maui --output /tmp/test-project

# Verify generated files
cd /tmp/test-project
cat src/Domain/Products/GetProducts.cs

# Build and test
dotnet build
dotnet test
```

### Q: Can I add custom placeholders?

**A**: Yes, define custom placeholders in `settings.json`:

```json
{
  "custom_placeholders": {
    "CompanyName": "MyCompany",
    "CompanyNamespace": "MyCompany.Platform",
    "CompanyWikiUrl": "https://wiki.mycompany.com"
  }
}
```

Use in templates: `{{CompanyName}}`, `{{CompanyWikiUrl}}`

---

## Related Documentation

- [Domain Layer Pattern](../patterns/domain-layer-pattern.md) - Domain operation patterns
- [MAUI Template Selection](./maui-template-selection.md) - Choose base template
- [Engine-to-Domain Migration](../migration/engine-to-domain.md) - Migrate UseCase/Engine to Domain
- [Agentecflow Template Specification](https://agentecflow.dev/docs/templates) - Template format reference

---

**Last Updated**: 2025-10-15
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
