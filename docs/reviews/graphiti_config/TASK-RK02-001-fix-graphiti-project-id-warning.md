---
complexity: 1
dependencies: []
feature_id: standalone
id: TASK-RK02-001
implementation_mode: direct
priority: low
status: backlog
tags:
  - graphiti
  - config
  - housekeeping
task_type: config
title: Add explicit project_id to RequireKit Graphiti config
wave: 1
---

# Task: Add Explicit project_id to RequireKit Graphiti Config

## Description

During FEAT-498F execution, every task emits the warning:

```
WARNING:guardkit.knowledge.graphiti_client:No explicit project_id in config,
auto-detected 'require-kit' from cwd. Set project_id in .guardkit/graphiti.yaml
for consistent behavior.
```

This fires 14 times per feature run (once per task) because the RequireKit repo has no `.guardkit/graphiti.yaml` with an explicit `project_id`. The Graphiti client falls back to inferring the project name from the current working directory, which works but is fragile (rename the directory and the project_id changes silently, breaking graph continuity).

## Origin

Review TASK-REV-A515 Finding #7 (P4 — Config).

## Files to Create

- `.guardkit/graphiti.yaml` — Project-level Graphiti configuration for the require-kit repo

## Changes Required

1. **Create `.guardkit/graphiti.yaml`** in the require-kit repo root:
   ```yaml
   # RequireKit — GuardKit Graphiti Configuration
   # Silences the "No explicit project_id" warning and ensures
   # consistent graph identity regardless of working directory name.
   project_id: require-kit
   ```

2. **Verify no `.gitignore` exclusion** — confirm `.guardkit/graphiti.yaml` is tracked by git (the `.guardkit/` directory already contains tracked files like `features/` and `bootstrap_state.json`, so this should be fine).

## Acceptance Criteria

- [ ] `.guardkit/graphiti.yaml` exists with `project_id: require-kit`
- [ ] Running `guardkit autobuild` on any task in the require-kit repo no longer emits the `No explicit project_id in config` warning
- [ ] The file is committed to the repo (not gitignored)
- [ ] Existing Graphiti graph data (if any) remains accessible under the same `require-kit` project scope

## Test Requirements

- [ ] YAML parses correctly (`python -c "import yaml; yaml.safe_load(open('.guardkit/graphiti.yaml'))"`)
- [ ] `project_id` value matches the auto-detected value (`require-kit`) to avoid breaking any existing graph data

## Notes

- This is a one-line config fix. The auto-detection already infers `require-kit` correctly, so setting it explicitly just makes the behaviour deterministic and silences 14 warnings per feature run.
- The same fix should be applied to any other repos that exhibit this warning (e.g. guardkit itself, gcse-english-tutor, etc.) but those are out of scope for this task.
- The `installer/global/config/graphiti.yaml` template (RequireKit's own Graphiti integration config) is a separate concern — that controls whether RequireKit pushes requirements data to Graphiti. This task is about the GuardKit-level project config that controls AutoBuild's knowledge graph integration.
