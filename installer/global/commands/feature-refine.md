# Feature Refine - Interactive Refinement of Existing Features

Interactively refine an existing feature specification with targeted questions, completeness scoring, and change summaries. Focuses on acceptance criteria specificity, requirements traceability, and BDD scenario coverage.

## Usage
```bash
/feature-refine <feature-id> [options]
```

## Examples
```bash
# Refine a feature (full interactive session)
/feature-refine FEAT-001

# Focus on a single category only
/feature-refine FEAT-001 --focus acceptance
/feature-refine FEAT-001 --focus traceability
/feature-refine FEAT-001 --focus bdd
/feature-refine FEAT-001 --focus technical
/feature-refine FEAT-001 --focus dependencies
/feature-refine FEAT-001 --focus scope

# Quick AI-suggested improvements (skip prompts)
/feature-refine FEAT-001 --quick
```

## Process

The `/feature-refine` command follows a three-phase flow (same pattern as `/epic-refine`):

### Phase 1: Current State Display

1. **Load feature markdown file** by ID from `docs/features/`
2. **Parse frontmatter** and content sections
3. **Calculate feature completeness score** using the 7-dimension model (see below)
4. **Show linked epic context** — display parent epic title, status, and completeness for context
5. **Display completeness assessment** with visual indicators:
   - ✅ dimension ≥ 0.8 (well-specified)
   - ⚠️ dimension 0.4–0.79 (needs attention)
   - ❌ dimension < 0.4 (needs refinement)

#### Current State Output
```
═══════════════════════════════════════════════
[REFINE] Feature: FEAT-001 — User Authentication
═══════════════════════════════════════════════

📋 Parent Epic: EPIC-001 — User Management System (72% complete)

📊 Feature Completeness: 58%

  ✅ Scope Within Epic         10% — Clear boundary defined
  ⚠️ Acceptance Criteria       15% — 2 criteria lack specificity
  ❌ Requirements Traceability   0% — No EARS requirements linked
  ❌ BDD Coverage                0% — No Gherkin scenarios
  ⚠️ Technical Considerations  10% — Architecture decisions incomplete
  ✅ Dependencies               10% — Dependencies mapped
  ❌ Test Strategy               0% — No test approach defined

💡 Recommendations:
  1. Link EARS requirements (run /formalize-ears to create them)
  2. Generate BDD scenarios (run /generate-bdd after linking requirements)
  3. Add specific, measurable acceptance criteria

═══════════════════════════════════════════════
Starting refinement — type 'skip' to skip a question, 'done' to finish
═══════════════════════════════════════════════
```

### Phase 2: Targeted Questions (Feature-Specific Categories)

Questions are organised into 6 feature-specific categories and presented one at a time. The weakest categories (lowest-scoring dimensions) are asked first. The `--focus` flag restricts questions to a single category only.

Natural language answers are accepted for all questions. After each answer, the system confirms what was captured.

| Category | When Asked | Focus |
|----------|-----------|-------|
| Acceptance Criteria | Criteria aren't testable/specific | Specificity and measurability |
| Requirements Traceability | Missing EARS requirement links | Link to EARS requirements |
| BDD Coverage | Missing/incomplete scenarios | Generate with `/generate-bdd` |
| Technical Considerations | Architecture decisions missing | API, performance, dependencies |
| Dependencies | No dependency analysis | Feature dependencies |
| Scope Within Epic | Overlap with other features | Differentiation |

#### Category 1: Acceptance Criteria

**When asked**: Acceptance criteria score < 0.8 (criteria aren't specific or measurable)

**Question**: "Your acceptance criteria could be more specific. Can you make this criterion testable with specific values?"
```
[REFINE] Current criterion: "User can log in"
         Suggestion: Add specific conditions — what constitutes valid credentials?
         What is the testable version of this criterion?

Example good answer: "User can log in with valid email (format: x@y.z) and password (8+ chars, 1 uppercase, 1 number), and the system responds within 200ms with a session token."

Type 'skip' to keep current criterion, or 'done' to end refinement.
```

#### Category 2: Requirements Traceability

**When asked**: Feature has no linked EARS requirements

**Question**: "This feature has no EARS requirements linked. Which requirements does it implement?"
```
[REFINE] No EARS requirements are linked to this feature.
         EARS requirements provide traceability from business needs to implementation.

         Do you have existing requirements to link (e.g., REQ-001, REQ-002)?
         Or should we create them? (Suggest: run /formalize-ears to generate EARS requirements)

Example good answer: "This feature implements REQ-042 (user login) and REQ-043 (session management). We also need a new requirement for password reset — please suggest one."

Type 'skip' to address later, or 'done' to end refinement.
```

#### Category 3: BDD Coverage

**When asked**: Feature has no or incomplete BDD/Gherkin scenarios

**Question**: "This feature has no BDD scenarios. Gherkin scenarios validate acceptance criteria are testable."
```
[REFINE] No BDD scenarios linked to this feature.
         BDD scenarios drive acceptance testing and validate requirements.

         Do you have existing scenarios to link (e.g., BDD-001)?
         Or should we generate them? (Suggest: run /generate-bdd to create Gherkin scenarios)

Example good answer: "Generate scenarios for the login happy path and the failed login error path. Also cover session expiry after 24 hours."

Type 'skip' to address later, or 'done' to end refinement.
```

#### Category 4: Technical Considerations

**When asked**: Architecture decisions, API design, or performance targets are missing

**Question**: "What technical decisions have been made for this feature?"
```
[REFINE] Technical considerations are incomplete.
         Document architecture decisions, API design, and performance targets.

         What are the key technical decisions for this feature?

Example good answer: "Authentication uses JWT tokens stored in httpOnly cookies. API endpoints: POST /auth/login, POST /auth/logout, POST /auth/refresh. Target: login < 200ms p95, token refresh < 50ms."

Type 'skip' to address later, or 'done' to end refinement.
```

#### Category 5: Dependencies

**When asked**: No dependency analysis exists for this feature

**Question**: "What does this feature depend on, and what depends on it?"
```
[REFINE] Feature dependency analysis is missing or incomplete.
         Map dependencies to prevent blocking and enable parallel work.

         What external systems, features, or teams does this depend on?

Example good answer: "Depends on FEAT-002 (user database schema) being complete. Blocks FEAT-004 (admin dashboard) which needs the auth API. External dependency: Redis for session storage."

Type 'skip' to address later, or 'done' to end refinement.
```

#### Category 6: Scope Within Epic

**When asked**: Feature boundary unclear or overlaps with other features in the epic

**Question**: "How does this feature differentiate from other features in the epic?"
```
[REFINE] Feature scope within the parent epic could be clearer.
         Clear boundaries prevent overlap and scope creep.

         What does this feature include/exclude relative to other features in EPIC-XXX?

Example good answer: "This feature covers authentication only — login, logout, session management. User profile editing is FEAT-003. Admin user management is FEAT-005. Social auth (OAuth) is out of scope for this release."

Type 'skip' to address later, or 'done' to end refinement.
```

### Phase 3: Change Summary and Commit

After all questions are answered (or user types 'done'):

1. **Display all changes** before writing — show a before/after comparison
2. **Show before/after completeness score** to track progress
3. **Present apply options**:
   - **Yes**: Update feature markdown in-place + push to Graphiti (if enabled)
   - **No**: Discard all changes
   - **Edit**: Manually adjust before applying
4. **Update markdown** in-place with refined content
5. **Append `refinement_history`** entry to frontmatter
6. **Push to Graphiti** if enabled (graceful degradation — if Graphiti is unavailable, the markdown update still succeeds)

#### Change Summary Output
```
═══════════════════════════════════════════════
[REFINE] Change Summary — FEAT-001
═══════════════════════════════════════════════

📊 Completeness Score: 58% → 82% (+24%)

📝 Changes Made:
  1. Acceptance Criteria: Added specific metrics to 3 criteria
  2. Requirements Traceability: Linked REQ-042, REQ-043
  3. Technical Considerations: Added JWT architecture decision

📋 Updated Sections:
  - Acceptance Criteria (3 criteria refined)
  - Requirements Traceability (2 requirements linked)
  - Technical Considerations (API endpoints, performance targets)

🧠 Graphiti Sync: ✅ Ready to push (or ⚠️ Skipped — Graphiti not configured)

Apply changes? [Yes / No / Edit]
═══════════════════════════════════════════════
```

#### Refinement History Schema

Appended to feature frontmatter after each refinement session:

```yaml
refinement_history:
  - date: 2026-02-19T14:30:00Z
    score_before: 58
    score_after: 82
    dimensions_changed:
      - acceptance_criteria
      - requirements_traceability
      - technical_considerations
    questions_asked: 5
    questions_skipped: 1
```

## Feature Completeness Score (7-Dimension Model)

The completeness score uses the same 7-dimension model defined in the requirements-analyst agent. Each dimension receives a score from 0.0 to 1.0 and is weighted:

| Dimension | Weight | Scoring Guidance |
|---|---|---|
| Scope Within Epic | 10% | Clear feature boundary within parent epic |
| Acceptance Criteria | 25% | Specific, testable conditions for feature completion |
| Requirements Traceability | 20% | EARS requirements linked to this feature |
| BDD Coverage | 15% | Gherkin scenarios covering acceptance criteria |
| Technical Considerations | 15% | Architecture, performance, security notes |
| Dependencies | 10% | Feature-level dependency mapping |
| Test Strategy | 5% | Testing approach and coverage expectations |

**Total: 100%**

### Score Interpretation

| Score Range | Interpretation |
|---|---|
| 80-100% | Well-specified, ready for implementation |
| 60-79% | Adequate, refinement recommended |
| 40-59% | Needs significant refinement |
| 0-39% | Incomplete, refinement required |

### Calculation

Final score = sum of (dimension_weight × dimension_score) across all 7 dimensions.

Each dimension receives partial credit:
- **1.0**: Fully addressed with specific, measurable content
- **0.5**: Partially addressed or lacking specificity
- **0.0**: Not addressed

## Options

### Focus Flag

The `--focus` flag restricts questions to a single category only, skipping all other categories:

```bash
/feature-refine FEAT-001 --focus acceptance      # Acceptance Criteria only
/feature-refine FEAT-001 --focus traceability     # Requirements Traceability only
/feature-refine FEAT-001 --focus bdd              # BDD Coverage only
/feature-refine FEAT-001 --focus technical        # Technical Considerations only
/feature-refine FEAT-001 --focus dependencies     # Dependencies only
/feature-refine FEAT-001 --focus scope            # Scope Within Epic only
```

### Quick Mode

The `--quick` flag skips interactive prompts and applies AI-suggested improvements automatically:

```bash
/feature-refine FEAT-001 --quick
```

## Cross-Command Integration

The `/feature-refine` command integrates with other require-kit commands:

- **`/formalize-ears`**: When Requirements Traceability is low, suggest running `/formalize-ears` to create linked EARS requirements for the feature
- **`/generate-bdd`**: When BDD Coverage is low, suggest running `/generate-bdd` to generate Gherkin scenarios from existing requirements
- **Parent epic completeness**: Display the parent epic's completeness score for context, so refinement decisions account for epic-level priorities

### Integration Examples
```bash
# After refining requirements traceability
💡 Suggestion: Run /formalize-ears to create EARS requirements for this feature

# After identifying missing BDD coverage
💡 Suggestion: Run /generate-bdd FEAT-001 to generate Gherkin scenarios

# Parent epic context shown in Phase 1
📋 Parent Epic: EPIC-001 — User Management (72% complete)
```

## Graphiti Integration

When Graphiti is configured, feature refinement pushes updated feature data as an episode:

### Feature Episode Schema

```python
{
    "name": f"Feature: {feature_title}",
    "episode_body": feature_markdown_content,
    "group_id": f"{project}__requirements",
    "source": EpisodeType.text,
    "source_description": f"RequireKit feature {feature_id} (refined)",
    "reference_time": datetime.now(),
    "_metadata": {
        "entity_type": "feature",
        "feature_id": feature_id,
        "epic_id": parent_epic_id,
        "status": feature_status,
        "priority": feature_priority,
        "completeness_score": updated_score,
        "last_refined": refinement_timestamp,
        "acceptance_criteria_count": ac_count,
        "bdd_scenario_ids": linked_bdd_ids,
        "requirement_ids": linked_requirement_ids,
        "task_count": task_count
    }
}
```

### Graceful Degradation

Graphiti integration uses graceful degradation:
- If Graphiti is available: push episode after markdown update
- If Graphiti is not configured: skip push, display `⚠️ Skipped — Graphiti not configured`
- If Graphiti push fails: log warning, markdown update still succeeds
- Feature refinement never fails due to Graphiti errors

## UX Design

The `/feature-refine` command follows the same UX patterns as `/epic-refine`:

### Mode Clarity
- **[REFINE] prefix**: All prompts and outputs use the `[REFINE]` prefix for mode clarity
- **Visual separators**: Use `═══` separators to clearly mark the start and end of refinement phases

### Question Presentation
- **One at a time**: Questions are always presented one at a time (never a list)
- **Skip**: User can type `skip` to move to the next question
- **Done**: User can type `done` to end the refinement session at any point
- **Natural language**: All answers accept natural language — bullet lists, freeform text, or structured input

### Feedback
- **Confirm capture**: After each answer, confirm what was captured
- **Before/after scores**: Show completeness scores before and after refinement
- **Change summary**: Always display a change summary before applying updates

## Output Format

### Refinement Complete
```
═══════════════════════════════════════════════
[REFINE] Refinement Complete — FEAT-001
═══════════════════════════════════════════════

📊 Feature Completeness: 58% → 82% (+24%)

📝 Sections Updated:
  - Acceptance Criteria (3 criteria refined)
  - Requirements Traceability (2 requirements linked)
  - Technical Considerations (API endpoints added)

🧠 Graphiti Sync: ✅ Synced (or ⚠️ Skipped — Graphiti not configured)

📁 Updated File: docs/features/active/FEAT-001-user-authentication.md

Next Steps:
1. Create linked requirements: /formalize-ears
2. Generate BDD scenarios: /generate-bdd FEAT-001
3. View feature status: /feature-status FEAT-001
4. View epic context: /hierarchy-view EPIC-001
```

### No Changes Made
```
═══════════════════════════════════════════════
[REFINE] No Changes — FEAT-001
═══════════════════════════════════════════════

📊 Feature Completeness: 82% (unchanged)

No refinement changes were applied.

Next Steps:
1. Review feature: /feature-status FEAT-001
2. Generate tasks: /feature-generate-tasks FEAT-001
```

## Validation

Before starting refinement:
- ✅ Feature ID must exist in `docs/features/`
- ✅ Feature file must have valid YAML frontmatter
- ✅ Parent epic must exist (for context display)
- ✅ `--focus` value must be one of: `acceptance`, `traceability`, `bdd`, `technical`, `dependencies`, `scope`

## File Organization

Feature files are loaded from and updated at:
```
docs/
├── features/
│   ├── active/
│   │   ├── FEAT-001-user-authentication.md
│   │   └── FEAT-002-user-profile.md
│   ├── in_progress/
│   ├── completed/
│   └── cancelled/
```

## Best Practices

1. **Refine early**: Refine features while requirements context is fresh
2. **Focus on weak areas**: Use `--focus` to target the lowest-scoring dimensions
3. **Link requirements first**: Run `/formalize-ears` before BDD generation for proper traceability
4. **Review parent epic**: Consider epic-level priorities when refining feature scope
5. **Iterate**: Multiple short refinement sessions are better than one long session
6. **Track progress**: Compare before/after scores to measure refinement effectiveness
