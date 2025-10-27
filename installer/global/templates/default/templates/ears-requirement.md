---
id: REQ-XXX
title: [Requirement Title]
type: ubiquitous | event-driven | state-driven | unwanted | optional
priority: high | medium | low
status: draft | review | approved | implemented
epic: EPIC-XXX
feature: FEAT-XXX
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: [Author Name]
reviewers: []
---

# Requirement: [Short Descriptive Title]

## EARS Statement

[Write the formal EARS requirement here using appropriate pattern]

Examples:
- **Ubiquitous**: The [system] shall [behavior]
- **Event-Driven**: When [trigger], the [system] shall [response]
- **State-Driven**: While [state], the [system] shall [behavior]
- **Unwanted**: If [error], then the [system] shall [recovery]
- **Optional**: Where [feature], the [system] shall [behavior]

## Rationale

[Explain why this requirement exists and what problem it solves]

## Acceptance Criteria

- [ ] [Specific, measurable criterion 1]
- [ ] [Specific, measurable criterion 2]
- [ ] [Specific, measurable criterion 3]
- [ ] [Include timing, quantities, thresholds where applicable]

## Constraints

- [Technical constraints]
- [Business constraints]
- [Regulatory constraints]

## Assumptions

- [List assumptions made about the system or environment]
- [Document any dependencies on other systems]

## Non-Functional Requirements

- **Performance**: [Response time, throughput requirements]
- **Security**: [Authentication, authorization, encryption needs]
- **Scalability**: [User load, data volume expectations]
- **Reliability**: [Uptime, error rate requirements]

## Related Requirements

- [REQ-YYY]: [How this requirement relates]
- [REQ-ZZZ]: [Dependencies or conflicts]

## BDD Scenarios

- [BDD-XXX](../bdd/features/[feature].feature): [Scenario description]
- [BDD-YYY](../bdd/features/[feature].feature): [Scenario description]

## Test Coverage

- **Unit Tests**: `tests/unit/[test-file].test.ts`
- **Integration Tests**: `tests/integration/[test-file].test.ts`
- **E2E Tests**: `tests/e2e/[test-file].spec.ts`

## Implementation

- **Component**: `src/[module]/[component].ts`
- **API Endpoint**: `[METHOD] /api/[endpoint]`
- **Database**: [Tables/collections affected]

## Risks

- [Potential risks if requirement is not met]
- [Technical risks in implementation]
- [Business impact of failure]

## Notes

[Additional context, clarifications, or considerations]

## Review History

| Date | Reviewer | Status | Comments |
|------|----------|--------|----------|
| YYYY-MM-DD | [Name] | [Status] | [Comments] |

## Change Log

| Date | Change | Author | Reason |
|------|--------|--------|--------|
| YYYY-MM-DD | Initial draft | [Name] | [Reason] |
