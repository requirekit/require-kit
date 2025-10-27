---
id: TASK-021
title: Implement Requirement Versioning System with Refinement Command
status: backlog
priority: medium
created: 2025-10-16T10:50:00Z
labels: [enhancement, sdd-alignment, requirements, versioning]
estimated_effort: 8-10 hours
complexity_estimate: 6

# Source
source: spectrum-driven-development-analysis.md
recommendation: Priority 2 - Medium Impact, Medium Effort
sdd_alignment: Incremental Refinement

# Requirements
requirements:
  - REQ-SDD-010: Enable iterative requirement refinement
  - REQ-SDD-011: Track requirement version history
  - REQ-SDD-012: Link tasks to specific requirement versions
---

# Implement Requirement Versioning System with Refinement Command

## Problem Statement

No way to iteratively refine requirements after initial creation. Requirements are single-pass only, with no version tracking or refinement workflow.

## Solution Overview

Add `/refine-requirements` command that:
- Creates new requirement versions (v1, v2, v3, etc.)
- Tracks version history with diffs
- Links tasks to specific requirement versions
- Provides interactive refinement options

## Acceptance Criteria

### 1. Version Tracking
- [ ] Store requirement versions in JSON format
- [ ] Track: version number, created_at, created_by, content, changes
- [ ] Maintain version history file per requirement

### 2. Refinement Command
- [ ] `/refine-requirements REQ-XXX` command
- [ ] Load current version
- [ ] Interactive refinement options:
  - Add more detail
  - Simplify/reduce verbosity
  - Add acceptance criteria
  - Modify scenarios
  - View version history

### 3. Task Linkage
- [ ] Link tasks to specific requirement versions
- [ ] Display version in task frontmatter
- [ ] Use latest version for new tasks
- [ ] Preserve historical version links

### 4. Version History Display
- [ ] Show all versions with timestamps
- [ ] Display changes between versions
- [ ] Support rollback to previous versions
- [ ] Export version history

## Implementation Plan

### Phase 1: Version Data Model (2 hours)
```python
# File: installer/global/commands/lib/requirement_versioning.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class RequirementVersion:
    version: int
    created_at: str
    created_by: str
    content: str
    word_count: int
    tasks_linked: List[str]
    changes_from_previous: List[str]

@dataclass
class RequirementHistory:
    requirement_id: str
    current_version: int
    versions: List[RequirementVersion]

    def add_version(self, content: str, changes: List[str], author: str) -> RequirementVersion:
        """Add new version to history."""
        new_version = RequirementVersion(
            version=self.current_version + 1,
            created_at=datetime.utcnow().isoformat() + "Z",
            created_by=author,
            content=content,
            word_count=len(content.split()),
            tasks_linked=[],
            changes_from_previous=changes
        )
        self.versions.append(new_version)
        self.current_version += 1
        return new_version

    def get_version(self, version: int) -> RequirementVersion:
        """Get specific version."""
        return next((v for v in self.versions if v.version == version), None)

    def get_latest(self) -> RequirementVersion:
        """Get latest version."""
        return self.versions[-1]

    def rollback(self, version: int):
        """Rollback to previous version."""
        if version < self.current_version:
            self.current_version = version
```

### Phase 2: Refine Requirements Command (3 hours)
```markdown
# File: installer/global/commands/refine-requirements.md

# Refine Requirements Command

Iteratively refine an existing requirement with version tracking.

## Usage

```bash
/refine-requirements REQ-XXX
```

## Interactive Refinement Options

1. **Add more detail** - Increase specificity
2. **Simplify** - Reduce verbosity
3. **Add acceptance criteria** - Define success conditions
4. **Modify success/error scenarios** - Update behavior specs
5. **View version history** - See all versions and changes
6. **Rollback** - Revert to previous version

## Workflow

### Step 1: Load Current Version
```
Loading REQ-042 (current version: v1)...

Current Requirement (v1):
  When valid credentials submitted, system shall validate,
  generate JWT token, return token, and log event.

Word count: 18
Created: 2025-10-10T10:00:00Z
Tasks linked: None
```

### Step 2: Select Refinement Type
```
What would you like to refine?
1. Add more detail (increase specificity)
2. Simplify (reduce verbosity)
3. Add acceptance criteria
4. Modify success/error scenarios
5. View version history

Your choice: 1
```

### Step 3: Specify Changes
```
What aspect needs more detail?
> Token expiration policy

Refining requirement with additional detail...

Updated Requirement (v2):
  When valid credentials submitted, system shall:
  1. Validate against authentication service
  2. Generate JWT token with:
     - 24-hour expiration
     - User ID and role claims
     - HS256 signature algorithm
  3. Return token in response body
  4. Log authentication event with timestamp and IP

Word count: 47 (+29 from v1)
```

### Step 4: Review Changes
```
Changes from v1 → v2:
  + Added token expiration details (24h)
  + Added token claims (user ID, role)
  + Added signature algorithm (HS256)
  + Added logging details (timestamp, IP)

[A]pprove v2  [E]dit Further  [R]evert to v1  [C]ancel

Your choice: A
```

### Step 5: Update Links
```
✅ REQ-042 updated to v2
Version history saved: docs/requirements/approved/REQ-042-history.json
Tasks linked to REQ-042: TASK-001, TASK-002 (will use v2 for future work)
```
```

### Phase 3: Version History Storage (2 hours)
```python
# File: installer/global/commands/lib/requirement_storage.py

import json
from pathlib import Path

class RequirementStore:
    def __init__(self, base_path: str = "docs/requirements"):
        self.base_path = Path(base_path)

    def save_history(self, history: RequirementHistory):
        """Save requirement history to JSON."""
        history_file = self.base_path / "approved" / f"{history.requirement_id}-history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)

        with open(history_file, 'w') as f:
            json.dump({
                'requirement_id': history.requirement_id,
                'current_version': history.current_version,
                'versions': [
                    {
                        'version': v.version,
                        'created_at': v.created_at,
                        'created_by': v.created_by,
                        'content': v.content,
                        'word_count': v.word_count,
                        'tasks_linked': v.tasks_linked,
                        'changes_from_previous': v.changes_from_previous
                    }
                    for v in history.versions
                ]
            }, f, indent=2)

    def load_history(self, requirement_id: str) -> RequirementHistory:
        """Load requirement history from JSON."""
        history_file = self.base_path / "approved" / f"{requirement_id}-history.json"

        if not history_file.exists():
            # Create initial history from current requirement
            return self._create_initial_history(requirement_id)

        with open(history_file, 'r') as f:
            data = json.load(f)
            return RequirementHistory(
                requirement_id=data['requirement_id'],
                current_version=data['current_version'],
                versions=[
                    RequirementVersion(**v) for v in data['versions']
                ]
            )
```

### Phase 4: Task Linkage (2 hours)
```yaml
# File: tasks/backlog/TASK-XXX.md (frontmatter)

---
id: TASK-042
requirements:
  - id: REQ-042
    version: 2
    content_hash: "abc123..."
    linked_at: "2025-10-10T14:30:00Z"
---
```

```python
# File: installer/global/commands/lib/task_requirement_linker.py

def link_task_to_requirement(task_id: str, requirement_id: str, version: int):
    """Link task to specific requirement version."""

    # Load task
    task = load_task(task_id)

    # Update frontmatter
    task.frontmatter['requirements'] = task.frontmatter.get('requirements', [])
    task.frontmatter['requirements'].append({
        'id': requirement_id,
        'version': version,
        'linked_at': datetime.utcnow().isoformat() + "Z"
    })

    # Update requirement history
    history = RequirementStore().load_history(requirement_id)
    version_obj = history.get_version(version)
    if task_id not in version_obj.tasks_linked:
        version_obj.tasks_linked.append(task_id)
        RequirementStore().save_history(history)

    save_task(task)
```

### Phase 5: Testing (1 hour)
```python
# File: tests/integration/test_requirement_versioning.py

def test_requirement_refinement_workflow():
    # Create initial requirement
    req_id = "REQ-TEST-001"
    initial_content = "When user logs in, system shall authenticate"

    # Refine requirement (add detail)
    refined_content = """
    When user submits credentials, system shall:
    1. Validate credentials
    2. Generate JWT token
    3. Return token
    """
    changes = ["Added validation step", "Added token generation", "Added token return"]

    # Version 2 created
    history = refine_requirement(req_id, refined_content, changes)
    assert history.current_version == 2
    assert len(history.versions) == 2

    # Link task to v2
    link_task_to_requirement("TASK-001", req_id, 2)

    # Verify linkage
    task = load_task("TASK-001")
    assert task.frontmatter['requirements'][0]['version'] == 2

    # Verify task appears in version history
    history = RequirementStore().load_history(req_id)
    version_2 = history.get_version(2)
    assert "TASK-001" in version_2.tasks_linked
```

## Files to Create/Modify

### New Files
- `installer/global/commands/refine-requirements.md`
- `installer/global/commands/lib/requirement_versioning.py`
- `installer/global/commands/lib/requirement_storage.py`
- `installer/global/commands/lib/task_requirement_linker.py`
- `tests/unit/test_requirement_versioning.py`
- `tests/integration/test_requirement_versioning.py`

### Modified Files
- `installer/global/commands/task-create.md` (link to requirement versions)
- `installer/global/commands/formalize-ears.md` (initialize version 1)

## Example Version History

```json
{
  "requirement_id": "REQ-042",
  "current_version": 3,
  "versions": [
    {
      "version": 1,
      "created_at": "2025-10-10T10:00:00Z",
      "created_by": "human",
      "content": "When valid credentials submitted, system shall validate, generate JWT token, return token, and log event.",
      "word_count": 18,
      "tasks_linked": [],
      "changes_from_previous": ["Initial version"]
    },
    {
      "version": 2,
      "created_at": "2025-10-10T14:30:00Z",
      "created_by": "human",
      "content": "When valid credentials submitted, system shall: 1. Validate against authentication service 2. Generate JWT token with 24-hour expiration, user ID and role claims, HS256 signature 3. Return token in response 4. Log event with timestamp and IP",
      "word_count": 47,
      "tasks_linked": ["TASK-001", "TASK-002"],
      "changes_from_previous": [
        "Added token expiration details",
        "Added token claims specification",
        "Added signature algorithm",
        "Added logging details"
      ]
    },
    {
      "version": 3,
      "created_at": "2025-10-11T09:15:00Z",
      "created_by": "human",
      "content": "When valid credentials submitted, system shall: 1. Validate against authentication service with rate limiting (5 attempts/minute) 2. Generate JWT token with 24-hour expiration, user ID and role claims, HS256 signature 3. Return token in response 4. Log event with timestamp, IP, and user agent",
      "word_count": 55,
      "tasks_linked": ["TASK-003"],
      "changes_from_previous": [
        "Added rate limiting (5 attempts/minute)",
        "Added user agent to logging"
      ]
    }
  ]
}
```

## Success Metrics

- **Version Tracking**: 100% requirements have version history
- **Refinement Cycles**: Average 2-3 versions per requirement
- **Task Linkage Accuracy**: 100% tasks linked to correct versions
- **Developer Satisfaction**: Improved clarity from iterative refinement

## Related Tasks

- TASK-019: Concise Mode for EARS
- TASK-022: Spec Templates by Type

## Dependencies

- None (standalone enhancement)

## Notes

- Version history stored in JSON for easy parsing
- Automatic version increment on refinement
- Support rollback to any previous version
- Consider adding diff visualization between versions
