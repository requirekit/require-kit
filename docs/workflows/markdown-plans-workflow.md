# Markdown Implementation Plans Workflow

## Overview

Implementation plans in Agentecflow Lite are stored as **human-readable Markdown files** instead of JSON. This design choice aligns with the Hubbard workflow principle of "visible artifacts" and provides significant benefits for team collaboration, manual review, and git-based workflows.

**Key Benefits:**
- **Human-Readable**: Plain text format readable in any text editor or IDE
- **Git-Friendly**: Meaningful diffs showing actual plan changes (not JSON formatting)
- **Manual Editable**: Can be edited directly without special tools
- **Review-Friendly**: Easy to review in PRs, no parsing required
- **Version Control**: Track plan evolution over time with standard git tools

**Location:** Plans are saved to `.claude/task-plans/{task_id}-implementation-plan.md`

## Markdown Plan Format

### Standard Structure

All implementation plans follow this consistent Markdown structure:

```markdown
# Implementation Plan: TASK-XXX

**Task**: [Task title]
**Complexity**: [Score]/10 ([Level])
**Estimated Duration**: [Hours] hours
**Technology Stack**: [Stack name]
**Generated**: [ISO 8601 timestamp]

## Summary

[1-2 sentence summary of what will be implemented]

## Files to Create

### 1. `path/to/file.ext` ([Estimated lines])
**Purpose**: [What this file does]
**Patterns**: [Design patterns used]
**Dependencies**: [External dependencies needed]

[Additional file details, interfaces, key functions]

### 2. `path/to/another/file.ext` ([Estimated lines])
...

## Files to Modify

### 1. `existing/file/path.ext`
**Changes**: [What will be modified]
**Reason**: [Why modification needed]
**Risk**: [Low/Medium/High] - [Explanation]

## Dependencies

1. **[Package name]** ([Version])
   - Purpose: [Why needed]
   - Installation: `[install command]`

2. **[Another package]** ([Version])
   ...

## Implementation Phases

### Phase 1: [Phase name] ([Duration estimate])
- [Step 1]
- [Step 2]
- [Step 3]

### Phase 2: [Phase name] ([Duration estimate])
- [Step 1]
- [Step 2]

## Risks and Mitigations

### 🔴 High Risk: [Risk description]
**Mitigation**: [How to address]

### 🟡 Medium Risk: [Risk description]
**Mitigation**: [How to address]

### 🟢 Low Risk: [Risk description]
**Mitigation**: [How to address]

## Test Strategy

**Unit Tests**: [Coverage target, key test cases]
**Integration Tests**: [What will be tested]
**Edge Cases**: [Specific edge cases to cover]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Notes

[Any additional context, assumptions, or decisions]
```

### Example: Complete Markdown Plan

```markdown
# Implementation Plan: TASK-042

**Task**: Implement JWT authentication endpoint
**Complexity**: 5/10 (Medium)
**Estimated Duration**: 4 hours
**Technology Stack**: Python (FastAPI)
**Generated**: 2025-10-20T14:30:00Z

## Summary

Implement a secure JWT-based authentication endpoint that validates user credentials and returns a signed token with configurable expiration.

## Files to Create

### 1. `src/auth/jwt_service.py` (80 lines)
**Purpose**: JWT token generation and validation service
**Patterns**: Factory Pattern, Singleton
**Dependencies**: pyjwt, python-dotenv

Key functions:
- `generate_token(user: User) -> str`: Creates signed JWT
- `validate_token(token: str) -> User | None`: Verifies and decodes
- `refresh_token(token: str) -> str`: Issues new token from valid token

### 2. `src/api/auth_endpoints.py` (60 lines)
**Purpose**: Authentication API endpoints (login, refresh, logout)
**Patterns**: REST API, Dependency Injection
**Dependencies**: fastapi, pydantic

Endpoints:
- `POST /auth/login`: Username/password → JWT token
- `POST /auth/refresh`: Refresh token → New JWT
- `POST /auth/logout`: Invalidate token (blacklist)

### 3. `src/middleware/jwt_middleware.py` (40 lines)
**Purpose**: FastAPI middleware for JWT validation on protected routes
**Patterns**: Middleware Pattern
**Dependencies**: fastapi

Middleware:
- Extracts JWT from Authorization header
- Validates token and injects user into request context
- Returns 401 Unauthorized if invalid

### 4. `tests/test_auth_service.py` (100 lines)
**Purpose**: Unit tests for JWT service
**Patterns**: Arrange-Act-Assert, Fixtures
**Dependencies**: pytest, freezegun

Test coverage:
- Token generation and validation
- Expiration handling
- Invalid token scenarios
- Refresh token logic

## Files to Modify

### 1. `src/main.py`
**Changes**: Add JWT middleware to FastAPI app
**Reason**: Enable authentication for protected routes
**Risk**: Low - Additive change only

### 2. `requirements.txt`
**Changes**: Add pyjwt==2.8.0, python-dotenv==1.0.0
**Reason**: New dependencies for JWT functionality
**Risk**: Low - Well-established libraries

## Dependencies

1. **pyjwt** (2.8.0)
   - Purpose: JWT token encoding/decoding
   - Installation: `pip install pyjwt==2.8.0`

2. **python-dotenv** (1.0.0)
   - Purpose: Load JWT_SECRET from environment
   - Installation: `pip install python-dotenv==1.0.0`

3. **freezegun** (1.2.2)
   - Purpose: Mock time in expiration tests
   - Installation: `pip install freezegun==1.2.2` (dev dependency)

## Implementation Phases

### Phase 1: JWT Service Core (1.5 hours)
- Create jwt_service.py with basic structure
- Implement token generation with HMAC-SHA256
- Implement token validation and decoding
- Add expiration logic (default 1 hour)

### Phase 2: API Endpoints (1 hour)
- Create auth_endpoints.py with FastAPI router
- Implement POST /auth/login endpoint
- Implement POST /auth/refresh endpoint
- Add request/response models with Pydantic

### Phase 3: Middleware Integration (0.5 hours)
- Create jwt_middleware.py
- Add authorization header parsing
- Integrate validation logic
- Add error handling (401, 403)

### Phase 4: Testing (1 hour)
- Write unit tests for JWT service (15 tests)
- Write API endpoint tests (10 tests)
- Write middleware integration tests (5 tests)
- Verify 80%+ coverage

## Risks and Mitigations

### 🔴 High Risk: JWT secret management
**Mitigation**: Use environment variables, never commit secrets, use strong secrets (32+ chars)

### 🟡 Medium Risk: Token refresh race conditions
**Mitigation**: Use short-lived access tokens (1 hour) and longer-lived refresh tokens (7 days)

### 🟢 Low Risk: Token expiration edge cases
**Mitigation**: Use freezegun for time-based tests, add buffer to expiration checks

## Test Strategy

**Unit Tests**:
- Target: 85% coverage
- Focus: Token generation, validation, expiration logic
- Edge cases: Expired tokens, invalid signatures, malformed tokens

**Integration Tests**:
- Full login flow (credentials → token → protected route)
- Token refresh workflow
- Middleware error handling

**Security Tests**:
- Invalid signature rejection
- Expired token rejection
- Missing token handling (401)

## Success Criteria

- [ ] All endpoints return correct status codes (200, 401, 403)
- [ ] JWT tokens are correctly signed and validated
- [ ] Expiration logic works (tokens expire after 1 hour)
- [ ] Middleware correctly protects routes
- [ ] All tests pass (30+ tests)
- [ ] Coverage ≥85%
- [ ] No hardcoded secrets in code

## Notes

- JWT_SECRET must be set in .env file (generate with `openssl rand -hex 32`)
- Consider adding token blacklist for logout (requires Redis or similar)
- Future enhancement: Add refresh token rotation for better security
```

## Benefits over JSON Plans

### 1. Git Diff Improvements

**JSON Plan Diff (Hard to Review):**
```diff
{
  "files_to_create": [
    {
-     "path": "src/auth/jwt_service.py",
-     "estimated_lines": 80,
+     "path": "src/auth/jwt_service.py",
+     "estimated_lines": 90,
      "purpose": "JWT token generation and validation service",
      "patterns": ["Factory Pattern", "Singleton"],
-     "dependencies": ["pyjwt", "python-dotenv"]
+     "dependencies": ["pyjwt", "python-dotenv", "cryptography"]
    }
  ],
  "estimated_duration": 4
}
```

**Markdown Plan Diff (Easy to Review):**
```diff
 ## Files to Create

 ### 1. `src/auth/jwt_service.py` (80 lines)
+### 1. `src/auth/jwt_service.py` (90 lines)
 **Purpose**: JWT token generation and validation service
 **Patterns**: Factory Pattern, Singleton
-**Dependencies**: pyjwt, python-dotenv
+**Dependencies**: pyjwt, python-dotenv, cryptography

+Key functions (updated):
+- `encrypt_token(token: str) -> str`: Additional layer of encryption
```

**Result**: Markdown diffs show actual content changes, JSON diffs show formatting noise.

### 2. Manual Editing Support

**JSON Plan Editing (Requires Careful Syntax):**
```json
{
  "files_to_create": [
    {
      "path": "src/auth/jwt_service.py",
      "estimated_lines": 80,  // ← Must be valid JSON (no trailing comma)
      "purpose": "JWT service"
    }  // ← Easy to make syntax errors
  ]
}
```

**Markdown Plan Editing (Any Text Editor):**
```markdown
### 1. `src/auth/jwt_service.py` (80 lines)
**Purpose**: JWT service

Just edit the text, no syntax issues!
```

**Result**: Markdown plans editable in any text editor (VS Code, Vim, Nano) without JSON syntax concerns.

### 3. Human Reviewability

**JSON Plan Review (Requires Mental Parsing):**
```json
{"files_to_create":[{"path":"src/auth/jwt_service.py","estimated_lines":80,"purpose":"JWT token generation and validation service","patterns":["Factory Pattern","Singleton"],"dependencies":["pyjwt","python-dotenv"]}],"estimated_duration":4,"risks":[{"severity":"high","description":"JWT secret management","mitigation":"Use environment variables"}]}
```
(One long line, hard to scan, requires parsing mental model)

**Markdown Plan Review (Natural Reading):**
```markdown
## Files to Create

### 1. `src/auth/jwt_service.py` (80 lines)
**Purpose**: JWT token generation and validation service
**Patterns**: Factory Pattern, Singleton
**Dependencies**: pyjwt, python-dotenv

## Risks

### 🔴 High Risk: JWT secret management
**Mitigation**: Use environment variables
```
(Natural sections, scannable, easy to review in GitHub PR)

**Result**: Markdown plans readable in GitHub PRs, GitLab merge requests, code review tools.

### 4. Hubbard Workflow Alignment

**Hubbard Principle: "Visible Artifacts"**
- Work products should be visible and reviewable by humans
- Tools should produce human-readable outputs
- Avoid black-box processes

**JSON Plans**: Machine-readable, requires tools to parse and display
**Markdown Plans**: Human-readable, no tools required, visible artifacts ✅

## Manual Editing Workflow

### Phase 2.8 Checkpoint Modification

At the Phase 2.8 human checkpoint, you can modify the implementation plan before proceeding to implementation.

**Step 1: Review Generated Plan**
```bash
# Open plan in editor
code .claude/task-plans/TASK-042-implementation-plan.md

# Or view in terminal
cat .claude/task-plans/TASK-042-implementation-plan.md
```

**Step 2: Edit Plan Directly**
```markdown
# Example: Add another file to plan

## Files to Create

### 1. `src/auth/jwt_service.py` (80 lines)
...

### 2. `src/api/auth_endpoints.py` (60 lines)
...

### 3. `src/middleware/jwt_middleware.py` (40 lines)  ← ADDED MANUALLY
**Purpose**: Middleware for JWT validation
**Patterns**: Middleware Pattern
**Dependencies**: fastapi
```

**Step 3: Save and Validate**
```bash
# System validates edited plan
/task-work TASK-042 --implement-only

# Validation checks:
# - Markdown syntax valid ✅
# - Required sections present ✅
# - File paths valid ✅
# - Dependencies parseable ✅
```

**Step 4: Proceed to Implementation**
System uses the manually edited plan for Phase 3 (implementation).

### Version Management

**Automatic Versioning:**
- Original plan: `TASK-042-implementation-plan.md`
- After edit: `TASK-042-implementation-plan-v2.md` (original preserved)
- After re-edit: `TASK-042-implementation-plan-v3.md`

**Version History:**
```bash
ls .claude/task-plans/TASK-042*

# Output:
# TASK-042-implementation-plan.md       (active version)
# TASK-042-implementation-plan-v1.md    (original)
# TASK-042-implementation-plan-v2.md    (after 1st edit)
```

**Compare Versions:**
```bash
diff .claude/task-plans/TASK-042-implementation-plan-v1.md \
     .claude/task-plans/TASK-042-implementation-plan.md
```

### Validation After Edits

**Validation Rules:**

1. **Markdown Syntax**: Must be valid Markdown
2. **Required Sections**: Must have Files, Dependencies, Phases, Risks
3. **File Paths**: Must be valid paths (no special characters)
4. **Dependencies**: Must be parseable (name + version)

**Validation Errors:**

```markdown
# Invalid: Missing estimated lines
### 1. `src/auth/jwt_service.py`
**Purpose**: JWT service

# Valid:
### 1. `src/auth/jwt_service.py` (80 lines)
**Purpose**: JWT service
```

**Error Message:**
```
❌ Plan validation failed

File entry missing estimated lines:
  Line 15: `src/auth/jwt_service.py`

Required format:
  ### [N]. `path/to/file.ext` ([N] lines)

Fix the plan and retry.
```

## Git Diff Best Practices

### Commit Plan Changes

**Recommendation**: Commit plans separately from code

```bash
# Step 1: Generate plan
/task-work TASK-042 --design-only

# Step 2: Commit plan
git add .claude/task-plans/TASK-042-implementation-plan.md
git commit -m "Add implementation plan for TASK-042"

# Step 3: Implement and commit code
/task-work TASK-042 --implement-only
git add src/ tests/
git commit -m "Implement TASK-042: JWT authentication"
```

**Benefits:**
- Plan review separate from code review
- Clear history (plan → implementation)
- Easy to revert plan changes without affecting code

### Review-Friendly Diffs

**Good PR Structure:**
```
📁 Pull Request: TASK-042 JWT Authentication

Commit 1: Add implementation plan for TASK-042
  - .claude/task-plans/TASK-042-implementation-plan.md

Commit 2: Implement JWT service (Phase 1)
  - src/auth/jwt_service.py

Commit 3: Implement API endpoints (Phase 2)
  - src/api/auth_endpoints.py

Commit 4: Add middleware (Phase 3)
  - src/middleware/jwt_middleware.py

Commit 5: Add tests (Phase 4)
  - tests/test_auth_service.py
```

**Review Process:**
1. Review plan first (Commit 1) - Approve design
2. Review implementation (Commits 2-4) - Approve code
3. Review tests (Commit 5) - Approve quality

### Merge Conflict Resolution

**Scenario**: Two developers work on same task, edit plan differently

**Conflict:**
```markdown
<<<<<<< HEAD
### 1. `src/auth/jwt_service.py` (80 lines)
**Purpose**: JWT service with HMAC-SHA256
=======
### 1. `src/auth/jwt_service.py` (90 lines)
**Purpose**: JWT service with RSA-256
>>>>>>> feature-branch
```

**Resolution:**
```markdown
### 1. `src/auth/jwt_service.py` (85 lines)
**Purpose**: JWT service with HMAC-SHA256 (default) and RSA-256 (optional)
```

**Easy with Markdown**: Human-readable conflict markers, easy to resolve manually.

## Migration from JSON Plans

### Backward Compatibility

**Phase 1: Both Formats Supported** (Current)
- System reads Markdown plans if available
- Falls back to JSON if Markdown not found
- No migration required

**Phase 2: Markdown Default** (Next Release)
- New plans generated as Markdown
- JSON plans still readable (deprecated warning)
- Gradual migration encouraged

**Phase 3: JSON Deprecated** (Future Release)
- JSON plans no longer generated
- JSON plans still readable (for old tasks)
- All new plans Markdown only

### Automatic Conversion

**Convert JSON to Markdown:**
```bash
# Convert single task plan
/plan-convert TASK-042 --from json --to markdown

# Convert all JSON plans in project
/plan-convert --all --from json --to markdown

# Output:
# Converted 15 plans:
# - TASK-001: JSON → Markdown ✅
# - TASK-002: JSON → Markdown ✅
# ...
```

**Conversion Preserves:**
- All plan content (files, dependencies, phases)
- Original timestamps
- Version history (JSON plan archived)

### Feature Flag Transition

**Control format via settings:**
```json
// .claude/settings.json
{
  "implementation_plans": {
    "format": "markdown",  // "markdown" | "json" | "both"
    "location": ".claude/task-plans/",
    "version_history": true
  }
}
```

**Options:**
- `"markdown"`: Generate Markdown plans only (recommended)
- `"json"`: Generate JSON plans only (legacy)
- `"both"`: Generate both formats (migration phase)

## Related Workflows

- **[Agentecflow Lite Workflow](../guides/agentecflow-lite-workflow.md)** - Complete workflow overview
- **[Design-First Workflow](./design-first-workflow.md)** - Design approval process with plan editing
- **[Quality Gates Workflow](./quality-gates-workflow.md)** - Plan audit (Phase 5.5) uses plans
- **[Iterative Refinement Workflow](./iterative-refinement-workflow.md)** - Context preservation includes plans

## FAQ

**Q: Can I write plans manually from scratch?**
A: Yes! Create a file following the standard structure. System will validate and use it for implementation.

**Q: What if I don't want Markdown plans?**
A: Set `"format": "json"` in settings. But Markdown is strongly recommended for team collaboration.

**Q: Can I edit plans after implementation starts?**
A: Yes, but plan becomes read-only after Phase 3 (implementation) begins. Use `/task-refine` for post-completion changes.

**Q: Do Markdown plans work with `/task-work --implement-only`?**
A: Yes! System loads the Markdown plan saved during `--design-only` run.

**Q: How do I view plan history?**
A: Use `git log .claude/task-plans/TASK-042-implementation-plan.md` to see all plan changes over time.

**Q: Can I use different Markdown styles?**
A: Standard structure recommended, but system is flexible. Required sections must be present, format can vary.

**Q: Are Markdown plans required?**
A: No. System can generate code without plans (Phases 2-5), but plans improve quality and reviewability.

**Q: Can I share plans across tasks?**
A: Plans are task-specific. For shared patterns, create template plans in `.claude/plan-templates/`.

**Q: Do plans count as documentation?**
A: Yes! Plans are permanent artifacts, committed to git, reviewable by team. Part of project documentation.

**Q: Can I export plans to PDF or other formats?**
A: Yes! Use Markdown converters: `pandoc plan.md -o plan.pdf` or tools like Markdown PDF (VS Code extension).
