---
id: TASK-040B
title: Rename taskwright to guardkit in guardkit repo
status: completed
completed: 2025-12-03T12:00:00Z
completion_note: Not needed - work completed as part of TASK-040A
created: 2025-12-03T11:00:00Z
updated: 2025-12-03T11:00:00Z
priority: high
tags: [refactoring, branding, rename, guardkit]
task_type: implementation
complexity: 5
parent_task: TASK-040
related_tasks: [TASK-040A, TASK-040C]
external_repo: true
---

# Task: Rename taskwright to guardkit in guardkit repo

## Description

Update all references from 'taskwright' to 'guardkit' within the guardkit repository (formerly taskwright). This is part of a coordinated rename across both packages.

**Note**: This task is tracked here for coordination but must be executed in the guardkit repository.

## Scope

**guardkit repo only** (external to require-kit)

### Expected Changes

#### 1. Package Identity

- Package name in all configs
- Marker file name created during install: `guardkit.marker.json`
- Repository references

#### 2. Runtime Code

- `installer/global/lib/feature_detection.py` - MUST match require-kit version
  - Function names
  - Marker file detection
  - Package name strings

#### 3. Documentation

- README.md
- CLAUDE.md
- All command specifications
- Integration guides

#### 4. Installer Scripts

- `install.sh` - creates `guardkit.marker.json`
- `uninstall.sh` - removes `guardkit.marker.json`

## Acceptance Criteria

- [ ] Package installs as `guardkit`
- [ ] Creates `~/.agentecflow/guardkit.marker.json` on install
- [ ] `feature_detection.py` matches require-kit version exactly
- [ ] All internal references updated
- [ ] GitHub repo URL updated (if applicable)

## Coordination Notes

### Sync with TASK-040A

The `feature_detection.py` file is **shared between both repos**. It MUST be identical after both tasks complete.

**Critical**: The header comment in this file lists both repo paths:
```python
# This file is duplicated across multiple repositories:
#   • taskwright/installer/global/lib/feature_detection.py  # UPDATE THIS PATH
#   • require-kit/installer/global/lib/feature_detection.py
```

After rename, this should read:
```python
# This file is duplicated across multiple repositories:
#   • guardkit/installer/global/lib/feature_detection.py
#   • require-kit/installer/global/lib/feature_detection.py
```

### Execution Order

1. TASK-040A (require-kit) and TASK-040B (guardkit) can run **in parallel**
2. Both must complete before TASK-040C
3. After both complete, test cross-repo detection

## External Execution

To execute this task:

```bash
cd /path/to/guardkit  # (formerly taskwright)
# Create equivalent task file or work directly
# Apply same rename patterns as TASK-040A
```

## Verification

After both TASK-040A and TASK-040B complete:

```bash
# Fresh install of guardkit should create new marker
ls ~/.agentecflow/guardkit.marker.json

# require-kit should detect it
python3 -c "
import sys
sys.path.insert(0, '$HOME/.agentecflow/lib')
from feature_detection import is_guardkit_installed
print('Guardkit detected:', is_guardkit_installed())
"
```

## Next Steps

1. Open guardkit repository
2. Create equivalent implementation task
3. Execute rename in parallel with TASK-040A
4. Verify cross-repo detection works
5. Proceed to TASK-040C
