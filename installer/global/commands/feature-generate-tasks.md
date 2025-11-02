# Feature Generate Tasks - Auto-Generate Implementation Tasks from Features

Automatically generate implementation tasks from feature requirements, acceptance criteria, and BDD scenarios for seamless transition from requirements to task management. For task execution, see taskwright.

## Usage
```bash
/feature-generate-tasks <feature-id> [options]
```

## Examples
```bash
# Generate all tasks for a feature
/feature-generate-tasks FEAT-001

# Generate tasks with specific types
/feature-generate-tasks FEAT-001 --types ui,api,tests

# Generate tasks and export to PM tools
/feature-generate-tasks FEAT-001 --export jira

# Interactive task generation with review
/feature-generate-tasks FEAT-001 --interactive

# Regenerate tasks (replaces existing)
/feature-generate-tasks FEAT-001 --regenerate
```

## ⚠️ CRITICAL: Task ID Generation (Duplication Prevention)

**IMPORTANT**: Task IDs MUST be unique within an epic. Always check existing task numbers before generating new tasks.

### Task ID Generation Logic

```bash
# REQUIRED: Get highest task number for SPECIFIC FEATURE
get_max_task_number_for_feature() {
    epic_id=$1      # e.g., EPIC-001
    feature_id=$2   # e.g., FEAT-001.2

    # Extract numbers
    epic_num=$(echo $epic_id | sed 's/EPIC-//')                     # 001
    feature_num=$(echo $feature_id | sed 's/FEAT-[0-9]*\.\([0-9]*\)/\1/')  # 2

    # Search ALL task directories for THIS FEATURE ONLY
    existing_tasks=$(find docs/tasks -type f -name "TASK-${epic_num}.${feature_num}.*.md" 2>/dev/null)

    if [ -z "$existing_tasks" ]; then
        echo "0"
        return
    fi

    # Extract task numbers and find maximum
    max_num=$(echo "$existing_tasks" | \
        sed -n "s/.*TASK-${epic_num}\.${feature_num}\.\([0-9]\+\).*/\1/p" | \
        sort -n | tail -1)

    echo "${max_num:-0}"
}

# Generate next feature-hierarchical task ID
generate_next_task_id() {
    epic_id=$1
    feature_id=$2

    epic_num=$(echo $epic_id | sed 's/EPIC-//')
    feature_num=$(echo $feature_id | sed 's/FEAT-[0-9]*\.\([0-9]*\)/\1/')

    max_num=$(get_max_task_number_for_feature $epic_id $feature_id)
    next_num=$((max_num + 1))

    # Zero-padded for proper sorting (01, 02, ..., 99)
    # Format: TASK-001.2.05 (Epic 001, Feature 2, Task 05)
    printf "TASK-%s.%s.%02d" "$epic_num" "$feature_num" "$next_num"
}

# Validate no duplicate exists
validate_task_id() {
    task_id=$1

    # Check all task directories
    conflicts=$(find docs/tasks -type f -name "${task_id}-*.md" 2>/dev/null)

    if [ -n "$conflicts" ]; then
        echo "❌ ERROR: Duplicate task ID detected: $task_id"
        echo "   Existing: $conflicts"
        return 1
    fi

    return 0
}
```

### Task Numbering Strategy

**Feature-Hierarchical** (Recommended) - Maintains Visual Feature Identity:
```
EPIC-001
├── FEAT-001.1 → TASK-001.1.01, TASK-001.1.02, TASK-001.1.03
├── FEAT-001.2 → TASK-001.2.01, TASK-001.2.02, TASK-001.2.03
└── FEAT-001.3 → TASK-001.3.01, TASK-001.3.02, TASK-001.3.03

EPIC-002
├── FEAT-002.1 → TASK-002.1.01, TASK-002.1.02
└── FEAT-002.2 → TASK-002.2.01, TASK-002.2.02
```

**Benefits**:
- ✅ **Visual feature identification** - TASK-001.2.xx clearly belongs to FEAT-001.2
- ✅ **Clear hierarchy** - Epic → Feature → Task structure visible in ID
- ✅ **Natural file grouping** - All tasks for same feature appear together
- ✅ **No duplicates possible** - Feature-scoped sequences prevent conflicts
- ✅ **Easy progress tracking** - See task count per feature at a glance
- ✅ **Better sprint planning** - Identify feature boundaries immediately

**Example in File Listing**:
```
TASK-001.1.01-mcp-server-skeleton.md
TASK-001.1.02-gather-requirements.md     ← All FEAT-001.1
TASK-001.1.03-validate-requirements.md
─────────────────────────────────────
TASK-001.2.01-ears-parser-tests.md
TASK-001.2.02-requirement-generator.md   ← All FEAT-001.2
TASK-001.2.03-bdd-scenarios.md
```

## Task Generation Strategy

### Automatic Task Types
Based on feature analysis, the system generates these task categories:

1. **UI/UX Tasks** (if design assets linked)
   - Component design and implementation
   - Responsive layout tasks
   - User interaction tasks

2. **API/Backend Tasks** (from requirements)
   - Endpoint implementation
   - Business logic tasks
   - Data model tasks

3. **Testing Tasks** (from BDD scenarios and acceptance criteria)
   - Unit test tasks
   - Integration test tasks
   - E2E test tasks

4. **Documentation Tasks**
   - API documentation
   - User documentation
   - Technical documentation

### EARS Requirements Analysis
```
REQ-001: "When user submits valid credentials, system shall authenticate within 1 second"

Generated Tasks:
├── TASK-XXX: Design login form UI
├── TASK-XXX: Implement authentication API endpoint
├── TASK-XXX: Add performance optimization for 1-second target
└── TASK-XXX: Create authentication performance tests
```

### BDD Scenario Analysis
```
BDD-001: "Successful user login flow"
Given user has valid credentials
When user submits login form
Then user is authenticated and redirected

Generated Tasks:
├── TASK-XXX: Implement login form validation
├── TASK-XXX: Create authentication success flow
├── TASK-XXX: Add post-login redirect logic
└── TASK-XXX: Create BDD test for login flow
```

## Task Generation Output

### Standard Generation
```bash
/feature-generate-tasks FEAT-001

# Output:
🔄 Generating Tasks for FEAT-001: User Authentication

📋 Feature Analysis
Title: User Authentication
Epic: EPIC-001 (User Management System)
Requirements: 3 linked (REQ-001, REQ-002, REQ-003)
BDD Scenarios: 2 linked (BDD-001, BDD-002)
Acceptance Criteria: 4 defined

🎯 Task Generation Strategy
Based on analysis, generating these task types:
✅ UI Tasks: 2 tasks (login form, error handling)
✅ API Tasks: 3 tasks (auth endpoint, session, validation)
✅ Testing Tasks: 4 tasks (unit, integration, e2e, performance)
✅ Documentation: 1 task (API docs)

📋 Generated Tasks (10)

🎨 UI/UX Tasks
✅ TASK-043: Design authentication UI components
   From: Feature design requirements
   Complexity: Medium | Timeline: 2 days

✅ TASK-044: Implement responsive login form
   From: REQ-001 (user login interface)
   Complexity: Medium | Timeline: 1 day

🔌 API/Backend Tasks
✅ TASK-045: Implement authentication API endpoint
   From: REQ-001 (authentication service)
   Complexity: High | Timeline: 2 days

✅ TASK-046: Add session management system
   From: REQ-002 (session security)
   Complexity: High | Timeline: 2 days

✅ TASK-047: Implement password validation logic
   From: REQ-003 (password complexity)
   Complexity: Medium | Timeline: 1 day

🧪 Testing Tasks
✅ TASK-048: Create authentication unit tests
   From: All requirements
   Complexity: Medium | Timeline: 1 day

✅ TASK-049: Implement integration tests for auth flow
   From: BDD-001 (successful login)
   Complexity: Medium | Timeline: 1 day

✅ TASK-050: Create E2E tests for complete login flow
   From: BDD-001, BDD-002 (full scenarios)
   Complexity: High | Timeline: 2 days

✅ TASK-051: Add performance tests for 1-second target
   From: REQ-001 (performance requirement)
   Complexity: Medium | Timeline: 1 day

📝 Documentation Tasks
✅ TASK-052: Create authentication API documentation
   From: API tasks and requirements
   Complexity: Low | Timeline: 0.5 days

📊 Generation Summary
Total Tasks: 10
Estimated Timeline: 12.5 days
Complexity Distribution: 3 High, 6 Medium, 1 Low

🔗 Feature Integration
All tasks linked to FEAT-001
Epic context: EPIC-001
External tool inheritance: Jira, Linear

📁 File Updates
Updated: docs/features/FEAT-001-user-authentication.md
Task files created in: tasks/backlog/

Next Steps:
1. Review generated tasks: /feature-status FEAT-001 --tasks
2. Begin implementation: /task-work TASK-043
3. Export to PM tools: /feature-sync FEAT-001 --include-tasks
4. Track progress: /feature-status FEAT-001
```

### Interactive Generation
```bash
/feature-generate-tasks FEAT-001 --interactive

# Interactive prompts:
🔄 Interactive Task Generation: FEAT-001

📋 Proposed Task Categories
1. UI/UX Tasks (2 proposed)
2. API/Backend Tasks (3 proposed)
3. Testing Tasks (4 proposed)
4. Documentation Tasks (1 proposed)

Select categories to generate [1,2,3,4] or 'all': all

🎨 UI/UX Task Review
Task 1: Design authentication UI components
├── Complexity: Medium
├── Timeline: 2 days
└── Source: Feature design requirements

Keep this task? [y/n]: y

Task 2: Implement responsive login form
├── Complexity: Medium
├── Timeline: 1 day
└── Source: REQ-001

Keep this task? [y/n]: y

... [continues for all proposed tasks]

✅ Task Generation Complete
Generated 8/10 proposed tasks
Skipped 2 tasks based on your selections
```

## Advanced Generation Options

### Task Type Filtering
```bash
# Generate only specific task types
/feature-generate-tasks FEAT-001 --types ui,api
/feature-generate-tasks FEAT-001 --types tests
/feature-generate-tasks FEAT-001 --types docs

# Exclude specific types
/feature-generate-tasks FEAT-001 --exclude tests,docs
```

### Complexity and Timeline Control
```bash
# Set maximum complexity
/feature-generate-tasks FEAT-001 --max-complexity medium

# Set target sprint timeline
/feature-generate-tasks FEAT-001 --sprint 2weeks

# Generate tasks for specific team capacity
/feature-generate-tasks FEAT-001 --team-capacity 5days
```

### Integration with PM Tools
```bash
# Generate and export immediately
/feature-generate-tasks FEAT-001 --export jira,linear

# Generate with PM tool task templates
/feature-generate-tasks FEAT-001 --template jira-story

# Generate and assign to team members
/feature-generate-tasks FEAT-001 --assign-mode auto
```

## Task Generation Rules

### From EARS Requirements
1. **Ubiquitous Requirements** → Implementation tasks
2. **Event-Driven Requirements** → Event handling and API tasks
3. **State-Driven Requirements** → State management tasks
4. **Unwanted Behavior** → Error handling and validation tasks
5. **Optional Features** → Feature flag and configuration tasks

### From BDD Scenarios
1. **Given clauses** → Setup and data preparation tasks
2. **When clauses** → Action and interaction tasks
3. **Then clauses** → Validation and result verification tasks

### From Acceptance Criteria
1. **Functional criteria** → Implementation tasks
2. **Performance criteria** → Performance optimization tasks
3. **Security criteria** → Security implementation tasks
4. **Usability criteria** → UI/UX tasks

## Quality Integration

### Test Coverage Requirements
Generated testing tasks ensure comprehensive coverage:
- **Unit Tests**: For each implementation task
- **Integration Tests**: For API and service interaction tasks
- **E2E Tests**: For complete user flows
- **Performance Tests**: For performance-critical requirements

### Documentation Requirements
Automatic documentation tasks for:
- **API Documentation**: For all API tasks
- **User Documentation**: For UI/UX tasks
- **Technical Documentation**: For complex implementation tasks

## Workflow Integration

### Human Checkpoint Integration
```bash
# Generate tasks for review
/feature-generate-tasks FEAT-001 --for-review

# Approve and finalize tasks
/feature-generate-tasks FEAT-001 --approve --export

# Reject and regenerate
/feature-generate-tasks FEAT-001 --regenerate
```

### MCP Integration
Tasks are generated with full MCP integration support:
- **Requirements MCP**: Pulls requirement details
- **PM Tools MCP**: Templates and task structures
- **Testing MCP**: Test framework specific tasks
- **Documentation MCP**: Documentation platform tasks

## Task Relationship Management

### Dependency Analysis
```
Generated task dependencies:
TASK-043: Design UI → TASK-044: Implement UI
TASK-045: API endpoint → TASK-046: Session management
TASK-048: Unit tests ← ALL implementation tasks
TASK-050: E2E tests ← TASK-044, TASK-045, TASK-046
```

### Sequential vs Parallel Tasks
- **Sequential**: Dependencies clearly defined
- **Parallel**: Independent tasks marked for concurrent work
- **Blocking**: Critical path tasks identified

## Best Practices

1. **Review Before Implementation**: Always review generated tasks before starting work
2. **Customize as Needed**: Generated tasks are starting points, customize for your context
3. **Epic Alignment**: Ensure all generated tasks contribute to epic objectives
4. **Team Capacity**: Consider team size and skills when generating tasks
5. **PM Tool Integration**: Export early to maintain external tool synchronization
6. **Iterative Refinement**: Regenerate tasks as requirements evolve

## Complexity Control and Automatic Task Breakdown

### Complexity-Based Breakdown (TASK-008)

The system automatically evaluates task complexity and breaks down complex tasks into manageable subtasks.

#### Complexity Thresholds
- **1-3 (Low)**: 🟢 No breakdown needed - implement as-is
- **4-6 (Medium)**: 🟡 Logical breakdown - split by components
- **7-8 (High)**: 🟡 File-based breakdown - group by modules
- **9-10 (Critical)**: 🔴 Phase-based breakdown - sequential implementation phases

#### Automatic Breakdown Example
```bash
# Generate tasks with automatic complexity evaluation
/feature-generate-tasks FEAT-001

# Output:
📋 Analyzing Task Complexity...

Task: TASK-001 - Implement authentication system
├── Files: 12 files
├── Patterns: Strategy, Repository, Factory
├── Complexity Score: 8/10 🟡
└── Breakdown Strategy: File-based

🔄 Applying automatic breakdown...

Generated Subtasks:
├── TASK-001.1: User models and DTOs (3 files) - 6h
├── TASK-001.2: User repository and database (2 files) - 4h
├── TASK-001.3: Authentication service (3 files) - 8h
├── TASK-001.4: API endpoints (2 files) - 4h
└── TASK-001.5: Tests and validation (2 files) - 4h

Total: 5 subtasks, 26 estimated hours
```

#### Breakdown Strategies

**1. No Breakdown Strategy** (Complexity 1-3)
```bash
Task: TASK-010 - Update user profile field
├── Complexity: 2/10 🟢
├── Files: 1 file
└── Decision: Simple task - no breakdown needed

✅ Task ready for implementation
```

**2. Logical Breakdown Strategy** (Complexity 4-6)
```bash
Task: TASK-020 - Build user dashboard
├── Complexity: 5/10 🟡
├── Components detected: UI, API, Data
└── Breakdown: By logical components

Generated Subtasks:
├── TASK-020.1: Dashboard UI components
├── TASK-020.2: Dashboard API endpoints
├── TASK-020.3: Dashboard data models
└── TASK-020.4: Dashboard tests
```

**3. File-Based Breakdown Strategy** (Complexity 7-8)
```bash
Task: TASK-030 - Payment processing system
├── Complexity: 8/10 🟡
├── Files: 15 files
└── Breakdown: By file groupings (2-3 files per subtask)

Generated Subtasks:
├── TASK-030.1: Payment models (payment.py, transaction.py, invoice.py)
├── TASK-030.2: Payment gateway (gateway.py, adapter.py)
├── TASK-030.3: Payment service (service.py, validator.py)
├── TASK-030.4: Payment API (routes.py, handlers.py)
└── TASK-030.5: Payment tests (test_payment.py, test_gateway.py)
```

**4. Phase-Based Breakdown Strategy** (Complexity 9-10)
```bash
Task: TASK-040 - Multi-tenant architecture
├── Complexity: 10/10 🔴
├── Files: 25+ files
└── Breakdown: By implementation phases

Generated Subtasks:
├── TASK-040.1: Phase 1 - Foundation (models, interfaces)
├── TASK-040.2: Phase 2 - Core Implementation (business logic)
├── TASK-040.3: Phase 3 - Integration (database, APIs)
├── TASK-040.4: Phase 4 - Advanced Features (optimization, edge cases)
└── TASK-040.5: Phase 5 - Testing & Documentation
```

### Complexity Visualization

#### Terminal Output
```
🔄 Evaluating Task Complexity...

Complexity Score: 7/10 🟡 High

Factor Breakdown:
├── 🟡 File Complexity: 2/3
│   └── Complex change (8 files) - multiple components
├── 🟢 Pattern Familiarity: 1/2
│   └── Moderate patterns: Strategy, Repository
└── 🟡 Risk Level: 2/3
    └── High risk (security, external_integration)

Breakdown Decision: File-based breakdown recommended
Estimated Subtasks: 4-6
Estimated Time: 20-30 hours
```

#### Duplicate Detection
```bash
# Automatic duplicate detection across all task directories
/feature-generate-tasks FEAT-001

# Output:
⚠️ Potential Duplicate Detected

Proposed Task: "Implement user authentication API"
Similar to:
├── TASK-012 in tasks/in_progress/
│   Title: "Build authentication API endpoint"
│   Similarity: 85%
└── TASK-089 in tasks/completed/
    Title: "Create user auth API"
    Similarity: 78%

Options:
1. Skip this task (recommended)
2. Generate anyway
3. Merge with TASK-012
```

### Customizing Breakdown Thresholds

```bash
# Use custom complexity threshold
/feature-generate-tasks FEAT-001 --threshold 8
# Only breaks down tasks with complexity >= 8

# Interactive threshold customization
/feature-generate-tasks FEAT-001 --interactive --customize-thresholds

# Prompts:
Enter breakdown threshold (1-10) [default: 7]: 6
Enter max subtasks per task [default: 5]: 4
```

### Quality Gate Integration

```bash
# Generate tasks with automatic test task creation
/feature-generate-tasks FEAT-001 --quality-gates

# Automatically adds:
├── Unit test tasks (one per implementation task)
├── Integration test tasks (for API/service tasks)
├── E2E test tasks (for user-facing features)
└── Performance test tasks (for performance requirements)
```

### Statistics and Reporting

```bash
# Generate tasks with detailed breakdown report
/feature-generate-tasks FEAT-001 --with-report

# Output includes:
📊 Breakdown Statistics

Total Original Tasks: 8
Total Subtasks Generated: 24
Breakdown Ratio: 3:1

Complexity Distribution:
├── 🟢 Low (1-3): 2 tasks (8%)
├── 🟡 Medium (4-6): 3 tasks (13%)
├── 🟡 High (7-8): 2 tasks (8%)
└── 🔴 Critical (9-10): 1 task (4%)

Total Estimated Time:
├── Original estimate: 120 hours
├── After breakdown: 115 hours (refined)
└── Time saved by breakdown: ~15% (early risk detection)

Average Subtasks per Breakdown: 3.2
Duplicate Tasks Prevented: 3
```

## Integration with Other Commands

### Workflow Integration
```bash
# Complete feature workflow with complexity control
/feature-create "User Auth" epic:EPIC-001 requirements:[REQ-001,REQ-002]
/feature-generate-tasks FEAT-001 --interactive --threshold 6
/feature-status FEAT-001 --tasks
/task-work TASK-043
```

### Cross-Command References
- Generated tasks automatically link to feature
- Feature progress updates based on task completion
- Epic progress rolls up from generated task completion
- Complexity scores tracked for velocity analysis

This command bridges the critical gap between requirements management and task execution, ensuring comprehensive task coverage with automatic complexity management and intelligent breakdown strategies while maintaining full integration with external PM tools. For task execution and workflow management, use taskwright.