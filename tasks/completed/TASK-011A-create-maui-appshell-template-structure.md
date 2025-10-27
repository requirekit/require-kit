---
id: TASK-011A
title: Create maui-appshell template structure with Domain pattern
status: completed
created: 2025-10-12T00:00:00Z
updated: 2025-10-12T10:50:00Z
completed_at: 2025-10-12T10:50:00Z
priority: high
previous_state: in_review
state_transition_reason: "All quality gates passed - task completed successfully"
phase: "1.1"
migration_plan: maui-template-migration-plan.md
estimated_complexity: 6
complexity_level: medium
estimated_hours: 4
actual_hours: 0.25
approved: true
approved_by: "user"
approved_at: "2025-10-12T10:35:00Z"
review_mode: "full_required"
complexity_evaluation:
  score: 8
  level: "complex"
  review_mode: "FULL_REQUIRED"
architectural_review:
  score: 88
  status: "approved"
code_review:
  score: 95
  status: "approved"
test_results:
  status: "passed"
  coverage: 100
  files_verified: 20
related_docs:
  - docs/shared/maui-template-architecture.md
  - docs/workflows/maui-template-migration-plan.md
---

# Create maui-appshell template structure with Domain pattern

## Task Description

Create the complete `maui-appshell` template directory structure with Domain pattern implementation (verb-based naming, no UseCase/Engine suffix). This is Phase 1.1 of the MAUI template migration plan.

## Requirements

### Directory Structure
- [ ] Create `installer/global/templates/maui-appshell/` directory structure
- [ ] Create `agents/` subdirectory for specialized agents
- [ ] Create `templates/` subdirectory for code templates
- [ ] Set up proper directory permissions

### Template Configuration Files
- [ ] Create `manifest.json` with complete template metadata
- [ ] Create `CLAUDE.md` with comprehensive AppShell navigation guidance
- [ ] Create `settings.json` for template configuration
- [ ] Include version information and dependencies

### Domain Pattern Implementation
- [ ] Include Domain pattern examples (verb-based naming: GetProducts, CreateOrder, UpdateUserProfile)
- [ ] NO UseCase or Engine suffix in naming
- [ ] Use ErrorOr pattern for functional error handling
- [ ] Include composition examples (Domain using Repositories + Services)

### Repository Pattern (Database Access)
- [ ] Create Repository pattern examples
- [ ] Interface-based design (IProductRepository)
- [ ] SQLite/LiteDB examples
- [ ] ONLY database access (no API calls)
- [ ] Clear error handling

### Service Pattern (APIs and Hardware)
- [ ] Create Service pattern examples
- [ ] Interface-based design (IApiService, ILocationService, ICacheService)
- [ ] HTTP API client examples
- [ ] Hardware service examples (GPS, Camera, Sensors)
- [ ] ONLY external systems (no database access)

### AppShell Navigation
- [ ] AppShell.xaml example with routing
- [ ] Navigation examples in ViewModels
- [ ] Route registration patterns
- [ ] Parameter passing examples
- [ ] Deep linking support

### CLAUDE.md Content
- [ ] Clear guidance on when to use AppShell vs NavigationPage
- [ ] Domain layer best practices
- [ ] Repository vs Service separation
- [ ] Navigation patterns
- [ ] Testing strategies
- [ ] ErrorOr pattern usage
- [ ] DI registration examples

## Acceptance Criteria

1. **Directory Structure**
   - Complete `maui-appshell/` directory created
   - All subdirectories (agents/, templates/) present
   - Matches specification in `maui-template-architecture.md`

2. **manifest.json**
   - Valid JSON format
   - Contains all required fields (name, description, version, scope)
   - Specifies navigation type (AppShell)
   - Lists all dependencies

3. **CLAUDE.md**
   - Comprehensive AppShell navigation guidance
   - Clear Domain pattern examples with verb-based naming
   - Repository (DB) vs Service (API/hardware) separation explained
   - Code examples for each layer
   - Testing strategies included

4. **settings.json**
   - Valid JSON format
   - Default namespace configuration
   - Testing framework settings
   - Quality gate thresholds

5. **Domain Pattern**
   - Examples use verb-based naming (GetProducts, CreateOrder)
   - NO UseCase or Engine suffix
   - Clear separation of concerns
   - ErrorOr pattern throughout

6. **Repository Pattern**
   - Clear database-only examples
   - Interface-based design
   - NO API calls in repositories
   - Proper error handling

7. **Service Pattern**
   - Clear external system examples (API, hardware)
   - Interface-based design
   - NO database access in services
   - Proper error handling

## Implementation Notes

### Directory Structure
```
installer/global/templates/maui-appshell/
├── manifest.json                       # Template metadata
├── CLAUDE.md                          # Comprehensive guidance
├── settings.json                      # Template configuration
├── agents/                            # Specialized agents (Phase 2)
│   ├── maui-domain-specialist.md
│   ├── maui-repository-specialist.md
│   ├── maui-service-specialist.md
│   ├── maui-viewmodel-specialist.md
│   ├── maui-ui-specialist.md
│   ├── architectural-reviewer.md
│   └── test-orchestrator.md
└── templates/                         # Code templates
    ├── Domain.cs                      # Business logic template
    ├── Repository.cs                  # Database template
    ├── IRepository.cs                 # Repository interface
    ├── Service.cs                     # External service template
    ├── IService.cs                    # Service interface
    ├── ViewModel.cs                   # ViewModel template
    ├── Page.xaml                      # XAML page
    ├── AppShell.xaml                  # Shell navigation
    ├── MauiProgram.cs                 # DI setup
    └── README.md                      # Template usage guide
```

### manifest.json Example
```json
{
  "name": "maui-appshell",
  "description": "Modern .NET MAUI template with AppShell navigation and Domain pattern",
  "version": "1.0.0",
  "scope": "global",
  "navigation_type": "AppShell",
  "architecture": {
    "domain_pattern": "verb-based",
    "domain_suffix": "none",
    "repository_pattern": "interface-based",
    "service_pattern": "interface-based"
  },
  "dependencies": {
    "dotnet": ">=8.0",
    "maui": ">=8.0",
    "packages": [
      "ErrorOr",
      "CommunityToolkit.Mvvm",
      "sqlite-net-pcl"
    ]
  },
  "testing": {
    "framework": "xunit",
    "coverage_tool": "coverlet",
    "ui_testing": "appium"
  }
}
```

### Key Patterns to Include

**Domain Layer (Verb-Based)**:
- `GetProducts` - Retrieve products with caching
- `CreateOrder` - Create new order
- `UpdateUserProfile` - Update user information
- `ValidatePayment` - Payment validation logic

**Repository Layer (Database)**:
- `IProductRepository` / `ProductRepository`
- `IOrderRepository` / `OrderRepository`
- `IUserRepository` / `UserRepository`

**Service Layer (External Systems)**:
- `IApiService` / `ApiService` - HTTP API client
- `ILocationService` / `LocationService` - GPS hardware
- `ICacheService` / `CacheService` - In-memory cache
- `IAuthService` / `AuthService` - Authentication

## Related Files

- **Architecture Spec**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/shared/maui-template-architecture.md`
- **Migration Plan**: `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/maui-template-migration-plan.md`

## Next Phase

After completing this task:
- Phase 2: Create specialized agents (TASK-012)
- Phase 3: Create maui-navigationpage template (TASK-013)
- Phase 4: Migrate MyDrive to local template (TASK-014)

## Success Metrics

- Directory structure 100% complete
- All configuration files valid JSON
- CLAUDE.md provides clear, actionable guidance
- Domain pattern examples are clear and follow verb-based naming
- Clear separation between Repository (DB) and Service (API/hardware)
- Template ready for use in new projects
