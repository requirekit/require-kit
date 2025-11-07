# EARS Notation

EARS (Easy Approach to Requirements Syntax) provides five clear patterns for writing unambiguous requirements.

## The Five EARS Patterns

### 1. Ubiquitous
**Format**: `The [system] shall [behavior]`

**Use when**: The requirement always applies, with no conditions or triggers.

**Examples:**
```
The system shall hash all passwords using bcrypt.
The system shall log all authentication attempts.
The system shall support UTF-8 encoding.
```

### 2. Event-Driven
**Format**: `When [trigger], the [system] shall [response]`

**Use when**: The requirement is triggered by a specific event.

**Examples:**
```
When a user submits valid credentials, the system shall authenticate
and redirect to dashboard within 1 second.

When a file upload exceeds 10MB, the system shall reject the upload
and display an error message.

When a user session expires, the system shall redirect to login page.
```

### 3. State-Driven
**Format**: `While [state], the [system] shall [behavior]`

**Use when**: The requirement applies during a specific system or user state.

**Examples:**
```
While a user session is active, the system shall validate
the session token on each request.

While offline mode is enabled, the system shall queue
changes for later synchronization.

While processing a payment, the system shall display
a loading indicator.
```

### 4. Unwanted Behavior
**Format**: `If [error condition], then the [system] shall [recovery action]`

**Use when**: Specifying error handling or recovery behavior.

**Examples:**
```
If authentication fails, then the system shall display
"Invalid email or password" message.

If database connection is lost, then the system shall
retry 3 times with exponential backoff.

If file parsing fails, then the system shall log the error
and continue processing remaining files.
```

### 5. Optional Feature
**Format**: `Where [feature is enabled], the [system] shall [behavior]`

**Use when**: The requirement applies only when an optional feature is present or enabled.

**Examples:**
```
Where two-factor authentication is enabled, the system shall
send a verification code via SMS.

Where dark mode is selected, the system shall apply
dark theme colors to all UI elements.

Where premium subscription is active, the system shall
remove advertising content.
```

## Choosing the Right Pattern

| Pattern | Trigger/Condition | Always Active |
|---------|-------------------|---------------|
| Ubiquitous | None | ✅ Yes |
| Event-Driven | Specific event | ❌ No |
| State-Driven | System/user state | ❌ No |
| Unwanted Behavior | Error condition | ❌ No |
| Optional Feature | Feature flag | ❌ No |

## Benefits of EARS

### Clarity
Each pattern has a specific structure that removes ambiguity.

**Before EARS:**
> "The system should handle login properly"

**After EARS:**
> "When a user submits valid credentials, the system shall authenticate and redirect to dashboard within 1 second."

### Testability
EARS requirements are inherently testable with clear triggers and expected behaviors.

### Consistency
Using the same patterns across all requirements improves understanding and reduces errors.

## Common Mistakes to Avoid

❌ **Don't use implementation details:**
```
Bad:  The system shall use React for the UI.
Good: The system shall provide a responsive user interface.
```

❌ **Don't use vague language:**
```
Bad:  The system shall respond quickly.
Good: When a user submits a search query, the system shall return
      results within 500 milliseconds.
```

❌ **Don't mix multiple requirements:**
```
Bad:  The system shall validate input and log errors and send notifications.
Good: Split into three separate requirements, each with EARS pattern.
```

❌ **Don't use "should" or "may":**
```
Bad:  The system should validate email format.
Good: The system shall validate email format according to RFC 5322.
```

## Best Practices

✅ **Be specific:** Include concrete values (times, sizes, counts)
✅ **One requirement per statement:** Don't combine multiple behaviors
✅ **Use measurable criteria:** "within 1 second" not "quickly"
✅ **Include error cases:** Use Unwanted Behavior pattern
✅ **Consider optional features:** Use Optional Feature pattern

## Real-World Example

**Feature:** User Password Reset

```
REQ-001 (Ubiquitous):
The system shall require passwords to be at least 12 characters.

REQ-002 (Event-Driven):
When a user requests password reset, the system shall send
a reset link to the registered email address within 30 seconds.

REQ-003 (State-Driven):
While a password reset link is valid, the system shall allow
the user to set a new password.

REQ-004 (Unwanted Behavior):
If a reset link is older than 1 hour, then the system shall
reject the link and require a new reset request.

REQ-005 (Optional Feature):
Where multi-factor authentication is enabled, the system shall
require MFA verification before password reset.
```

## Next Steps

- 🎯 [Learn about BDD Scenarios](bdd-scenarios.md)
- 📝 [Try gathering your first requirements](../getting-started/first-requirements.md)
- 💡 [See more examples](../examples/requirements.md)

---

For detailed examples and templates, see the [Complete User Guide](../guides/require_kit_user_guide.md).
