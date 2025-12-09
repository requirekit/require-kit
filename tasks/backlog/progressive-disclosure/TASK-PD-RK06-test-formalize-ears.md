---
id: TASK-PD-RK06
title: Test /formalize-ears with split files
status: backlog
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T11:00:00Z
priority: medium
tags: [progressive-disclosure, testing, wave-3]
task_type: implementation
complexity: 2
execution_mode: direct
wave: 3
conductor_workspace: progressive-disclosure-test-ears
parallel: true
blocking: false
parent_review: TASK-REV-PD01
depends_on: [TASK-PD-RK04]
---

# Task: Test /formalize-ears with split files

## Description

Verify that the `/formalize-ears` command works correctly after splitting `requirements-analyst.md` into core and extended files. Ensure no regression in EARS formalization quality.

## Execution Mode

**Direct Claude Code** - Manual testing, no code generation needed.

## Conductor Parallel Execution

```bash
conductor create progressive-disclosure-test-ears
# In workspace: Execute test scenarios
```

Can be executed in parallel with TASK-PD-RK05.

## Test Scenarios

### Test 1: Event-Driven Requirement

**Input** (natural language):
```
When a user clicks the submit button, the form should be validated and saved
```

**Expected EARS Output**:
```
WHEN user clicks submit button, the system SHALL validate form data AND save to database
```

**Verify**:
- Uses correct EARS pattern (Event-Driven)
- Measurable outcome stated
- Clear trigger identified

### Test 2: State-Driven Requirement

**Input** (natural language):
```
The dashboard should show real-time updates while the user is logged in
```

**Expected EARS Output**:
```
WHILE user is authenticated, the system SHALL display real-time dashboard updates
```

**Verify**:
- Uses correct EARS pattern (State-Driven)
- State condition clearly defined
- Continuous behavior captured

### Test 3: Unwanted Behavior Requirement

**Input** (natural language):
```
If the database connection fails, retry 3 times then show error message
```

**Expected EARS Output**:
```
IF database connection fails, THEN the system SHALL retry connection 3 times AND display error message to user
```

**Verify**:
- Uses correct EARS pattern (Unwanted Behavior)
- Recovery action specified
- Error handling clear

### Test 4: Vague Requirement Clarification

**Input** (vague):
```
The system should be fast
```

**Expected Behavior**:
- Agent asks for specific metrics (ASK boundary triggered)
- Requests measurable criteria (e.g., "< 200ms response time")
- Does not accept vague term as-is

### Test 5: Extended Content Loading

**Test**: Verify extended content loads for detailed gathering processes.

**Steps**:
1. Request detailed requirements gathering process
2. Verify Claude loads `requirements-analyst-ext.md` when needed
3. Confirm domain-specific patterns are available

## Acceptance Criteria

- [ ] All 5 EARS patterns correctly identified and applied
- [ ] Vague terms trigger clarification requests (not accepted as-is)
- [ ] Extended content loads when detailed processes needed
- [ ] No quality regression compared to pre-split output
- [ ] Loading instruction in core file is clear and actionable
- [ ] Acceptance criteria included in output

## Validation Checklist

After running each test:
- [ ] EARS pattern correctly identified
- [ ] Requirement is atomic (single behavior)
- [ ] Measurable criteria present
- [ ] Trigger/state clearly defined
- [ ] Traceability maintained (epic/feature links if applicable)

## Files to Verify

- `installer/global/agents/requirements-analyst.md` (core file works standalone)
- `installer/global/agents/requirements-analyst-ext.md` (extended loads when needed)

## Dependencies

- TASK-PD-RK04 (Split requirements-analyst.md)

## Estimated Effort

30 minutes

## Notes

All 5 EARS patterns should be available from the core file. Extended content is only needed for detailed gathering processes, question templates, and domain-specific patterns.
