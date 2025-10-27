---
id: TASK-011J
title: Create comprehensive MAUI template documentation
status: completed
created: 2025-10-12T10:35:00Z
updated: 2025-10-17T00:00:00Z
completed: 2025-10-17T00:00:00Z
previous_state: in_progress
state_transition_reason: "All quality gates passed - ready for human review"
completed_phases:
  - phase_1: "Requirements Analysis"
  - phase_2: "Implementation Planning"
  - phase_2_5a: "Pattern Suggestion"
  - phase_2_5b: "Architectural Review (82/100)"
  - phase_2_7: "Complexity Evaluation (4/10)"
  - phase_2_8: "Human Checkpoint (auto-approved)"
  - phase_3: "Implementation (5 files created)"
  - phase_4: "Testing (95/100 quality score)"
  - phase_4_5: "Fix Loop (no fixes needed)"
  - phase_5: "Code Review (95/100)"
quality_metrics:
  documentation_quality: 95
  word_count: 12444
  code_examples: 306
  diagrams: 13
  faq_questions: 28
  cross_references: 28
priority: medium
tags: [documentation, maui, templates, migration, phase-5]
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
      score: 2
      max_score: 3
      justification: "4 new documentation files to create"
    - factor: "pattern_familiarity"
      score: 1
      max_score: 2
      justification: "Following established documentation patterns from TASK-010"
    - factor: "risk_level"
      score: 1
      max_score: 3
      justification: "Documentation only, low risk"
    - factor: "dependencies"
      score: 1
      max_score: 2
      justification: "Depends on existing architecture docs"
---

# Task: Create Comprehensive MAUI Template Documentation

## Context

This is Phase 5 of the MAUI template migration plan, which involves creating all documentation for the new MAUI template system. The migration introduces a dual-template system with global generic templates (Domain pattern) and local custom templates (project-specific patterns like Engine).

Related documents:
- `docs/shared/maui-template-architecture.md` - Architecture overview (already created)
- `docs/workflows/maui-template-migration-plan.md` - Complete migration plan
- TASK-010 - Similar documentation task for workflow guides (provides pattern reference)

## Objective

Create comprehensive documentation covering template selection, local template creation, Domain pattern best practices, and migration from Engine to Domain pattern. Documentation should follow the Progressive Disclosure pattern established in TASK-010.

## Requirements

### Documentation Files to Create

1. **docs/guides/maui-template-selection.md**
   - When to use AppShell vs NavigationPage
   - Template feature comparison
   - Use case recommendations
   - Decision framework

2. **docs/guides/creating-local-templates.md**
   - Step-by-step local template creation
   - Customization options
   - Version control best practices
   - Template inheritance patterns
   - Real-world examples

3. **docs/patterns/domain-layer-pattern.md**
   - Domain pattern best practices
   - Verb-based naming conventions
   - Repository (database) vs Service (API/hardware) separation
   - ErrorOr pattern usage
   - Testing strategies
   - Anti-patterns to avoid

4. **docs/migration/engine-to-domain.md**
   - Migration from Engine pattern to Domain pattern
   - Before/after code examples
   - MyDrive case study
   - Step-by-step migration process
   - Common pitfalls and solutions
   - Pattern translation guide

### Documentation Standards

- Follow Progressive Disclosure pattern (Quick Start → Core Concepts → Complete Reference → Examples → FAQ)
- Include real-world code examples
- Provide decision frameworks and checklists
- Add troubleshooting sections
- Include visual diagrams where appropriate
- Cross-reference related documentation
- Use consistent terminology

### Content Quality Requirements

- All code examples must be syntactically valid
- Examples should be tested and working
- Include both positive and negative examples (what to do and what to avoid)
- Provide rationale for design decisions
- Address common questions and concerns
- Include performance considerations
- Add security best practices where relevant

### Integration Requirements

- Update CLAUDE.md with references to new documentation
- Cross-reference with existing MAUI template architecture doc
- Link to migration plan
- Reference from installer documentation
- Add to main documentation index

## Acceptance Criteria

### Content Completeness ✅
- [ ] All 4 guide documents created and comprehensive
- [ ] Template selection guide clearly explains use cases
- [ ] Local template creation guide has step-by-step instructions
- [ ] Domain pattern guide includes examples and anti-patterns
- [ ] Migration guide shows before/after examples
- [ ] All sections outlined in requirements are present
- [ ] Each guide has Quick Start, Core Concepts, Examples, and FAQ sections

### Code Quality ✅
- [ ] All code examples are syntactically valid
- [ ] Examples follow established MAUI patterns
- [ ] Both positive and negative examples included
- [ ] Code snippets properly formatted with syntax highlighting
- [ ] Complete working examples provided (not just fragments)

### Usability ✅
- [ ] Clear decision frameworks for template selection
- [ ] Step-by-step instructions are actionable
- [ ] Migration path is clearly defined
- [ ] Troubleshooting section covers common issues
- [ ] FAQ addresses likely questions
- [ ] Navigation is intuitive with clear headings

### Consistency ✅
- [ ] Terminology consistent with CLAUDE.md
- [ ] Follows Progressive Disclosure pattern from TASK-010
- [ ] Cross-references to related documentation are accurate
- [ ] Formatting consistent across all four guides
- [ ] Examples follow same patterns as existing docs

### Integration ✅
- [ ] CLAUDE.md updated with new template references
- [ ] Cross-references with maui-template-architecture.md
- [ ] Links to migration plan included
- [ ] Main documentation index updated
- [ ] All internal links validated

### Visual Elements (Optional) ✅
- [ ] Architecture diagrams for layer separation
- [ ] Decision tree for template selection
- [ ] Before/after comparison diagrams for migration
- [ ] Flow diagrams for local template creation process

## Implementation Guidelines

### Follow TASK-010 Pattern
Use the successful documentation pattern from TASK-010 as a reference:
- Progressive Disclosure structure
- Clear section organization
- Comprehensive examples
- Practical FAQ sections
- Cross-reference strategy

### Documentation Structure
Each guide should include:
1. **Quick Start** (2-5 minutes) - Immediate action
2. **Core Concepts** - Essential understanding
3. **Complete Reference** - Comprehensive details
4. **Real-World Examples** - Practical scenarios
5. **FAQ** - Common questions
6. **Troubleshooting** - Problem resolution

### Code Examples
- Use realistic scenarios (not toy examples)
- Show complete working code when possible
- Include comments explaining key concepts
- Provide both C# and XAML examples
- Show test examples for testable code

### Visual Diagrams
Consider using Mermaid diagrams for:
- Architecture layer relationships
- Template selection decision tree
- Migration workflow steps
- Pattern comparison visualizations

## Related Documentation

### Existing Documents
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/shared/maui-template-architecture.md` - Architecture overview
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/maui-template-migration-plan.md` - Complete migration plan
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/CLAUDE.md` - Main project documentation (needs update)

### Reference Documents
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/tasks/completed/TASK-010-create-workflow-guides.md` - Documentation pattern reference
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/complexity-management-workflow.md` - Progressive Disclosure example
- `/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/ux-design-integration-workflow.md` - Comprehensive guide example

## Estimated Complexity

**Score**: 5/10 (Medium)

**Justification**:
- **File Complexity** (2/3): Creating 4 new documentation files plus updating CLAUDE.md
- **Pattern Familiarity** (1/2): Following established documentation patterns from TASK-010
- **Risk Level** (1/3): Documentation only, low risk of breaking changes
- **Dependencies** (1/2): Depends on existing architecture documentation

**Review Mode**: QUICK_OPTIONAL (30-second timeout at human checkpoint)

**Estimated Duration**: 4-6 hours

## Success Metrics

### Completeness
- All 4 documentation files created: 100%
- All sections per requirements: 100%
- Code examples tested: 100%
- Cross-references validated: 100%

### Quality
- Documentation clarity score: Target 95/100
- Code example validity: 100%
- Consistency score: Target 95/100
- Usability score: Target 90/100

### Impact
- Developers can select appropriate template: Self-service
- Local template creation: Clear process
- Domain pattern adoption: Clear guidance
- Migration path: Actionable steps

## Notes

### Migration Plan Context
This task is **Phase 5** of the MAUI template migration plan:
- **Phase 1**: ✅ Create Global Templates (completed)
- **Phase 2**: 🔄 Create Specialized Agents (in progress)
- **Phase 3**: 📦 Migrate MyDrive to Local Template (pending)
- **Phase 4**: 🔧 Update Installer for Local Templates (pending)
- **Phase 5**: 📚 Documentation (this task)

### Key Documentation Goals
1. Make template selection obvious and easy
2. Enable teams to create custom templates confidently
3. Provide clear migration path from legacy patterns
4. Establish Domain pattern as the standard approach
5. Support both global and local template workflows

### Design Decisions to Document
- Why verb-based naming over UseCase/Engine suffix
- Why Repository (database) separate from Service (API)
- When to use AppShell vs NavigationPage
- When to create local templates vs using global
- How to inherit from global templates

### Audience Considerations
- **New Users**: Need clear template selection guidance
- **Existing Users**: Need migration path from Engine pattern
- **Team Leads**: Need local template creation guidance
- **All Users**: Need Domain pattern best practices

## Priority Justification

**MEDIUM** priority because:
- Completes Phase 5 of migration plan
- Enables self-service for template selection and creation
- Not blocking Phase 1-2 implementation
- Supports Phase 3-4 (MyDrive migration and installer updates)
- Enhances user experience and adoption
- Establishes clear patterns for MAUI development

## Next Steps After Completion

1. Update installer documentation to reference new guides
2. Create template selection wizard (optional enhancement)
3. Add inline help to template commands
4. Consider video tutorials for complex workflows
5. Gather feedback from early adopters
6. Iterate on examples based on real-world usage

---

**Status**: Ready for implementation
**Timeline**: 4-6 hours estimated
**Dependencies**: Phase 1-2 templates and agents
**Deliverables**: 4 comprehensive documentation files + CLAUDE.md update
