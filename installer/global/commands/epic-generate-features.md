# Epic Generate Features - Auto-Generate Features from Epic Requirements

Automatically generate feature breakdown from epic business objectives, requirements, and success criteria for seamless transition from requirements gathering to feature specifications.

**Standalone Operation:** This command works independently and creates feature specification files with full requirements traceability. Generated features can be exported to PM tools or used with taskwright for task execution workflow.

## Usage
```bash
/epic-generate-features <epic-id> [options]
```

## Examples
```bash
# Generate all features for an epic
/epic-generate-features EPIC-001

# Generate features with specific focus areas
/epic-generate-features EPIC-001 --focus ui,api,infrastructure

# Generate features and export to PM tools
/epic-generate-features EPIC-001 --export jira,linear

# Interactive feature generation with review
/epic-generate-features EPIC-001 --interactive

# Regenerate features (replaces existing)
/epic-generate-features EPIC-001 --regenerate
```

## ⚠️ CRITICAL: Feature ID Generation (Duplication Prevention)

**IMPORTANT**: Feature IDs MUST be unique within an epic. Always check existing feature numbers before generating new features.

### Feature ID Generation Logic

```bash
# REQUIRED: Get highest feature number for SPECIFIC EPIC
get_max_feature_number_for_epic() {
    epic_id=$1      # e.g., EPIC-001

    # Extract epic number
    epic_num=$(echo $epic_id | sed 's/EPIC-//')  # 001

    # Search ALL feature directories for THIS EPIC ONLY
    existing_features=$(find docs/features -type f -name "FEAT-${epic_num}.*.md" 2>/dev/null)

    if [ -z "$existing_features" ]; then
        echo "0"
        return
    fi

    # Extract feature numbers and find maximum
    max_num=$(echo "$existing_features" | \
        sed -n "s/.*FEAT-${epic_num}\.\([0-9]\+\).*/\1/p" | \
        sort -n | tail -1)

    echo "${max_num:-0}"
}

# Generate next feature ID
generate_next_feature_id() {
    epic_id=$1

    epic_num=$(echo $epic_id | sed 's/EPIC-//')

    max_num=$(get_max_feature_number_for_epic $epic_id)
    next_num=$((max_num + 1))

    # Format: FEAT-001.4 (Epic 001, Feature 4)
    printf "FEAT-%s.%d" "$epic_num" "$next_num"
}

# Validate no duplicate exists
validate_feature_id() {
    feature_id=$1

    # Check all feature directories for conflicts
    conflicts=$(find docs/features -type f -name "${feature_id}-*.md" 2>/dev/null)

    if [ -n "$conflicts" ]; then
        echo "❌ ERROR: Duplicate feature ID detected: $feature_id"
        echo "   Existing: $conflicts"
        return 1
    fi

    return 0
}
```

### Feature Numbering Strategy

**Sequential per Epic** - Maintains Epic Association:
```
EPIC-001
├── FEAT-001.1 (First feature)
├── FEAT-001.2 (Second feature)
├── FEAT-001.3 (Third feature)
└── FEAT-001.4 (Fourth feature)

EPIC-002
├── FEAT-002.1
└── FEAT-002.2
```

**Benefits**:
- ✅ **Clear epic association** - FEAT-001.X clearly belongs to EPIC-001
- ✅ **Sequential numbering** - Easy to track feature count
- ✅ **No duplicates possible** - Epic-scoped sequences prevent conflicts
- ✅ **Natural grouping** - All features for same epic appear together

## Feature Generation Strategy

### Automatic Feature Analysis

Based on epic analysis, the system generates these feature categories:

1. **User-Facing Features** (from business objectives)
   - UI/UX capabilities
   - User workflows
   - Customer-facing functionality

2. **Backend/API Features** (from requirements)
   - API endpoints and services
   - Business logic components
   - Data processing features

3. **Infrastructure Features** (from technical needs)
   - Database and persistence
   - Authentication and security
   - Performance and scalability
   - Deployment and monitoring

4. **Testing & Quality Features** (from success criteria)
   - Quality assurance features
   - Testing infrastructure
   - Monitoring and observability

### EARS Requirements Analysis

```
Epic: User Management System
Requirements: REQ-001, REQ-002, REQ-003

Generated Features:
├── FEAT-001.1: User Authentication & Session Management
│   └── From: REQ-001 (user login), REQ-002 (session security)
├── FEAT-001.2: User Profile Management
│   └── From: REQ-003 (profile data), business objective
├── FEAT-001.3: Role-Based Access Control
│   └── From: Success criteria (permissions system)
└── FEAT-001.4: User Analytics Dashboard
    └── From: Out of scope → Deferred to EPIC-002
```

### Business Objective Analysis

```
Epic: "Build comprehensive payment processing system"

Generated Features:
├── FEAT-002.1: Payment Gateway Integration (Stripe, PayPal)
├── FEAT-002.2: Transaction Management & History
├── FEAT-002.3: Fraud Detection & Prevention
├── FEAT-002.4: Refund & Dispute Handling
├── FEAT-002.5: Payment Analytics & Reporting
└── FEAT-002.6: PCI Compliance Infrastructure
```

## Feature Generation Output

### Standard Generation
```bash
/epic-generate-features EPIC-001

# Output:
🔄 Generating Features for EPIC-001: User Management System

📋 Epic Analysis
Title: User Management System
Status: PLANNING
Requirements: 5 linked (REQ-001 through REQ-005)
Success Criteria: 4 defined
Stakeholders: Product Team, Engineering Team
Timeline: 8 weeks, Q1-2024

🎯 Feature Generation Strategy
Based on analysis, generating feature categories:
✅ User-Facing: 2 features (authentication, profile management)
✅ Backend/API: 2 features (user service, permissions API)
✅ Infrastructure: 2 features (user database, session storage)
✅ Testing: 1 feature (user testing suite)

📋 Generated Features (7)

👤 User-Facing Features
✅ FEAT-001.1: User Authentication & Session Management
   From: REQ-001 (user login), REQ-002 (session security)
   Complexity: High | Timeline: 2 weeks
   Sub-features: Login, logout, password reset, 2FA

✅ FEAT-001.2: User Profile Management
   From: REQ-003 (profile data), Business Objective
   Complexity: Medium | Timeline: 1.5 weeks
   Sub-features: Profile CRUD, avatar upload, preferences

🔌 Backend/API Features
✅ FEAT-001.3: User Service API
   From: Technical requirements
   Complexity: High | Timeline: 2 weeks
   Sub-features: User CRUD API, authentication endpoints

✅ FEAT-001.4: Role-Based Access Control
   From: REQ-004 (permissions), Success Criteria
   Complexity: High | Timeline: 1.5 weeks
   Sub-features: Role management, permission checks

🏗️ Infrastructure Features
✅ FEAT-001.5: User Database & Schema
   From: Data requirements
   Complexity: Medium | Timeline: 1 week
   Sub-features: User table, migrations, indexes

✅ FEAT-001.6: Session Storage (Redis)
   From: REQ-002 (session management)
   Complexity: Medium | Timeline: 1 week
   Sub-features: Session store, cache layer

🧪 Testing Features
✅ FEAT-001.7: User Management Testing Suite
   From: Quality requirements
   Complexity: Medium | Timeline: 1.5 weeks
   Sub-features: Unit tests, integration tests, E2E tests

📊 Generation Summary
Total Features: 7
Estimated Timeline: 10.5 weeks (exceeds epic 8-week target)
Complexity Distribution: 3 High, 4 Medium, 0 Low

⚠️ Timeline Warning:
Generated features total 10.5 weeks vs epic target of 8 weeks.
Recommendation: Consider prioritizing or deferring features.

🔗 Epic Integration
All features linked to EPIC-001
External tool inheritance: Jira (PROJ-123), Linear (PROJECT-456)

📁 File Updates
Updated: docs/epics/active/EPIC-001-user-management-system.md
Feature files created in: docs/features/active/
Updated: docs/epics/active/EPIC-001-FEATURES-SUMMARY.md

Next Steps:
1. Review generated features: /epic-status EPIC-001 --features
2. Generate tasks for first feature: /feature-generate-tasks FEAT-001.1
3. Export to PM tools: /epic-sync EPIC-001 --include-features
4. Track progress: /epic-status EPIC-001 --hierarchy
```

### Interactive Generation
```bash
/epic-generate-features EPIC-001 --interactive

# Interactive prompts:
🔄 Interactive Feature Generation: EPIC-001

📋 Proposed Feature Categories
1. User-Facing Features (2 proposed)
2. Backend/API Features (2 proposed)
3. Infrastructure Features (2 proposed)
4. Testing Features (1 proposed)

Select categories to generate [1,2,3,4] or 'all': all

👤 User-Facing Feature Review
Feature 1: User Authentication & Session Management
├── Complexity: High
├── Timeline: 2 weeks
├── Source: REQ-001, REQ-002
└── Sub-features: Login, logout, password reset, 2FA

Keep this feature? [y/n]: y

Feature 2: User Profile Management
├── Complexity: Medium
├── Timeline: 1.5 weeks
├── Source: REQ-003, Business Objective
└── Sub-features: Profile CRUD, avatar upload, preferences

Keep this feature? [y/n]: y

... [continues for all proposed features]

✅ Feature Generation Complete
Generated 6/7 proposed features
Skipped 1 feature based on your selections
Total timeline: 9 weeks (within 10% of epic target)
```

## Advanced Generation Options

### Feature Category Filtering
```bash
# Generate only specific feature types
/epic-generate-features EPIC-001 --categories user-facing,backend
/epic-generate-features EPIC-001 --categories infrastructure
/epic-generate-features EPIC-001 --categories testing

# Exclude specific categories
/epic-generate-features EPIC-001 --exclude infrastructure,testing
```

### Complexity and Timeline Control
```bash
# Set maximum complexity per feature
/epic-generate-features EPIC-001 --max-complexity medium

# Set target timeline constraint
/epic-generate-features EPIC-001 --timeline 8weeks

# Generate features for specific team capacity
/epic-generate-features EPIC-001 --team-size 5 --sprint-length 2weeks
```

### Integration with PM Tools
```bash
# Generate and export immediately
/epic-generate-features EPIC-001 --export jira,linear

# Generate with PM tool feature templates
/epic-generate-features EPIC-001 --template jira-story

# Generate and assign to teams
/epic-generate-features EPIC-001 --assign-mode auto
```

## Feature Generation Rules

### From EARS Requirements
1. **Functional Requirements** → User-facing and API features
2. **Performance Requirements** → Infrastructure and optimization features
3. **Security Requirements** → Security and authentication features
4. **Data Requirements** → Database and storage features
5. **Integration Requirements** → Integration and API features

### From Business Objectives
1. **User Goals** → User-facing feature set
2. **Business Metrics** → Analytics and reporting features
3. **Competitive Features** → Differentiation features
4. **Market Requirements** → Essential feature set

### From Success Criteria
1. **Measurable Outcomes** → Features that deliver metrics
2. **Quality Gates** → Testing and validation features
3. **Performance Targets** → Optimization features
4. **User Satisfaction** → UX and usability features

## Quality Integration

### Feature Decomposition Guidelines
Each generated feature should:
- **Be independently deliverable** - Can ship without other features
- **Have clear boundaries** - Distinct scope and responsibilities
- **Align with epic goals** - Contributes to business objectives
- **Be testable** - Has measurable acceptance criteria
- **Fit timeline** - Can be completed within 1-3 weeks

### Feature Validation
Before finalizing features:
- ✅ **Coverage Check**: All requirements mapped to features
- ✅ **Timeline Validation**: Total feature timeline vs epic timeline
- ✅ **Complexity Balance**: Mix of high/medium/low complexity
- ✅ **Dependency Analysis**: Feature dependencies identified
- ✅ **Team Capacity**: Features match available team size

## Workflow Integration

### Human Checkpoint Integration
```bash
# Generate features for review
/epic-generate-features EPIC-001 --for-review

# Approve and finalize features
/epic-generate-features EPIC-001 --approve --export

# Reject and regenerate
/epic-generate-features EPIC-001 --regenerate --adjust-scope
```

### MCP Integration
Features are generated with full MCP integration support:
- **Requirements MCP**: Pulls EARS requirements and validates coverage
- **PM Tools MCP**: Feature templates and hierarchy structures
- **Analysis MCP**: AI-powered feature decomposition
- **Documentation MCP**: Auto-generated feature documentation

## Feature Relationship Management

### Dependency Analysis
```
Generated feature dependencies:
FEAT-001.1: User Authentication → FEAT-001.5: User Database (depends on)
FEAT-001.2: User Profile → FEAT-001.1: Authentication (depends on)
FEAT-001.3: User Service API → FEAT-001.5: User Database (depends on)
FEAT-001.4: RBAC → FEAT-001.1: Authentication (depends on)
FEAT-001.7: Testing Suite → ALL features (tests)
```

### Sequential vs Parallel Features
- **Sequential**: Features with hard dependencies (auth before profile)
- **Parallel**: Independent features (can develop concurrently)
- **Critical Path**: Features blocking epic completion

## Best Practices

1. **Review Before Task Generation**: Always review generated features before creating tasks
2. **Align with Epic Timeline**: Ensure feature timeline fits epic constraints
3. **Balance Complexity**: Mix of quick wins and complex features
4. **Consider Team Size**: Feature count should match team capacity
5. **PM Tool Integration**: Export early to maintain external tool synchronization
6. **Iterative Refinement**: Regenerate features as epic scope evolves

## Integration with Other Commands

### Complete Epic → Feature → Task Workflow
```bash
# 1. Create epic
/epic-create "User Management System" priority:high export:jira

# 2. Generate features automatically
/epic-generate-features EPIC-001 --interactive

# 3. Review feature breakdown
/epic-status EPIC-001 --features

# 4. Generate tasks for first feature
/feature-generate-tasks FEAT-001.1 --interactive

# 5. Monitor epic progress
/epic-status EPIC-001 --hierarchy
```

### Cross-Command References
- Generated features automatically link to epic
- Epic progress updates based on feature completion
- Feature completion rolls up to epic metrics
- External tool IDs inherited from epic configuration

## Output Files Created

### Feature Files (docs/features/active/)
```markdown
---
id: FEAT-001.1
title: User Authentication & Session Management
epic: EPIC-001
status: planned
created: 2024-01-15T10:00:00Z
complexity: high
estimated_weeks: 2
requirements: [REQ-001, REQ-002]
external_ids:
  epic_jira: PROJ-123
  epic_linear: PROJECT-456
  jira: null  # Populated on feature export
---

# Feature: User Authentication & Session Management

## Description
Comprehensive authentication system with session management...

## Sub-Features
1. Login flow with email/password
2. Logout functionality
3. Password reset via email
4. Two-factor authentication (2FA)

## Acceptance Criteria
- [ ] Users can login with valid credentials
- [ ] Sessions expire after 24 hours
- [ ] Password reset emails sent within 1 minute
- [ ] 2FA optional but encouraged

## Dependencies
- FEAT-001.5: User Database (data layer required)

## Tasks
[Will be populated by /feature-generate-tasks]
```

### Epic Update (docs/epics/active/EPIC-XXX.md)
```markdown
## Feature Breakdown

✅ **Total Features**: 7 generated
📊 **Timeline**: 10.5 weeks estimated
🎯 **Complexity**: 3 High, 4 Medium

### Features
1. **FEAT-001.1**: User Authentication & Session Management (2 weeks, High)
2. **FEAT-001.2**: User Profile Management (1.5 weeks, Medium)
3. **FEAT-001.3**: User Service API (2 weeks, High)
4. **FEAT-001.4**: Role-Based Access Control (1.5 weeks, High)
5. **FEAT-001.5**: User Database & Schema (1 week, Medium)
6. **FEAT-001.6**: Session Storage (Redis) (1 week, Medium)
7. **FEAT-001.7**: User Management Testing Suite (1.5 weeks, Medium)
```

### Feature Summary (docs/epics/active/EPIC-XXX-FEATURES-SUMMARY.md)
```markdown
# EPIC-001 Features Summary

**Epic**: User Management System
**Total Features**: 7
**Status**: Feature breakdown complete

## Feature List

| ID | Title | Category | Complexity | Weeks | Status |
|----|-------|----------|------------|-------|--------|
| FEAT-001.1 | User Authentication | User-Facing | High | 2.0 | Planned |
| FEAT-001.2 | User Profile Mgmt | User-Facing | Medium | 1.5 | Planned |
| FEAT-001.3 | User Service API | Backend | High | 2.0 | Planned |
| FEAT-001.4 | RBAC | Backend | High | 1.5 | Planned |
| FEAT-001.5 | User Database | Infrastructure | Medium | 1.0 | Planned |
| FEAT-001.6 | Session Storage | Infrastructure | Medium | 1.0 | Planned |
| FEAT-001.7 | Testing Suite | Testing | Medium | 1.5 | Planned |

## Next Steps
1. Review feature breakdown with stakeholders
2. Prioritize features for sprints
3. Generate tasks: /feature-generate-tasks FEAT-001.1
4. Begin implementation
```

## Validation

Features are validated before creation:
- ✅ Epic must exist and be valid
- ✅ Feature titles must be unique within epic
- ✅ Timeline must be reasonable (1-4 weeks per feature)
- ✅ All requirements must be mapped to at least one feature
- ✅ Feature complexity must be assessable
- ✅ No duplicate feature IDs

## Error Handling

### Invalid Epic
```
❌ Feature generation failed

Epic not found: EPIC-999

Available epics:
- EPIC-001: User Management System (active)
- EPIC-002: Payment Processing (planned)
```

### Timeline Exceeded
```
⚠️ Warning: Timeline constraint exceeded

Generated features: 12 weeks
Epic timeline: 8 weeks
Overage: 4 weeks (50%)

Recommendations:
1. Review and prioritize features
2. Consider splitting into multiple epics
3. Defer low-priority features to future epic
4. Increase team size or extend timeline
```

This command bridges the critical gap between requirements gathering (epic creation) and task definition (feature → task breakdown), ensuring comprehensive feature coverage while maintaining full integration with external PM tools. For task execution, see taskwright.
