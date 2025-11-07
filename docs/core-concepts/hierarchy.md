# Epic/Feature Hierarchy

Organize requirements using Epic → Feature → Requirement hierarchy for clear traceability.

## Hierarchy Structure

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
/epic-status EPIC-001
/epic-generate-features EPIC-001
```

## Features

**Definition**: Specific capability or behavior that delivers value.

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
```

## Requirements

**Definition**: EARS-formatted requirement specifying precise behavior.

**Link to:** Features (one requirement can belong to multiple features)

## Traceability

### Forward Traceability
Track from strategic goals to implementation:
```
EPIC-001 (Business Goal)
  → FEAT-001 (Capability)
    → REQ-001 (Requirement)
      → BDD-001 (Test Specification)
        → TASK-001 (Implementation)
```

### Backward Traceability
Track from implementation back to business goals:
```
TASK-001 (Code) → BDD-001 → REQ-001 → FEAT-001 → EPIC-001
```

## Real-World Example

```
EPIC-001: E-Commerce Platform
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

## Best Practices

✅ **Epics should be strategic**: Business objectives, not technical tasks
✅ **Features should be independently deliverable**: Each provides value alone
✅ **Requirements should be atomic**: One behavior per requirement
✅ **Maintain links**: Always connect requirements to features and epics

## Benefits

- **Clear organization**: Hierarchical structure is easy to understand
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
```

## Next Steps

- 🔍 [Learn about Requirements Traceability](traceability.md)
- 📝 [Try creating your first epic](../getting-started/first-requirements.md)
- 💡 [See hierarchy examples](../examples/features.md)
