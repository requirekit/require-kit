# Requirements Examples

Sample EARS-formatted requirements demonstrating all five patterns.

## Ubiquitous Pattern

```
REQ-001: The system shall hash all passwords using bcrypt.

REQ-002: The system shall log all authentication attempts with timestamp and IP address.

REQ-003: The system shall support UTF-8 encoding for all user-generated content.
```

## Event-Driven Pattern

```
REQ-004: When a user submits valid credentials, the system shall authenticate
and redirect to dashboard within 1 second.

REQ-005: When a file upload completes, the system shall send a notification
to the user via email.

REQ-006: When a payment transaction succeeds, the system shall generate
an order confirmation and send to user within 5 seconds.
```

## State-Driven Pattern

```
REQ-007: While a user session is active, the system shall validate
the session token on each request.

REQ-008: While offline mode is enabled, the system shall queue changes
for synchronization when connection is restored.

REQ-009: While processing a payment, the system shall display
a loading indicator and disable the submit button.
```

## Unwanted Behavior Pattern

```
REQ-010: If authentication fails, then the system shall display
"Invalid email or password" message.

REQ-011: If database connection is lost, then the system shall retry
3 times with exponential backoff before returning error.

REQ-012: If file parsing fails, then the system shall log the error,
skip the file, and continue processing remaining files.
```

## Optional Feature Pattern

```
REQ-013: Where two-factor authentication is enabled, the system shall
send a verification code via SMS after password validation.

REQ-014: Where dark mode is selected, the system shall apply
dark theme colors to all UI elements.

REQ-015: Where premium subscription is active, the system shall
remove advertising content from all pages.
```

For more examples, see the [Complete User Guide](../guides/require_kit_user_guide.md).
