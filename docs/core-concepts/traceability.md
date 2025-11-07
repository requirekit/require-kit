# Requirements Traceability

Track relationships between requirements, features, epics, and implementation for complete visibility.

## What is Traceability?

**Requirements traceability** is the ability to trace a requirement through its lifecycle: from origin through specification, implementation, testing, and deployment.

## Traceability in RequireKit

RequireKit maintains automatic traceability through markdown files with structured metadata:

```
EPIC-001 (Strategic)
    ↓ contains
FEAT-001 (Tactical)
    ↓ implements
REQ-001 (EARS Specification)
    ↓ verified by
BDD-001 (Test Scenarios)
    ↓ executed by (with taskwright)
TASK-001 (Implementation)
```

## Types of Traceability

### Forward Traceability
**From requirements to implementation:**
- Which features implement this requirement?
- What tests verify this requirement?
- Which tasks implement this feature?

### Backward Traceability
**From implementation to requirements:**
- Why was this code written?
- Which requirement justified this feature?
- Which business objective does this support?

### Horizontal Traceability
**Between peer artifacts:**
- Which requirements relate to each other?
- Which features share requirements?
- Which tests cover multiple requirements?

## Traceability Links

### Epic Metadata
```yaml
---
id: EPIC-001
title: User Management System
features: [FEAT-001, FEAT-002, FEAT-003]
---
```

### Feature Metadata
```yaml
---
id: FEAT-001
title: User Authentication
epic: EPIC-001
requirements: [REQ-001, REQ-002, REQ-003]
bdd_scenarios: [BDD-001]
---
```

### Requirement Metadata
```yaml
---
id: REQ-001
title: User login with valid credentials
feature: FEAT-001
bdd_scenarios: [BDD-001]
---
```

## Benefits

### Impact Analysis
Quickly understand the effect of changes:
```
Change REQ-003 → Affects:
  - FEAT-001 (must update)
  - BDD-001 (must regenerate)
  - TASK-001 (may need changes)
```

### Change Management
Track why changes were made:
```
Code changed in TASK-001 → Because:
  - REQ-003 was updated
  - Which affected FEAT-001
  - To satisfy EPIC-001 goal
```

### Compliance
Demonstrate requirement coverage:
```
Requirement REQ-001
  → Implemented by FEAT-001
    → Tested by BDD-001
      → Verified by automated tests
```

### Gap Analysis
Identify missing coverage:
- Requirements without features
- Features without tests
- Epics without features

## Commands

```bash
# View complete hierarchy
/hierarchy-view EPIC-001

# Check requirement links
/requirement-trace REQ-001

# Generate traceability report
/trace-report EPIC-001
```

## Example: Complete Traceability

```
Business Need: Secure user access
    ↓
EPIC-001: User Management System
    ↓
FEAT-001: User Authentication
    ↓
REQ-001: When a user submits valid credentials,
         the system shall authenticate within 1s
    ↓
BDD-001: Scenario: Successful login
         Given valid credentials
         When user submits login
         Then authenticate within 1s
    ↓
TASK-001: Implement authentication endpoint
    ↓
Code: auth-service.ts:42-89
    ↓
Test: auth.test.ts:15-35 (passes)
    ↓
Deployed: v1.2.0
```

## Maintaining Traceability

### During Requirements Gathering
```bash
/gather-requirements
/formalize-ears
# Requirements automatically linked to session
```

### During Organization
```bash
/epic-create "Title"
/feature-create "Title" epic:EPIC-001
# Links maintained in frontmatter
```

### During Implementation (with taskwright)
```bash
/feature-generate-tasks FEAT-001
# Tasks include requirement context
```

### During Updates
```bash
# Update requirement
/formalize-ears --refresh

# Regenerate BDD
/generate-bdd --refresh

# Links automatically updated
```

## Best Practices

✅ **Always link requirements to features**
✅ **Update BDD when requirements change**
✅ **Use hierarchy commands to visualize**
✅ **Document rationale in requirement files**
✅ **Review traceability during changes**

## Tools

### View Commands
```bash
/hierarchy-view EPIC-001  # Visual hierarchy
/requirement-trace REQ-001  # Requirement links
/feature-status FEAT-001  # Feature completeness
```

### Export Commands
```bash
/epic-sync EPIC-001 --export  # Export traceability data
/feature-sync FEAT-001 --jira  # Sync to PM tools
```

## Next Steps

- 🏗️ [Learn about Epic/Feature Hierarchy](hierarchy.md)
- 📝 [Practice with examples](../examples/features.md)
- 🔗 [Explore integration options](../getting-started/integration.md)
