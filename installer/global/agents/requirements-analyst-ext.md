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

## Refinement Question Templates

When refinement mode is active (`/epic-refine` or `/feature-refine`), use these targeted question templates. Present questions one at a time. The user can always type **skip** to move to the next question or **done** to end the refinement session.

### Scope Refinement Questions

**Question**: "What is explicitly out of scope for this epic/feature?"
- **Example good answer**: "Integration with third-party payment providers is out of scope. We will only support our internal billing system for this release."
- **Skip guidance**: Skip if scope boundaries are already well-defined in the specification.

**Question**: "Can you describe the boundary between this feature and adjacent features?"
- **Example good answer**: "This feature handles user registration only. Email verification is handled by FEAT-003 and profile management by FEAT-004."
- **Skip guidance**: Skip if the feature exists in isolation without overlapping concerns.

### Success Criteria Questions

**Question**: "What measurable outcome would indicate this epic is successful?"
- **Example good answer**: "User onboarding completion rate increases from 60% to 85% within 3 months of launch."
- **Skip guidance**: Skip if success criteria already have specific, quantified targets.

**Question**: "How will you measure whether this feature meets its goals?"
- **Example good answer**: "API response time stays under 200ms at p95 with 1000 concurrent users, and error rate remains below 0.1%."
- **Skip guidance**: Skip if measurable criteria are already documented with specific thresholds.

### Risk Assessment Questions

**Question**: "What could prevent this epic/feature from being delivered successfully?"
- **Example good answer**: "The upstream authentication API has no SLA, so if it goes down during peak hours, our login flow fails. Mitigation: implement a cached token strategy with 5-minute TTL."
- **Skip guidance**: Skip if risks are already identified with mitigation strategies.

**Question**: "Are there any technical unknowns or unproven approaches?"
- **Example good answer**: "We haven't tested the Graphiti integration at scale. We plan a spike in week 1 to validate performance with 10K episodes."
- **Skip guidance**: Skip if all technical approaches are proven and well-understood.

### Dependency Discovery Questions

**Question**: "What external systems, teams, or services does this depend on?"
- **Example good answer**: "Depends on the Identity Service team to expose a new /verify endpoint by March 15. Also requires the staging environment to support Redis 7+."
- **Skip guidance**: Skip if all dependencies are already mapped with owners and timelines.

**Question**: "Are there any features or tasks that must be completed before this can start?"
- **Example good answer**: "FEAT-002 (database schema migration) must be complete first, as this feature relies on the new user_preferences table."
- **Skip guidance**: Skip if dependency ordering is already established in the epic hierarchy.

### Organisation Pattern Assessment Questions

**Question**: "Does this epic decompose into features, or does it contain tasks directly?"
- **Example good answer**: "This epic has two features (FEAT-001 for UI and FEAT-002 for API), plus two direct tasks for documentation updates that don't warrant a feature wrapper."
- **Skip guidance**: Skip if organisation pattern (direct, features, or mixed) is already defined.

---

## Graphiti Integration Patterns

RequireKit can optionally sync epic and feature data to Graphiti for knowledge graph querying. When Graphiti is not installed, RequireKit operates in **standalone mode** using markdown files only.

### Standalone Mode Behavior

When Graphiti is not detected:
- All data is stored in markdown files under `docs/epics/` and `docs/features/`
- Completeness scores are calculated from markdown frontmatter
- Refinement history is tracked in YAML frontmatter arrays
- No sync operations are attempted
- No error messages about missing Graphiti — the system works fully independently

### Episode Schema for Epics

When Graphiti is available, epics are synced as episodes:

```python
{
    "name": f"Epic: {epic_title}",
    "episode_body": epic_markdown_content,
    "group_id": f"{project}__requirements",
    "source": EpisodeType.text,
    "source_description": f"RequireKit epic {epic_id}",
    "reference_time": datetime.now(),
    "_metadata": {
        "entity_type": "epic",
        "epic_id": epic_id,
        "status": epic_status,
        "priority": epic_priority,
        "organisation_pattern": "direct|features|mixed",
        "completeness_score": 78,
        "last_refined": "2026-02-10T14:30:00Z",
        "refinement_count": 2,
        "feature_ids": ["FEAT-001", "FEAT-002"],
        "direct_task_ids": [],
        "success_criteria_count": 4,
        "risk_count": 3,
        "has_constraints": True
    }
}
```

### Episode Schema for Features

Features are synced as separate episodes linked to their parent epic:

```python
{
    "name": f"Feature: {feature_title}",
    "episode_body": feature_markdown_content,
    "group_id": f"{project}__requirements",
    "source": EpisodeType.text,
    "source_description": f"RequireKit feature {feature_id}",
    "reference_time": datetime.now(),
    "_metadata": {
        "entity_type": "feature",
        "feature_id": feature_id,
        "epic_id": parent_epic_id,
        "status": feature_status,
        "priority": feature_priority,
        "completeness_score": 65,
        "last_refined": "2026-02-10T15:00:00Z",
        "acceptance_criteria_count": 5,
        "bdd_scenario_ids": ["BDD-001", "BDD-002"],
        "requirement_ids": ["REQ-001", "REQ-002"],
        "task_count": 4
    }
}
```

### Group ID Strategy

All RequireKit entities share a single group ID: `{project}__requirements`

- **Format**: `{project_name}__requirements` (double underscore separator)
- **Purpose**: Groups all epics and features for a project in one queryable namespace
- **Entity differentiation**: Use `entity_type` metadata field (`"epic"` or `"feature"`)
- **Example**: `myapp__requirements` for project "myapp"

### Sync Error Handling

When syncing to Graphiti, handle errors gracefully:

1. **Connection errors**: Log warning, continue with local markdown (do not block workflow)
2. **Schema validation errors**: Log the specific field that failed, sync remaining valid fields
3. **Duplicate episodes**: Use upsert semantics — update existing episode if `epic_id` or `feature_id` matches
4. **Timeout errors**: Retry once with exponential backoff, then fall back to local-only mode
5. **Partial sync failures**: Record which entities failed in a sync log for manual retry

```python
try:
    await graphiti_client.add_episode(episode_data)
except ConnectionError:
    logger.warning(f"Graphiti sync failed for {entity_id}, continuing in standalone mode")
except ValidationError as e:
    logger.warning(f"Schema validation failed for {entity_id}: {e.field}")
except TimeoutError:
    logger.warning(f"Graphiti timeout for {entity_id}, retrying once")
    await retry_with_backoff(graphiti_client.add_episode, episode_data)
```

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
