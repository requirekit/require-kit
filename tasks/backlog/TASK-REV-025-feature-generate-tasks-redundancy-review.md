---
id: TASK-REV-025
title: Review /feature-generate-tasks for Redundancy with guardkit's /feature-plan
status: completed
task_type: review
decision_required: true
created: 2025-12-09T12:00:00Z
updated: 2025-12-09T14:00:00Z
completed: 2025-12-09T14:00:00Z
priority: normal
tags: [architecture-review, command-redundancy, guardkit-integration, decision-point]
epic: null
feature: null
requirements: []
external_ids:
  epic_jira: null
  epic_linear: null
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: pending
  coverage: null
  last_run: null
review_results:
  decision: keep_both_complementary
  recommendation: Keep both commands - they serve different purposes
  effort_estimate: 0.5 days (documentation only)
  report_path: .claude/reviews/TASK-REV-025-feature-generate-tasks-review-report.md
---

# Task: Review /feature-generate-tasks for Redundancy with guardkit's /feature-plan

## Context

The `/feature-generate-tasks` command in require-kit may now be redundant given that guardkit has the `/feature-plan` command. This review task will analyze:

1. Whether the two commands serve overlapping purposes
2. If `/feature-generate-tasks` should be deprecated/deleted
3. What migration path (if any) is needed for existing users

## Background

### require-kit's /feature-generate-tasks

**Location**: `installer/global/commands/feature-generate-tasks.md`

**Purpose**: Auto-generate implementation task specifications from features

**Key Capabilities**:
- Generates task markdown files from feature requirements
- Applies complexity evaluation and automatic task breakdown
- Creates hierarchical task IDs (TASK-001.2.01)
- Links tasks to requirements, BDD scenarios, and acceptance criteria
- Exports task specifications to PM tools (Jira, Linear, GitHub, Azure DevOps)
- Provides complexity analysis (1-10 scale) with automatic breakdown for complex tasks
- Supports interactive mode for task review and customization

**Standalone Operation**: Works independently of guardkit. Creates task specification files that can be:
- Exported to PM tools for team collaboration
- Used as implementation blueprints in any development workflow
- Executed via guardkit's task workflow system (if installed)

### guardkit's /feature-plan

**Location**: guardkit repository (external)

**Purpose**: [Needs investigation - analyze what guardkit's /feature-plan command does]

**Key Questions**:
- Does `/feature-plan` generate task specifications?
- Does it support complexity evaluation?
- Does it create hierarchical task IDs?
- Does it export to PM tools?
- What is the intended workflow?

## Review Objectives

### 1. Feature Comparison

Compare the two commands across these dimensions:

| Feature | /feature-generate-tasks | /feature-plan |
|---------|------------------------|---------------|
| Task generation | ✅ Yes | ? |
| Complexity evaluation | ✅ Yes (1-10 scale) | ? |
| Auto-breakdown | ✅ Yes (complexity ≥ 7) | ? |
| Hierarchical IDs | ✅ Yes (TASK-001.2.01) | ? |
| PM tool export | ✅ Yes (Jira, Linear, etc.) | ? |
| Interactive mode | ✅ Yes | ? |
| BDD scenario linking | ✅ Yes | ? |
| Requirements linking | ✅ Yes | ? |

### 2. User Value Analysis

- Who uses `/feature-generate-tasks`?
- What workflow does it enable?
- Would removing it break any existing workflows?
- Is there a gap if we remove it?

### 3. Migration Path (if deleting)

If `/feature-generate-tasks` is redundant:
- What deprecation notice is needed?
- How do users migrate to `/feature-plan`?
- What documentation updates are required?
- Are there any feature gaps to address first?

## Analysis Tasks

- [ ] Read guardkit's `/feature-plan` command specification
- [ ] Document feature comparison table
- [ ] Identify unique capabilities of each command
- [ ] Assess user impact of removal
- [ ] Determine if commands complement each other vs duplicate
- [ ] Make recommendation: keep, deprecate, merge, or delete

## Acceptance Criteria

- [ ] Both commands fully documented and compared
- [ ] Clear recommendation made with justification
- [ ] If deleting: migration path documented
- [ ] If keeping: clarification of when to use each command

## Recommendation Options

### Option A: Delete /feature-generate-tasks
- **When**: If `/feature-plan` fully replaces functionality
- **Action**: Remove command, update docs, add deprecation notice
- **Risk**: Low if guardkit is always used with require-kit

### Option B: Keep Both (Complementary)
- **When**: If commands serve different purposes
- **Action**: Document when to use each
- **Risk**: User confusion about which to use

### Option C: Merge Functionality
- **When**: If each has unique valuable features
- **Action**: Consolidate into one command (likely in guardkit)
- **Risk**: Development effort required

### Option D: Deprecate with Timeline
- **When**: If replacement exists but migration time needed
- **Action**: Mark deprecated, provide migration path, remove after N releases
- **Risk**: Maintenance burden during transition

## Initial Hypothesis

Based on the context provided: **Likely Option A (Delete)**

Reasoning:
- require-kit focuses on requirements management (gathering, EARS, BDD)
- guardkit focuses on task execution and workflow
- Task generation from features logically belongs in guardkit
- Having both creates confusion and maintenance burden

This hypothesis should be validated by examining guardkit's `/feature-plan` command.

## Notes

- This review was triggered by user observation that the command may be redundant
- TASK-008 (completed) enhanced `/feature-generate-tasks` with complexity control
- Consider whether that enhancement work should migrate to guardkit if deleting
