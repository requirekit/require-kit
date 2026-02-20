---
completed: '2026-02-19'
completed_location: tasks/completed/TASK-RK01-003/
complexity: 3
dependencies: []
feature_id: FEAT-RK-001
id: TASK-RK01-003
implementation_mode: direct
organized_files:
- TASK-RK01-003.md
parent_review: TASK-REV-RK01
previous_state: in_review
priority: normal
state_transition_reason: All quality gates passed - 18/18 tests passing, code review
  approved
status: completed
tags:
- graphiti
- config
- scaffolding
task_type: scaffolding
title: Create Graphiti configuration template
updated: '2026-02-19'
wave: 1
---

# Task: Create Graphiti Configuration Template

## Description

Create the Graphiti configuration template file that controls whether Graphiti integration is enabled. This is the config that refinement commands and sync check to determine standalone vs Graphiti mode.

## Files to Create

- `installer/global/config/graphiti.yaml` - Configuration template with defaults

## Changes Required

1. **Create Configuration Template**:
   ```yaml
   # RequireKit Graphiti Integration Configuration
   # Set enabled: true when Graphiti/Neo4j is available
   graphiti:
     enabled: false  # Default: off (standalone mode)
     endpoint: "bolt://localhost:7687"
     project_namespace: "my_project"
     group_id_pattern: "{project}__requirements"
     sync_on_create: true   # Auto-push on /epic-create and /feature-create
     sync_on_refine: true   # Auto-push after /epic-refine and /feature-refine
   ```

2. **Document Configuration Options**:
   - Each field with description and valid values
   - How to enable Graphiti integration
   - What happens in standalone mode (all commands work, just no Graphiti push)
   - Tip message for standalone users

## Acceptance Criteria

- [x] Config file exists at `installer/global/config/graphiti.yaml`
- [x] Default is `enabled: false` (standalone mode)
- [x] All fields documented with comments
- [x] Group ID pattern uses `{project}__requirements` convention from FEAT-RK-001 spec

## Test Requirements

- [x] Verify YAML parses correctly
- [x] Verify default values are sensible