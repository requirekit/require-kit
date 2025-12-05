---
id: TASK-8C3E
title: Clarify PM tool sync commands are specification-only
status: in_review
created: 2025-12-05T12:00:00Z
updated: 2025-12-05T12:15:00Z
completed: 2025-12-05T12:15:00Z
priority: high
tags: [documentation, pm-tools, feature-sync, epic-sync, clarification]
task_type: implementation
complexity: 2
parent_task: TASK-F92D
test_results:
  status: passed
  coverage: null
  last_run: 2025-12-05T12:15:00Z
---

# Task: Clarify PM tool sync commands are specification-only

## Description

Following the review in TASK-F92D, update RequireKit documentation to clearly indicate that `/feature-sync` and `/epic-sync` commands are **specification documents** that describe the intended API integration, but are NOT currently implemented.

The current documentation at https://requirekit.ai/integration/pm-tools/ presents these commands as working functionality, which is misleading to users.

## Implementation Scope

### 1. Update docs/integration/pm-tools.md

Add clear status badges and notices:
- Mark as "Specification Ready - Implementation Required"
- Add notice box explaining these are specifications, not working commands
- Clarify what IS provided (structured metadata) vs what requires implementation (API calls)

### 2. Update installer/global/commands/feature-sync.md

Add header notice:
```markdown
> **Status: Specification Only**
> This document describes the intended feature-sync command behavior.
> Actual PM tool API integration requires MCP server or custom implementation.
```

### 3. Update installer/global/commands/epic-sync.md

Add same header notice as feature-sync.

### 4. Update docs/index.md Integration Section

Ensure the integration link clearly indicates specification status.

### 5. Review Other Documentation

- Check docs/INTEGRATION-GUIDE.md for accuracy
- Check any other files referencing PM tool sync

## Files to Modify

- `docs/integration/pm-tools.md` - Main PM tools documentation
- `installer/global/commands/feature-sync.md` - Feature sync specification
- `installer/global/commands/epic-sync.md` - Epic sync specification
- `docs/index.md` - If integration section needs clarification
- `docs/INTEGRATION-GUIDE.md` - If PM tool references need updating

## Acceptance Criteria

- [x] All PM sync command docs clearly marked as "Specification Only"
- [x] Users understand these are specifications, not working commands
- [x] Clear explanation of what IS provided (structured metadata for export)
- [x] Clear explanation of what IS NOT provided (actual API integration)
- [x] Path forward documented (MCP server or custom implementation)
- [x] No misleading claims about working functionality

## Implementation Summary

### Files Updated

1. **docs/integration/pm-tools.md**
   - Added prominent "Status: Specification Ready - Implementation Required" notice at top
   - Changed "Supported PM Tools" to "Supported PM Tools (Specification)"
   - Added "# When implemented:" comments to all command examples
   - Changed "API Integration: Requires MCP server..." to "API Integration Not Implemented"

2. **installer/global/commands/feature-sync.md**
   - Added header notice: "Status: Specification Only"
   - Clarified this describes intended behavior, requires MCP server or custom implementation

3. **installer/global/commands/epic-sync.md**
   - Added same header notice as feature-sync

4. **docs/INTEGRATION-GUIDE.md**
   - Updated require-kit command examples to comment out feature-sync with note
   - Removed "PM tool exports" from output artifacts list
   - Changed PM Tool Export row in feature matrix from "✅ Full" to "⚠️ Metadata Ready"
   - Rewrote Workflow 3 to clarify PM metadata is ready but API not implemented

## Notes

From TASK-F92D review findings:
- feature-sync.md: 452 lines of specification
- epic-sync.md: 485 lines of specification
- No MCP server for PM tools exists
- No API integration code exists
- Current docs/integration/pm-tools.md does mention "requires MCP server" but it's buried and not prominent enough
