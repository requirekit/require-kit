# Epic/Feature Hierarchy

Organize requirements using a flexible hierarchy that adapts to your project's needs. RequireKit supports three organisation patterns so you can choose the right level of structure for each epic.

## Organisation Patterns

RequireKit offers three ways to organise work within an epic:

| Pattern | Structure | Best For |
|---|---|---|
| **Standard** | Epic → Feature → Task | Large epics with 8+ tasks across distinct capabilities |
| **Direct** | Epic → Task | Small, focused epics with 3-5 closely related tasks |
| **Mixed** | Epic → Feature + Task | Transitional epics migrating between patterns |

### Standard Pattern (Epic → Feature → Task)

The default pattern groups tasks under features for maximum organisation.

```
EPIC (Strategic Business Objective)
├── FEATURE (Implementation Unit)
│   ├── REQ-001 (EARS Requirement)
│   ├── REQ-002 (EARS Requirement)
│   └── BDD-001 (Gherkin Scenarios)
├── FEATURE (Implementation Unit)
│   ├── REQ-003 (EARS Requirement)
│   └── BDD-002 (Gherkin Scenarios)
```

**When to use:**

- Epic spans multiple distinct capabilities (authentication, notifications, reporting)
- More than 8 tasks expected
- Multiple team members working on different areas
- You need feature-level progress tracking

### Direct Pattern (Epic → Task)

Skip the feature layer for small, focused epics where features add unnecessary overhead.

```
EPIC (Focused Business Objective)
├── TASK-001 (Implementation)
├── TASK-002 (Implementation)
├── TASK-003 (Implementation)
├── REQ-001 (EARS Requirement)
└── BDD-001 (Gherkin Scenarios)
```

**When to use:**

- Epic has 3-5 closely related tasks
- All tasks serve a single capability
- Single developer or small team
- Quick iteration is more important than detailed hierarchy

### Mixed Pattern (Epic → Feature + Task)

Combine features and direct tasks in one epic. Useful during transitions but avoid as a permanent structure.

```
EPIC (Business Objective)
├── FEATURE (Grouped Capability)
│   ├── TASK-001 (Implementation)
│   └── TASK-002 (Implementation)
├── TASK-003 (Direct Task - ungrouped)
└── TASK-004 (Direct Task - ungrouped)
```

!!! warning "Use Mixed Pattern Sparingly"
    The mixed pattern works during migration between direct and standard patterns, but permanent mixed structures make tracking and reporting harder. Prefer committing to either standard or direct.

**When to use:**

- Transitioning from direct to standard (grouping related tasks into features)
- Transitioning from standard to direct (dissolving unnecessary features)
- Temporary state during epic restructuring

## PM Tool Mapping

Each organisation pattern maps to common project management tools:

| RequireKit | Jira | Linear | GitHub Projects | Azure DevOps |
|---|---|---|---|---|
| **Epic** | Epic | Project | Project | Epic |
| **Feature** | Story / Feature | Sub-project | Milestone | Feature |
| **Task** | Task / Sub-task | Issue | Issue | Work Item |
| **Requirement** | Acceptance Criteria | Issue description | Issue body | Requirement |
| **BDD Scenario** | Test Case | — | — | Test Case |

### Pattern-Specific Mapping

=== "Standard Pattern"

    ```
    Jira:    Epic → Story → Sub-task
    Linear:  Project → Sub-project → Issue
    GitHub:  Project → Milestone → Issue
    ```

=== "Direct Pattern"

    ```
    Jira:    Epic → Task (no Story layer)
    Linear:  Project → Issue (no Sub-project)
    GitHub:  Project → Issue (no Milestone)
    ```

=== "Mixed Pattern"

    ```
    Jira:    Epic → Story + Task (mixed children)
    Linear:  Project → Sub-project + Issue (mixed children)
    GitHub:  Project → Milestone + Issue (mixed children)
    ```

## Epics

**Definition**: Strategic business objective or large body of work.

**Examples:**

- User Management System
- E-Commerce Platform
- Mobile Application
- API Integration Layer

**Commands:**
```bash
/epic-create "User Management System"
/epic-create "Config Refactor" --pattern direct    # Use direct pattern
/epic-status EPIC-001
/epic-generate-features EPIC-001
/epic-refine EPIC-001                              # Iteratively improve epic
```

## Features

**Definition**: Specific capability or behavior that delivers value. Used in the standard and mixed patterns.

**Examples:**

- User Authentication
- Shopping Cart
- Payment Processing
- Email Notifications

**Commands:**
```bash
/feature-create "User Authentication" epic:EPIC-001
/feature-status FEAT-001
/feature-generate-tasks FEAT-001
/feature-refine FEAT-001                           # Iteratively improve feature
```

!!! note "Features Are Optional"
    In the direct pattern, tasks attach directly to epics without a feature layer. Features are only required in the standard pattern.

## Requirements

**Definition**: EARS-formatted requirement specifying precise behavior.

**Link to:** Features (standard pattern) or Epics (direct pattern). One requirement can belong to multiple features or epics.

## Traceability

### Forward Traceability (Standard Pattern)

Track from strategic goals to implementation:
```
EPIC-001 (Business Goal)
  → FEAT-001 (Capability)
    → REQ-001 (Requirement)
      → BDD-001 (Test Specification)
        → TASK-001 (Implementation)
```

### Forward Traceability (Direct Pattern)

Track from strategic goals directly to implementation:
```
EPIC-001 (Business Goal)
  → REQ-001 (Requirement)
    → BDD-001 (Test Specification)
      → TASK-001 (Implementation)
```

### Backward Traceability

Track from implementation back to business goals:

=== "Standard Pattern"

    ```
    TASK-001 (Code) → BDD-001 → REQ-001 → FEAT-001 → EPIC-001
    ```

=== "Direct Pattern"

    ```
    TASK-001 (Code) → BDD-001 → REQ-001 → EPIC-001
    ```

## Real-World Examples

### Large Epic with Standard Pattern

```
EPIC-001: E-Commerce Platform          [pattern: standard]
├── FEAT-001: Product Catalog
│   ├── REQ-001: Product search functionality
│   ├── REQ-002: Product filtering
│   ├── REQ-003: Product sorting
│   └── BDD-001: Product browsing scenarios
├── FEAT-002: Shopping Cart
│   ├── REQ-004: Add items to cart
│   ├── REQ-005: Remove items from cart
│   ├── REQ-006: Update quantities
│   └── BDD-002: Shopping cart scenarios
└── FEAT-003: Checkout Process
    ├── REQ-007: Payment processing
    ├── REQ-008: Order confirmation
    └── BDD-003: Checkout scenarios
```

### Small Epic with Direct Pattern

```
EPIC-002: Configuration Refactor       [pattern: direct]
├── TASK-001: Extract config from hardcoded values
├── TASK-002: Add environment variable support
├── TASK-003: Add config validation on startup
├── REQ-001: The system shall load configuration from environment variables
└── BDD-001: Configuration loading scenarios
```

### Mixed Pattern (Transitional)

!!! warning
    This example shows a transitional state. The direct tasks (TASK-004, TASK-005) should eventually be grouped into a feature or the features should be dissolved.

```
EPIC-003: API Integration Layer        [pattern: mixed]
├── FEAT-001: REST Client
│   ├── TASK-001: HTTP client wrapper
│   ├── TASK-002: Retry logic
│   └── TASK-003: Response parsing
├── TASK-004: API key management       (direct, ungrouped)
└── TASK-005: Rate limiting setup      (direct, ungrouped)
```

## Migrating Between Patterns

Use `/epic-refine` to change an epic's organisation pattern:

```bash
# Promote direct → standard (group tasks into features)
/epic-refine EPIC-002 --pattern standard

# Simplify standard → direct (dissolve features)
/epic-refine EPIC-001 --pattern direct
```

**Migration guidelines:**

- **Direct → Standard**: When an epic grows beyond 5 tasks, group related tasks into features
- **Standard → Direct**: When features have only 1-2 tasks each, dissolve features and attach tasks directly
- **Mixed → Standard or Direct**: Resolve the mixed state by committing to one pattern

## Best Practices

### Pattern Selection

| Epic Size | Recommended Pattern | Rationale |
|---|---|---|
| 3-5 tasks | Direct | Features add overhead without value |
| 6-7 tasks | Either | Use judgement based on task relatedness |
| 8+ tasks | Standard | Features provide necessary organisation |

### General Guidelines

- **Epics should be strategic**: Business objectives, not technical tasks
- **Features should be independently deliverable**: Each provides value alone
- **Requirements should be atomic**: One behavior per requirement
- **Maintain links**: Always connect requirements to features or epics
- **Avoid mixed unless transitioning**: Commit to standard or direct
- **Refine iteratively**: Use `/epic-refine` and `/feature-refine` to improve hierarchy over time

## Benefits

- **Clear organization**: Hierarchical structure is easy to understand
- **Flexible patterns**: Choose the right level of structure for each epic
- **Impact analysis**: Quickly assess effect of changes
- **Progress tracking**: Monitor completion at epic, feature, and requirement levels
- **Stakeholder communication**: Discuss at appropriate abstraction level

## Commands

```bash
# View hierarchy
/hierarchy-view EPIC-001

# Generate features from epic
/epic-generate-features EPIC-001

# Generate tasks from feature
/feature-generate-tasks FEAT-001

# Refine existing epic (change pattern, improve structure)
/epic-refine EPIC-001
/epic-refine EPIC-001 --pattern standard

# Refine existing feature
/feature-refine FEAT-001
```

## Next Steps

- [Learn about Requirements Traceability](traceability.md)
- [Try creating your first epic](../getting-started/first-requirements.md)
- [See hierarchy examples](../examples/features.md)
