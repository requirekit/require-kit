---
id: TASK-001B
title: "Transfer Core Commands"
created: 2025-10-19
status: backlog
priority: high
complexity: 4
parent_task: TASK-001
subtasks: []
estimated_hours: 2
---

# TASK-001B: Transfer Core Commands

## Description

Copy core task workflow commands from ai-engineer to agentecflow, removing all references to epic/feature/requirements management.

## Files to Transfer

### Core Commands (COPY with modifications)

```
Source: ai-engineer/installer/global/commands/
Target: agentecflow/installer/global/commands/

FILES:
✓ task-create.md       - MODIFY (remove epic/feature/requirements frontmatter)
✓ task-work.md         - MODIFY (remove requirements context loading)
✓ task-complete.md     - KEEP AS-IS
✓ task-status.md       - MODIFY (remove epic/feature filters)
✓ task-refine.md       - EVALUATE (decide if needed for lite)
✓ debug.md             - KEEP AS-IS
✓ figma-to-react.md    - KEEP AS-IS
✓ zeplin-to-maui.md    - KEEP AS-IS
```

### Commands to EXCLUDE

```
❌ epic-create.md
❌ epic-status.md
❌ epic-sync.md
❌ epic-generate-features.md
❌ feature-create.md
❌ feature-status.md
❌ feature-sync.md
❌ feature-generate-tasks.md
❌ gather-requirements.md
❌ formalize-ears.md
❌ generate-bdd.md
❌ hierarchy-view.md
❌ portfolio-dashboard.md
❌ task-sync.md (PM tool integration)
❌ mcp-zeplin.md (if requirements-focused)
```

## Modifications Required

### 1. task-create.md

**Change frontmatter template from**:
```yaml
---
id: {TASK_ID}
title: "{title}"
created: {date}
status: backlog
priority: {priority}
complexity: 0
epic: {epic_id}
feature: {feature_id}
requirements: [{requirement_ids}]
parent_task: none
subtasks: []
---
```

**To**:
```yaml
---
id: {TASK_ID}
title: "{title}"
created: {date}
status: backlog
priority: {priority}
complexity: 0
parent_task: none
subtasks: []
---
```

**Remove sections**:
- Epic/feature linking logic
- Requirements validation
- PM tool sync prompts

**Remove flags**:
- `epic:EPIC-XXX`
- `feature:FEAT-XXX`
- `requirements:[REQ-001,REQ-002]`

**Keep flags**:
- `priority:high|medium|low`
- `--parent TASK-XXX` (for subtasks)

### 2. task-work.md

**Remove from Phase 1 (Requirements Analysis)**:
- Loading EARS requirements
- Loading BDD scenarios
- Validating requirement links
- Epic/feature context gathering

**Simplify to**:
- Load task description
- Load parent task context (if subtask)
- Identify technology stack

**Keep all phases**:
- ✅ Phase 1: Task Analysis (SIMPLIFIED - no requirements)
- ✅ Phase 2: Implementation Planning
- ✅ Phase 2.5: Architectural Review
- ✅ Phase 2.6: Human Checkpoint (if triggered)
- ✅ Phase 2.7: Complexity Evaluation
- ✅ Phase 3: Implementation
- ✅ Phase 4: Testing
- ✅ Phase 4.5: Test Enforcement (auto-fix loop)
- ✅ Phase 5: Code Review

**Remove flags**:
- `--sync-progress` (PM tool sync)
- `--with-context` (epic/feature context - make this default behavior for parent tasks)

**Keep flags**:
- `--mode=tdd|bdd|standard`
- `--design-only`
- `--implement-only`
- `--micro`

**Update agent orchestration**:
- Remove requirements-analyst agent
- Remove bdd-generator agent
- Keep all other agents

### 3. task-status.md

**Remove filters**:
- `--epic EPIC-XXX`
- `--feature FEAT-XXX`
- `--requirements REQ-XXX`

**Keep filters**:
- `--status backlog|in_progress|in_review|blocked|completed`
- `--priority high|medium|low`
- `--complexity N`
- `--parent TASK-XXX`

**Remove views**:
- Epic rollup view
- Feature progress view
- Requirements traceability view
- PM tool sync status

**Keep views**:
- Kanban board (default)
- Task list
- Complexity distribution
- Parent/subtask hierarchy

### 4. task-refine.md

**Decision**: INCLUDE but simplify

**Remove**:
- Requirements refinement
- BDD scenario updates
- Epic/feature impact analysis

**Keep**:
- Task description clarification
- Complexity re-evaluation
- Subtask breakdown suggestions
- Priority adjustment

### 5. figma-to-react.md, zeplin-to-maui.md

**Keep completely as-is** - These are UX integration features, not requirements management.

### 6. debug.md

**Keep completely as-is** - Development tool.

## Implementation Checklist

### Step 1: Copy Files

```bash
cd ai-engineer

# Copy core commands
cp installer/global/commands/task-create.md ../agentecflow/installer/global/commands/
cp installer/global/commands/task-work.md ../agentecflow/installer/global/commands/
cp installer/global/commands/task-complete.md ../agentecflow/installer/global/commands/
cp installer/global/commands/task-status.md ../agentecflow/installer/global/commands/
cp installer/global/commands/task-refine.md ../agentecflow/installer/global/commands/
cp installer/global/commands/debug.md ../agentecflow/installer/global/commands/
cp installer/global/commands/figma-to-react.md ../agentecflow/installer/global/commands/
cp installer/global/commands/zeplin-to-maui.md ../agentecflow/installer/global/commands/
```

### Step 2: Modify task-create.md

```bash
cd ../agentecflow/installer/global/commands/

# Edit task-create.md
# Remove:
# - epic: {epic_id}
# - feature: {feature_id}
# - requirements: [{requirement_ids}]
# - All epic/feature linking documentation
# - All requirements validation documentation

# Verify no references remain
grep -i "epic\|feature\|requirement\|ears\|bdd" task-create.md
# Should return NO matches (or only in historical context)
```

### Step 3: Modify task-work.md

```bash
# Edit task-work.md
# Remove Phase 1 requirements loading
# Remove epic/feature context loading
# Remove --sync-progress, --with-context flags
# Remove references to requirements-analyst, bdd-generator agents

# Verify
grep -i "epic\|feature\|requirement\|ears" task-work.md
# Should return NO matches in active instructions
```

### Step 4: Modify task-status.md

```bash
# Edit task-status.md
# Remove epic/feature/requirements filters
# Remove PM tool sync status

# Verify
grep -i "epic\|feature\|requirement" task-status.md
# Should return NO matches
```

### Step 5: Modify task-refine.md

```bash
# Edit task-refine.md
# Simplify to task-focused refinement only

# Verify
grep -i "epic\|feature\|requirement\|ears\|bdd" task-refine.md
# Should return NO matches
```

### Step 6: Verify Other Files

```bash
# These should be unchanged
diff ../ai-engineer/installer/global/commands/task-complete.md task-complete.md
diff ../ai-engineer/installer/global/commands/debug.md debug.md
diff ../ai-engineer/installer/global/commands/figma-to-react.md figma-to-react.md
diff ../ai-engineer/installer/global/commands/zeplin-to-maui.md zeplin-to-maui.md
```

## Testing Checklist

### Smoke Tests

```bash
# In a test project
cd /tmp/test-project
agentecflow init default

# Test task-create (should NOT ask for epic/feature)
/task-create "Test task creation"
# Expected: Creates TASK-001 without epic/feature fields

# Verify frontmatter
cat tasks/backlog/TASK-001-test-task-creation.md | head -15
# Should NOT contain: epic, feature, requirements

# Test task-status
/task-status
# Should show simple kanban without epic/feature columns

# Test task-work (dry-run or very simple task)
echo "Just verify it starts without errors - don't need to complete"
```

### Validation Tests

```bash
# Check no requirements features leaked through
cd agentecflow/installer/global/commands/
grep -r "epic" *.md | grep -v "# Historical" | grep -v "# Related"
grep -r "feature" *.md | grep -v "# Historical" | grep -v "# Related"
grep -r "requirement" *.md | grep -v "# Historical"
grep -r "EARS" *.md
grep -r "BDD" *.md | grep -v "mode=bdd" # bdd mode is fine, BDD scenarios are not

# All should return empty or only historical context mentions
```

## Acceptance Criteria

- [ ] 8 core commands copied
- [ ] task-create.md: Frontmatter simplified (no epic/feature/requirements)
- [ ] task-work.md: Phase 1 simplified, agent orchestration updated
- [ ] task-status.md: Filters simplified, views simplified
- [ ] task-refine.md: Simplified to task-only refinement
- [ ] task-complete.md: Unchanged (already task-focused)
- [ ] debug.md: Unchanged
- [ ] figma-to-react.md: Unchanged
- [ ] zeplin-to-maui.md: Unchanged
- [ ] No references to epic/feature/requirements in active instructions
- [ ] Smoke tests pass
- [ ] Validation tests pass

## Estimated Time

2 hours

## Notes

- **Be thorough with grep verification** - Easy to miss references
- **Keep historical context** - OK to mention "this is different from full agentecflow-requirements"
- **Test early** - Don't modify all files then test, test after each modification
- **Document changes** - Add comments like `# LITE: Simplified from full version`
