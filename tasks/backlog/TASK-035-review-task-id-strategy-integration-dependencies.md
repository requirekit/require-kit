---
id: TASK-035
title: Review Task ID Strategy and Integration Dependencies Between require-kit and taskwright
status: backlog
created: 2025-11-29T15:30:00Z
updated: 2025-11-29T15:30:00Z
priority: high
tags: [architecture, integration, design-decision, review]
complexity: 0
task_type: review
decision_required: true
test_results:
  status: pending
  coverage: null
  last_run: null
---

# Task: Review Task ID Strategy and Integration Dependencies

## Context

This is an **architectural review and decision-making task** that examines two critical integration concerns between require-kit and taskwright:

1. **Task ID Generation Strategy**: Hash-based IDs in taskwright vs hierarchical IDs in require-kit
2. **Integration Philosophy**: Optional standalone tools vs required dependencies

## Background

### Current Situation

**taskwright** uses **hash-based collision-free Task IDs**:
- Format: `TASK-{hash}` or `TASK-{prefix}-{hash}`
- Example: `TASK-A3F2`, `TASK-E01-B2C4`
- Uses SHA-256 cryptographic hashing for uniqueness
- Implemented in `/installer/global/lib/id_generator.py`
- Zero collision risk even at 5,000+ tasks

**require-kit** uses **hierarchical feature-scoped Task IDs**:
- Format: `TASK-{epic}.{feature}.{seq}`
- Example: `TASK-001.2.05` (Epic 001, Feature 2, Task 05)
- Documented in [feature-generate-tasks.md](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/feature-generate-tasks.md#35-99)
- Visual hierarchy and feature identity preservation
- Sequential numbering within feature scope

**Current require-kit Project**: Uses simple sequential IDs (TASK-001, TASK-021, TASK-034)

### Integration Philosophy Precedent

Recently, a **precedent was set** with BDD mode:
- `taskwright /task-work --mode=BDD` now **requires** require-kit
- Guards check for `.requirekit-marker` file
- Presents error if require-kit not installed: "require-kit needs to be installed for BDD functionality"

This challenges the original vision of "both optional standalone tools that work together."

## Decision Points

### 1. Task ID Generation Strategy

**Options:**

**A) Adopt Hash-Based IDs Across Both Packages**
- ✅ Collision-free guarantee
- ✅ Consistent ID format across tools
- ✅ Works well for standalone task creation
- ❌ Loses visual feature hierarchy (TASK-001.2.05 → TASK-A3F2)
- ❌ Harder to identify which feature a task belongs to at a glance

**B) Keep Hierarchical IDs for require-kit, Hash for taskwright**
- ✅ Preserves feature identity and visual hierarchy
- ✅ Better for requirements traceability
- ✅ Natural file grouping by feature
- ❌ Two different ID systems to maintain
- ❌ Potential confusion when both tools are used together
- ❌ `/feature-generate-tasks` would need custom ID logic

**C) Hybrid Approach: Hierarchical with Hash Suffix**
- Format: `TASK-{epic}.{feature}.{hash}`
- Example: `TASK-001.2.A3F2`
- ✅ Maintains hierarchy visibility
- ✅ Collision-free via hash
- ✅ Best of both worlds
- ❌ Longer IDs
- ❌ More complex implementation
- ❌ Requires coordination between packages

**D) Use Hash-Based IDs but Store Hierarchy Metadata**
- Format: `TASK-A3F2` with frontmatter `epic: EPIC-001, feature: FEAT-001.2`
- ✅ Collision-free IDs
- ✅ Hierarchy tracked in metadata
- ✅ Consistent with taskwright
- ❌ Hierarchy not visible in ID or filename
- ❌ Requires opening file to see feature relationship

### 2. Integration Philosophy

**Options:**

**A) Make taskwright a Required Dependency of require-kit**
- Rationale: "Who's going to use require-kit without taskwright?"
- ✅ Simplifies integration - one source of truth
- ✅ Can use taskwright's ID generation directly
- ✅ Matches BDD mode precedent
- ❌ Breaks standalone requirements management use case
- ❌ Forces users who only want requirements tooling to install task execution system
- ❌ Contradicts original design philosophy

**B) Make require-kit a Required Dependency of taskwright**
- Rationale: BDD mode already requires require-kit
- ✅ BDD/requirements management is core to quality workflows
- ✅ Task execution benefits from requirements traceability
- ❌ Forces users who only want task execution to install requirements system
- ❌ taskwright loses standalone viability

**C) Keep Both Optional with Feature Detection**
- Maintain bidirectional detection via marker files
- ✅ Maximum flexibility for users
- ✅ Each tool remains viable standalone
- ✅ Graceful degradation when one is missing
- ❌ More complex to maintain
- ❌ Requires careful coordination of shared features
- ❌ Two ID generation strategies to maintain

**D) Create Unified Package**
- Merge require-kit and taskwright into single system
- ✅ No integration complexity
- ✅ Single ID strategy
- ✅ Simplified installation
- ❌ Loses modularity
- ❌ Forces all-or-nothing adoption
- ❌ Major architectural change

## Recommendation Questions

To make informed recommendations, this review should answer:

1. **User Personas**: Who actually uses require-kit without taskwright? What's their use case?
2. **ID Traceability**: How critical is visual hierarchy (TASK-001.2.05) vs metadata-based hierarchy?
3. **PM Tool Integration**: Do external PM tools (Jira, Linear) care about ID format or just metadata?
4. **Migration Path**: If we change ID strategy, how do we migrate existing tasks?
5. **Precedent Analysis**: Does BDD mode requiring require-kit set a justified precedent, or is it an exception?

## Analysis Areas

### Files to Review

1. **Hash-Based ID Implementation** (taskwright):
   - `/installer/global/lib/id_generator.py` - SHA-256 ID generation
   - `/installer/global/commands/task-create.md` - Hash ID documentation

2. **Hierarchical ID Implementation** (require-kit):
   - [feature-generate-tasks.md:35-99](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/feature-generate-tasks.md#L35-L99) - Feature-scoped ID generation
   - Task ID validation and duplication detection logic

3. **Integration Points**:
   - BDD mode guards in taskwright `/task-work`
   - Feature detection mechanisms
   - Marker file usage (`.taskwright-marker`, `.requirekit-marker`)

4. **User Documentation**:
   - Installation guides suggesting standalone vs combined use
   - Command documentation for `/feature-generate-tasks`
   - Integration guide between packages

### Impact Analysis

**If require-kit requires taskwright:**
- `/feature-generate-tasks` can use `installer/global/lib/id_generator.py` directly
- Single source of truth for IDs
- Breaks standalone requirements management workflow

**If IDs are harmonized:**
- Choose one strategy and implement across both
- Migration plan for existing tasks
- Documentation updates
- Potential breaking change for existing users

## Success Criteria

This review task is complete when:

1. ✅ Clear recommendation on Task ID strategy (A/B/C/D above)
2. ✅ Clear recommendation on integration philosophy (A/B/C/D above)
3. ✅ Impact analysis of each option documented
4. ✅ Migration path outlined if changes are recommended
5. ✅ User persona analysis completed
6. ✅ Decision rationale documented for future reference

## Next Steps After Review

Depending on decisions:
- **If harmonizing IDs**: Create implementation task for ID migration
- **If maintaining separate strategies**: Document integration guidelines
- **If changing dependencies**: Update installation documentation
- **If keeping as-is**: Document the rationale and close

## References

- [feature-generate-tasks.md](file:///Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/feature-generate-tasks.md) - Hierarchical ID strategy
- taskwright `/task-create` - Hash-based ID strategy
- `installer/global/lib/id_generator.py` - Hash ID implementation
- `.requirekit-marker` / `.taskwright-marker` - Feature detection

## Notes

- This is a **review task**, not an implementation task
- Use `/task-review TASK-035` for systematic analysis
- Decision should be made collaboratively with maintainers
- Consider backward compatibility and user migration impact
