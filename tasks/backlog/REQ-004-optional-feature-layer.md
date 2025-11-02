---
id: REQ-004
title: "Support Optional Feature Layer (Epic → Task Direct)"
created: 2025-11-02
status: backlog
priority: high
complexity: 6
parent_task: none
subtasks: []
estimated_hours: 8
---

# REQ-004: Support Optional Feature Layer in Epic Hierarchy

## Business Context

**Product Owner Request**: Allow epics to contain tasks directly without requiring an intermediate feature layer.

**Rationale**: Many epics are small (3-5 tasks) and adding a feature layer is unnecessary overhead. The feature layer should be optional based on epic complexity and team preference.

## Current State

**Rigid hierarchy** (always required):
```
EPIC → FEATURE → TASK
```

**Example**:
```
EPIC-001: User Management
  └── FEAT-001: User Authentication (feels artificial if only 3 tasks)
        └── TASK-001: Implement login
        └── TASK-002: Add session handling
        └── TASK-003: Create tests
```

## Target State

**Flexible hierarchy** (feature layer optional):
```
EPIC → TASK               (for simple epics)
EPIC → FEATURE → TASK     (for complex epics)
```

**Example 1 - Simple epic (no features)**:
```
EPIC-002: Fix Auth Bugs
  └── TASK-004: Debug session timeout
  └── TASK-005: Fix password reset
  └── TASK-006: Update tests
```

**Example 2 - Complex epic (with features)**:
```
EPIC-001: User Management
  └── FEAT-001: Authentication
        └── TASK-001: Implement login
        └── TASK-002: Add session handling
  └── FEAT-002: Profile Management
        └── TASK-003: Create profile form
        └── TASK-004: Add avatar upload
```

## Use Cases

### When to Skip Features (Epic → Task)
1. **Small epics**: 3-5 tasks total
2. **Bug fix epics**: Group of related bug fixes
3. **Technical debt**: Cleanup/refactoring tasks
4. **Research/spikes**: Investigative work
5. **Infrastructure**: Deployment/configuration tasks
6. **Solo developers**: Less coordination needed
7. **Quick wins**: Fast iteration on simple work

### When to Use Features (Epic → Feature → Task)
1. **Large epics**: 10+ tasks
2. **Customer-facing**: User-visible capabilities
3. **Natural groupings**: Clear feature boundaries
4. **Team coordination**: 3+ developers
5. **Requirements traceability**: Link to EARS requirements
6. **Long-running**: Multi-sprint initiatives
7. **PM tool reporting**: Feature-level metrics needed

## Implementation Changes

### 1. Task Creation Command Updates

**NOTE**: The `/task-create` command implementation is in the **taskwright repo**, not require-kit.

**Implementation Task**: See `taskwright/tasks/backlog/TASK-007-task-create-epic-link.md`

**Summary of changes needed** (implemented in taskwright):
- Accept `epic:EPIC-XXX` parameter
- Validate epic XOR feature (not both)
- Update task metadata schema
- Update epic metadata to track direct tasks

**Not in scope for require-kit**: This repo focuses on requirements management only.

### 2. Epic Status Command Updates

**Current**: Shows only features
```bash
/epic-status EPIC-001
# Output: FEAT-001, FEAT-002, etc.
```

**Enhanced**: Shows features AND direct tasks
```bash
/epic-status EPIC-001

# Output:
# Features (2):
#   FEAT-001: Authentication (3 tasks)
#   FEAT-002: Profile (2 tasks)
# Direct Tasks (0):
#   (none)

# For epic without features:
/epic-status EPIC-002

# Output:
# Features (0):
#   (none)
# Direct Tasks (3):
#   TASK-004: Debug session timeout [in_progress]
#   TASK-005: Fix password reset [backlog]
#   TASK-006: Update tests [backlog]
```

### 3. Hierarchy View Updates

**Enhanced hierarchy display**:
```bash
/hierarchy-view EPIC-001

# Output:
EPIC-001: User Management System
├── FEAT-001: User Authentication
│   ├── TASK-001: Implement login [completed]
│   └── TASK-002: Add session handling [in_progress]
├── FEAT-002: Profile Management
│   └── TASK-003: Create profile form [backlog]
└── [Direct Tasks]
    ├── TASK-007: Update epic documentation [backlog]
    └── TASK-008: Create integration tests [backlog]
```

### 4. PM Tool Mapping

**Jira**:
```yaml
# With features
Epic → Story (feature) → Sub-task (task)

# Without features (NEW)
Epic → Story (task)
```

**Linear**:
```yaml
# With features
Initiative → Feature → Issue

# Without features (NEW)
Initiative → Issue
```

**GitHub Projects**:
```yaml
# With features
Milestone → Issue (feature) → Linked Issue (task)

# Without features (NEW)
Milestone → Issue (task)
```

### 5. Validation Rules

**Task Creation**:
- ✅ Must specify EITHER `epic:EPIC-XXX` OR `feature:FEAT-XXX`
- ❌ Cannot specify both epic and feature
- ✅ If epic specified, epic must exist and be active
- ✅ If feature specified, feature must exist and belong to an epic

**Epic Organization**:
- ✅ Epic can have ONLY features
- ✅ Epic can have ONLY tasks
- ✅ Epic can have BOTH features and tasks (mixed mode)
- ⚠️ Warn if mixing features and direct tasks (suggest consistency)

## File Changes Required

**IMPORTANT**: This task is a **specification and research task** for require-kit. The actual implementation of task-related commands happens in the **taskwright repo**.

### require-kit Changes (This Repo)
**Scope**: Requirements management, epic/feature specifications only

1. **Documentation Files**:
   - `README.md` - Add epic → task pattern examples
   - `CLAUDE.md` - Document when to use each pattern
   - `docs/research/optional-feature-layer-analysis.md` - ✅ Already created

2. **Template Files** (if they exist):
   - Epic template - Add `direct_tasks` field documentation
   - Feature template - Clarify optional nature

3. **No Command Changes**: require-kit has no task execution commands

### taskwright Changes (Separate Repo)
**Scope**: Task execution and workflow

**Implementation Task**: `taskwright/tasks/backlog/TASK-007-task-create-epic-link.md`

1. **Command Files**:
   - `task-create.md` - Add epic:EPIC-XXX option
   - `epic-status.md` - Show direct tasks
   - `hierarchy-view.md` - Display mixed hierarchy
   - `epic-sync.md` - Handle task-only epics in PM tool sync

2. **Metadata Schemas**:
   - Task metadata - Add `parent_type`, `parent_id` fields
   - Epic metadata - Add `direct_tasks`, `has_features` fields

3. **Agent Files**:
   - No changes required (agents work with metadata)

## Documentation Updates

### 1. README.md
```markdown
## Epic Organization Patterns

### Pattern 1: Epic → Task (Simple)
Use for small epics (3-5 tasks):
```bash
/epic-create "Fix Auth Bugs"
/task-create "Debug session timeout" epic:EPIC-002
```

### Pattern 2: Epic → Feature → Task (Complex)
Use for large epics (10+ tasks):
```bash
/epic-create "User Management"
/feature-create "Authentication" epic:EPIC-001
/task-create "Implement login" feature:FEAT-001
```
```

### 2. CLAUDE.md
```markdown
## When to Use Each Pattern

**Epic → Task** (simple):
- Small epics (<5 tasks)
- Bug fixes, tech debt, spikes
- Solo developers, quick iterations

**Epic → Feature → Task** (complex):
- Large epics (>10 tasks)
- Customer-facing features
- Team coordination, requirements traceability
```

## Benefits

### 1. User Experience
- ✅ Reduces ceremony for small epics
- ✅ Matches real-world PM tool usage
- ✅ Flexibility for different team sizes
- ✅ Faster iteration on simple work

### 2. Real-World Usage
- ✅ Jira/Linear commonly use epic → task for small work
- ✅ GitHub Projects naturally uses milestone → issue
- ✅ Prevents artificial feature creation
- ✅ Better fits agile teams

### 3. Scalability
- ✅ Start simple (epic → task)
- ✅ Add features later if epic grows
- ✅ Teams choose appropriate granularity
- ✅ No forced complexity

## Migration Strategy

### For Existing Epics with Artificial Features
```bash
# Identify single-feature epics
/epic-status --audit

# Suggest: "EPIC-002 has only FEAT-001. Consider flattening to epic → task"

# Provide migration command
/epic-flatten EPIC-002
# Converts: EPIC → FEAT-001 → [tasks]
# To:       EPIC → [tasks] (feature removed)
```

## Acceptance Criteria

### require-kit (This Repo)
- [ ] Research document completed - ✅ `docs/research/optional-feature-layer-analysis.md`
- [ ] Documentation explains when to use each pattern
- [ ] README includes both patterns with examples (if applicable)
- [ ] CLAUDE.md includes pattern guidance (if applicable)
- [ ] Epic/feature templates updated with optional feature documentation

### taskwright (Separate Repo)
**See**: `taskwright/tasks/backlog/TASK-007-task-create-epic-link.md`

- [ ] `/task-create` accepts `epic:EPIC-XXX` parameter
- [ ] Validation prevents both epic and feature in same task
- [ ] `/epic-status` shows direct tasks when features absent
- [ ] `/hierarchy-view` displays mixed epic/feature/task structure
- [ ] PM tool sync handles epic → task mapping correctly
- [ ] Validation warns if mixing features and direct tasks in same epic
- [ ] Epic metadata tracks `has_features` flag
- [ ] Task metadata includes `parent_type` field

## Testing Scenarios

### Scenario 1: Epic with Direct Tasks Only
```bash
/epic-create "Fix Auth Bugs"
/task-create "Debug timeout" epic:EPIC-002
/task-create "Fix reset" epic:EPIC-002
/epic-status EPIC-002
# Should show: 2 direct tasks, 0 features
```

### Scenario 2: Epic with Features Only
```bash
/epic-create "User Management"
/feature-create "Authentication" epic:EPIC-001
/task-create "Implement login" feature:FEAT-001
/epic-status EPIC-001
# Should show: 1 feature with 1 task, 0 direct tasks
```

### Scenario 3: Mixed Epic (Both)
```bash
/epic-create "Platform Upgrade"
/feature-create "UI Redesign" epic:EPIC-003
/task-create "Update logo" feature:FEAT-002
/task-create "Upgrade dependencies" epic:EPIC-003
/epic-status EPIC-003
# Should show: 1 feature (1 task), 1 direct task
# Should warn: "Epic has mixed organization. Consider consistency."
```

### Scenario 4: Invalid Usage
```bash
/task-create "Bad task" epic:EPIC-001 feature:FEAT-001
# Should error: "Cannot specify both epic and feature"
```

## Timeline Estimate

### require-kit (This Repo)
- Research document: 2 hours - ✅ COMPLETED
- Documentation updates: 1 hour
- Template updates: 0.5 hours

**Total (require-kit)**: ~1.5 hours

### taskwright (Separate Repo)
See `taskwright/tasks/backlog/TASK-007-task-create-epic-link.md`
- Command implementation: ~3 hours
- Additional commands (epic-status, hierarchy-view): ~5 hours
- PM tool sync: ~2 hours

**Total (taskwright)**: ~10 hours

## Notes

- This is a **high-value, low-risk enhancement**
- Matches real-world PM tool usage patterns
- Improves UX for small teams and simple epics
- Maintains backward compatibility (features still supported)
- Provides natural migration path as epics grow

**Repository Split**:
- **require-kit** (this repo): Requirements management, specifications, research
- **taskwright** (separate repo): Task execution, command implementations

## Related Tasks

### require-kit (This Repo)
- REQ-004 (this task): Research and specification
- Research document: `docs/research/optional-feature-layer-analysis.md`

### taskwright (Separate Repo)
- TASK-007: `/task-create` command enhancement
- Future tasks: `/epic-status`, `/hierarchy-view`, `/epic-sync` updates

## Success Metrics

- **Adoption**: % of new epics using direct task pattern
- **Feedback**: User satisfaction with flexibility
- **Usage patterns**: When teams choose epic → task vs epic → feature → task
- **Refactoring**: Frequency of flattening artificial features
