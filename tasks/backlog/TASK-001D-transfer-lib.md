---
id: TASK-001D
title: "Transfer Implementation Library"
created: 2025-10-19
status: backlog
priority: high
complexity: 5
parent_task: TASK-001
subtasks: []
estimated_hours: 3
---

# TASK-001D: Transfer Implementation Library

## Description

Copy installer/global/commands/lib/ directory, removing requirements-related modules while keeping all quality gate implementation (Phase 2.5, 4.5).

## Files to Transfer

### ✅ INCLUDE (Core Modules)

```python
# Phase 2.5, 2.6, 2.7 (Architectural Review & Checkpoints)
checkpoint_display.py
plan_persistence.py
plan_modifier.py
review_modes.py
user_interaction.py
upfront_complexity_adapter.py
plan_markdown_parser.py
plan_audit.py

# Phase 4.5 (Test Enforcement)
# (Implementation likely in task-manager or test-verifier agent)

# Task Management
git_state_helper.py
agent_utils.py
micro_task_workflow.py
version_manager.py
error_messages.py
visualization.py
spec_drift_detector.py

# Metrics
metrics/__init__.py
metrics/plan_audit_metrics.py

# Supporting
__init__.py
```

### ❌ EXCLUDE (Requirements Features)

```python
feature_generator.py  # Feature generation from epics
# Any other epic/feature/requirements modules
```

### Supporting Files to Copy

```bash
lib/MICRO_TASK_README.md
lib/QUICK_REVIEW_API.md
lib/README-CHECKPOINT-DISPLAY.md
lib/README-PLAN-MODIFIER.md
lib/README.md
lib/verify_micro_implementation.sh
```

## Implementation

```bash
cd ai-engineer/installer/global/commands

# Copy entire lib directory
cp -r lib/ ../../agentecflow/installer/global/commands/

cd ../../agentecflow/installer/global/commands/lib

# Remove requirements features
rm -f feature_generator.py
rm -f test_feature_generator.py  # if exists

# Remove any test files for requirements features
rm -f test_*ears*.py test_*bdd*.py test_*epic*.py test_*feature*.py
```

## Verification

```bash
cd agentecflow/installer/global/commands/lib

# Check imports (should not import removed modules)
grep -r "feature_generator" *.py
# Expected: EMPTY

grep -r "requirements" *.py | grep -v "# " | grep -v "acceptance"
# Should be EMPTY or only comments

# Test imports work
python3 -c "
import sys
sys.path.insert(0, '.')
from checkpoint_display import *
from plan_persistence import *
from review_modes import *
from git_state_helper import *
print('All imports successful')
"
```

## Acceptance Criteria

- [ ] lib/ directory copied
- [ ] feature_generator.py removed
- [ ] No broken imports
- [ ] All Phase 2.5, 4.5, 2.6, 2.7 modules present
- [ ] Python imports test passes
- [ ] No references to removed modules

## Estimated Time

3 hours
