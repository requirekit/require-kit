---
id: TASK-XXX
title: [Task Title]
type: feature | bug | chore | spike
status: todo | in-progress | review | testing | done | blocked
priority: critical | high | medium | low
points: [Story Points]
epic: EPIC-XXX
feature: FEAT-XXX
assignee: [Developer Name]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sprint: [Sprint Number]
---

# Task: [Descriptive Task Title]

## Description

[Clear description of what needs to be done and why]

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] All related EARS requirements implemented
- [ ] All BDD scenarios passing
- [ ] Code review approved
- [ ] Documentation updated

## Requirements

### EARS Requirements
- [REQ-XXX](../requirements/REQ-XXX.md): [Requirement summary]
- [REQ-YYY](../requirements/REQ-YYY.md): [Requirement summary]

### BDD Scenarios
- [BDD-XXX](../bdd/features/feature.feature): [Scenario summary]
- [BDD-YYY](../bdd/features/feature.feature): [Scenario summary]

## Technical Details

### Implementation Approach
[High-level technical approach]

### Components Affected
- `src/[module]/[component].ts`
- `src/[module]/[service].ts`
- `api/[endpoint].ts`

### Database Changes
- [ ] Schema migration required
- [ ] Data migration required
- Tables affected: [list tables]

### API Changes
- [ ] New endpoints
- [ ] Modified endpoints
- [ ] Breaking changes
- [ ] Documentation updates

## Dependencies

### Blocked By
- [TASK-YYY]: [Why this blocks]

### Blocks
- [TASK-ZZZ]: [What this blocks]

### External Dependencies
- [Third-party service]
- [External API]
- [Library upgrade]

## Testing Plan

### Unit Tests
- [ ] Test file: `tests/unit/[component].test.ts`
- [ ] Coverage target: ≥80%
- [ ] Key test cases:
  - [Test case 1]
  - [Test case 2]

### Integration Tests
- [ ] Test file: `tests/integration/[feature].test.ts`
- [ ] API endpoints tested
- [ ] Database interactions tested

### E2E Tests
- [ ] Test file: `tests/e2e/[journey].spec.ts`
- [ ] User journey covered
- [ ] Critical path tested

### BDD Tests
- [ ] All scenarios automated
- [ ] Step definitions implemented
- [ ] Test data prepared

## Definition of Done

- [ ] Code complete and functioning
- [ ] All EARS requirements satisfied
- [ ] All BDD scenarios passing
- [ ] Unit test coverage ≥80%
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No high/critical security issues
- [ ] Performance benchmarks met
- [ ] Deployed to staging environment
- [ ] Product owner acceptance

## Effort Breakdown

| Activity | Estimated Hours | Actual Hours |
|----------|----------------|--------------|
| Analysis | 2 | |
| Design | 2 | |
| Implementation | 8 | |
| Testing | 4 | |
| Documentation | 1 | |
| Review & Fixes | 2 | |
| **Total** | **19** | |

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk description] | L/M/H | L/M/H | [Mitigation plan] |

## Notes

### Implementation Notes
[Technical notes for implementation]

### Review Comments
[Comments from code review]

### Blockers Encountered
[Any blockers and how they were resolved]

## Progress Updates

### YYYY-MM-DD
- Status: Started implementation
- Progress: 25%
- Notes: [Any relevant notes]

### YYYY-MM-DD
- Status: Implementation complete, testing started
- Progress: 60%
- Notes: [Any relevant notes]

### YYYY-MM-DD
- Status: In review
- Progress: 90%
- Notes: [Review feedback to address]

## Checklist Before Closing

- [ ] All acceptance criteria met
- [ ] Tests passing in CI/CD
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Sprint demo prepared
- [ ] Stakeholders notified

## Related Links

- [GitHub Issue](https://github.com/org/repo/issues/XXX)
- [Pull Request](https://github.com/org/repo/pull/XXX)
- [Design Document](link-to-design)
- [API Documentation](link-to-api-docs)
- [Confluence Page](link-to-confluence)

## Retrospective Notes

[After completion, what went well, what could be improved]

### What Went Well
- [Positive point 1]
- [Positive point 2]

### What Could Be Improved
- [Improvement area 1]
- [Improvement area 2]

### Lessons Learned
- [Lesson 1]
- [Lesson 2]
