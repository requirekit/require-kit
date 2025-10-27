# Task Numbering Strategy - CORRECTION

## Problem with Current Recommendation

In our earlier analysis, we recommended **sequential numbering per epic** (TASK-001.01-35), but this creates a critical usability problem:

**❌ Current Sequential Numbering**:
```
docs/tasks/backlog/
├── TASK-001.01-mcp-server-skeleton.md          [FEAT-001.1]
├── TASK-001.02-gather-requirements-tool.md      [FEAT-001.1]
├── TASK-001.03-refine-requirement-tool.md       [FEAT-001.1]
├── TASK-001.04-validate-requirements-tool.md    [FEAT-001.1]
├── TASK-001.05-input-format-parsers.md          [FEAT-001.1]
├── TASK-001.06-comprehensive-testing.md         [FEAT-001.1]
├── TASK-001.07-api-documentation.md             [FEAT-001.1]
├── TASK-001.08-docker-integration.md            [FEAT-001.1]
├── TASK-001.09-ears-parser-unit-tests.md        [FEAT-001.2] ← Can't tell this is different feature!
├── TASK-001.10-requirement-generator-tests.md   [FEAT-001.2]
...
```

**Problem**: You cannot visually distinguish which feature a task belongs to by looking at the task ID!

---

## Corrected Solution: Feature-Hierarchical Numbering

### ✅ RECOMMENDED: Feature-Hierarchical Task IDs

**Format**: `TASK-{epic}.{feature}.{task}`

**Example Structure**:
```
EPIC-001 (Requirements MCP Server)
├── FEAT-001.1 (Specification Analysis) → TASK-001.1.01, TASK-001.1.02, ..., TASK-001.1.08
├── FEAT-001.2 (EARS Requirements)     → TASK-001.2.01, TASK-001.2.02, ..., TASK-001.2.08
├── FEAT-001.3 (Storage & Retrieval)   → TASK-001.3.01, TASK-001.3.02, ..., TASK-001.3.13
└── FEAT-001.4 (LangGraph)             → TASK-001.4.01, TASK-001.4.02, ..., TASK-001.4.06

EPIC-002 (Engineering MCP Server)
├── FEAT-002.1 → TASK-002.1.01, TASK-002.1.02, ...
└── FEAT-002.2 → TASK-002.2.01, TASK-002.2.02, ...
```

### Benefits ✅

1. **Visual Feature Identification**
   - `TASK-001.1.xx` → Immediately know it's FEAT-001.1
   - `TASK-001.2.xx` → Immediately know it's FEAT-001.2
   - At a glance, you can see feature boundaries

2. **Clear Hierarchy**
   ```
   EPIC-001 → FEAT-001.2 → TASK-001.2.05
      ↓           ↓              ↓
    Epic       Feature        Task
   ```

3. **No Duplicates Possible**
   - Each feature has its own task sequence
   - `TASK-001.1.01` cannot conflict with `TASK-001.2.01`
   - System ensures uniqueness within feature scope

4. **Natural Grouping in File Listings**
   ```
   TASK-001.1.01-xxx.md
   TASK-001.1.02-xxx.md
   TASK-001.1.03-xxx.md  ← All FEAT-001.1 tasks together
   ──────────────────────
   TASK-001.2.01-xxx.md
   TASK-001.2.02-xxx.md  ← All FEAT-001.2 tasks together
   ```

5. **Progress Tracking Easier**
   - See exactly how many tasks per feature
   - Identify feature bottlenecks
   - Better sprint planning

---

## Updated Task ID Generation Logic

### For `/feature-generate-tasks`

```bash
# CORRECTED: Feature-hierarchical task ID generation
generate_task_id_for_feature() {
    epic_id=$1      # e.g., EPIC-001
    feature_id=$2   # e.g., FEAT-001.2

    # Extract numbers
    epic_num=$(echo $epic_id | sed 's/EPIC-//')           # 001
    feature_num=$(echo $feature_id | sed 's/FEAT-[0-9]*\.//')  # 2

    # Find highest task number for THIS FEATURE
    existing_tasks=$(find docs/tasks -type f -name "TASK-${epic_num}.${feature_num}.*.md" 2>/dev/null)

    if [ -z "$existing_tasks" ]; then
        task_num="01"
    else
        max_num=$(echo "$existing_tasks" | \
            sed -n "s/.*TASK-${epic_num}\.${feature_num}\.\([0-9]\+\).*/\1/p" | \
            sort -n | tail -1)
        task_num=$(printf "%02d" $((10#$max_num + 1)))
    fi

    # Generate: TASK-001.2.01
    echo "TASK-${epic_num}.${feature_num}.${task_num}"
}

# Validation: Check no duplicate exists
validate_task_id() {
    task_id=$1

    conflicts=$(find docs/tasks -type f -name "${task_id}-*.md" 2>/dev/null)

    if [ -n "$conflicts" ]; then
        echo "❌ ERROR: Duplicate task ID: $task_id"
        echo "   Existing: $conflicts"
        return 1
    fi

    return 0
}
```

### For `/task-create`

```bash
# Manual task creation with feature context
generate_task_id_manual() {
    epic_id=$1
    feature_id=$2

    # If no feature specified, user must provide it
    if [ -z "$feature_id" ]; then
        echo "❌ ERROR: Feature ID required for task creation"
        echo "   Usage: /task-create \"Title\" epic:EPIC-001 feature:FEAT-001.2"
        return 1
    fi

    # Use same logic as feature-generate-tasks
    generate_task_id_for_feature "$epic_id" "$feature_id"
}
```

---

## Migration Plan for agentecflow_platform

### Current State (Sequential)
```
TASK-001.01 through TASK-001.35 (no feature visibility)
```

### Target State (Feature-Hierarchical)
```
FEAT-001.1: TASK-001.1.01 through TASK-001.1.08 (8 tasks)
FEAT-001.2: TASK-001.2.01 through TASK-001.2.08 (8 tasks)
FEAT-001.3: TASK-001.3.01 through TASK-001.3.13 (13 tasks)
FEAT-001.4: TASK-001.4.01 through TASK-001.4.06 (6 tasks)
```

### Renumbering Script

```bash
#!/bin/bash
# renumber-tasks-feature-hierarchical.sh

cd /Users/richardwoollcott/Projects/appmilla_github/agentecflow_platform

# FEAT-001.1 tasks (currently TASK-001.01-08)
for i in {1..8}; do
    old_num=$(printf "%02d" $i)
    new_num=$(printf "%02d" $i)
    old_file=$(ls docs/tasks/backlog/TASK-001.$old_num-*.md 2>/dev/null)
    if [ -n "$old_file" ]; then
        base_name=$(basename "$old_file" | sed "s/TASK-001\.$old_num/TASK-001.1.$new_num/")
        git mv "$old_file" "docs/tasks/backlog/$base_name"
        echo "Renamed: TASK-001.$old_num → TASK-001.1.$new_num"
    fi
done

# FEAT-001.2 tasks (currently TASK-001.09-16)
for i in {9..16}; do
    old_num=$(printf "%02d" $i)
    new_num=$(printf "%02d" $((i - 8)))
    old_file=$(ls docs/tasks/backlog/TASK-001.$old_num-*.md 2>/dev/null)
    if [ -n "$old_file" ]; then
        base_name=$(basename "$old_file" | sed "s/TASK-001\.$old_num/TASK-001.2.$new_num/")
        git mv "$old_file" "docs/tasks/backlog/$base_name"
        echo "Renamed: TASK-001.$old_num → TASK-001.2.$new_num"
    fi
done

# FEAT-001.3 tasks (currently TASK-001.17-29)
for i in {17..29}; do
    old_num=$(printf "%02d" $i)
    new_num=$(printf "%02d" $((i - 16)))
    old_file=$(ls docs/tasks/backlog/TASK-001.$old_num-*.md 2>/dev/null)
    if [ -n "$old_file" ]; then
        base_name=$(basename "$old_file" | sed "s/TASK-001\.$old_num/TASK-001.3.$new_num/")
        git mv "$old_file" "docs/tasks/backlog/$base_name"
        echo "Renamed: TASK-001.$old_num → TASK-001.3.$new_num"
    fi
done

# FEAT-001.4 tasks (currently TASK-001.30-35)
for i in {30..35}; do
    old_num=$(printf "%02d" $i)
    new_num=$(printf "%02d" $((i - 29)))
    old_file=$(ls docs/tasks/backlog/TASK-001.$old_num-*.md 2>/dev/null)
    if [ -n "$old_file" ]; then
        base_name=$(basename "$old_file" | sed "s/TASK-001\.$old_num/TASK-001.4.$new_num/")
        git mv "$old_file" "docs/tasks/backlog/$base_name"
        echo "Renamed: TASK-001.$old_num → TASK-001.4.$new_num"
    fi
done

echo "✅ Renumbering complete!"
echo ""
echo "Verify with: ls docs/tasks/backlog/ | grep TASK-001"
```

---

## Updated Command Documentation

### feature-generate-tasks.md

**Change from**:
```
Sequential per Epic:
EPIC-001 → TASK-001.01, TASK-001.02, TASK-001.03, ...
```

**Change to**:
```
Feature-Hierarchical:
EPIC-001, FEAT-001.1 → TASK-001.1.01, TASK-001.1.02, ...
EPIC-001, FEAT-001.2 → TASK-001.2.01, TASK-001.2.02, ...
```

### task-create.md

**Change from**:
```bash
# Task creation (old - no feature required)
/task-create "Title" epic:EPIC-001
# Generated: TASK-001.23 (next available)
```

**Change to**:
```bash
# Task creation (new - feature REQUIRED)
/task-create "Title" epic:EPIC-001 feature:FEAT-001.2
# Generated: TASK-001.2.05 (next in feature)

# Error if feature not specified
/task-create "Title" epic:EPIC-001
❌ ERROR: Feature ID required
```

---

## Comparison Table

| Aspect | Sequential (Wrong) | Feature-Hierarchical (Correct) |
|--------|-------------------|--------------------------------|
| **Format** | TASK-001.01 | TASK-001.2.01 |
| **Visual Feature ID** | ❌ No | ✅ Yes |
| **Hierarchy Clear** | ❌ No | ✅ Yes |
| **Duplicate Prevention** | ✅ Yes (but harder) | ✅ Yes (easier) |
| **File Grouping** | ❌ Mixed | ✅ Natural |
| **Progress Tracking** | ❌ Difficult | ✅ Easy |
| **Sprint Planning** | ❌ Need to lookup | ✅ Immediate |
| **At-a-Glance Understanding** | ❌ No | ✅ Yes |

---

## Examples in Practice

### Backlog View (Feature-Hierarchical)
```
docs/tasks/backlog/
├── TASK-001.1.01-mcp-server-skeleton.md
├── TASK-001.1.02-gather-requirements-tool.md
├── TASK-001.1.03-refine-requirement-tool.md
├── TASK-001.1.04-validate-requirements-tool.md
├── TASK-001.1.05-input-format-parsers.md
├── TASK-001.1.06-comprehensive-testing.md
├── TASK-001.1.07-api-documentation.md
├── TASK-001.1.08-docker-integration.md
│
├── TASK-001.2.01-ears-parser-unit-tests.md
├── TASK-001.2.02-requirement-generator-tests.md
├── TASK-001.2.03-bdd-scenario-tests.md
...
```

**Benefit**: Immediately see "TASK-001.1.xx are all FEAT-001.1 tasks"

### Command Usage
```bash
# Generate tasks for feature
/feature-generate-tasks FEAT-001.2
# Creates: TASK-001.2.01, 001.2.02, 001.2.03, ...

# Manually create task in feature
/task-create "Additional EARS test" epic:EPIC-001 feature:FEAT-001.2
# Creates: TASK-001.2.09 (continues sequence)

# Status check
/feature-status FEAT-001.2 --tasks
# Shows: TASK-001.2.01 through TASK-001.2.09 (clear grouping)
```

---

## Decision

**ADOPT**: Feature-Hierarchical Task Numbering

**Format**: `TASK-{epic}.{feature}.{task}`

**Rationale**:
1. ✅ Visual feature identification at a glance
2. ✅ Clear hierarchy (Epic → Feature → Task)
3. ✅ Natural file grouping in directories
4. ✅ Easier progress tracking and sprint planning
5. ✅ Better user experience for developers
6. ✅ No duplicate risk (feature-scoped sequences)

**Migration**: Use provided renumbering script for agentecflow_platform

---

**Created**: 2025-10-04
**Status**: RECOMMENDED APPROACH (corrects earlier sequential numbering decision)
**Priority**: HIGH (significantly improves usability)
