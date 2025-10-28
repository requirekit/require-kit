---
id: REQ-002C
title: "Delete Stack Templates and Library"
created: 2025-10-27
status: backlog
priority: high
complexity: 4
parent_task: REQ-002
subtasks: []
estimated_hours: 1
---

# REQ-002C: Delete Stack Templates and Library

## Description

Delete all stack templates and task execution library modules, keeping only requirements-related code.

## Templates to DELETE (ALL)

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/templates/

# Delete ALL stack templates
rm -rf react/
rm -rf python/
rm -rf typescript-api/
rm -rf maui-appshell/
rm -rf maui-navigationpage/
rm -rf dotnet-microservice/
rm -rf fullstack/
rm -rf default/

# Verify templates directory is empty
ls -la
```

## Library Modules to DELETE

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/lib/

# Option 1: Delete entire lib/ directory if fully task-focused
cd ..
rm -rf lib/

# Option 2: Selective deletion if some requirements modules exist
cd lib/

# Delete quality gate modules
rm -f checkpoint_display.py
rm -f plan_persistence.py
rm -f plan_modifier.py
rm -f review_modes.py
rm -f upfront_complexity_adapter.py
rm -f plan_audit.py
rm -f plan_markdown_parser.py
rm -f spec_drift_detector.py

# Delete task execution modules
rm -f git_state_helper.py
rm -f agent_utils.py
rm -f micro_task_workflow.py
rm -f user_interaction.py
rm -f version_manager.py
rm -f error_messages.py
rm -f visualization.py

# Delete metrics (if task-focused)
rm -rf metrics/

# Keep ONLY if requirements-specific
# - feature_generator.py (if exists)
# - Any epic/feature management utilities
```

## Implementation

```bash
# Delete templates
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/templates/
rm -rf react/ python/ typescript-api/ maui-appshell/ maui-navigationpage/ dotnet-microservice/ fullstack/ default/

# Verify empty
echo "Templates directory after deletion:"
ls -la

# Delete library (entire directory - simpler approach)
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/
rm -rf lib/

# Verify lib is gone
ls -la | grep lib
# Should return EMPTY
```

## Alternative: Keep lib/ for Requirements Utilities

If we need to keep some utilities:

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/commands/lib/

# Review files first
ls -la *.py

# Delete task execution files
rm -f checkpoint_display.py plan_persistence.py plan_modifier.py review_modes.py
rm -f upfront_complexity_adapter.py plan_audit.py plan_markdown_parser.py
rm -f git_state_helper.py agent_utils.py micro_task_workflow.py
rm -f user_interaction.py version_manager.py error_messages.py
rm -f visualization.py spec_drift_detector.py

# Delete test files
rm -f test_*.py

# Delete metrics
rm -rf metrics/

# Keep ONLY requirements utilities (if any exist)
# List what remains
ls -la
```

## Verification

```bash
# Verify templates deleted
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/installer/global/
ls -la templates/
# Should show empty directory or no directory

# Verify lib deleted or cleaned
ls -la commands/lib/ 2>/dev/null || echo "lib/ directory removed (expected)"

# If lib exists, verify only requirements utilities remain
if [ -d "commands/lib" ]; then
  ls -la commands/lib/*.py
  # Should show ONLY requirements-specific files (if any)
fi
```

## Acceptance Criteria

- [ ] All stack templates deleted (8 templates)
- [ ] templates/ directory is empty or removed
- [ ] lib/ directory deleted OR cleaned of task execution modules
- [ ] No checkpoint, plan, review, complexity modules
- [ ] No task execution utilities
- [ ] Only requirements utilities remain (if applicable)
- [ ] Verification tests pass

## Estimated Time

1 hour

## Notes

- **Recommended**: Delete entire lib/ and templates/ directories
- Simpler to delete everything than selective deletion
- Can rebuild requirements utilities later if needed
- Commit after verification
