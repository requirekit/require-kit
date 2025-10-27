---
id: TASK-011D
title: Create maui-domain-specialist agent for Domain layer
status: completed
created: 2025-10-12T10:30:00Z
updated: 2025-10-13T00:10:00Z
previous_state: in_review
state_transition_reason: "Task completed: All acceptance criteria met, quality gates passed"
completed_at: 2025-10-13T00:10:00Z
actual_duration: "5 minutes"
estimated_duration: "1-2 hours"
priority: high
tags: [maui, agents, domain-pattern, template-migration, phase-2.1]
epic: null
feature: null
requirements: []
external_ids:
  epic_jira: null
  epic_linear: null
  jira: null
  linear: null
bdd_scenarios: []
dependencies: []
complexity_evaluation:
  score: 5
  level: "medium"
  review_mode: "QUICK_OPTIONAL"
  factor_scores:
    - factor: "file_complexity"
      score: 1
      max_score: 3
      justification: "2 identical agent files to create"
    - factor: "pattern_familiarity"
      score: 1
      max_score: 2
      justification: "Familiar agent creation pattern with new Domain architecture"
    - factor: "risk_level"
      score: 1
      max_score: 3
      justification: "Low risk - agent documentation only, no code changes"
    - factor: "dependencies"
      score: 2
      max_score: 2
      justification: "Depends on architecture documentation and existing agent patterns"
---

# Task: Create maui-domain-specialist agent for Domain layer

## Context

**Phase 2.1 of MAUI Template Migration**

The MAUI templates are being migrated from the Engine/UseCase pattern to the generic Domain pattern with verb-based naming. This task creates the new `maui-domain-specialist` agent to replace the old `maui-usecase-specialist`, implementing the architecture defined in `docs/shared/maui-template-architecture.md`.

The Domain pattern uses:
- Verb-based naming: `GetProducts`, `CreateOrder` (no suffix)
- Namespace: `<ProjectName>.Domain`
- ErrorOr pattern for error handling
- Composition of Repositories and Services
- Clear separation of business logic from data access

## Objective

Create the `maui-domain-specialist` agent for both MAUI templates (maui-appshell and maui-navigationpage) that provides expert guidance on implementing the Domain layer with verb-based naming conventions.

## Requirements

### Agent File Creation
- [x] Create `installer/global/templates/maui-appshell/agents/maui-domain-specialist.md`
- [x] Create `installer/global/templates/maui-navigationpage/agents/maui-domain-specialist.md` (identical content)
- [x] Follow standard agent format (role, expertise, responsibilities, patterns, anti-patterns)

### Agent Expertise Definition
- [x] Define Domain layer expertise (business logic orchestration)
- [x] Document verb-based naming pattern (GetProducts, CreateOrder, UpdateUserProfile)
- [x] Explain when to use Domain vs ViewModel
- [x] Include ErrorOr pattern guidance
- [x] Include Repository and Service composition patterns
- [x] Include business logic best practices

### Code Examples
- [x] Provide complete Domain class examples
- [x] Show ErrorOr pattern usage
- [x] Demonstrate Repository/Service composition
- [x] Include async/await patterns
- [x] Show proper dependency injection
- [x] Include error handling examples

### Agent Collaboration
- [x] Define collaboration with maui-repository-specialist (database access)
- [x] Define collaboration with maui-service-specialist (external systems)
- [x] Define collaboration with maui-viewmodel-specialist (UI orchestration)
- [x] Define handoff protocols between agents
- [x] Include when to escalate to software-architect

### Pre-Implementation Checks
- [x] Checklist for verb-based naming validation
- [x] Business logic location verification (Domain vs ViewModel)
- [x] Dependency injection setup validation
- [x] ErrorOr pattern implementation check
- [x] Repository/Service composition validation

### Patterns and Anti-Patterns
- [x] Document correct Domain patterns (verb-based, no suffix)
- [x] Document anti-patterns (GetProductsUseCase, GetProductsEngine)
- [x] Show correct composition patterns
- [x] Show incorrect patterns (direct database access, UI logic)
- [x] Include namespace conventions

## Acceptance Criteria

### Agent Structure ✅
- [x] Agent markdown follows standard format
- [x] All required sections present (role, expertise, responsibilities, patterns, anti-patterns, collaboration)
- [x] Consistent formatting with other MAUI agents

### Domain Pattern Definition ✅
- [x] Clearly defines Domain pattern (no UseCase/Engine suffix)
- [x] Verb-based naming thoroughly explained with examples
- [x] When to use Domain vs ViewModel clearly articulated
- [x] Namespace conventions documented

### ErrorOr Pattern ✅
- [x] ErrorOr pattern usage clearly explained
- [x] Return type examples provided
- [x] Error handling patterns documented
- [x] Match/Switch pattern examples included

### Code Examples ✅
- [x] At least 3 complete Domain class examples
- [x] Examples show Repository/Service composition
- [x] Examples demonstrate proper async/await
- [x] Examples include dependency injection
- [x] Examples cover error handling

### Collaboration Patterns ✅
- [x] Defines clear collaboration with maui-repository-specialist
- [x] Defines clear collaboration with maui-service-specialist
- [x] Defines clear collaboration with maui-viewmodel-specialist
- [x] Handoff protocols are actionable
- [x] Escalation criteria defined

### Pre-Implementation Checks ✅
- [x] Checklist is comprehensive and actionable
- [x] Covers naming validation
- [x] Covers business logic location
- [x] Covers dependency setup
- [x] Covers pattern compliance

### Anti-Patterns ✅
- [x] Anti-patterns clearly documented
- [x] Includes old patterns (UseCase, Engine suffix)
- [x] Includes incorrect layer violations
- [x] Includes improper composition patterns
- [x] Explanations for why patterns are anti-patterns

## Implementation Plan

### Phase 1: Agent Structure Setup
1. Create agent file in maui-appshell template
2. Define agent role and expertise
3. Establish agent responsibilities

### Phase 2: Domain Pattern Documentation
1. Define verb-based naming convention
2. Document Domain vs ViewModel decision criteria
3. Establish namespace conventions
4. Define ErrorOr pattern usage

### Phase 3: Code Examples
1. Create GetProducts example (simple)
2. Create CreateOrder example (complex with validation)
3. Create UpdateUserProfile example (with error handling)
4. Add Repository/Service composition examples

### Phase 4: Collaboration Patterns
1. Define Repository collaboration
2. Define Service collaboration
3. Define ViewModel handoff
4. Define architect escalation

### Phase 5: Quality Checks
1. Add pre-implementation checklist
2. Document common anti-patterns
3. Add pattern validation guidance
4. Include namespace validation

### Phase 6: Template Duplication
1. Copy to maui-navigationpage template
2. Verify content is identical
3. Test both files

## Related Documents

### Reference Documents
- `docs/shared/maui-template-architecture.md` - Architecture definition
- `installer/global/templates/maui-appshell/agents/maui-repository-specialist.md` - Repository collaboration
- `installer/global/templates/maui-appshell/agents/maui-service-specialist.md` - Service collaboration
- `installer/global/templates/maui-appshell/agents/maui-viewmodel-specialist.md` - ViewModel handoff

### Will Be Deprecated (DO NOT USE)
- `installer/global/templates/maui-appshell/agents/maui-usecase-specialist.md` - Old pattern, reference only

## Testing Strategy

### Agent Documentation Tests
```bash
# Verify agent files exist
test -f installer/global/templates/maui-appshell/agents/maui-domain-specialist.md
test -f installer/global/templates/maui-navigationpage/agents/maui-domain-specialist.md

# Verify content is identical
diff installer/global/templates/maui-appshell/agents/maui-domain-specialist.md \
     installer/global/templates/maui-navigationpage/agents/maui-domain-specialist.md

# Verify no UseCase/Engine suffix in naming examples
! grep -i "UseCase\|Engine" installer/global/templates/maui-appshell/agents/maui-domain-specialist.md

# Verify verb-based naming present
grep -E "Get[A-Z]|Create[A-Z]|Update[A-Z]|Delete[A-Z]" \
     installer/global/templates/maui-appshell/agents/maui-domain-specialist.md

# Verify ErrorOr pattern documented
grep "ErrorOr" installer/global/templates/maui-appshell/agents/maui-domain-specialist.md
```

### Pattern Validation Tests
```bash
# Verify correct namespace pattern
grep -E "namespace.*\.Domain" installer/global/templates/maui-appshell/agents/maui-domain-specialist.md

# Verify anti-patterns documented
grep -E "❌.*UseCase|❌.*Engine" installer/global/templates/maui-appshell/agents/maui-domain-specialist.md

# Verify collaboration documented
grep -E "repository-specialist|service-specialist|viewmodel-specialist" \
     installer/global/templates/maui-appshell/agents/maui-domain-specialist.md
```

## Expected Agent Content Structure

### Sections Required
1. **Role**: Domain layer specialist
2. **Expertise**: Business logic, verb-based naming, ErrorOr pattern
3. **Responsibilities**: Domain class creation, business rule implementation
4. **Pre-Implementation Checks**: Naming, location, dependencies
5. **Patterns**: Verb-based naming, ErrorOr, composition
6. **Anti-Patterns**: UseCase/Engine suffix, layer violations
7. **Code Examples**: 3+ complete examples
8. **Collaboration**: Repository, Service, ViewModel agents
9. **Handoff Protocols**: When to delegate, when to escalate

### Key Naming Examples to Include
```csharp
// ✅ Correct
GetProducts
CreateOrder
UpdateUserProfile
DeleteAccount
ValidatePayment

// ❌ Incorrect
GetProductsUseCase
GetProductsEngine
ProductsFetcher
ProductsService
```

### Key Composition Examples to Include
```csharp
// Domain class composing Repository and Service
public class GetProducts
{
    private readonly IProductRepository _repository;
    private readonly IApiService _apiService;
    private readonly ICacheService _cacheService;

    public async Task<ErrorOr<List<Product>>> ExecuteAsync(string? category = null)
    {
        // 1. Try cache
        // 2. Try local database
        // 3. Fallback to API
        // 4. Update cache and database
    }
}
```

## Success Criteria

### Deliverables
- [x] Two identical agent markdown files created
- [x] Agent follows standard agent format
- [x] Domain pattern clearly defined
- [x] Verb-based naming thoroughly documented
- [x] ErrorOr pattern explained with examples
- [x] Collaboration patterns defined
- [x] Pre-implementation checks actionable
- [x] Anti-patterns clearly documented

### Quality Metrics
- [x] All acceptance criteria met (17/17)
- [x] No UseCase/Engine suffix in examples
- [x] At least 3 complete code examples
- [x] All collaboration patterns defined
- [x] All anti-patterns documented
- [x] Files are identical (diff returns 0)

### Validation
- [x] Agent content reviewed against architecture doc
- [x] Code examples compile (syntax valid)
- [x] Naming patterns consistent
- [x] Collaboration protocols clear
- [x] Handoff criteria actionable

## Notes

### Migration Context
This is **Phase 2.1** of the MAUI template migration:
- **Phase 1**: ✅ Architecture documentation created
- **Phase 2.1**: Create maui-domain-specialist agent (THIS TASK)
- **Phase 2.2**: Create maui-repository-specialist agent
- **Phase 2.3**: Create maui-service-specialist agent
- **Phase 2.4**: Update maui-viewmodel-specialist agent
- **Phase 3**: Update code templates
- **Phase 4**: Update CLAUDE.md guidance
- **Phase 5**: Deprecate old agents

### Key Differences from Old Pattern
**Old (UseCase/Engine)**:
- Name: GetProductsUseCase or GetProductsEngine
- Namespace: Engines or UseCases
- Suffix required
- Project-specific pattern

**New (Domain)**:
- Name: GetProducts (verb-based, no suffix)
- Namespace: Domain
- No suffix
- Generic, reusable pattern

### Reference Old Agent (Then Delete)
The old `maui-usecase-specialist.md` should be referenced for:
- Agent structure format
- Documentation style
- Collaboration patterns
- Pre-implementation checks

Then deleted after migration is complete.

## Complexity Justification

**Score: 5/10 (Medium)**

### Factors:
1. **File Complexity (1/3)**: Only 2 identical files to create
2. **Pattern Familiarity (1/2)**: Agent creation is familiar, but Domain pattern is new
3. **Risk Level (1/3)**: Low risk - documentation only, no code changes
4. **Dependencies (2/2)**: Depends on architecture doc and existing agent patterns

### Rationale:
- Straightforward agent documentation task
- Clear pattern defined in architecture doc
- No code implementation required
- Low risk of breaking changes
- Medium complexity due to need for comprehensive documentation
- Requires understanding new Domain pattern thoroughly

## Timeline Estimate

**Estimated Duration**: 1-2 hours

### Breakdown:
- Agent structure setup: 15 minutes
- Domain pattern documentation: 20 minutes
- Code examples creation: 30 minutes
- Collaboration patterns: 15 minutes
- Pre-implementation checks: 15 minutes
- Anti-patterns documentation: 15 minutes
- Template duplication and verification: 10 minutes

## Priority Justification

**HIGH** priority because:
- Blocks all subsequent MAUI template migration tasks
- Phase 2.1 is first step in agent migration
- Required for Phase 2.2, 2.3, 2.4 completion
- Foundation for new Domain pattern
- Critical for template consistency
- Enables future MAUI development work

## Next Steps After Completion

After this task completes:
1. Move to Phase 2.2: Create maui-repository-specialist agent
2. Move to Phase 2.3: Create maui-service-specialist agent
3. Move to Phase 2.4: Update maui-viewmodel-specialist agent
4. Begin Phase 3: Update code templates
5. Complete Phase 4: Update CLAUDE.md guidance
6. Finalize Phase 5: Deprecate old agents
