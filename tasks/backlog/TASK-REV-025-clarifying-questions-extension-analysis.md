---
id: TASK-REV-025
title: Analyze Clarifying Questions Feature for RequireKit Extension
status: review_complete
type: review
task_type: review
decision_required: true
created: 2025-12-09T10:00:00Z
completed: 2025-12-09T11:30:00Z
priority: normal
tags: [architecture-review, clarifying-questions, cross-project, feature-analysis]
complexity: 6
review_mode: decision
review_results:
  decision: partial_go
  recommendation: Targeted enhancement for hierarchy commands
  effort_estimate: 1.75-2.25 days
  report_path: .claude/reviews/TASK-REV-025-review-report.md
  implementation_tasks:
    - TASK-CLQ-001
    - TASK-CLQ-002
    - TASK-CLQ-003
    - TASK-CLQ-004
    - TASK-CLQ-005
  implementation_path: tasks/backlog/clarifying-questions/
references:
  guardkit_review: /Users/richardwoollcott/Projects/appmilla_github/guardkit/.claude/reviews/TASK-REV-B130-review-report.md
  guardkit_tasks: /Users/richardwoollcott/Projects/appmilla_github/guardkit/tasks/backlog/clarifying-questions/
  requirekit_gather: .claude/commands/gather-requirements.md
---

# Review Task: Clarifying Questions Extension for RequireKit

## Review Objective

Analyze the clarifying questions feature being implemented in GuardKit and determine whether/how it should be extended into RequireKit commands beyond the existing `gather-requirements` implementation.

## Context

### Current State in RequireKit

The `/gather-requirements` command already implements a clarifying questions pattern with:
- **3-phase discovery framework**: Discovery (High-Level) → Exploration (Detailed) → Validation
- **5W1H Framework**: What/Who/When/Where/Why/How question categories
- **Interactive Q&A format**: Progressive question-answer sessions
- **Output**: Natural language requirements ready for EARS formalization

### GuardKit's New Clarifying Questions Feature

GuardKit is implementing a comprehensive clarifying questions system (TASK-REV-B130) that:

1. **Applies to multiple commands**: `/task-work`, `/task-review`, `/feature-plan`
2. **Uses three clarification contexts**:
   - **Context A (Review Scope)**: Guide what analysis should focus on
   - **Context B (Implementation Prefs)**: Guide subtask creation approach
   - **Context C (Implementation Planning)**: Guide scope, tech choices, trade-offs
3. **Features complexity gating**: Skip/Quick/Full modes based on task complexity
4. **Includes unified module architecture**: Shared core, detection, display, templates
5. **Supports command-line flags**: `--no-questions`, `--with-questions`, `--defaults`

### Key Design Principles from GuardKit Analysis

From the TASK-REV-B130 review report:
- **Questions come AFTER context gathering** (informed, specific questions)
- **Blocking pattern** for complex tasks (requires human input)
- **3-7 questions max** to avoid question fatigue
- **Sensible defaults** with explicit "use defaults" option
- **Persistence to frontmatter** for audit trail

## Questions to Answer

### Primary Decision Questions

1. **Should RequireKit adopt the unified clarification module pattern?**
   - Could `/formalize-ears` benefit from clarifying questions about ambiguous requirements?
   - Could `/generate-bdd` benefit from clarifying questions about test scope/coverage?
   - Could `/epic-create` and `/feature-create` benefit from scope clarification?

2. **Is there overlap/conflict with existing `gather-requirements`?**
   - Does the new system complement or compete with gather-requirements?
   - Should gather-requirements be refactored to use the unified module?
   - Is the 3-phase discovery framework compatible with the new approach?

3. **What integration approach makes sense?**
   - Option A: Import GuardKit's clarification module as a dependency
   - Option B: Create RequireKit-specific implementation inspired by the pattern
   - Option C: Extend gather-requirements as the single clarification touchpoint
   - Option D: No extension needed - current approach is sufficient

### Secondary Analysis Questions

4. **Which RequireKit commands would benefit most from clarification?**
   - Rank by impact: formalize-ears, generate-bdd, epic-create, feature-create
   - Consider complexity distribution of typical use cases

5. **What RequireKit-specific question categories are needed?**
   - Requirements ambiguity detection
   - EARS pattern selection guidance
   - BDD scenario scope clarification
   - Epic/feature hierarchy decisions

6. **How does this align with RequireKit's technology-agnostic philosophy?**
   - GuardKit's approach includes tech-specific questions (JWT vs Sessions, etc.)
   - RequireKit focuses on specification, not implementation
   - What clarification is appropriate at the requirements level?

## Analysis Scope

### Files to Analyze in RequireKit

- [.claude/commands/gather-requirements.md](.claude/commands/gather-requirements.md) - Current Q&A implementation
- [.claude/commands/formalize-ears.md](.claude/commands/formalize-ears.md) - EARS conversion (could benefit?)
- [.claude/commands/generate-bdd.md](.claude/commands/generate-bdd.md) - BDD generation (could benefit?)
- [.claude/commands/epic-create.md](.claude/commands/epic-create.md) - Epic creation
- [.claude/commands/feature-create.md](.claude/commands/feature-create.md) - Feature creation

### External References (Already Read)

- GuardKit TASK-REV-B130 review report (comprehensive spec)
- GuardKit clarifying-questions implementation tasks (12 subtasks)
- GuardKit IMPLEMENTATION-GUIDE.md (wave structure, architecture)

## Expected Deliverables

1. **Decision recommendation**: GO/NO-GO/PARTIAL for extending clarifying questions
2. **If GO/PARTIAL**:
   - Which commands should receive clarification
   - Recommended architecture approach (A/B/C/D from above)
   - RequireKit-specific question categories
   - Integration points with GuardKit (if any)
3. **If NO-GO**:
   - Justification for current approach being sufficient
   - Any minor enhancements to gather-requirements recommended

## Acceptance Criteria

- [ ] All RequireKit commands analyzed for clarification benefit
- [ ] Comparison matrix: current gather-requirements vs GuardKit approach
- [ ] Clear recommendation with rationale
- [ ] If implementing: rough scope estimate (effort in days)
- [ ] Alignment check with RequireKit philosophy documented

## Notes

- This review should focus on RequireKit's role as a **requirements management** toolkit
- Consider that RequireKit users are gathering/formalizing requirements, not implementing code
- The clarification needs at the requirements level differ from implementation-level clarification
- Maintain technology-agnostic stance - no implementation-specific questions

## Suggested Workflow

1. Use `/task-review TASK-REV-025` to execute this analysis
2. Review will analyze all referenced files
3. Generate decision report with recommendation
4. Present at checkpoint for user decision [A]ccept/[R]evise/[I]mplement/[C]ancel
