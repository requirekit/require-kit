# Requirements Analyst Agent - Extended Content

**Core File**: `installer/global/agents/requirements-analyst.md`

This file contains detailed processes, templates, and domain-specific patterns for requirements gathering and formalization. Load this content when you need comprehensive guidance on requirements engineering methodology.

---

## Requirements Gathering Process

### Phase 1: Discovery
Start with open-ended questions to understand the big picture:
- What problem are we solving?
- Who are the users?
- What are the key goals?
- What constraints exist?

### Phase 2: Exploration
Drill down into specifics:
- What triggers each behavior?
- What are the expected outcomes?
- What error conditions might occur?
- How will we measure success?

### Phase 3: Validation
Confirm understanding:
- Review requirements with stakeholders
- Verify completeness
- Check for conflicts
- Ensure testability

---

## Question Templates

### For Event-Driven Requirements
- What event triggers this behavior?
- Who or what initiates the event?
- What is the expected system response?
- How quickly must the system respond?
- What happens if the event fails?

### For State-Driven Requirements
- What states can the system be in?
- What behaviors are specific to each state?
- How does the system transition between states?
- What maintains the state?

### For Error Handling
- What could go wrong?
- How should the system recover?
- Who should be notified?
- What data needs to be preserved?

---

## Common Patterns by Domain

### Authentication & Security
- Login/logout flows
- Session management
- Access control
- Password policies
- Security events

### Data Management
- CRUD operations
- Validation rules
- Data transformation
- Archival policies
- Backup procedures

### Integration
- API contracts
- Event handling
- Error recovery
- Rate limiting
- Timeout handling

### User Interface
- User interactions
- Form submissions
- Navigation flows
- Responsive behavior
- Accessibility requirements

---

## Full Output Format Example

### Complete EARS Requirement Document

```markdown
---
id: REQ-042-001
type: event-driven
priority: high
status: approved
epic: EPIC-010
feature: FEAT-025
created: 2025-10-29
updated: 2025-10-29
---

# Requirement: User Authentication

## EARS Statement
When a user submits valid credentials, the system shall authenticate within 200ms and establish a secure session.

## Rationale
User authentication is critical for system security and user identity management. The 200ms response time ensures a responsive user experience while maintaining security through proper credential validation.

## Acceptance Criteria
- [ ] Login succeeds with valid username/password combination
- [ ] Login fails with invalid credentials and returns appropriate error message
- [ ] Session established on successful authentication with secure token
- [ ] Authentication completes within 200ms (p95 latency)
- [ ] Failed login attempts are logged for security monitoring
- [ ] Account lockout after 5 consecutive failed attempts

## Related Requirements
- REQ-042-002 (Session Management)
- REQ-042-003 (Password Validation)
- REQ-042-004 (Account Lockout Policy)
- REQ-042-005 (Security Logging)

## Notes
- Integrates with OAuth2 for SSO scenarios
- Must support multi-factor authentication in future iterations
- Password hashing uses bcrypt with salt rounds >= 10
- Session tokens expire after 30 minutes of inactivity
```

### Example: State-Driven Requirement

```markdown
---
id: REQ-043-001
type: state-driven
priority: high
status: approved
epic: EPIC-011
feature: FEAT-026
created: 2025-10-29
updated: 2025-10-29
---

# Requirement: Maintenance Mode Display

## EARS Statement
While in maintenance mode, the system shall display a maintenance message and reject all user requests except health checks.

## Rationale
Maintenance mode allows system administrators to perform updates and repairs without impacting user data integrity or causing partial service failures.

## Acceptance Criteria
- [ ] Maintenance message displays on all user-facing pages
- [ ] User requests return 503 Service Unavailable status
- [ ] Health check endpoint remains accessible
- [ ] Administrator access remains available
- [ ] Scheduled maintenance end time is displayed to users
- [ ] System logs all rejected requests during maintenance

## Related Requirements
- REQ-043-002 (Maintenance Mode Toggle)
- REQ-043-003 (Health Check Endpoint)
- REQ-043-004 (Administrator Override)

## Notes
- Maintenance mode can be scheduled or triggered manually
- Redis flag controls maintenance state across all instances
- Estimated time displayed based on scheduled maintenance window
```

### Example: Unwanted Behavior Requirement

```markdown
---
id: REQ-044-001
type: unwanted
priority: critical
status: approved
epic: EPIC-012
feature: FEAT-027
created: 2025-10-29
updated: 2025-10-29
---

# Requirement: Database Connection Failure Recovery

## EARS Statement
If database connection fails, then the system shall retry 3 times with exponential backoff before alerting operations team.

## Rationale
Network transients and brief database restarts are common in cloud environments. Automatic retry with backoff prevents false alerts while ensuring persistent issues are escalated.

## Acceptance Criteria
- [ ] First retry after 1 second delay
- [ ] Second retry after 2 seconds delay
- [ ] Third retry after 4 seconds delay
- [ ] Alert sent to operations team after 3 failed attempts
- [ ] Connection pooling resumes after successful retry
- [ ] Failed queries return 500 error with retry-after header
- [ ] All retry attempts logged with timestamps

## Related Requirements
- REQ-044-002 (Connection Pool Management)
- REQ-044-003 (Operations Alerting)
- REQ-044-004 (Error Response Format)

## Notes
- Uses exponential backoff to avoid overwhelming recovering database
- Alert includes connection error details and retry history
- Circuit breaker pattern may be considered for future enhancement
```

---

**Return to Core File**: `installer/global/agents/requirements-analyst.md`
