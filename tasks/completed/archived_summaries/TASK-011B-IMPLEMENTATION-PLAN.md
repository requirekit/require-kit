# TASK-011B Implementation Plan: MAUI AppShell Template Code

## Executive Summary

**Task**: Create/validate all code template files for maui-appshell template
**Complexity**: 7/10 (Complex - 13 interdependent template files)
**Current State**: **13 template files ALREADY EXIST** in `/installer/global/templates/maui-appshell/templates/`
**Actual Scope**: **VALIDATION AND ENHANCEMENT** (not creation from scratch)

## Critical Discovery

From git status analysis, the following templates **ALREADY EXIST**:
```
installer/global/templates/maui-appshell/templates/
├── domain/
│   ├── command-operation.cs.template ✅ EXISTS
│   └── query-operation.cs.template ✅ EXISTS
├── presentation/
│   ├── navigation-service.cs.template ✅ EXISTS
│   ├── page.xaml.cs.template ✅ EXISTS
│   ├── page.xaml.template ✅ EXISTS
│   └── viewmodel.cs.template ✅ EXISTS
├── repository/
│   ├── repository-implementation.cs.template ✅ EXISTS
│   └── repository-interface.cs.template ✅ EXISTS
├── service/
│   ├── service-implementation.cs.template ✅ EXISTS
│   └── service-interface.cs.template ✅ EXISTS
└── testing/
    ├── domain-test.cs.template ✅ EXISTS
    ├── repository-test.cs.template ✅ EXISTS
    └── service-test.cs.template ✅ EXISTS
```

**Task Redefinition**: This is a **VALIDATION AND ENHANCEMENT** task, not a creation task.

## Phase 1: Template Validation (Current State Analysis)

### 1.1 Initial Code Review Results

**Existing Templates Quality Assessment**:

| Template | Status | Quality | Issues Found |
|----------|--------|---------|--------------|
| `domain/command-operation.cs.template` | ✅ | Good | Minor: ArgumentNullException (should avoid exceptions) |
| `domain/query-operation.cs.template` | ✅ | Good | Minor: ArgumentNullException (should avoid exceptions) |
| `presentation/viewmodel.cs.template` | ✅ | Excellent | CommunityToolkit patterns correct |
| `presentation/page.xaml.template` | ✅ | Good | Needs StaticResource verification |
| `presentation/page.xaml.cs.template` | ✅ | Unknown | Need to review |
| `presentation/navigation-service.cs.template` | ✅ | Unknown | Need to review |
| `repository/repository-interface.cs.template` | ✅ | Excellent | Perfect ErrorOr usage |
| `repository/repository-implementation.cs.template` | ✅ | Unknown | Need to review |
| `service/service-interface.cs.template` | ✅ | Good | Clean interface design |
| `service/service-implementation.cs.template` | ✅ | Unknown | Need to review |
| `testing/domain-test.cs.template` | ✅ | Excellent | xUnit + NSubstitute + FluentAssertions |
| `testing/repository-test.cs.template` | ✅ | Unknown | Need to review |
| `testing/service-test.cs.template` | ✅ | Unknown | Need to review |

### 1.2 Missing Templates Analysis

**Critical Missing**: ViewModel test template!

The manifest.json lists:
```json
"testing": [
  "testing/domain-test.cs.template",
  "testing/repository-test.cs.template",
  "testing/service-test.cs.template"
]
```

**Gap**: No `testing/viewmodel-test.cs.template` exists, but MVVM testing is critical for Outside-In TDD.

**Recommendation**: Create `testing/viewmodel-test.cs.template` as new file.

### 1.3 Verification Checklist Against Requirements

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Verb-based naming (no UseCase suffix) | ✅ | Templates use `{{OperationName}}` |
| ErrorOr pattern throughout | ✅ | All interfaces return `ErrorOr<T>` |
| Clean layer separation | ✅ | Domain/Repository/Service/Presentation clear |
| Multi-tier data access | ⚠️ | Need to verify repository implementation |
| CommunityToolkit MVVM | ✅ | `[ObservableProperty]`, `[RelayCommand]` |
| Comprehensive XML docs | ✅ | All reviewed templates have `<summary>` |
| Outside-In TDD templates | ⚠️ | Missing ViewModel test template |
| No exception throwing | ❌ | `ArgumentNullException` found in 2 templates |

## Phase 2: Gap Analysis & Enhancement Requirements

### 2.1 Critical Issues to Fix

**Issue 1: ArgumentNullException in Constructors**
- **Location**: `domain/command-operation.cs.template`, `domain/query-operation.cs.template`, `presentation/viewmodel.cs.template`
- **Problem**: Lines like `throw new ArgumentNullException(nameof(repository))` violate "no exception throwing" principle
- **Fix**: Remove or replace with ErrorOr validation in ExecuteAsync
- **Impact**: Affects 3 templates

**Issue 2: Missing ViewModel Test Template**
- **Location**: `testing/` directory
- **Problem**: Outside-In TDD requires acceptance tests (ViewModel tests) first
- **Fix**: Create new `testing/viewmodel-test.cs.template`
- **Impact**: Critical for test-driven workflow

**Issue 3: Unverified Implementation Templates**
- **Location**: `repository/repository-implementation.cs.template`, `service/service-implementation.cs.template`
- **Problem**: Haven't reviewed implementation details (error handling, patterns)
- **Fix**: Full code review and enhancement
- **Impact**: Affects 2 templates

### 2.2 Enhancement Opportunities

**Enhancement 1: Multi-Tier Data Access Pattern**
Current repository template needs to show cache → database → API pattern:
```csharp
public async Task<ErrorOr<List<Product>>> GetAllAsync()
{
    // 1. Try cache first
    var cached = await _cache.GetAsync<List<Product>>("products");
    if (cached != null) return cached;

    // 2. Try database
    var dbResult = await _context.Products.ToListAsync();
    if (dbResult.Any())
    {
        await _cache.SetAsync("products", dbResult, TimeSpan.FromMinutes(5));
        return dbResult;
    }

    // 3. Fallback to API (if service available)
    return await _apiService.GetProductsAsync();
}
```

**Enhancement 2: Retry Logic in Service Template**
Service template should include Polly retry pattern:
```csharp
private readonly IAsyncPolicy<HttpResponseMessage> _retryPolicy = Policy
    .HandleResult<HttpResponseMessage>(r => !r.IsSuccessStatusCode)
    .WaitAndRetryAsync(3, retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
```

**Enhancement 3: Placeholder Consistency**
Audit all placeholders for consistency:
- `{{ProjectName}}` vs `{{RootNamespace}}`
- `{{FeatureName}}` vs `{{Feature}}`
- `{{OperationName}}` vs `{{Verb}}{{Entity}}`

### 2.3 Documentation Requirements

**Missing Documentation**:
1. **Template Usage Guide**: How to use each template with examples
2. **Placeholder Reference**: Complete list with descriptions
3. **Architecture Decision Records**: Why ErrorOr? Why verb-based naming?
4. **Testing Strategy Document**: Outside-In TDD workflow with these templates

## Phase 3: Implementation Strategy

### 3.1 Validation Phase (Read-Only Analysis)

**Goal**: Thoroughly review all existing templates without modifications.

**Tasks**:
1. Read and analyze remaining 6 unreviewed templates
2. Create template quality scorecard
3. Document all placeholder usage
4. Map template interdependencies
5. Identify compilation risks

**Deliverable**: Comprehensive validation report with issues categorized by severity.

### 3.2 Enhancement Phase (Modifications)

**Goal**: Fix critical issues and add missing templates.

**Priority 1 - Critical Fixes** (Required for acceptance):
1. Remove `ArgumentNullException` from 3 templates
2. Create `testing/viewmodel-test.cs.template`
3. Fix any ErrorOr pattern violations
4. Ensure XML documentation completeness

**Priority 2 - High-Value Enhancements** (Recommended):
1. Add multi-tier data access to repository implementation
2. Add retry logic to service implementation
3. Standardize placeholder naming
4. Add navigation service tests

**Priority 3 - Nice-to-Have** (Optional):
1. Add advanced error handling examples
2. Add performance optimization comments
3. Add security best practice comments
4. Add accessibility comments in XAML

### 3.3 Verification Phase (Quality Assurance)

**Goal**: Ensure all templates compile and follow patterns.

**Tasks**:
1. Create sample project from templates
2. Verify all templates compile
3. Run generated tests (should pass)
4. Verify placeholder substitution works
5. Check XML documentation renders correctly

**Acceptance Criteria**:
- All 14 templates compile without errors
- Generated code passes all quality gates
- All placeholders properly documented
- Complete test coverage (unit + integration)

## Phase 4: Detailed File-by-File Analysis

### 4.1 Domain Layer Templates

#### `domain/command-operation.cs.template`
- **Status**: ✅ Exists, 65 lines
- **Quality**: 8/10
- **Issues**:
  - Line 15: `throw new ArgumentNullException` (violates no-exceptions rule)
  - Line 54: `Result.Success` should be `ErrorOr<Success>.From(default)`
- **Dependencies**: `I{{Entity}}Repository`, ErrorOr package
- **Placeholders**: `{{ProjectName}}`, `{{FeatureName}}`, `{{OperationName}}`, `{{Entity}}`, `{{ReturnType}}`, `{{RequestType}}`, `{{RepositoryMethod}}`, `{{RequiredField}}`, `{{EntityPropertyMappings}}`
- **Enhancements Needed**:
  - Remove ArgumentNullException
  - Add more validation examples (email, phone, date ranges)
  - Add comments explaining validation strategy
- **Estimated Effort**: 30 minutes

#### `domain/query-operation.cs.template`
- **Status**: ✅ Exists, 31 lines
- **Quality**: 8/10
- **Issues**:
  - Line 15: `throw new ArgumentNullException` (violates no-exceptions rule)
- **Dependencies**: `I{{Entity}}Repository`, ErrorOr package
- **Placeholders**: `{{ProjectName}}`, `{{FeatureName}}`, `{{OperationName}}`, `{{Entity}}`, `{{ReturnType}}`, `{{Parameters}}`, `{{RepositoryMethod}}`, `{{RepositoryParameters}}`
- **Enhancements Needed**:
  - Remove ArgumentNullException
  - Add optional filtering/sorting parameters example
  - Add pagination support example
- **Estimated Effort**: 20 minutes

### 4.2 Repository Layer Templates

#### `repository/repository-interface.cs.template`
- **Status**: ✅ Exists, 36 lines
- **Quality**: 10/10 (Perfect)
- **Issues**: None
- **Dependencies**: ErrorOr package, `{{Entity}}` model
- **Placeholders**: `{{ProjectName}}`, `{{Entity}}`
- **Enhancements Needed**: None (already excellent)
- **Estimated Effort**: 0 minutes (validation only)

#### `repository/repository-implementation.cs.template`
- **Status**: ✅ Exists (NOT YET REVIEWED)
- **Quality**: Unknown
- **Expected Issues**:
  - Likely has try-catch blocks (need to verify ErrorOr usage)
  - May need multi-tier access pattern (cache → db → api)
  - Possibly missing connection disposal patterns
- **Dependencies**: EF Core or SQLite, `I{{Entity}}Repository`, `{{Entity}}`
- **Placeholders**: TBD (need to review)
- **Enhancements Needed**: TBD after review
- **Estimated Effort**: 45 minutes (review + enhancements)

### 4.3 Service Layer Templates

#### `service/service-interface.cs.template`
- **Status**: ✅ Exists, 16 lines
- **Quality**: 9/10
- **Issues**: None significant
- **Dependencies**: ErrorOr package
- **Placeholders**: `{{ProjectName}}`, `{{Purpose}}`, `{{ServiceName}}`, `{{MethodDescription}}`, `{{ReturnType}}`, `{{MethodName}}`, `{{Parameters}}`
- **Enhancements Needed**:
  - Add more method examples (POST, PUT, DELETE)
  - Add authentication header examples
- **Estimated Effort**: 15 minutes

#### `service/service-implementation.cs.template`
- **Status**: ✅ Exists (NOT YET REVIEWED)
- **Quality**: Unknown
- **Expected Issues**:
  - Need retry logic with Polly or manual exponential backoff
  - Need proper HttpClient disposal
  - Need timeout configuration
  - Need authentication token handling
- **Dependencies**: HttpClient, ErrorOr, possibly Polly
- **Placeholders**: TBD (need to review)
- **Enhancements Needed**: TBD after review
- **Estimated Effort**: 60 minutes (complex with retry logic)

### 4.4 Presentation Layer Templates

#### `presentation/viewmodel.cs.template`
- **Status**: ✅ Exists, 57 lines
- **Quality**: 9/10 (Excellent)
- **Issues**:
  - Line 26: `throw new ArgumentNullException` (violates no-exceptions rule)
- **Dependencies**: CommunityToolkit.Mvvm, `{{DomainOperation}}`
- **Placeholders**: `{{ProjectName}}`, `{{FeatureName}}`, `{{ViewModelName}}`, `{{PageName}}`, `{{DomainOperation}}`, `{{ItemType}}`, `{{OperationParameters}}`, `{{DetailRoute}}`
- **Enhancements Needed**:
  - Remove ArgumentNullException
  - Add example of command with parameters
  - Add navigation with query parameters example
- **Estimated Effort**: 20 minutes

#### `presentation/page.xaml.template`
- **Status**: ✅ Exists, 37 lines
- **Quality**: 8/10
- **Issues**:
  - Line 21: References `{StaticResource IsNotNullOrEmptyConverter}` (may not exist in new project)
  - Line 22: References `{StaticResource Error}` (may not exist)
- **Dependencies**: MAUI, `{{ViewModelName}}`
- **Placeholders**: `{{ProjectName}}`, `{{FeatureName}}`, `{{PageName}}`, `{{ViewModelName}}`, `{{PageTitle}}`, `{{ContentPlaceholder}}`
- **Enhancements Needed**:
  - Add converter creation instructions
  - Add more content examples (CollectionView, RefreshView)
  - Add platform-specific styling examples
- **Estimated Effort**: 30 minutes

#### `presentation/page.xaml.cs.template`
- **Status**: ✅ Exists (NOT YET REVIEWED)
- **Quality**: Unknown (but usually minimal for MVVM)
- **Expected Pattern**: Constructor injection of ViewModel, set BindingContext
- **Dependencies**: MAUI, `{{ViewModelName}}`
- **Placeholders**: TBD (need to review)
- **Enhancements Needed**: TBD after review
- **Estimated Effort**: 10 minutes (should be simple)

#### `presentation/navigation-service.cs.template`
- **Status**: ✅ Exists (NOT YET REVIEWED)
- **Quality**: Unknown
- **Expected Pattern**: Wrapper around Shell.Current.GoToAsync
- **Dependencies**: MAUI Shell
- **Placeholders**: TBD (need to review)
- **Enhancements Needed**: TBD after review
- **Estimated Effort**: 20 minutes

### 4.5 Testing Templates

#### `testing/domain-test.cs.template`
- **Status**: ✅ Exists, 68 lines
- **Quality**: 10/10 (Perfect)
- **Issues**: None
- **Dependencies**: xUnit, NSubstitute, FluentAssertions, ErrorOr
- **Placeholders**: `{{ProjectName}}`, `{{FeatureName}}`, `{{OperationName}}`, `{{Entity}}`, `{{ReturnType}}`, `{{PropertyInitializers}}`, `{{RepositoryMethod}}`, `{{RepositoryParameters}}`, `{{OperationParameters}}`, `{{RequestType}}`, `{{InvalidPropertyValues}}`
- **Enhancements Needed**: None (already excellent)
- **Estimated Effort**: 0 minutes (validation only)

#### `testing/repository-test.cs.template`
- **Status**: ✅ Exists (NOT YET REVIEWED)
- **Quality**: Unknown
- **Expected Pattern**: In-memory database testing (EF Core InMemory or SQLite InMemory)
- **Dependencies**: xUnit, FluentAssertions, EF Core InMemory
- **Placeholders**: TBD (need to review)
- **Enhancements Needed**: TBD after review
- **Estimated Effort**: 30 minutes

#### `testing/service-test.cs.template`
- **Status**: ✅ Exists (NOT YET REVIEWED)
- **Quality**: Unknown
- **Expected Pattern**: HttpClient mocking with MockHttpMessageHandler
- **Dependencies**: xUnit, FluentAssertions, mock HTTP library
- **Placeholders**: TBD (need to review)
- **Enhancements Needed**: TBD after review
- **Estimated Effort**: 30 minutes

#### `testing/viewmodel-test.cs.template`
- **Status**: ❌ MISSING (MUST CREATE)
- **Quality**: N/A
- **Pattern Needed**: Mock domain operations, verify ViewModel behavior, test command execution
- **Dependencies**: xUnit, NSubstitute, FluentAssertions, CommunityToolkit.Mvvm
- **Placeholders**: `{{ProjectName}}`, `{{FeatureName}}`, `{{ViewModelName}}`, `{{DomainOperation}}`, `{{ItemType}}`, etc.
- **Enhancements Needed**: Create from scratch following Outside-In TDD pattern
- **Estimated Effort**: 90 minutes (new file, critical importance)

## Phase 5: Risk Assessment

### 5.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Templates don't compile after placeholder substitution | Medium | High | Create test project with all templates |
| Placeholder naming inconsistencies | High | Medium | Comprehensive placeholder audit |
| Missing dependencies in generated code | Low | High | Verify all using statements |
| ErrorOr pattern misuse | Low | High | Review all ErrorOr usage carefully |
| Multi-tier access pattern too complex | Medium | Medium | Provide simplified default, advanced example |

### 5.2 Workflow Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Unclear which template to use when | High | Medium | Create decision tree diagram |
| Developers don't understand ErrorOr | High | High | Add ErrorOr usage guide |
| Templates too rigid for real-world use | Medium | High | Add variation examples |
| Testing templates not followed | Medium | High | Make Outside-In TDD workflow explicit |

### 5.3 Maintenance Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Templates become outdated | High | Medium | Version templates, document update process |
| Inconsistency between templates | Medium | High | Use shared snippets, automated validation |
| Placeholder drift over time | Medium | Medium | Lock placeholder names in settings.json |

## Phase 6: Implementation Sequencing

### 6.1 Optimal Sequence (Dependency-Based)

**Wave 1: Foundation Validation** (Day 1, Morning)
1. Read and analyze all 6 remaining templates
2. Create comprehensive placeholder inventory
3. Document all template interdependencies
4. Identify all critical issues

**Wave 2: Critical Fixes** (Day 1, Afternoon)
1. Remove `ArgumentNullException` from domain templates (30 min)
2. Remove `ArgumentNullException` from viewmodel template (10 min)
3. Fix `Result.Success` in command template (5 min)
4. Fix StaticResource references in XAML template (15 min)

**Wave 3: Create Missing Template** (Day 2, Morning)
1. Design `testing/viewmodel-test.cs.template` structure (30 min)
2. Implement ViewModel test template (60 min)
3. Add comprehensive examples (30 min)
4. Review and refine (30 min)

**Wave 4: High-Value Enhancements** (Day 2, Afternoon)
1. Add multi-tier access to repository implementation (45 min)
2. Add retry logic to service implementation (60 min)
3. Add validation examples to domain templates (30 min)
4. Add navigation examples to presentation templates (30 min)

**Wave 5: Verification** (Day 3)
1. Create test project with all templates (60 min)
2. Verify compilation of generated code (30 min)
3. Run generated tests (30 min)
4. Fix any issues discovered (60-120 min buffer)

### 6.2 Parallel Work Opportunities

**Can be done in parallel**:
- Validating domain templates + validating presentation templates
- Fixing domain exceptions + fixing viewmodel exceptions
- Creating ViewModel test template + enhancing service template

**Must be sequential**:
- Validation → Fixes → Enhancements → Verification
- Template creation → Placeholder audit → Documentation

## Phase 7: Acceptance Criteria Checklist

### 7.1 Functional Requirements

- [ ] All 13 existing templates validated and enhanced
- [ ] New `testing/viewmodel-test.cs.template` created
- [ ] All templates compile without errors
- [ ] Generated code follows ErrorOr pattern (100%)
- [ ] No exception throwing (except truly exceptional cases)
- [ ] XML documentation complete (100% coverage)
- [ ] All placeholders documented and consistent

### 7.2 Quality Requirements

- [ ] Verb-based domain naming enforced
- [ ] Repository/Service separation clear
- [ ] CommunityToolkit.Mvvm patterns correct
- [ ] Outside-In TDD workflow supported
- [ ] Multi-tier data access pattern shown
- [ ] Retry logic in service template
- [ ] Test templates use xUnit + NSubstitute + FluentAssertions

### 7.3 Architecture Requirements

- [ ] SOLID principles demonstrated
- [ ] DRY principle applied (no duplication across templates)
- [ ] YAGNI principle followed (minimal but complete)
- [ ] Dependency injection configured
- [ ] AppShell navigation integrated
- [ ] Layer separation maintained (Domain/Repository/Service/Presentation)

### 7.4 Documentation Requirements

- [ ] Each template has usage example
- [ ] All placeholders documented in settings.json
- [ ] Template selection guide created
- [ ] ErrorOr usage guide included
- [ ] Outside-In TDD workflow documented
- [ ] Troubleshooting section complete

### 7.5 Testing Requirements

- [ ] Domain operation tests cover success/error/validation cases
- [ ] Repository tests use in-memory database
- [ ] Service tests mock HttpClient
- [ ] ViewModel tests mock domain operations
- [ ] All test templates follow naming convention
- [ ] Test coverage targets defined (80% line, 75% branch)

## Phase 8: Effort Estimation

### 8.1 Task Breakdown by Time

| Phase | Tasks | Time (minutes) | Cumulative |
|-------|-------|----------------|------------|
| **Validation** | Review 6 templates, create inventory | 120 | 120 |
| **Critical Fixes** | Remove exceptions, fix patterns | 60 | 180 |
| **Create Missing** | ViewModel test template | 150 | 330 |
| **Enhancements** | Multi-tier, retry, examples | 165 | 495 |
| **Verification** | Test project, compilation, tests | 180 | 675 |
| **Documentation** | Usage guide, troubleshooting | 90 | 765 |
| **Buffer** | Unexpected issues | 135 | 900 |

**Total Estimated Effort**: **900 minutes (15 hours / 2 work days)**

### 8.2 Breakdown by Template

| Template | Validation | Fixes | Enhancements | Total |
|----------|------------|-------|--------------|-------|
| command-operation | 10 | 30 | 20 | 60 |
| query-operation | 10 | 20 | 10 | 40 |
| repository-interface | 5 | 0 | 0 | 5 |
| repository-implementation | 20 | 15 | 45 | 80 |
| service-interface | 5 | 0 | 15 | 20 |
| service-implementation | 20 | 15 | 60 | 95 |
| viewmodel | 10 | 20 | 15 | 45 |
| page.xaml | 10 | 15 | 30 | 55 |
| page.xaml.cs | 10 | 5 | 10 | 25 |
| navigation-service | 10 | 5 | 20 | 35 |
| domain-test | 5 | 0 | 0 | 5 |
| repository-test | 15 | 10 | 20 | 45 |
| service-test | 15 | 10 | 20 | 45 |
| viewmodel-test (NEW) | 0 | 0 | 150 | 150 |
| Documentation | 0 | 0 | 90 | 90 |

**Total**: 795 minutes + 105 buffer = **900 minutes**

## Phase 9: Success Metrics

### 9.1 Quantitative Metrics

- **Template Completeness**: 14/14 templates (100%)
- **Compilation Success**: 100% (all generated code compiles)
- **Test Pass Rate**: 100% (all generated tests pass)
- **XML Documentation**: 100% coverage
- **ErrorOr Usage**: 100% (all fallible operations return ErrorOr)
- **Exception Throwing**: 0% (no exceptions in business logic)
- **Placeholder Consistency**: 100% (all placeholders documented and used correctly)

### 9.2 Qualitative Metrics

- **Developer Experience**: Templates feel "right-sized" and not overwhelming
- **Pattern Clarity**: Clear which template to use in which scenario
- **Code Quality**: Generated code passes all quality gates without modification
- **Test Quality**: Generated tests are comprehensive and maintainable
- **Documentation Quality**: Developers can use templates without external help

### 9.3 Validation Tests

**Test 1: Simple CRUD Feature**
1. Generate Product entity with all templates
2. Verify compilation
3. Run all generated tests
4. Expected: All green, <5 minutes to generate

**Test 2: Complex Business Logic**
1. Generate Order processing with validation
2. Verify multi-tier data access works
3. Verify retry logic in service
4. Expected: All patterns work correctly

**Test 3: Outside-In TDD Workflow**
1. Start with ViewModel acceptance test
2. Generate domain, repository, service
3. Wire up ViewModel
4. Expected: TDD workflow smooth and intuitive

## Phase 10: Next Steps & Dependencies

### 10.1 Immediate Next Steps (Phase 1)

1. **Complete Template Validation** (2 hours)
   - Read remaining 6 templates
   - Create quality scorecard
   - Document placeholder inventory
   - Identify all issues

2. **Create Implementation Ticket Breakdown** (30 min)
   - Create TASK-011B-1: Critical Fixes
   - Create TASK-011B-2: Create ViewModel Test Template
   - Create TASK-011B-3: High-Value Enhancements
   - Create TASK-011B-4: Verification & Testing

### 10.2 Blocking Dependencies

**None identified** - All work can proceed independently once validation complete.

### 10.3 Related Tasks

- **TASK-011A**: ✅ Completed (template structure created)
- **TASK-011C**: maui-navigationpage-template (can proceed in parallel)
- **TASK-011D**: Create maui-domain-specialist-agent (depends on template completion)
- **TASK-011E**: maui-repository-specialist (depends on template completion)
- **TASK-011F**: maui-service-specialist-agent (depends on template completion)
- **TASK-011G**: maui-mydrive-local-template (independent)

### 10.4 Post-Completion Tasks

After TASK-011B completion:
1. Update manifest.json with viewmodel test template
2. Create template usage documentation
3. Test template generation with real project
4. Gather feedback from initial users
5. Create video tutorial for template usage

## Appendix A: Placeholder Inventory

### A.1 Project-Level Placeholders
- `{{ProjectName}}` - Root project name (e.g., "MyMauiApp")
- `{{RootNamespace}}` - Root namespace (usually same as ProjectName)

### A.2 Feature-Level Placeholders
- `{{FeatureName}}` - Feature/module name (e.g., "Products", "Orders")
- `{{Entity}}` - Entity name (e.g., "Product", "Order")
- `{{Verb}}` - Action verb (e.g., "Get", "Create", "Update", "Delete")

### A.3 Operation-Level Placeholders
- `{{OperationName}}` - Complete operation name (e.g., "GetProducts", "CreateOrder")
- `{{ReturnType}}` - Return type (e.g., "Product", "List<Product>")
- `{{Parameters}}` - Method parameters
- `{{RequestType}}` - Request DTO type (for commands)

### A.4 Repository-Level Placeholders
- `{{RepositoryName}}` - Repository name (e.g., "ProductRepository")
- `{{RepositoryMethod}}` - Repository method name (e.g., "GetAllAsync")
- `{{RepositoryParameters}}` - Repository method parameters

### A.5 Service-Level Placeholders
- `{{ServiceName}}` - Service name (e.g., "PaymentService")
- `{{Purpose}}` - Service purpose (e.g., "Payment", "Authentication")
- `{{MethodName}}` - Service method name
- `{{MethodDescription}}` - XML doc description

### A.6 Presentation-Level Placeholders
- `{{ViewModelName}}` - ViewModel name (e.g., "ProductListViewModel")
- `{{PageName}}` - Page name (e.g., "ProductListPage")
- `{{PageTitle}}` - Page title (e.g., "Products")
- `{{ItemType}}` - Collection item type (e.g., "Product")
- `{{DomainOperation}}` - Injected domain operation
- `{{ContentPlaceholder}}` - XAML content area

### A.7 Test-Level Placeholders
- `{{PropertyInitializers}}` - Test object property setup
- `{{InvalidPropertyValues}}` - Invalid values for validation tests
- `{{OperationParameters}}` - Operation execution parameters

## Appendix B: Template Interdependencies

```
repository-interface.cs.template
    ↓
repository-implementation.cs.template
    ↓
domain/query-operation.cs.template ← Uses I{{Entity}}Repository
domain/command-operation.cs.template ← Uses I{{Entity}}Repository
    ↓
service-interface.cs.template
    ↓
service-implementation.cs.template
    ↓
presentation/viewmodel.cs.template ← Uses domain operations
    ↓
presentation/page.xaml.template ← Binds to ViewModel
presentation/page.xaml.cs.template ← Injects ViewModel
    ↓
presentation/navigation-service.cs.template ← Used by ViewModels

Testing Templates (parallel dependencies):
domain-test.cs.template ← Mocks I{{Entity}}Repository
repository-test.cs.template ← Uses repository implementation
service-test.cs.template ← Mocks HttpClient
viewmodel-test.cs.template ← Mocks domain operations (NEW)
```

## Appendix C: Quality Gate Checklist

### C.1 Compilation Gates
- [ ] All templates generate valid C# code
- [ ] All templates generate valid XAML code
- [ ] No missing using statements
- [ ] No undefined types
- [ ] No syntax errors

### C.2 Pattern Gates
- [ ] ErrorOr used for all fallible operations
- [ ] No exception throwing (except ArgumentNullException in constructors)
- [ ] Interfaces for all repositories and services
- [ ] Verb-based domain naming (no UseCase suffix)
- [ ] CommunityToolkit.Mvvm attributes used correctly

### C.3 Architecture Gates
- [ ] Domain layer has no UI dependencies
- [ ] Repository layer has no service dependencies
- [ ] Service layer has no repository dependencies
- [ ] Presentation layer depends only on domain operations
- [ ] Test templates use proper mocking (interfaces only)

### C.4 Documentation Gates
- [ ] All public classes have XML summary
- [ ] All public methods have XML summary
- [ ] All parameters documented
- [ ] All return values documented
- [ ] Usage examples provided

### C.5 Testing Gates
- [ ] All templates have corresponding test templates
- [ ] Test templates follow naming convention
- [ ] Tests cover success, error, and validation cases
- [ ] Tests use xUnit + NSubstitute + FluentAssertions
- [ ] Tests demonstrate Outside-In TDD workflow

## Conclusion

This implementation plan transforms TASK-011B from a "create templates" task to a "validate and enhance existing templates" task. The critical discovery that 13/14 templates already exist changes the scope significantly:

**Original Assumption**: Create 15 templates from scratch (~40 hours)
**Actual Scope**: Validate 13 templates, fix 8 issues, create 1 missing template, enhance 6 templates (~15 hours)

**Key Deliverables**:
1. Comprehensive validation of all existing templates
2. Critical bug fixes (ArgumentNullException removal, ErrorOr pattern compliance)
3. New ViewModel test template (critical for Outside-In TDD)
4. High-value enhancements (multi-tier access, retry logic)
5. Complete verification with test project

**Risk Level**: Medium (existing templates reduce risk, but interdependencies increase complexity)
**Estimated Effort**: 15 hours (2 work days)
**Success Probability**: High (90%) - Most work is enhancement, not creation

This plan provides a clear, phased approach with specific tasks, time estimates, and acceptance criteria for successful completion of TASK-011B.
