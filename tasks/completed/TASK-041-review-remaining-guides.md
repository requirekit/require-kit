---
id: TASK-041
title: Review remaining guide files in docs/guides/ directory
status: completed
created: 2025-11-03T12:00:00Z
updated: 2025-11-03T16:00:00Z
completed: 2025-11-03T16:00:00Z
priority: medium
tags: [documentation, guides, cleanup, audit]
complexity: 7
---

# Task: Review Remaining Guide Files in docs/guides/

## Description

Review approximately 20+ guide files in `docs/guides/` directory to identify taskwright feature references, outdated content, and files that should be deprecated, moved to taskwright, or updated to focus on require-kit.

This is a comprehensive audit and cleanup task for all documentation not covered by TASK-038.

## Files to Review (25 total)

Based on `ls -la docs/guides/*.md` output:

1. agentecflow-lite-creation-strategy.md (63,007 bytes)
2. agentic-flow-task-management-with-verification.md (14,626 bytes)
3. design-patterns-mcp-setup.md (19,855 bytes)
4. DOCUMENTATION-UPDATE-SUMMARY.md (6,098 bytes)
5. ENTERPRISE-FEATURES-GUIDE.md (13,803 bytes)
6. MIGRATION-GUIDE.md (6,892 bytes)
7. model-optimization-guide.md (13,923 bytes)
8. NET_STACKS_INTEGRATION.md (9,274 bytes)
9. QUICK_REFERENCE.md (11,014 bytes)
10. README.md (7,427 bytes)
11. task-creation-implementation-workflow.md (12,358 bytes)
12. task-work-practical-example.md (10,568 bytes)
13. TEMPLATE_INTEGRATION_SUMMARY.md (8,426 bytes)
14. template-creation-workflow.md (21,590 bytes)
15. typical_installation_of_Agentecflow.md (10,534 bytes)
16. V2-MIGRATION-GUIDE.md (10,379 bytes)
17. conductor-user-guide.md (26,580 bytes)
18. maui-mydrive-setup-completion.md (17,549 bytes)
19. maui-mydrive-setup-guide.md (17,015 bytes)
20. maui-mydrive-setup-summary.md (11,426 bytes)
21. MARKDOWN-SPEC-DRIVEN-DEVELOPMENT-PRESENTATION.md (54,741 bytes)

**Note**: Files updated in TASK-038 are excluded from this list.

## Review Criteria for Each File

For each guide file, determine:

1. **Scope Classification**
   - Pure require-kit: Requirements/BDD/Epic/Feature content
   - Pure taskwright: Task execution/testing/quality gates
   - Mixed: Contains both
   - Deprecated: Outdated or no longer relevant

2. **Action Required**
   - ✅ Keep as-is (already correct for require-kit)
   - 📝 Update (has taskwright references, needs cleanup)
   - 🗂️ Deprecate (move to .deprecated/)
   - 🔄 Move to taskwright (belongs in taskwright repo)
   - ❌ Delete (truly obsolete)

3. **Integration Links Needed**
   - Files that mention task execution need integration guide links
   - Files that describe complete workflows need clear handoff points

## High Priority Files (Review First)

Based on file names, these likely need attention:

### Task-Focused Guides (Likely taskwright)
- task-creation-implementation-workflow.md
- task-work-practical-example.md
- agentic-flow-task-management-with-verification.md

**Expected Action**: Move to taskwright or deprecate

### Migration Guides
- MIGRATION-GUIDE.md
- V2-MIGRATION-GUIDE.md

**Expected Action**: Review for require-kit vs taskwright migration content

### Feature Guides
- ENTERPRISE-FEATURES-GUIDE.md
- conductor-user-guide.md

**Expected Action**: Verify scope, update if needed

### Quick References
- QUICK_REFERENCE.md
- README.md (in guides/)

**Expected Action**: Ensure commands are require-kit only

## Acceptance Criteria

- [ ] All 21+ guide files reviewed and categorized
- [ ] Taskwright-specific guides moved to `.deprecated/taskwright/` or removed
- [ ] Mixed guides updated with clear integration sections
- [ ] require-kit guides verified for accuracy
- [ ] docs/guides/README.md updated with current file list and descriptions
- [ ] No broken internal links after changes
- [ ] Clear navigation path for users (what to read when)

## Deliverable: Guide Audit Report

Create a summary document: `docs/guides/GUIDE-AUDIT-REPORT-TASK-041.md`

```markdown
# Guide Files Audit Report

**Date**: 2025-11-03
**Task**: TASK-041

## Summary

- Total Files Reviewed: XX
- Kept as-is: XX files
- Updated: XX files
- Deprecated: XX files
- Moved to taskwright: XX files
- Deleted: XX files

## Files by Category

### require-kit Guides (Keep)
- file1.md - Description
- file2.md - Description

### Updated Guides
- file3.md - Added integration links
- file4.md - Removed taskwright sections

### Deprecated Guides
- file5.md - Reason for deprecation
- file6.md - Superseded by X

### Moved to taskwright
- file7.md - Pure task execution guide
- file8.md - Task workflow examples

## Recommended Guide Structure

[Proposed new structure for docs/guides/]

## Next Steps

[Actions needed to complete cleanup]
```

## Test Requirements

- [ ] All remaining guides accurately represent require-kit features
- [ ] No guides claim taskwright features as built-in
- [ ] Integration guide linked appropriately
- [ ] docs/guides/README.md provides clear navigation
- [ ] No broken links in any guide file
- [ ] Consistent terminology across all guides

## Implementation Approach

### Phase 1: Quick Scan (2 hours)
- Read each file's first 50 lines
- Categorize based on content
- Flag obvious moves/deletes

### Phase 2: Detailed Review (4 hours)
- Deep read of mixed/unclear files
- Decide on specific actions
- Document decisions in audit report

### Phase 3: Cleanup (2 hours)
- Move/update/deprecate files
- Update docs/guides/README.md
- Fix broken links
- Verify navigation

## Special Considerations

### Template and Stack Guides
Files like:
- maui-mydrive-setup-*.md
- template-creation-workflow.md
- NET_STACKS_INTEGRATION.md

**Decision needed**: Do these belong in require-kit or taskwright?
- If they're about generating requirements/specs: keep
- If they're about implementation templates: consider moving

### MCP and Integration Guides
Files like:
- design-patterns-mcp-setup.md
- conductor-user-guide.md

**Decision needed**: Integration guides for external tools
- Keep if relevant to requirements management
- Consider separate integrations/ directory

### Historical/Summary Docs
Files like:
- DOCUMENTATION-UPDATE-SUMMARY.md
- MARKDOWN-SPEC-DRIVEN-DEVELOPMENT-PRESENTATION.md

**Decision needed**: Archive vs keep
- Move to docs/history/ if historical
- Keep if still relevant documentation

## Related Tasks

- TASK-038: Core documentation (completed before this)
- TASK-039: Commands cleanup (may reference guides)
- TASK-040: CLAUDE.md review (should align with guide content)

## Success Metrics

- Clear separation of require-kit vs taskwright documentation
- Users can easily find relevant guides for their use case
- No confusion about feature availability
- Maintained documentation is up-to-date and accurate
