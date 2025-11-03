---
id: TASK-036
title: Update GitHub README Badges to Show Both Packages Separately
status: completed
created: 2025-11-03T10:30:00Z
updated: 2025-11-03T11:32:25Z
previous_state: in_review
state_transition_reason: "Task approved and completed via /task-complete"
completed_at: "2025-11-03T11:32:25Z"
completed_location: "tasks/completed/TASK-036/"
organized_files: ["TASK-036-update-github-readme-badges.md", "validate-task-036.py"]
actual_duration_minutes: 42
priority: medium
tags: [documentation, github, badges, require-kit, taskwright, branding]
epic: null
feature: null
requirements: []
bdd_scenarios: []
estimated_time: 1-2 hours
auto_approved: true
approved_by: "system"
approved_at: "2025-11-03T11:20:28Z"
review_mode: "auto_proceed"
implementation_plan:
  file_path: "docs/state/TASK-036/implementation_plan.json"
  generated_at: "2025-11-03T11:15:00Z"
  version: 1
  approved: true
complexity_evaluation:
  score: 2
  level: "low"
  file_path: "docs/state/TASK-036/complexity_score.json"
  calculated_at: "2025-11-03T11:15:00Z"
  review_mode: "auto_proceed"
  forced_review_triggers: []
  factors:
    file_complexity: 0.5
    pattern_familiarity: 0
    risk_level: 0.5
    dependency_complexity: 1
plan_audit:
  audit_file: "docs/state/TASK-036/plan_audit_report.json"
  audited_at: "2025-11-03T11:25:00Z"
  severity: "high"
  decision: "approve"
  decided_by: "system"
  extra_files: 1
  loc_variance_pct: 255.0
  outcome: "approved_with_audit_notes"
test_results:
  status: passed
  validation_checks: 15
  passed: 15
  failed: 0
  pass_rate: "100%"
  last_run: "2025-11-03T11:23:00Z"
---

# Task: Update GitHub README Badges to Show Both Packages Separately

## Description

Update the GitHub README files for both require-kit and taskwright repositories to display separate badges that clearly communicate:
1. Each package is standalone
2. They have optional bidirectional integration
3. Clear status indicators for each package independently

This task ensures users immediately understand the package separation and optional nature of integration.

## Context

Following the split of the monolithic ai-engineer repository into:
- **require-kit**: Requirements management toolkit (EARS, BDD, Epic/Feature hierarchy)
- **taskwright**: Task execution workflow system (TDD, quality gates, testing)

The GitHub READMEs need to reflect this new architecture with proper badges that communicate:
- Independence of each package
- Optional integration model
- Current status/version of each package

## Acceptance Criteria

### 1. require-kit README Badges

- [ ] Add package-specific badges:
  - Version badge (shields.io format)
  - License badge (MIT)
  - Build/CI status (if applicable)
  - "Standalone" badge indicating no dependencies
- [ ] Add integration section badges:
  - "Optional Integration: taskwright" badge with link
  - "Bidirectional Detection" badge explaining automatic detection
- [ ] Remove any old "ai-engineer" or monolithic badges
- [ ] Update badge placement (top of README after title)

### 2. taskwright README Badges

- [ ] Add package-specific badges:
  - Version badge (shields.io format)
  - License badge (MIT)
  - Build/CI status (if applicable)
  - "Standalone" badge indicating no dependencies
- [ ] Add integration section badges:
  - "Optional Integration: require-kit" badge with link
  - "Bidirectional Detection" badge explaining automatic detection
- [ ] Remove any old "ai-engineer" or monolithic badges
- [ ] Update badge placement (top of README after title)

### 3. Badge Consistency

- [ ] Use consistent color scheme across both repos:
  - require-kit primary color: Blue (#0366d6)
  - taskwright primary color: Green (#28a745)
  - Optional integration: Yellow (#ffd33d)
  - Standalone: Purple (#6f42c1)
- [ ] Use shields.io format for all badges
- [ ] Ensure badge links are functional and point to correct locations

### 4. README Integration Section

- [ ] Add "Package Status" section near top showing:
  ```markdown
  ## Package Status

  ![Standalone](badge) ![Version](badge) ![License](badge)

  **require-kit** is a standalone requirements management toolkit.
  No dependencies required. Optionally integrates with taskwright.
  ```
- [ ] Link to integration documentation (TASK-037)
- [ ] Show example of checking installed packages:
  ```bash
  ls ~/.agentecflow/*.marker
  ```

### 5. Documentation Updates

- [ ] Update main README.md in both repos
- [ ] Update CLAUDE.md in both repos (if references badges)
- [ ] Ensure consistency with updated documentation from boundary review

## Badge Examples

### require-kit Badges
```markdown
# require-kit

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Standalone](https://img.shields.io/badge/standalone-no%20dependencies-purple)
![Optional Integration](https://img.shields.io/badge/integration-taskwright%20optional-yellow)

**Requirements Management Toolkit** - EARS notation, BDD scenarios, Epic/Feature hierarchy
```

### taskwright Badges
```markdown
# taskwright

![Version](https://img.shields.io/badge/version-2.0.0-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Standalone](https://img.shields.io/badge/standalone-no%20dependencies-purple)
![Optional Integration](https://img.shields.io/badge/integration-require--kit%20optional-yellow)

**Task Execution Workflow** - TDD/BDD modes, quality gates, automated testing
```

## Implementation Notes

### Badge Creation Resources
- **shields.io**: https://shields.io/
- **Badge format**: `https://img.shields.io/badge/{label}-{message}-{color}`
- **Custom badges**: Use `-` for spaces, `--` for hyphens in message

### Color Scheme Rationale
- **Blue (require-kit)**: Associated with documentation/requirements
- **Green (taskwright)**: Associated with execution/testing/success
- **Purple (standalone)**: Unique color to highlight independence
- **Yellow (optional)**: Warning/attention color for "optional" integration

### Cross-Repository Consistency
- Ensure badge order is consistent across both repos
- Use same badge text (except package names)
- Link badges to appropriate documentation sections

## Testing Checklist

- [ ] All badge links are functional
- [ ] Badges render correctly on GitHub
- [ ] Mobile view displays badges properly
- [ ] Badges are accessible (alt text if applicable)
- [ ] Links from badges go to correct sections/repos
- [ ] Color scheme is consistent across both repos

## Related Tasks

- **TASK-037**: Create integration guide (linked from badges)
- **Boundary Review**: Documentation updates completed

## Files to Update

### require-kit Repository
- `README.md` (main badges section)
- `CLAUDE.md` (if badge references exist)

### taskwright Repository
- `README.md` (main badges section)
- `CLAUDE.md` (if badge references exist)

## Success Criteria

- ✅ Both READMEs show clear standalone status
- ✅ Optional integration is prominently displayed
- ✅ Badges are visually consistent
- ✅ Users can immediately understand package independence
- ✅ Links to integration documentation work
- ✅ No references to old monolithic "ai-engineer" badges

## Notes

- Keep badges above the fold (visible without scrolling)
- Ensure badges don't clutter the README
- Consider adding "Getting Started" badge linking to quick start
- May want to add npm/pip badges if packages are published to registries in future
