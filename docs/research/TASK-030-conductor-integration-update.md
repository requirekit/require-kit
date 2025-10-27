# TASK-030 Update: Conductor Parallel Development Integration

**Updated**: 2025-10-18T16:45:00Z
**Related**: TASK-030, TASK-031

## Summary

Updated TASK-030 to include documentation for **TASK-031: Conductor Workflow State Loss** bug and its workarounds. This ensures users have clear guidance on Conductor parallel development while the underlying issue is being fixed.

## What Changed

### 1. Added TASK-031 to Feature List

**New Section**: Critical Bug Fix to Document
- Documents known issue with state loss in Conductor workspaces
- Affects TASK-026 and TASK-027 (both completed via Conductor)
- Implementation summaries, test results, and metadata lost after merge
- Path resolution issues requiring full paths

### 2. Updated Core Components

Added to core Agentecflow Lite components:
- **Parallel development** with Conductor.build (with known issues to document)

### 3. Enhanced CLAUDE.md Documentation

Added Section 8 to CLAUDE.md updates:
```markdown
8. **Conductor Integration (Parallel Development)** (update existing section)
   - Add TASK-031 known issues
   - Document workarounds until fixed
   - Add pre-merge checklist
   - Include state preservation best practices
   - Link to updated conductor-user-guide.md
```

### 4. Added Conductor User Guide Update

New Workflow Guide to Update:
```markdown
7. Update `docs/guides/conductor-user-guide.md` (EXISTING - UPDATE)
   - Add TASK-031 known issues section
   - Document state loss problem and workarounds
   - Add pre-merge checklist to prevent state loss
   - Include manual recovery procedures
   - Add troubleshooting section
   - Document path resolution workaround (full paths)
   - Best practices for state preservation
   - Link to TASK-031 for tracking fix progress
```

### 5. Updated Implementation Plan

**Phase 5: Workflow Guides** (increased from 1.5h to 2h)
- Added conductor-user-guide.md update with TASK-031 known issues
- Total time increased from 8h to 8.5h (~1 day)

### 6. Updated Dependencies

Added to internal dependencies:
```markdown
- 🚨 TASK-031: Conductor state loss bug (must document known issue)
```

Added to existing documentation:
```markdown
- ✅ docs/guides/conductor-user-guide.md (exists, needs update for TASK-031)
- ✅ CLAUDE.md has Conductor section (needs TASK-031 known issues)
```

### 7. Updated Acceptance Criteria

Added:
- [ ] Conductor known issues (TASK-031) documented with workarounds
- [ ] Conductor known issues clearly documented
- [ ] Workarounds provided until TASK-031 is fixed

## Conductor Known Issues Section (Preview)

The documentation will include a section like this:

```markdown
## ⚠️ Known Issues (Conductor Workflows)

### State Loss After Merge (TASK-031) 🚨

**Issue**: When using `/task-work` and `/task-complete` in Conductor workspaces,
implementation summaries and state metadata may be lost after merging to main.

**Symptoms**:
- Missing files in `docs/state/{task_id}/`
  - implementation_plan.md
  - test_results.json
  - code_review.json
  - plan_audit.json
- Incomplete task frontmatter (missing test results, review scores)
- Path resolution requires full paths instead of task IDs

**Root Cause**: Under investigation (TASK-031)
- State files created but not automatically committed
- Path resolution issues in worktree environments
- State directory isolation between worktrees

**Current Workarounds** (until TASK-031 is fixed):

1. **Use Full Paths**:
   ```bash
   # Instead of:
   /task-work TASK-026

   # Use:
   /task-work /full/path/to/tasks/backlog/TASK-026-*.md
   ```

2. **Manually Commit State Files**:
   ```bash
   # After /task-work
   git add docs/state/
   git commit -m "Add state files for TASK-026"

   # After /task-complete
   git add docs/state/ tasks/completed/
   git commit -m "Complete TASK-026 with state"
   ```

3. **Pre-Merge Checklist**:
   Before merging Conductor workspace to main:
   ```bash
   # 1. Check for uncommitted state
   git status | grep "docs/state/"

   # 2. Verify state directories exist for completed tasks
   for task in tasks/completed/*.md; do
       task_id=$(basename "$task" .md)
       [ -d "docs/state/$task_id" ] || echo "⚠️ Missing state: $task_id"
   done

   # 3. Commit any missing state
   git add docs/state/
   git commit -m "Preserve task state before merge"
   ```

4. **Manual State Recovery** (if already lost):
   ```bash
   # Reconstruct from git history
   git log --all --grep="TASK-026" --stat
   git show <commit-hash>:docs/state/TASK-026/implementation_plan.md

   # Recreate state directory
   mkdir -p docs/state/TASK-026
   # Manually recreate files from commits or implementation
   ```

**Track the Fix**: Follow [TASK-031](../../tasks/backlog/TASK-031-fix-conductor-workflow-state-loss.md)
for progress on permanent resolution.

**Expected Fix Timeline**: TASK-031 is HIGH priority (6 hours estimated)
```

## Documentation Structure

### Existing Conductor Documentation
- `docs/guides/conductor-user-guide.md` - General Conductor usage guide
- `CLAUDE.md` - Section on Conductor Integration (Parallel Development)

### What TASK-030 Will Add/Update
1. **Known Issues Section** in conductor-user-guide.md
2. **Troubleshooting Section** with TASK-031 workarounds
3. **Pre-Merge Checklist** to prevent state loss
4. **Manual Recovery Procedures** for lost state
5. **Updated Best Practices** for state preservation

### Cross-References
All Conductor documentation will:
- Link to TASK-031 for tracking fix progress
- Provide clear "known issue" callouts
- Separate workarounds from permanent solutions
- Include examples from TASK-026 and TASK-027

## Benefits of This Approach

### 1. Transparency
Users know the issue exists and are warned upfront

### 2. Actionable Workarounds
Clear, tested procedures to avoid data loss

### 3. Trackable Progress
Link to TASK-031 shows fix is underway

### 4. Separate Concerns
Known issues don't pollute feature documentation

### 5. Safety Net
Pre-merge checklist prevents most state loss scenarios

## Implementation Notes for TASK-030

When documenting Conductor integration:

**DO**:
- ✅ Clearly mark as "Known Issue"
- ✅ Provide tested workarounds
- ✅ Link to TASK-031 for fix tracking
- ✅ Include real examples (TASK-026, TASK-027)
- ✅ Add pre-merge checklist
- ✅ Show manual recovery procedures

**DON'T**:
- ❌ Hide or minimize the issue
- ❌ Suggest Conductor is broken (it's our workflow that needs fixing)
- ✅ Present workarounds as permanent solutions
- ❌ Mix known issues with feature documentation

## Success Metrics

After TASK-030 completion:
- [ ] Zero state loss incidents from users who read the guide
- [ ] Pre-merge checklist adopted by Conductor users
- [ ] Support questions about state loss include reference to known issue
- [ ] Users aware TASK-031 is in progress

After TASK-031 completion:
- [ ] Update documentation to remove workarounds
- [ ] Add "Fixed in vX.X" note
- [ ] Simplify workflow (no more manual state commits)
- [ ] Remove pre-merge checklist (no longer needed)

## Timeline

**TASK-030 Documentation**: 8.5 hours (~1 day)
- Document known issue: 30 minutes
- Write workarounds: 30 minutes
- Create pre-merge checklist: 30 minutes
- Manual recovery procedures: 30 minutes
- Update existing sections: integrated into other phases

**TASK-031 Fix**: 6 hours
- Once fixed, documentation updates minimal (remove workarounds)

## Related Files

**To Be Updated by TASK-030**:
- `docs/guides/conductor-user-guide.md`
- `CLAUDE.md` (Conductor Integration section)
- `docs/research/agentecflow-lite-positioning-summary.md` (mention parallel development)

**Referenced**:
- `tasks/backlog/TASK-031-fix-conductor-workflow-state-loss.md`
- `tasks/completed/TASK-026-create-task-refine-command.md` (affected task)
- `tasks/completed/TASK-027-convert-plan-storage-to-markdown.md` (affected task)

---

**Status**: TASK-030 updated to include Conductor documentation
**Next Step**: Execute TASK-030 to update all documentation
**Priority**: HIGH (prevents data loss for Conductor users)
**Impact**: Improved safety and user confidence in parallel development workflows
