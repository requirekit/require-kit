# Formalize EARS Command

Convert natural language requirements into formal EARS (Easy Approach to Requirements Syntax) notation.

## Command
```
/formalize-ears [requirement-file]
```

## What This Does

Takes your natural language requirements and converts them into one of five EARS patterns:

1. **Ubiquitous** - Always active requirements
2. **Event-Driven** - Triggered by events
3. **State-Driven** - Active during states
4. **Unwanted Behavior** - Error handling
5. **Optional Feature** - Feature-specific

## Input Format

Provide requirements in natural language:
```
Users should be able to login with their email and password.
The system needs to lock accounts after too many failed attempts.
When logged in, users should see personalized content.
If the database is down, show a maintenance message.
```

## Output Format

```markdown
## REQ-001: User Login [Event-Driven]
When a user submits valid email and password credentials, the system shall authenticate the user and create a session within 1 second.

## REQ-002: Account Lockout [Unwanted Behavior]
If a user submits invalid credentials 3 times within 5 minutes, then the system shall lock the account for 15 minutes and send a security alert.

## REQ-003: Personalized Content [State-Driven]
While a user session is active, the system shall display personalized content based on user preferences.

## REQ-004: Database Failure [Unwanted Behavior]
If the database connection fails, then the system shall display a maintenance message and log the error for administrators.
```

## Pattern Selection Guide

### Use Ubiquitous When:
- Requirement applies all the time
- No specific trigger or condition
- System-wide behaviors

### Use Event-Driven When:
- Specific action triggers behavior
- User interactions
- System events

### Use State-Driven When:
- Behavior depends on system state
- Different modes of operation
- Conditional functionality

### Use Unwanted Behavior When:
- Handling errors or exceptions
- Recovery procedures
- Fallback mechanisms

### Use Optional Feature When:
- Feature can be enabled/disabled
- Premium functionality
- Configuration-dependent

## Quality Checks

Each EARS requirement will be validated for:
- ✅ Correct pattern usage
- ✅ Atomic behavior (single responsibility)
- ✅ Testable criteria
- ✅ Measurable outcomes
- ✅ Clear actors and actions

## Examples

### Input:
"Users need to reset their password if they forget it"

### Output:
```
## REQ-005: Password Reset Request [Event-Driven]
When a user requests a password reset, the system shall send a reset link to the registered email address within 30 seconds.

## REQ-006: Password Reset Completion [Event-Driven]
When a user submits a new password via a valid reset link, the system shall update the password and invalidate the reset link.
```

## Metadata Added

Each requirement will include:
```yaml
---
id: REQ-XXX
type: event-driven
priority: high
status: draft
epic: EPIC-XXX
feature: FEAT-XXX
---
```

## Best Practices

1. **Keep requirements atomic** - One behavior per requirement
2. **Be specific** - Include timing, quantities, and thresholds
3. **Make them testable** - Avoid subjective terms
4. **Use consistent terminology** - Define terms once, use everywhere
5. **Include error cases** - Don't just focus on happy paths

## Next Steps

After formalizing to EARS:
1. Review requirements for completeness
2. Run `/generate-bdd` to create test scenarios
3. Begin implementation with clear specifications

## Usage

```bash
# Formalize requirements from gathered session
/formalize-ears

# Formalize specific file
/formalize-ears docs/requirements/auth-requirements.md

# Formalize with validation
/formalize-ears --validate
```

Ready to formalize your requirements into EARS notation!
