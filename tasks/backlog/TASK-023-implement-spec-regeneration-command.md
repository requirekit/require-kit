---
id: TASK-023
title: Implement Spec Regeneration Command (Spec-as-Source)
status: backlog
priority: low
created: 2025-10-16T11:00:00Z
labels: [enhancement, sdd-alignment, regeneration, spec-as-source]
estimated_effort: 16-20 hours
complexity_estimate: 8

# Source
source: spectrum-driven-development-analysis.md
recommendation: Priority 3 - High Impact, High Effort
sdd_alignment: Spec-as-Source

# Requirements
requirements:
  - REQ-SDD-016: Rebuild implementation from updated specs
  - REQ-SDD-017: Preserve manual customizations
  - REQ-SDD-018: True spec-as-source workflow
---

# Implement Spec Regeneration Command (Spec-as-Source)

## Problem Statement

No way to rebuild implementation from updated requirements. When requirements change (v1 → v2), developers must manually update code. This prevents true "spec-as-source" workflow.

## Solution Overview

Add `/regenerate TASK-XXX` command that:
- Rebuilds implementation from current requirement version
- Preserves manual customizations (annotated code)
- Runs full quality gates (arch review, tests, code review)
- Creates diff report showing changes
- Enables true spec-as-source development

## Acceptance Criteria

### 1. Regeneration Detection
- [ ] Detect requirement version changes (v1 → v2)
- [ ] Compare current implementation vs requirement version
- [ ] Identify manual customizations (code not in requirements)
- [ ] Generate regeneration strategy

### 2. Manual Preservation
- [ ] Annotate manual code with `[MANUAL]` tags
- [ ] Preserve manual code during regeneration
- [ ] Track manual code reasons and authors
- [ ] Warn if manual code conflicts with new requirements

### 3. Regeneration Workflow
- [ ] Phase 1: Load Context (task + current implementation)
- [ ] Phase 2: Implementation Planning (from new requirements)
- [ ] Phase 2.5: Architectural Review
- [ ] Phase 3: Implementation (preserve manual code)
- [ ] Phase 4: Testing
- [ ] Phase 4.5: Fix Loop
- [ ] Phase 5: Code Review

### 4. Diff Reporting
- [ ] Files modified count
- [ ] Lines added/removed/preserved
- [ ] New tests added
- [ ] Quality gate results
- [ ] Git diff command for review

## Implementation Plan

### Phase 1: Annotation System (4 hours)
```python
# File: installer/global/commands/lib/code_annotator.py

from dataclasses import dataclass
from typing import List
import re

@dataclass
class ManualAnnotation:
    file_path: str
    start_line: int
    end_line: int
    reason: str
    added_by: str
    added_at: str

class CodeAnnotator:
    GENERATED_TAG = "[GENERATED]"
    MANUAL_TAG = "[MANUAL]"

    def annotate_generated(self, code: str, requirement_id: str, version: int) -> str:
        """Annotate generated code with requirement reference."""
        lines = code.split('\n')
        annotated_lines = []

        for line in lines:
            if self._is_significant_line(line):
                annotated_lines.append(f"{line}  // {self.GENERATED_TAG} From {requirement_id} v{version}")
            else:
                annotated_lines.append(line)

        return '\n'.join(annotated_lines)

    def annotate_manual(self, code: str, reason: str, author: str) -> str:
        """Annotate manual code to preserve during regeneration."""
        return f"""
// {self.MANUAL_TAG} Added outside requirements
// {self.MANUAL_TAG}:REASON: {reason}
// {self.MANUAL_TAG}:ADDED: {author} at {datetime.utcnow().isoformat()}
{code}
// {self.MANUAL_TAG}:END
"""

    def extract_manual_sections(self, code: str) -> List[ManualAnnotation]:
        """Extract all manual code sections."""
        manual_sections = []
        in_manual_section = False
        section_start = None
        reason = None
        author = None

        for i, line in enumerate(code.split('\n')):
            if self.MANUAL_TAG in line:
                if "REASON:" in line:
                    reason = line.split("REASON:")[1].strip()
                elif "ADDED:" in line:
                    author = line.split("ADDED:")[1].strip()
                elif in_manual_section and "END" in line:
                    manual_sections.append(ManualAnnotation(
                        file_path="",  # Set by caller
                        start_line=section_start,
                        end_line=i,
                        reason=reason,
                        added_by=author,
                        added_at=""
                    ))
                    in_manual_section = False
                elif not in_manual_section:
                    in_manual_section = True
                    section_start = i

        return manual_sections
```

Example annotated code:
```csharp
// AuthService.cs
public class AuthService {
    // [GENERATED] From REQ-042 v2
    public string GenerateToken(User user) {
        var claims = new[] {
            new Claim("user_id", user.Id),    // [GENERATED] From REQ-042 v2
            new Claim("role", user.Role)      // [GENERATED] From REQ-042 v2
        };

        var token = new JwtSecurityToken(
            claims: claims,
            expires: DateTime.UtcNow.AddHours(24),  // [GENERATED] From REQ-042 v2
            signingCredentials: new SigningCredentials(
                new SymmetricSecurityKey(key),
                SecurityAlgorithms.HmacSha256  // [GENERATED] From REQ-042 v2
            )
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    // [MANUAL] Added outside requirements
    // [MANUAL]:REASON: Enables better UX for long sessions
    // [MANUAL]:ADDED: developer at 2025-10-10T14:30:00Z
    public string RefreshToken(string expiredToken) {
        // Validate expired token
        var principal = ValidateExpiredToken(expiredToken);

        // Generate new token with same claims
        return GenerateToken(principal.Identity.Name);
    }
    // [MANUAL]:END
}
```

### Phase 2: Regeneration Command (6 hours)
```markdown
# File: installer/global/commands/regenerate.md

# Regenerate Command

Rebuild task implementation from updated requirements.

## Usage

```bash
/regenerate TASK-XXX [--force] [--no-preserve]
```

## Flags

- `--force`: Skip confirmation prompts
- `--no-preserve`: Don't preserve manual customizations (regenerate from scratch)

## Workflow

### Step 1: Analyze Changes
```
Loading TASK-042...
  - Current state: COMPLETED
  - Requirements: REQ-042 (v2)
  - Last implementation: Oct 10, 2025

Analyzing requirement changes...
  REQ-042: v1 → v2 (Oct 10, 14:30)
  Changes:
    + Added token expiration details (24h)
    + Added token claims (user ID, role)
    + Added signature algorithm (HS256)
    + Added logging details (timestamp, IP)

Current implementation based on: REQ-042 v1
Regeneration will update to: REQ-042 v2
```

### Step 2: Identify Manual Customizations
```
Manual customizations detected:
  - AuthService.cs:67-76 (token refresh - not in requirements)
  - AuthController.cs:89-95 (rate limiting - not in requirements)

Regeneration strategy:
  1. Preserve manual customizations (annotate as manual)
  2. Rebuild from REQ-042 v2
  3. Run all quality gates (arch review, tests, code review)
  4. Create diff report
```

### Step 3: Confirm Regeneration
```
[P]roceed with Regeneration  [V]iew Diff Preview  [C]ancel

Your choice: P
```

### Step 4: Execute Regeneration
```
Regenerating TASK-042 from REQ-042 v2...

Phase 1: Load Context ✅
Phase 2: Implementation Planning ✅ (using REQ-042 v2)
Phase 2.5: Architectural Review ✅ (Score: 88/100)
Phase 3: Implementation ✅
  - Updated TokenConfig.cs (24h expiration)
  - Updated AuthService.cs (added claims: user ID, role)
  - Updated TokenGenerator.cs (HS256 signature)
  - Updated Logger.cs (added timestamp, IP)
  - Preserved: AuthService.cs:67-76 (manual - token refresh)
  - Preserved: AuthController.cs:89-95 (manual - rate limiting)
Phase 4: Testing ✅
  - All tests passing (18/18)
  - New tests added for claims validation
Phase 4.5: Fix Loop ✅ (no fixes needed)
Phase 5: Code Review ✅
```

### Step 5: Review Results
```
Regeneration complete!

Diff Report:
  Files modified: 4
  Lines added: 47
  Lines removed: 23
  Lines preserved (manual): 34
  New tests: 3
  Passing tests: 18/18 ✅

Task updated: REQ-042 v1 → REQ-042 v2
State: COMPLETED (regenerated)

Next steps:
  1. Review diff: git diff HEAD~1
  2. Test manually: npm test
  3. Deploy: /task-complete TASK-042 --stage-transition
```
```

### Phase 3: Preservation Logic (4 hours)
```python
# File: installer/global/commands/lib/manual_preservation.py

class ManualPreserver:
    def __init__(self, annotator: CodeAnnotator):
        self.annotator = annotator

    def preserve_manual_code(
        self,
        old_code: str,
        new_code: str,
        requirement_id: str,
        new_version: int
    ) -> str:
        """Preserve manual code during regeneration."""

        # Extract manual sections from old code
        manual_sections = self.annotator.extract_manual_sections(old_code)

        if not manual_sections:
            # No manual code to preserve
            return self.annotator.annotate_generated(new_code, requirement_id, new_version)

        # Merge manual sections into new code
        merged_code = new_code
        for section in manual_sections:
            # Find insertion point in new code
            insertion_point = self._find_insertion_point(merged_code, section)

            # Insert manual section
            merged_code = self._insert_at(merged_code, insertion_point, section.code)

        # Annotate generated portions
        return self.annotator.annotate_generated(merged_code, requirement_id, new_version)

    def _find_insertion_point(self, code: str, section: ManualAnnotation) -> int:
        """Find appropriate insertion point for manual code."""
        # Strategy: Try to maintain same relative position
        # If not possible, append to end of class/file
        pass

    def _insert_at(self, code: str, position: int, insertion: str) -> str:
        """Insert code at specified position."""
        lines = code.split('\n')
        lines.insert(position, insertion)
        return '\n'.join(lines)
```

### Phase 4: Diff Reporting (3 hours)
```python
# File: installer/global/commands/lib/regeneration_reporter.py

@dataclass
class RegenerationReport:
    task_id: str
    requirement_id: str
    old_version: int
    new_version: int
    files_modified: int
    lines_added: int
    lines_removed: int
    lines_preserved: int
    new_tests: int
    tests_passing: int
    tests_total: int

    def display(self):
        """Display regeneration report."""
        print(f"""
Regeneration complete!

Diff Report:
  Files modified: {self.files_modified}
  Lines added: {self.lines_added}
  Lines removed: {self.lines_removed}
  Lines preserved (manual): {self.lines_preserved}
  New tests: {self.new_tests}
  Passing tests: {self.tests_passing}/{self.tests_total} ✅

Task updated: {self.requirement_id} v{self.old_version} → v{self.new_version}
State: COMPLETED (regenerated)

Next steps:
  1. Review diff: git diff HEAD~1
  2. Test manually: npm test
  3. Deploy: /task-complete {self.task_id} --stage-transition
""")
```

### Phase 5: Integration with Task Manager (2 hours)
```markdown
# File: installer/global/agents/task-manager.md

## Regeneration Workflow (when /regenerate command used)

When regenerating task from updated requirements:

1. **Load Current Implementation**
   - Read all implementation files
   - Extract manual annotations
   - Identify requirement version used

2. **Load New Requirements**
   - Read updated requirement version
   - Compare with implementation version
   - Calculate diff

3. **Plan Regeneration**
   - Use new requirement version for planning
   - Identify where to preserve manual code
   - Generate preservation strategy

4. **Execute Phases**
   - Phase 1: Load Context
   - Phase 2: Planning (from new requirements)
   - Phase 2.5: Architectural Review
   - Phase 3: Implementation (with preservation)
   - Phase 4: Testing
   - Phase 4.5: Fix Loop
   - Phase 5: Code Review

5. **Report Results**
   - Display diff report
   - Save regeneration metadata
   - Update task frontmatter with new version
```

### Phase 6: Testing (1 hour)
```python
# File: tests/integration/test_regeneration.py

def test_full_regeneration_workflow():
    # Setup: Create task with REQ-042 v1
    task_id = "TASK-TEST-001"
    create_task_from_requirement(task_id, "REQ-042", version=1)

    # Implement task
    run_task_work(task_id)
    assert get_task_status(task_id) == "completed"

    # Add manual customization
    add_manual_code(task_id, "AuthService.cs", "RefreshToken method", "Better UX")

    # Update requirement to v2
    refine_requirement("REQ-042", "Add token claims")

    # Regenerate
    result = run_regenerate(task_id)

    # Verify
    assert result.new_version == 2
    assert result.lines_preserved > 0  # Manual code preserved
    assert result.tests_passing == result.tests_total  # All tests pass
    assert "RefreshToken" in read_file("AuthService.cs")  # Manual code still there
    assert "user_id" in read_file("AuthService.cs")  # New requirement implemented
```

## Files to Create/Modify

### New Files
- `installer/global/commands/regenerate.md`
- `installer/global/commands/lib/code_annotator.py`
- `installer/global/commands/lib/manual_preservation.py`
- `installer/global/commands/lib/regeneration_reporter.py`
- `tests/unit/test_code_annotator.py`
- `tests/unit/test_manual_preservation.py`
- `tests/integration/test_regeneration.py`

### Modified Files
- `installer/global/agents/task-manager.md` (add regeneration workflow)
- `installer/global/commands/task-work.md` (integrate annotation system)

## Success Metrics

- **Regeneration Accuracy**: 95%+ correct regeneration from specs
- **Manual Preservation**: 100% manual code preserved (no data loss)
- **Test Pass Rate**: 90%+ tests pass after regeneration
- **Time Savings**: 60-80% vs manual refactoring

## Related Tasks

- TASK-021: Requirement Versioning (dependency)
- TASK-018: Spec Drift Detection

## Dependencies

- TASK-021: Requirement Versioning (must be completed first)

## Notes

- This is the most complex enhancement (complexity 8/10)
- Requires careful testing to prevent data loss
- Manual code preservation is critical
- Consider splitting into 2 subtasks:
  1. TASK-023.1: Annotation & Preservation System (8 hours)
  2. TASK-023.2: Regeneration Command & Integration (8 hours)
