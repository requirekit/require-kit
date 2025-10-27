---
id: TASK-030B-1.8
title: Document Feature 3.8 - MCP Tool Discovery
status: in_review
created: 2025-10-19T12:30:00Z
updated: 2025-10-19T13:50:00Z
completed: 2025-10-19T13:50:00Z
priority: high
parent_task: TASK-030B-1
tags: [documentation, agentecflow-lite, feature-deep-dive, tier-3]
estimated_effort: 15 minutes
actual_effort: 8 minutes
complexity_estimate: 1/10
dependencies: [TASK-030B-1.7]
blocks: [TASK-030B-1.9]
previous_state: backlog
state_transition_reason: "All quality gates passed - micro-task workflow"
workflow_mode: micro
phases_executed: [1, 3, 4, 4.5, 5]
phases_skipped: [2, 2.5A, 2.5B, 2.6, 2.7]
---

# Document Feature 3.8 - MCP Tool Discovery

## Parent Task
**TASK-030B-1**: Complete Part 3 - Feature Deep Dives (9 Features)

**Tier**: 3 (Advanced Features)
**Position**: Feature 8 of 9

## Context

Second feature in Tier 3. Maintains style from Features 1-7.

**Target file**: `docs/guides/agentecflow-lite-workflow.md`
**Insert location**: After Feature 3.7 content
**Content to add**: ~105 lines for Feature 3.8

## Description

Document the **MCP Tool Discovery** feature (Phase 2.8 extension) - automatic detection of available MCP tools and plan enhancement.

## Scope

### Key Topics to Cover

**Discovery Process**:
- Phase 2.8 scans for available MCP tools
- Detects Figma, Zeplin, Design Patterns, and other MCPs
- Enhances implementation plan with tool-specific capabilities
- Suggests appropriate commands for detected tools

**Supported Tools**:
- Figma (via @figma/mcp-server)
- Zeplin (via @zeplin/mcp-server)
- Design Patterns MCP
- Context7 documentation
- Custom MCP servers

**Plan Enhancement**:
- Adds tool capabilities to implementation plan
- Suggests integration commands
- Updates complexity score if tools reduce effort

**Real-World Example**:
- Show Figma MCP detected during planning
- Demonstrate plan enhancement with design-to-code suggestions
- Show automatic `/figma-to-react` command suggestion

## Acceptance Criteria

### Content Completeness
- [ ] 3-tier structure complete
- [ ] ~105 lines total (enhancement feature)
- [ ] Hubbard alignment: N/A (specialized workflow)
- [ ] Minimum 4 code examples
- [ ] Tool discovery process explained
- [ ] Supported tools table

### Quality Standards
- [ ] Matches Tier 3 style
- [ ] Cross-references to Design System Detection, Human Checkpoints
- [ ] Links to MCP server docs
- [ ] Parameters table for detected tools
- [ ] Troubleshooting table

## Implementation Notes

### Source Material

**Primary References**:
- `/task-work` command: `installer/global/commands/task-work.md` (Phase 2.8 MCP discovery)
- MCP documentation: Context7, Figma, Zeplin servers

### Discovery Example

```bash
Phase 2.8: MCP Tool Discovery

Detected MCP tools:
  ✅ Figma Dev Mode (@figma/mcp-server)
  ✅ Design Patterns (mcp__design-patterns)

Enhancing plan...

Suggested integrations:
  - Use /figma-to-react for component generation
  - Query design patterns for API resilience

Plan updated with tool capabilities.
```

## Success Metrics

- [ ] Feature 3.8 complete (~105 lines)
- [ ] Tier 3 style consistent
- [ ] Blocks TASK-030B-1.9

---

**Estimated Effort**: 15 minutes
**Complexity**: 1/10 (Simple - follows template)
**Risk**: Low
