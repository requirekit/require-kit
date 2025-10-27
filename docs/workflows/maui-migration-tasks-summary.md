# MAUI Template Migration - Task Summary

## Overview

This document summarizes all tasks created for the MAUI template migration from MyDrive-specific Engine pattern to generic Domain pattern with local template support.

**Total Tasks Created**: 10
**Total Estimated Effort**: 35-40 hours
**Migration Strategy**: Option A (Create all templates first, then migrate MyDrive)

## Task Breakdown by Phase

### Phase 1: Create Global Templates (3 tasks, 12-14 hours)

#### TASK-011: Create maui-appshell Template Structure
**File**: `tasks/backlog/TASK-011-create-maui-appshell-template-structure.md`
**Complexity**: 6/10 (Medium)
**Estimated**: 4 hours
**Status**: BACKLOG

**Deliverables**:
- Complete `installer/global/templates/maui-appshell/` directory structure
- manifest.json, CLAUDE.md, settings.json configuration files
- Domain pattern framework (verb-based naming, no suffix)
- Repository/Service layer separation
- AppShell navigation setup

**Key Features**:
- Verb-based naming: GetProducts, CreateOrder, UpdateUserProfile
- Clear separation: Repository (database) vs Service (API/hardware)
- ErrorOr pattern for functional error handling
- AppShell routing and navigation patterns

---

#### TASK-011: Create maui-appshell Template Code Files
**File**: `tasks/backlog/TASK-011-maui-appshell-template-code.md`
**Complexity**: 7/10 (Complex)
**Estimated**: 4-6 hours
**Status**: BACKLOG

**Deliverables** (15 template files):

**Domain & Data Access** (5 files):
- Domain.cs - Business logic with verb-based naming
- IRepository.cs, Repository.cs - Database access only
- IService.cs, Service.cs - APIs and hardware only

**Presentation Layer** (3 files):
- ViewModel.cs - MVVM with CommunityToolkit
- Page.xaml, Page.xaml.cs - UI templates

**Application Structure** (3 files):
- AppShell.xaml, AppShell.xaml.cs - Shell navigation
- MauiProgram.cs - Dependency injection setup

**Test Templates** (4 files):
- DomainTests.cs, RepositoryTests.cs, ServiceTests.cs, ViewModelTests.cs

**Key Features**:
- All templates use Domain pattern (no UseCase/Engine suffix)
- ErrorOr pattern throughout
- Comprehensive XML documentation
- Multi-tier data access (cache → database → API)
- Template placeholders for customization

---

#### TASK-011: Create maui-navigationpage Template
**File**: `tasks/backlog/TASK-011-maui-navigationpage-template.md`
**Complexity**: 6/10 (Medium)
**Estimated**: 4-6 hours
**Status**: BACKLOG

**Deliverables**:
- Complete `installer/global/templates/maui-navigationpage/` structure
- NavigationService.cs and INavigationService.cs (NEW)
- MauiProgram.cs with NavigationService DI setup
- Reuse Domain, Repository, Service, ViewModel, Page templates from maui-appshell
- Documentation on when to use NavigationPage vs AppShell

**Key Features**:
- Type-safe navigation using ViewModel types
- Strongly-typed parameter passing
- Automatic page resolution via convention
- Full DI support for pages and ViewModels
- Clear decision framework: NavigationPage vs AppShell

**When to Use**:
- NavigationPage: Complex flows, multiple stacks, legacy migration
- AppShell: Modern apps, flyout menus, tabs, simple navigation

---

### Phase 2: Create Specialized Agents (3 tasks, 12-15 hours)

#### TASK-011: Create maui-domain-specialist Agent
**File**: `tasks/backlog/TASK-011-create-maui-domain-specialist-agent.md`
**Complexity**: 5/10 (Medium)
**Estimated**: 4-5 hours
**Status**: BACKLOG

**Deliverables**:
- `maui-appshell/agents/maui-domain-specialist.md`
- `maui-navigationpage/agents/maui-domain-specialist.md` (identical)
- Replaces old `maui-usecase-specialist` agent

**Key Features**:
- Domain layer expertise (business logic orchestration)
- Verb-based naming pattern (GetProducts, CreateOrder)
- ErrorOr pattern guidance
- Repository/Service composition patterns
- Collaboration with repository-specialist and service-specialist
- Pre-implementation checks
- Anti-patterns documentation

**Focus Areas**:
- Domain pattern (no UseCase/Engine suffix)
- Business logic orchestration
- Functional error handling with ErrorOr
- Clear layer boundaries

---

#### TASK-011: Create maui-repository-specialist Agent
**File**: `tasks/backlog/TASK-011-maui-repository-specialist.md`
**Complexity**: 5/10 (Medium)
**Estimated**: 4-5 hours
**Status**: BACKLOG

**Deliverables**:
- `maui-appshell/agents/maui-repository-specialist.md`
- `maui-navigationpage/agents/maui-repository-specialist.md` (identical)

**Key Features**:
- Database access ONLY (SQLite, LiteDB, EF Core, Realm)
- Repository pattern implementation (interface-first)
- ErrorOr pattern for database errors
- Query optimization and performance
- Thread-safety for mobile
- Migration strategies
- Testing with in-memory databases

**Critical Boundaries**:
- ❌ NO API calls (use Services)
- ❌ NO business logic (use Domain layer)
- ❌ NO caching logic (use CacheService)

---

#### TASK-011: Create maui-service-specialist Agent
**File**: `tasks/backlog/TASK-011-maui-service-specialist-agent.md`
**Complexity**: 5/10 (Medium)
**Estimated**: 4-5 hours
**Status**: BACKLOG

**Deliverables**:
- `maui-appshell/agents/maui-service-specialist.md`
- `maui-navigationpage/agents/maui-service-specialist.md` (identical)

**Key Features**:
- External systems ONLY (APIs, GPS, Camera, Sensors)
- HTTP API client patterns (RestSharp, Refit, HttpClient)
- Hardware service patterns (Location, Camera, Sensors)
- Cache service patterns (in-memory, persistent)
- Authentication services
- ErrorOr pattern for service failures
- Testing strategies (mocking, HttpClientInterception)

**Critical Boundaries**:
- ❌ NO database access (use Repositories)
- ❌ NO business logic (use Domain layer)
- ❌ NO direct ViewModel interaction

---

### Phase 3: Migrate MyDrive to Local Template (2 tasks, 6-8 hours)

#### TASK-011: Create MyDrive Local Template
**File**: `tasks/backlog/TASK-011-maui-mydrive-local-template.md`
**Complexity**: 4/10 (Medium-Low)
**Estimated**: 3-4 hours
**Status**: BACKLOG

**Deliverables**:
- `.claude/templates/maui-mydrive/` directory in MyDrive project
- Copy all Engine-suffixed templates from global maui template
- manifest.json with local scope and Engine pattern metadata
- Update MyDrive settings.json to reference local template
- MyDrive-specific agents (engine-pattern-specialist, mydrive-architect)
- Comprehensive README.md documentation

**Key Features**:
- Preserves Engine pattern (GetProductsEngine, CreateOrderEngine)
- Preserves DeCUK.Mobile.MyDrive namespace
- Preserves Engines/ namespace for domain layer
- All MyDrive-specific customizations maintained
- Version controlled with MyDrive project source

**Success Criteria**:
- MyDrive workflow continues unchanged
- Engine pattern preserved in local template
- Local template overrides global template
- Zero breaking changes for MyDrive team

---

#### TASK-011: Delete Old Global MAUI Template
**File**: `tasks/backlog/TASK-011-cleanup-old-maui-template.md`
**Complexity**: 3/10 (Low)
**Estimated**: 3-4 hours
**Status**: BACKLOG

**Deliverables**:
- Delete `installer/global/templates/maui/` directory completely
- Update installer scripts to remove references
- Update completion scripts
- Update documentation
- Verify MyDrive works with local template
- Verify new projects work with new templates
- Run comprehensive integration tests

**Verification Checklist**:
- ✅ MyDrive verified working with local template
- ✅ Test project created with maui-appshell successfully
- ✅ Test project created with maui-navigationpage successfully
- ✅ All installer tests passing
- ✅ No breaking changes for existing workflows
- ✅ Clear error messages for deprecated template usage

---

### Phase 4: Update Installer (1 task, 3-4 hours)

#### TASK-011: Update Installer for Local Template Support
**File**: `tasks/backlog/TASK-011-installer-local-template-support.md`
**Complexity**: 6/10 (Medium)
**Estimated**: 3-4 hours
**Status**: BACKLOG

**Deliverables**:
- Template discovery function (finds local templates in `.claude/templates/`)
- Template resolution function (priority: local → global → default)
- Template validation function (validates structure and manifest)
- Update agentic-init to check local templates first
- Update agenticflow doctor to show local template status
- Update bash completion to include local templates
- Update template listing commands
- Add error handling for invalid local templates

**Key Features**:
- Automatic local template discovery
- Clear template priority resolution
- Helpful error messages for invalid templates
- Template source logging (local vs global)
- Backward compatibility maintained

**Testing Scenarios**:
1. Global template only (works as before)
2. Local template override (local takes precedence)
3. Invalid local template (helpful error message)
4. Template discovery (lists both local and global)
5. Completion integration (includes local templates)
6. Priority resolution (correct order)

---

### Phase 5: Documentation (1 task, 4-6 hours)

#### TASK-011: Create Comprehensive MAUI Template Documentation
**File**: `tasks/backlog/TASK-011-maui-template-documentation.md`
**Complexity**: 5/10 (Medium)
**Estimated**: 4-6 hours
**Status**: BACKLOG

**Deliverables** (4 new documents + 1 update):

1. **docs/guides/maui-template-selection.md**
   - When to use AppShell vs NavigationPage
   - Template feature comparison
   - Decision framework and use cases
   - Examples for each template type

2. **docs/guides/creating-local-templates.md**
   - Step-by-step local template creation
   - Customization options and inheritance
   - Version control best practices
   - MyDrive case study

3. **docs/patterns/domain-layer-pattern.md**
   - Domain pattern best practices
   - Verb-based naming conventions
   - Repository vs Service separation
   - ErrorOr pattern usage
   - Testing strategies
   - Anti-patterns to avoid

4. **docs/migration/engine-to-domain.md**
   - Migration from Engine to Domain pattern
   - Before/after code examples
   - MyDrive migration walkthrough
   - Step-by-step migration process
   - Common pitfalls and solutions

5. **CLAUDE.md** (update)
   - Add references to new templates
   - Update command examples
   - Add template selection guidance

**Documentation Standards**:
- Progressive Disclosure pattern (following TASK-010 success)
- Quick Start → Core Concepts → Complete Reference → Examples → FAQ
- Real-world tested code examples
- Visual diagrams using Mermaid
- Comprehensive troubleshooting sections

**Success Metrics**:
- Documentation clarity: 95/100
- Code example validity: 100%
- Consistency score: 95/100
- Usability score: 90/100

---

## Summary Statistics

### Effort Distribution

| Phase | Tasks | Hours | Percentage |
|-------|-------|-------|------------|
| Phase 1: Global Templates | 3 | 12-14 | 34% |
| Phase 2: Specialized Agents | 3 | 12-15 | 36% |
| Phase 3: MyDrive Migration | 2 | 6-8 | 18% |
| Phase 4: Installer Updates | 1 | 3-4 | 9% |
| Phase 5: Documentation | 1 | 4-6 | 13% |
| **Total** | **10** | **37-47** | **110%** |

### Complexity Distribution

| Complexity | Tasks | Percentage |
|------------|-------|------------|
| Low (3/10) | 1 | 10% |
| Medium-Low (4/10) | 1 | 10% |
| Medium (5-6/10) | 7 | 70% |
| Complex (7/10) | 1 | 10% |

### Priority Distribution

| Priority | Tasks |
|----------|-------|
| High | 6 |
| Medium | 4 |

## Implementation Strategy

### Recommended Order (Option A)

**Week 1: Foundation (Phase 1)**
- Day 1-2: TASK-011 (maui-appshell structure)
- Day 3-4: TASK-011 (maui-appshell code files)
- Day 5: TASK-011 (maui-navigationpage)

**Week 2: Agents & Migration (Phases 2-3)**
- Day 1: TASK-011 (maui-domain-specialist)
- Day 2: TASK-011 (maui-repository-specialist)
- Day 3: TASK-011 (maui-service-specialist)
- Day 4: TASK-011 (MyDrive local template)
- Day 5: TASK-011 (Cleanup old template)

**Week 3: Finalization (Phases 4-5)**
- Day 1: TASK-011 (Installer updates)
- Day 2-3: TASK-011 (Documentation)
- Day 4-5: Integration testing and polish

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| MyDrive workflow breaking | HIGH | Local template isolation, thorough testing |
| Agent collaboration issues | MEDIUM | Clear collaboration patterns defined |
| Template complexity confusion | MEDIUM | Comprehensive documentation, examples |
| Installer regression | MEDIUM | Extensive testing, backward compatibility |
| Documentation drift | LOW | Cross-references, version control |

## Success Criteria

### Technical Success
- ✅ Two working global MAUI templates (AppShell + NavigationPage)
- ✅ Three specialized agents (domain, repository, service)
- ✅ MyDrive continues working with local template
- ✅ Installer supports local templates with priority resolution
- ✅ All tests passing
- ✅ Zero breaking changes

### Documentation Success
- ✅ Template selection guide complete
- ✅ Local template creation guide complete
- ✅ Domain pattern guide complete
- ✅ Migration guide complete
- ✅ All examples tested and working

### Business Success
- ✅ Generic templates suitable for any MAUI project
- ✅ Local templates enable project-specific customization
- ✅ Clear architectural patterns (Domain, Repository, Service)
- ✅ Team productivity maintained or improved
- ✅ Onboarding simplified with clear documentation

## Related Documents

- **Architecture**: [docs/shared/maui-template-architecture.md](../shared/maui-template-architecture.md)
- **Migration Plan**: [docs/workflows/maui-template-migration-plan.md](maui-template-migration-plan.md)
- **MyDrive Project**: `/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive`

## Next Steps

1. **Review Tasks**: Review all 10 tasks for completeness and accuracy
2. **Prioritize**: Confirm task execution order
3. **Start Phase 1**: Begin with `TASK-011-create-maui-appshell-template-structure`
4. **Progress Tracking**: Use `/task-status` to monitor progress
5. **Documentation**: Update this summary as tasks are completed

---

**Document Version**: 1.0
**Created**: 2025-10-12
**Status**: READY FOR REVIEW
**Total Tasks**: 10
**Total Estimated Effort**: 37-47 hours
