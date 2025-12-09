---
id: TASK-PD-RK02
title: Copy reusable scripts from GuardKit
status: completed
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T21:10:00Z
completed: 2025-12-09T21:10:00Z
priority: high
tags: [progressive-disclosure, setup, wave-1]
task_type: implementation
complexity: 2
execution_mode: direct
wave: 1
conductor_workspace: null
parallel: false
blocking: true
parent_review: TASK-REV-PD01
---

# Task: Copy reusable scripts from GuardKit

## Description

Copy the progressive disclosure infrastructure from GuardKit to RequireKit. These scripts handle the split-file architecture and can be reused with minimal modifications.

## Execution Mode

**Direct Claude Code** - File copying with minor path adjustments.

## Source Files (GuardKit)

```
guardkit/installer/global/lib/
├── agent_enhancement/
│   ├── models.py           # 100% reusable - AgentEnhancement, SplitContent dataclasses
│   ├── applier.py          # 90% reusable - needs path updates
│   └── boundary_utils.py   # 100% reusable - boundary section utilities
└── utils/
    └── file_io.py          # 100% reusable - safe file read/write
```

## Target Location (RequireKit)

```
require-kit/installer/global/lib/
├── agent_enhancement/
│   ├── __init__.py         # NEW - package init
│   ├── models.py           # COPY
│   ├── applier.py          # COPY + MODIFY
│   └── boundary_utils.py   # COPY
└── utils/
    ├── __init__.py         # NEW - package init
    └── file_io.py          # COPY
```

## Acceptance Criteria

- [x] Create directory structure `installer/global/lib/agent_enhancement/`
- [x] Create directory structure `installer/global/lib/utils/`
- [x] Copy `models.py` without modifications
- [x] Copy `boundary_utils.py` without modifications
- [x] Copy `file_io.py` without modifications
- [x] Copy `applier.py` with path modifications
- [x] Create `__init__.py` files for Python packages
- [x] Verify imports work correctly

## Implementation Steps

1. **Create directories**:
   ```bash
   mkdir -p installer/global/lib/agent_enhancement
   mkdir -p installer/global/lib/utils
   ```

2. **Copy models.py** (no changes):
   ```bash
   cp <guardkit>/installer/global/lib/agent_enhancement/models.py \
      installer/global/lib/agent_enhancement/
   ```

3. **Copy boundary_utils.py** (no changes):
   ```bash
   cp <guardkit>/installer/global/lib/agent_enhancement/boundary_utils.py \
      installer/global/lib/agent_enhancement/
   ```

4. **Copy file_io.py** (no changes):
   ```bash
   cp <guardkit>/installer/global/lib/utils/file_io.py \
      installer/global/lib/utils/
   ```

5. **Copy and modify applier.py**:
   - Update `_format_loading_instruction()` method
   - Change footer text from "GuardKit" to "RequireKit"
   - Update agent path references

6. **Create __init__.py files**:
   ```python
   # installer/global/lib/agent_enhancement/__init__.py
   from .models import AgentEnhancement, SplitContent, EnhancementResult
   from .applier import EnhancementApplier

   # installer/global/lib/utils/__init__.py
   from .file_io import safe_read_file, safe_write_file
   ```

## Modifications to applier.py

### Update loading instruction (line ~705):
```python
def _format_loading_instruction(self, agent_name: str) -> str:
    return f"""## Extended Documentation

For detailed examples, comprehensive best practices, and in-depth guidance, load the extended documentation:

```bash
cat agents/{agent_name}-ext.md
```

The extended file contains:
- Detailed code examples with explanations
- Framework-specific step definitions
- Common anti-patterns and how to avoid them
- Cross-stack considerations
- Troubleshooting guides

*Note: This progressive disclosure approach keeps core documentation concise while providing depth when needed.*"""
```

### Update footer (line ~685):
```python
lines.append("*This extended documentation is part of RequireKit's progressive disclosure system.*")
```

## Dependencies

None - this is a prerequisite task.

## Blocks

- TASK-PD-RK03 (Split bdd-generator.md)
- TASK-PD-RK04 (Split requirements-analyst.md)

## Estimated Effort

15 minutes

## Notes

The scripts are intentionally copied rather than shared via a common package to maintain independence between GuardKit and RequireKit repositories. Each can evolve independently while sharing the same initial implementation.
