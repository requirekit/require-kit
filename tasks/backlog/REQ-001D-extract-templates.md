---
id: REQ-001D
title: "Extract Documentation Templates"
created: 2025-10-27
status: backlog
priority: high
complexity: 4
parent_task: REQ-001
subtasks: []
estimated_hours: 2
---

# REQ-001D: Extract Documentation Templates

## Description

Extract requirements documentation templates (EARS, BDD, epic, feature) from ai-engineer to require-kit.

## Templates to Extract

### Requirements Templates

```bash
✅ requirements/
   ├── requirement-template.md       # EARS requirement
   ├── requirement-ubiquitous.md     # Ubiquitous pattern
   ├── requirement-event-driven.md   # Event-driven pattern
   ├── requirement-state-driven.md   # State-driven pattern
   ├── requirement-unwanted.md       # Unwanted behavior pattern
   └── requirement-optional.md       # Optional feature pattern
```

### BDD Templates

```bash
✅ bdd/
   ├── scenario-template.feature     # Gherkin scenario
   ├── feature-template.feature      # Feature file
   └── examples/
       ├── user-authentication.feature
       └── data-validation.feature
```

### Epic Templates

```bash
✅ epics/
   ├── epic-template.md
   └── examples/
       └── user-management-epic.md
```

### Feature Templates

```bash
✅ features/
   ├── feature-template.md
   └── examples/
       └── user-login-feature.md
```

## Templates to Exclude

```bash
❌ tasks/                    # Task templates (Agentecflow)
❌ implementation-plan.md    # Implementation planning (Agentecflow)
❌ Stack-specific templates  # React, Python, MAUI, etc.
❌ Quality gate templates    # Architectural review, test reports
```

## Template Structure

### requirement-template.md

```markdown
---
id: REQ-XXX
title: ""
type: functional|non-functional
priority: must-have|should-have|could-have|won't-have
status: draft|approved|implemented|deprecated
epic: EPIC-XXX
feature: FEAT-XXX
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# REQ-XXX: [Title]

## EARS Pattern

[Select: Ubiquitous | Event-Driven | State-Driven | Unwanted | Optional]

## Requirement Statement

[EARS-formatted requirement]

## Rationale

[Why this requirement exists]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Related Requirements

- REQ-YYY: [Relationship]

## Traceability

- Epic: EPIC-XXX
- Feature: FEAT-XXX
- BDD Scenarios: [SCEN-001, SCEN-002]

## Notes

[Additional context]
```

### epic-template.md

```markdown
---
id: EPIC-XXX
title: ""
status: active|completed|cancelled
priority: high|medium|low
business_value: high|medium|low
created: YYYY-MM-DD
target_date: YYYY-MM-DD
---

# EPIC-XXX: [Title]

## Overview

[High-level description]

## Business Value

[Why this epic matters]

## Features

- [ ] FEAT-001: [Feature name]
- [ ] FEAT-002: [Feature name]

## Requirements

- REQ-001: [Requirement summary]
- REQ-002: [Requirement summary]

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies

[External dependencies]

## Risks

[Potential risks]

## Timeline

[Estimated timeline]
```

### feature-template.md

```markdown
---
id: FEAT-XXX
title: ""
epic: EPIC-XXX
status: active|in_progress|completed
priority: high|medium|low
created: YYYY-MM-DD
---

# FEAT-XXX: [Title]

## Overview

[Feature description]

## Requirements

- REQ-001: [Requirement]
- REQ-002: [Requirement]

## BDD Scenarios

[Link to scenarios or embed here]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies

[Dependencies]

## Notes

[Additional context]
```

### scenario-template.feature

```gherkin
Feature: [Feature Name]
  As a [role]
  I want [functionality]
  So that [business value]

  Background:
    Given [common setup]

  Scenario: [Scenario name]
    Given [precondition]
    When [action]
    Then [expected outcome]

  Scenario Outline: [Parameterized scenario]
    Given [precondition with <parameter>]
    When [action with <parameter>]
    Then [expected outcome with <parameter>]

    Examples:
      | parameter |
      | value1    |
      | value2    |
```

## Implementation Steps

```bash
# Create template directories
mkdir -p /path/to/require-kit/requirements/templates/{requirements,bdd,epics,features}
mkdir -p /path/to/require-kit/requirements/templates/{requirements,bdd,epics,features}/examples

# If ai-engineer has these templates, copy them
# Otherwise, create them from the specifications above

# Copy or create requirement templates
# Copy or create BDD templates
# Copy or create epic templates
# Copy or create feature templates
```

## Verification

```bash
cd /path/to/require-kit/requirements/templates/

# Verify structure
tree -L 2

# Expected:
# ├── requirements/
# │   ├── requirement-template.md
# │   └── examples/
# ├── bdd/
# │   ├── scenario-template.feature
# │   └── examples/
# ├── epics/
# │   ├── epic-template.md
# │   └── examples/
# └── features/
#     ├── feature-template.md
#     └── examples/

# Check no task/implementation references
grep -r "task\|implementation\|quality.*gate" . | grep -v "# "
# Should be EMPTY
```

## Acceptance Criteria

- [ ] All requirement templates created
- [ ] All BDD templates created
- [ ] All epic templates created
- [ ] All feature templates created
- [ ] Example templates provided for each type
- [ ] No task execution references
- [ ] No implementation references
- [ ] Templates focused on requirements management

## Estimated Time

2 hours

## Notes

- These are markdown/feature file templates, not code templates
- Focus on requirements documentation structure
- Provide good examples in examples/ directories
- Keep templates simple and focused
