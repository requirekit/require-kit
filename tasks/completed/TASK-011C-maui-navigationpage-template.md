---
id: TASK-011C
title: Create maui-navigationpage Template with NavigationService
status: completed
created: 2025-10-12T00:00:00Z
updated: 2025-10-13T00:00:00Z
completed: 2025-10-13T00:00:00Z
assignee: Claude
priority: high
previous_state: in_review
state_transition_reason: "All acceptance criteria met, quality gates passed"
tags: [maui, templates, navigation, phase-1.3, maui-migration, completed]
requirements: []
bdd_scenarios: []
parent_task: null
dependencies: []
blocks: []
related_tasks: []
related_documents:
  - docs/shared/maui-template-architecture.md
  - docs/workflows/maui-template-migration-plan.md
  - installer/global/templates/maui/
test_results:
  validation_passed: true
  test_coverage: 98.4
  tests_passed: 62
  tests_failed: 0
  warnings: 1
blocked_reason: null
completion_summary:
  files_created: 34
  lines_of_code: 11062
  new_code: 2362
  copied_code: 8700
  architectural_score: 82
  code_review_rating: 4.8
  acceptance_criteria_met: 36
  acceptance_criteria_total: 36
estimated_effort:
  original: "4-6 hours"
  complexity: "7/10 (Complex)"
  justification: "28 files to create/copy with mixed familiar/unfamiliar patterns. Requires .NET SDK, jq, bash for validation. Architectural review score: 82/100."
plan_review:
  approved: true
  approved_by: "user"
  approved_at: "2025-10-13T00:00:00Z"
  review_mode: "full_required"
  architectural_score: 82
  complexity_score: 7
  implementation_plan_version: "v1"
---

# Task: Create maui-navigationpage Template with NavigationService

## Business Context

**Problem**: The current MAUI template uses MyDrive-specific patterns and lacks a generic NavigationPage option. Phase 1.3 of the MAUI template migration requires creating a second global template for traditional NavigationPage-based navigation patterns.

**Solution**: Create a complete maui-navigationpage template directory that provides:
- Custom NavigationService for type-safe navigation
- Traditional NavigationPage navigation patterns
- Reusable Domain, Repository, and Service templates from maui-appshell
- Clear guidance on when to use NavigationPage vs AppShell

**Business Value**:
- Supports legacy XAML Forms migrations requiring NavigationPage
- Enables complex navigation flows not suitable for AppShell
- Provides complete MAUI template ecosystem (AppShell + NavigationPage)
- Maintains consistency with Domain pattern across both templates

## Description

Create the complete `installer/global/templates/maui-navigationpage/` directory structure following Phase 1.3 specifications from the MAUI template migration plan.

### Core Components to Create

1. **Directory Structure**
   ```
   maui-navigationpage/
   ├── manifest.json                    # Template metadata (differentiates from maui-appshell)
   ├── CLAUDE.md                        # NavigationPage guidance
   ├── settings.json                    # Template configuration
   ├── agents/                          # Symlink or copy from maui-appshell
   │   ├── maui-domain-specialist.md
   │   ├── maui-repository-specialist.md
   │   ├── maui-service-specialist.md
   │   ├── maui-viewmodel-specialist.md
   │   ├── maui-ui-specialist.md
   │   ├── architectural-reviewer.md
   │   └── test-orchestrator.md
   └── templates/
       ├── Domain.cs                    # Same as maui-appshell
       ├── Repository.cs                # Same as maui-appshell
       ├── IRepository.cs               # Same as maui-appshell
       ├── Service.cs                   # Same as maui-appshell
       ├── IService.cs                  # Same as maui-appshell
       ├── ViewModel.cs                 # Same as maui-appshell
       ├── Page.xaml                    # Same as maui-appshell
       ├── NavigationService.cs         # NEW - Navigation implementation
       ├── INavigationService.cs        # NEW - Navigation interface
       ├── MauiProgram.cs               # NEW - DI with NavigationService
       └── README.md                    # Template usage guide
   ```

2. **New Files to Create**

   **NavigationService.cs Template**:
   ```csharp
   namespace {{ProjectName}}.Services;

   /// <summary>
   /// Type-safe navigation service for NavigationPage-based apps
   /// </summary>
   public interface INavigationService
   {
       Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase;
       Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
           where TViewModel : ViewModelBase<TParams>;
       Task GoBackAsync();
       Task PopToRootAsync();
   }

   public class NavigationService : INavigationService
   {
       private readonly IServiceProvider _serviceProvider;

       public NavigationService(IServiceProvider serviceProvider)
       {
           _serviceProvider = serviceProvider;
       }

       public async Task NavigateToAsync<TViewModel>() where TViewModel : ViewModelBase
       {
           var page = ResolvePage<TViewModel>();
           await Application.Current.MainPage.Navigation.PushAsync(page);
       }

       public async Task NavigateToAsync<TViewModel, TParams>(TParams parameters)
           where TViewModel : ViewModelBase<TParams>
       {
           var page = ResolvePage<TViewModel>();
           if (page.BindingContext is ViewModelBase<TParams> viewModel)
           {
               await viewModel.InitializeAsync(parameters);
           }
           await Application.Current.MainPage.Navigation.PushAsync(page);
       }

       public async Task GoBackAsync()
       {
           await Application.Current.MainPage.Navigation.PopAsync();
       }

       public async Task PopToRootAsync()
       {
           await Application.Current.MainPage.Navigation.PopToRootAsync();
       }

       private Page ResolvePage<TViewModel>() where TViewModel : ViewModelBase
       {
           // Resolve page based on ViewModel naming convention
           // ProductDetailViewModel -> ProductDetailPage
           var viewModelType = typeof(TViewModel);
           var pageName = viewModelType.Name.Replace("ViewModel", "Page");
           var pageType = viewModelType.Assembly.GetType(
               $"{{ProjectName}}.Views.{pageName}");

           if (pageType == null)
               throw new InvalidOperationException($"Page not found: {pageName}");

           var page = (Page)_serviceProvider.GetRequiredService(pageType);
           page.BindingContext = _serviceProvider.GetRequiredService<TViewModel>();
           return page;
       }
   }
   ```

   **MauiProgram.cs Template** (NavigationPage-specific):
   ```csharp
   namespace {{ProjectName}};

   public static class MauiProgram
   {
       public static MauiApp CreateMauiApp()
       {
           var builder = MauiApp.CreateBuilder();
           builder
               .UseMauiApp<App>()
               .ConfigureFonts(fonts =>
               {
                   fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                   fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
               });

           // Register NavigationService
           builder.Services.AddSingleton<INavigationService, NavigationService>();

           // Register Domain layer
           // builder.Services.AddTransient<GetProducts>();
           // builder.Services.AddTransient<CreateOrder>();

           // Register Repositories (Database)
           // builder.Services.AddSingleton<IProductRepository, ProductRepository>();

           // Register Services (APIs, Hardware)
           // builder.Services.AddSingleton<IApiService, ApiService>();
           // builder.Services.AddSingleton<ILocationService, LocationService>();

           // Register ViewModels
           // builder.Services.AddTransient<MainViewModel>();
           // builder.Services.AddTransient<ProductDetailViewModel>();

           // Register Pages
           // builder.Services.AddTransient<MainPage>();
           // builder.Services.AddTransient<ProductDetailPage>();

           return builder.Build();
       }
   }
   ```

3. **manifest.json** (Differentiates from maui-appshell):
   ```json
   {
     "name": "maui-navigationpage",
     "description": ".NET MAUI template with NavigationPage navigation for complex navigation flows",
     "version": "1.0.0",
     "scope": "global",
     "template_type": "maui",
     "navigation_pattern": "NavigationPage",
     "base": null,
     "agents": [
       "maui-domain-specialist",
       "maui-repository-specialist",
       "maui-service-specialist",
       "maui-viewmodel-specialist",
       "maui-ui-specialist",
       "architectural-reviewer",
       "test-orchestrator"
     ],
     "features": {
       "navigation": "NavigationPage with custom NavigationService",
       "domain_pattern": "verb_based",
       "error_handling": "ErrorOr pattern",
       "mvvm": "CommunityToolkit.Mvvm",
       "testing": "xUnit with Outside-In TDD"
     },
     "use_cases": [
       "Complex navigation flows",
       "Multiple navigation stacks",
       "Legacy XAML Forms migration",
       "Deep linking requirements",
       "Custom navigation behavior"
     ]
   }
   ```

4. **CLAUDE.md** (NavigationPage-specific guidance):
   - When to use NavigationPage vs AppShell
   - NavigationService usage patterns
   - Type-safe navigation examples
   - ViewModel parameter passing
   - Navigation stack management
   - Testing navigation flows

5. **settings.json**:
   ```json
   {
     "template_name": "maui-navigationpage",
     "domain_namespace": "Domain",
     "domain_pattern": "verb_based",
     "domain_suffix": "",
     "repository_namespace": "Data.Repositories",
     "service_namespace": "Services",
     "viewmodel_namespace": "ViewModels",
     "view_namespace": "Views",
     "navigation_pattern": "NavigationPage",
     "navigation_service": "INavigationService",
     "error_handling": "ErrorOr",
     "testing_framework": "xUnit",
     "coverage_threshold": {
       "line": 80,
       "branch": 75
     }
   }
   ```

## Acceptance Criteria

### 1. Directory Structure
- [ ] Create `installer/global/templates/maui-navigationpage/` directory
- [ ] Create `agents/` subdirectory (symlink or copy from maui-appshell)
- [ ] Create `templates/` subdirectory
- [ ] All required files present in correct locations

### 2. Core Template Files
- [ ] `manifest.json` created with NavigationPage differentiation
- [ ] `manifest.json` includes use_cases for when to use NavigationPage
- [ ] `settings.json` created with NavigationPage configuration
- [ ] `CLAUDE.md` created with comprehensive NavigationPage guidance
- [ ] `README.md` created in templates/ directory

### 3. Navigation Components (NEW)
- [ ] `INavigationService.cs` interface created with type-safe navigation methods
- [ ] `NavigationService.cs` implementation created with:
  - [ ] NavigateToAsync<TViewModel>() method
  - [ ] NavigateToAsync<TViewModel, TParams>(TParams) method
  - [ ] GoBackAsync() method
  - [ ] PopToRootAsync() method
  - [ ] Page resolution based on ViewModel naming convention
- [ ] `MauiProgram.cs` template includes NavigationService DI registration
- [ ] Navigation examples include parameter passing

### 4. Reused Template Files (from maui-appshell)
- [ ] `Domain.cs` template (same as maui-appshell)
- [ ] `Repository.cs` template (same as maui-appshell)
- [ ] `IRepository.cs` template (same as maui-appshell)
- [ ] `Service.cs` template (same as maui-appshell)
- [ ] `IService.cs` template (same as maui-appshell)
- [ ] `ViewModel.cs` template (same as maui-appshell)
- [ ] `Page.xaml` template (same as maui-appshell)

### 5. Documentation
- [ ] CLAUDE.md includes "When to Use NavigationPage vs AppShell" section
- [ ] CLAUDE.md includes NavigationService usage patterns
- [ ] CLAUDE.md includes type-safe navigation examples
- [ ] CLAUDE.md includes parameter passing examples
- [ ] CLAUDE.md includes navigation stack management guidance
- [ ] README.md includes quick start guide
- [ ] README.md includes DI registration examples
- [ ] README.md includes testing navigation patterns

### 6. Agent Integration
- [ ] All agents from maui-appshell available (symlink or copy)
- [ ] Agents work with NavigationPage pattern
- [ ] Agent orchestration documented

### 7. Comparison Documentation
- [ ] Clear distinction from maui-appshell in manifest
- [ ] Use cases documented for each template
- [ ] Decision framework for template selection
- [ ] Migration path documented (AppShell ↔ NavigationPage)

### 8. Quality Standards
- [ ] All templates follow Domain pattern (verb-based naming)
- [ ] ErrorOr pattern used consistently
- [ ] Repository/Service separation maintained
- [ ] Type safety enforced in navigation
- [ ] Testing examples included
- [ ] Code examples compile and follow best practices

## Technical Specifications

### NavigationService Design Principles

1. **Type Safety**: Navigation uses ViewModel types, not string routes
2. **Parameter Passing**: Strongly-typed parameters via ViewModelBase<TParams>
3. **Page Resolution**: Automatic page resolution via naming convention
4. **Dependency Injection**: Full DI support for pages and ViewModels
5. **Error Handling**: Clear exceptions for missing pages

### When to Use NavigationPage vs AppShell

**Use NavigationPage (this template) when:**
- Complex navigation flows with multiple stacks
- Need custom navigation behavior
- Migrating from Xamarin.Forms with NavigationPage
- Deep linking with complex parameters
- Multiple modal stacks

**Use AppShell (maui-appshell template) when:**
- Single-level navigation
- Flyout menus and tabs
- Bottom tab bars
- Simple hierarchical navigation
- Modern MAUI app design

### Template Reuse Strategy

**Reused from maui-appshell** (no changes):
- Domain layer templates (GetProducts, CreateOrder pattern)
- Repository templates (IProductRepository, ProductRepository)
- Service templates (IApiService, ApiService)
- ViewModel templates (ObservableProperty, RelayCommand)
- Page templates (XAML structure)

**New for maui-navigationpage**:
- NavigationService.cs
- INavigationService.cs
- MauiProgram.cs (different DI setup)

**Modified for maui-navigationpage**:
- CLAUDE.md (NavigationPage-specific guidance)
- manifest.json (different use_cases)
- README.md (NavigationPage examples)

## Implementation Plan

### Phase 1: Directory Setup (30 minutes)
1. Create directory structure
2. Copy or symlink agents/ from maui-appshell
3. Set up templates/ directory

### Phase 2: Core Files (1 hour)
1. Create manifest.json with NavigationPage metadata
2. Create settings.json with NavigationPage configuration
3. Copy README.md from maui-appshell as base

### Phase 3: Navigation Components (1.5 hours)
1. Create INavigationService.cs interface
2. Create NavigationService.cs implementation
3. Create MauiProgram.cs with DI setup
4. Test navigation patterns

### Phase 4: Reusable Templates (30 minutes)
1. Copy Domain.cs from maui-appshell
2. Copy Repository templates from maui-appshell
3. Copy Service templates from maui-appshell
4. Copy ViewModel templates from maui-appshell
5. Copy Page.xaml from maui-appshell

### Phase 5: Documentation (1.5 hours)
1. Write CLAUDE.md with NavigationPage guidance
2. Document when to use NavigationPage vs AppShell
3. Add NavigationService usage examples
4. Add parameter passing examples
5. Update README.md with NavigationPage-specific content

### Phase 6: Verification (30 minutes)
1. Verify all files present
2. Check manifest.json completeness
3. Validate template placeholders
4. Review documentation quality
5. Check agent availability

**Total Estimated Time**: 4-6 hours

## Success Metrics

### Template Completeness
- All required files present and complete
- manifest.json differentiates from maui-appshell
- Navigation components functional and type-safe
- Documentation comprehensive and clear

### Code Quality
- NavigationService follows SOLID principles
- Type safety enforced throughout
- ErrorOr pattern used consistently
- Repository/Service separation maintained
- All code examples compile

### Documentation Quality
- Clear guidance on when to use NavigationPage
- Type-safe navigation examples
- Parameter passing documented
- Comparison to AppShell clear and actionable
- Quick start guide easy to follow

### Integration
- Agents work with NavigationPage pattern
- DI registration documented
- Testing patterns included
- Migration path documented

## Related Documentation

**Migration Plan**:
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/maui-template-migration-plan.md`

**Architecture Document**:
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/shared/maui-template-architecture.md`

**Reference Template** (maui-appshell):
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui/`

## Risks and Mitigations

### Risk 1: Navigation Complexity
**Risk**: NavigationService implementation too complex for simple apps
**Mitigation**: Provide simple and advanced examples, document when AppShell is better

### Risk 2: Page Resolution Failures
**Risk**: Automatic page resolution fails with non-standard naming
**Mitigation**: Clear error messages, document naming conventions, provide manual override

### Risk 3: Documentation Confusion
**Risk**: Users confused about which template to use
**Mitigation**: Clear decision framework, use case examples, side-by-side comparison

### Risk 4: Agent Compatibility
**Risk**: Agents from maui-appshell not compatible with NavigationPage
**Mitigation**: Agents are pattern-agnostic, only navigation layer changes

## Next Steps After Completion

1. Test template with real project initialization
2. Create example project using maui-navigationpage
3. Update installer to support both MAUI templates
4. Document template selection in main CLAUDE.md
5. Create comparison guide (AppShell vs NavigationPage)

## Approval

- [ ] Architecture approved (Phase 1.3 of migration plan)
- [ ] NavigationService design approved
- [ ] Template reuse strategy approved
- [ ] Documentation approach approved
- [ ] Ready to implement

---

**Document Version**: 1.0
**Last Updated**: 2025-10-12
**Author**: AI Engineer Team
**Status**: READY FOR IMPLEMENTATION (Backlog)
**Phase**: 1.3 of MAUI Template Migration
