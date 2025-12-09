---
id: TASK-PD-RK05
title: Test /generate-bdd with split files
status: completed
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T21:42:00Z
completed: 2025-12-09T21:30:00Z
completed_location: tasks/completed/TASK-PD-RK05/
organized_files: [TASK-PD-RK05.md]
priority: medium
tags: [progressive-disclosure, testing, wave-3]
task_type: implementation
complexity: 2
execution_mode: direct
wave: 3
conductor_workspace: progressive-disclosure-test-bdd
parallel: true
blocking: false
parent_review: TASK-REV-PD01
depends_on: [TASK-PD-RK03]
---

# Task: Test /generate-bdd with split files

## Description

Verify that the `/generate-bdd` command works correctly after splitting `bdd-generator.md` into core and extended files. Ensure no regression in BDD scenario generation quality.

## Execution Mode

**Direct Claude Code** - Manual testing, no code generation needed.

## Conductor Parallel Execution

```bash
conductor create progressive-disclosure-test-bdd
# In workspace: Execute test scenarios
```

Can be executed in parallel with TASK-PD-RK06.

## Test Scenarios

### Test 1: Simple EARS Conversion

**Input**:
```
WHEN user submits login form, system SHALL authenticate credentials
```

**Expected Output**:
- Gherkin scenario with Given/When/Then structure
- Correct mapping from EARS Event-Driven pattern
- Appropriate tags (@requirement-REQ-XXX, @happy-path)

### Test 2: Complex Multi-Scenario Feature

**Input**: An EARS requirement with error handling:
```
IF login fails 3 times, system SHALL lock account for 30 minutes
```

**Expected Output**:
- Error handling scenario with @error-handling tag
- Clear recovery steps
- Linked to requirement ID

### Test 3: Optional Feature Scenario

**Input**:
```
WHERE two-factor authentication is enabled, system SHALL require verification code
```

**Expected Output**:
- Scenario Outline testing both enabled and disabled states
- Examples table with 2FA variations
- @optional-feature tag

### Test 4: Extended Content Loading

**Test**: Verify extended content loads when explicitly requested.

**Steps**:
1. Run `/generate-bdd` with a request for pytest-bdd step definitions
2. Verify Claude loads `bdd-generator-ext.md` when needed
3. Confirm framework-specific examples are available

## Acceptance Criteria

- [x] Simple EARS-to-Gherkin conversion works correctly
- [x] Error handling scenarios generated properly
- [x] Optional feature scenarios use Scenario Outline
- [x] Extended content loads when explicitly needed
- [x] No quality regression compared to pre-split output
- [x] Loading instruction in core file is clear and actionable

## Validation Checklist

After running each test:
- [x] Gherkin syntax is valid
- [x] Tags are appropriate
- [x] Requirement links are maintained
- [x] Business language used (no implementation details)
- [x] Scenarios are independent

## Files to Verify

- `installer/global/agents/bdd-generator.md` (core file works standalone)
- `installer/global/agents/bdd-generator-ext.md` (extended loads when needed)

## Dependencies

- TASK-PD-RK03 (Split bdd-generator.md)

## Estimated Effort

30 minutes

## Notes

Focus on verifying that core functionality works with the split file. Extended content should only be needed for framework-specific step definitions and advanced techniques, not for basic EARS-to-Gherkin conversion.
