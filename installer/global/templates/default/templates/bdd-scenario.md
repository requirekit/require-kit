---
id: BDD-XXX
requirement: REQ-XXX
epic: EPIC-XXX
feature: FEAT-XXX
status: draft | ready | automated | deprecated
priority: critical | high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: [Author Name]
---

# Feature: [Feature Name]

## Description
[Brief description of the feature's purpose and value]

## Acceptance Criteria
[High-level acceptance criteria from stakeholder perspective]

## Background
```gherkin
Background:
  Given [common setup for all scenarios]
  And [additional common context]
  And [test data initialization]
```

## Scenarios

### Happy Path

```gherkin
@requirement-REQ-XXX @happy-path @smoke
Scenario: [Primary success scenario]
  Given [initial context/state]
  When [user action or event]
  Then [expected primary outcome]
  And [additional expected results]
```

### Edge Cases

```gherkin
@edge-case @boundary
Scenario: [Boundary condition description]
  Given [edge case setup]
  When [boundary action]
  Then [boundary behavior]
```

```gherkin
@edge-case @limits
Scenario: [System limits test]
  Given [setup at system limits]
  When [action at limits]
  Then [expected limit behavior]
```

### Error Handling

```gherkin
@error @validation
Scenario: [Input validation error]
  Given [setup for invalid input]
  When [invalid input provided]
  Then [validation error displayed]
  And [system remains stable]
```

```gherkin
@error @recovery
Scenario: [Error recovery]
  Given [setup that will fail]
  When [failure occurs]
  Then [graceful error handling]
  And [recovery mechanism activated]
```

### Performance

```gherkin
@performance @sla
Scenario: [Performance requirement]
  Given [performance test setup]
  When [action performed]
  Then [action completes within X seconds]
  And [resource usage within limits]
```

### Security

```gherkin
@security @authorization
Scenario: [Authorization check]
  Given [unauthorized user]
  When [attempts restricted action]
  Then [access denied]
  And [security event logged]
```

## Scenario Outline Examples

```gherkin
@validation @comprehensive
Scenario Outline: [Validation rules]
  Given a user on the [form] page
  When they enter "<value>" in "<field>"
  Then validation result should be "<result>"
  And message should be "<message>"

  Examples:
    | field    | value          | result  | message                |
    | email    | test@test.com  | valid   |                        |
    | email    | invalid        | invalid | Invalid email format   |
    | phone    | 1234567890     | valid   |                        |
    | phone    | 123            | invalid | Phone too short        |
    | password | Pass123!       | valid   |                        |
    | password | weak           | invalid | Password too weak      |
```

## Data Tables

```gherkin
@data-driven
Scenario: [Bulk operation]
  Given an admin user
  When they import data with:
    | field1 | field2 | field3 |
    | value1 | value2 | value3 |
    | value4 | value5 | value6 |
  Then 2 records should be created
  And all validations should pass
```

## Tags Used

- `@requirement-REQ-XXX` - Links to EARS requirement
- `@epic-EPIC-XXX` - Links to epic
- `@feature-FEAT-XXX` - Links to feature
- `@smoke` - Include in smoke test suite
- `@regression` - Include in regression suite
- `@happy-path` - Primary success flow
- `@edge-case` - Boundary conditions
- `@error` - Error handling
- `@performance` - Performance testing
- `@security` - Security testing
- `@wip` - Work in progress
- `@skip` - Skip this scenario

## Test Implementation

### Step Definitions
- Location: `tests/step-definitions/[feature].steps.ts`
- Shared steps: `tests/step-definitions/common.steps.ts`

### Test Data
- Fixtures: `tests/fixtures/[feature].fixtures.ts`
- Factories: `tests/factories/[model].factory.ts`

### Page Objects (UI Tests)
- Pages: `tests/pages/[page].page.ts`
- Components: `tests/components/[component].ts`

## Execution Notes

### Prerequisites
- [Required services running]
- [Test data requirements]
- [Environment configuration]

### Cleanup
- [Data cleanup requirements]
- [Service reset needs]

### Known Issues
- [Any flaky tests]
- [Environment-specific issues]

## Coverage Mapping

| Scenario | Unit Tests | Integration Tests | E2E Tests |
|----------|------------|-------------------|-----------|
| Happy path | ✅ | ✅ | ✅ |
| Validation | ✅ | ✅ | ❌ |
| Error handling | ✅ | ⚠️ | ❌ |
| Performance | ❌ | ✅ | ✅ |

## Review History

| Date | Reviewer | Comments |
|------|----------|----------|
| YYYY-MM-DD | [Name] | [Review comments] |

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| YYYY-MM-DD | Initial scenarios | Requirement implementation |
| YYYY-MM-DD | Added edge cases | Test coverage improvement |
