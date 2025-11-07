# Feature Examples

Sample feature specifications with linked requirements.

## Example: User Authentication Feature

```yaml
---
id: FEAT-001
title: User Authentication
epic: EPIC-001
requirements: [REQ-001, REQ-002, REQ-003]
bdd_scenarios: [BDD-001]
status: planned
---

# Feature: User Authentication

Secure user authentication using email and password.

## Requirements

- REQ-001: Password hashing
- REQ-002: Login with valid credentials
- REQ-003: Failed authentication handling

## BDD Scenarios

- BDD-001: User authentication scenarios

## Acceptance Criteria

- Users can log in with email/password
- Passwords are hashed using bcrypt
- Failed logins show appropriate error
- Session tokens are generated on success
```

See the [`features/` directory](../guides/README.md) for more examples.
