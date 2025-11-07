# Quickstart Guide

Get up and running with RequireKit in 5 minutes. This guide will walk you through your first requirements gathering session.

## Your First Requirements Session

Let's capture requirements for a simple user login feature.

### Step 1: Gather Requirements (2 minutes)

```bash
/gather-requirements user-login
```

**The system will guide you through questions:**

```
Claude: Let's gather requirements for user-login. What problem are we solving?

You: Users need to securely log into our application with email and password.

Claude: Who will be using this feature?

You: Regular users and administrators.

Claude: What should happen on successful login?

You: Redirect to dashboard and create a session.

Claude: What should happen on failed login?

You: Show an error message.

Claude: Any performance requirements?

You: Login should complete in under 1 second.

Claude: Security requirements?

You: Passwords must be hashed. Use HTTPS only.

Claude: ✅ Requirements captured!

Output: docs/requirements/draft/user-login.md
```

### Step 2: Formalize with EARS (1 minute)

```bash
/formalize-ears
```

**Output:**
```
✅ Created 5 EARS requirements:

REQ-001: When a user submits valid credentials, the system shall
         authenticate and redirect to dashboard within 1 second.

REQ-002: If authentication fails, then the system shall display
         "Invalid email or password" message.

REQ-003: The system shall hash all passwords using bcrypt.

REQ-004: The system shall accept authentication requests only over HTTPS.

REQ-005: While a user session is active, the system shall validate
         the session token on each request.

Files: docs/requirements/REQ-001.md through REQ-005.md
```

### Step 3: Generate BDD Scenarios (1 minute)

```bash
/generate-bdd
```

**Output:**
```
✅ Generated BDD scenarios:

Feature: User Authentication
  Scenario: Successful login
  Scenario: Failed login
  Scenario: HTTPS enforcement
  Scenario: Session validation

File: docs/bdd/BDD-001-user-authentication.feature
```

### 🎉 Congratulations!

You've just created complete, testable requirements in under 5 minutes:
- ✅ 5 EARS-formatted requirements
- ✅ 4 BDD scenarios for testing
- ✅ Full traceability

## Understanding the Workflow

```
┌─────────────────┐
│ 1. GATHER       │  Interactive Q&A
│  Requirements   │  /gather-requirements
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. FORMALIZE    │  Convert to EARS
│  with EARS      │  /formalize-ears
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. GENERATE     │  Create BDD scenarios
│  BDD Scenarios  │  /generate-bdd
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. ORGANIZE     │  Epic/Feature hierarchy
│  Hierarchy      │  /epic-create, /feature-create
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. EXPORT       │  PM tools or implementation
│  Integration    │  /feature-sync --jira
└─────────────────┘
```

## EARS Notation Quick Reference

RequireKit uses five patterns for clear requirements:

1. **Ubiquitous**: `The system shall [behavior]` - Always applies, no conditions
2. **Event-Driven**: `When [trigger], the system shall [response]` - Triggered by specific events
3. **State-Driven**: `While [state], the system shall [behavior]` - Applies in certain states
4. **Unwanted Behavior**: `If [error], then the system shall [recovery]` - Error handling
5. **Optional Feature**: `Where [feature], the system shall [behavior]` - Optional/conditional features

## Organizing with Epics and Features

After creating requirements, organize them into epics and features:

```bash
# Create epic
/epic-create "User Management System"

# Create feature linked to epic
/feature-create "User Authentication" epic:EPIC-001

# View complete hierarchy
/hierarchy-view EPIC-001
```

## What's Next?

- 📖 [Learn more about EARS notation](../core-concepts/ears-notation.md)
- 🎯 [Understand BDD scenario generation](../core-concepts/bdd-scenarios.md)
- 📝 [Explore the complete user guide](../guides/require_kit_user_guide.md)
- 💡 [See more examples](../examples/index.md)

## Need Help?

- Check the [FAQ](../faq.md) for common questions
- Review [Troubleshooting](../troubleshooting/index.md) for common issues
- Visit the [Commands Reference](../commands/index.md) for detailed documentation

---

**Ready for more?** Check out the [Complete User Guide](../guides/require_kit_user_guide.md)
