# EARS Requirements Methodology

## Overview
EARS (Easy Approach to Requirements Syntax) provides a structured way to write clear, unambiguous requirements that can be automatically converted to test specifications.

## The Five EARS Patterns

### 1. Ubiquitous Requirements
**Format**: `The [system] shall [behavior]`
**Use**: Requirements that apply at all times

### 2. Event-Driven Requirements  
**Format**: `When [trigger], the [system] shall [response]`
**Use**: Behavior triggered by specific events

### 3. State-Driven Requirements
**Format**: `While [state], the [system] shall [behavior]`  
**Use**: Behavior dependent on system state

### 4. Unwanted Behavior
**Format**: `If [unwanted condition], then the [system] shall [mitigation]`
**Use**: Error handling and recovery

### 5. Optional Features
**Format**: `Where [feature enabled], the [system] shall [behavior]`
**Use**: Configurable or optional functionality

## Best Practices

1. **Atomic**: Each requirement describes ONE behavior
2. **Testable**: Must be verifiable through testing
3. **Measurable**: Include specific metrics where applicable
4. **Clear**: No ambiguous terms
5. **Consistent**: Use standard terminology throughout

## Requirement Template

```markdown
---
id: REQ-XXX
type: [ubiquitous|event-driven|state-driven|unwanted|optional]
priority: [high|medium|low]
status: [draft|approved|implemented]
---

# Requirement: [Title]

## EARS Statement
[Formal EARS requirement]

## Rationale
[Why this requirement exists]

## Acceptance Criteria
- [ ] Specific, measurable criterion
- [ ] Must be testable
- [ ] Include thresholds/metrics

## Traceability
- Epic: [Link]
- BDD: [Scenarios]
- Tests: [Test cases]
```

## Converting Natural Language to EARS

### Example Transformations

**Natural Language**: "Users need to log in with their email"
**EARS**: "When a user submits valid email credentials, the system shall authenticate the user within 1 second"

**Natural Language**: "The system should handle errors gracefully"
**EARS**: "If a database connection fails, then the system shall retry 3 times before displaying an error message"

**Natural Language**: "Admin users have extra features"
**EARS**: "Where admin privileges are enabled, the system shall display the administration panel"
