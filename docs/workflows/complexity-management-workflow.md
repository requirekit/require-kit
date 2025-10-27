# Complexity Management Workflow

**Purpose**: Complete guide to task complexity evaluation, automatic breakdown, and intelligent routing in the agentecflow system.

**Learn complexity management in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Get Started Immediately

```bash
# System automatically evaluates complexity when creating tasks
/task-create "Implement user authentication" requirements:[REQ-001]

# If complex (≥7), system suggests breakdown:
# → Accept breakdown: 5 smaller tasks created
# → Reject breakdown: Single complex task created

# During implementation, complexity determines review mode
/task-work TASK-001
# → Simple (1-3): Auto-proceeds to implementation
# → Medium (4-6): 30-second optional checkpoint
# → Complex (7-10): Mandatory human review
```

**That's it!** Complexity evaluation happens automatically.

**Learn More**: See "Core Concepts" below for two-stage evaluation and scoring details.

---

## Core Concepts (10 minutes)

### Two-Stage Complexity System

The system evaluates complexity at TWO distinct stages with different purposes:

#### Stage 1: Upfront Estimation (During `/task-create`)

**When**: Before work starts, during task creation

**Purpose**: Decide if task should be split before implementation begins

**Input**: Task title, description, requirements (EARS notation)

**Threshold**: Complexity ≥7 triggers split recommendations

**Example**:
```bash
/task-create "Implement event sourcing for orders" requirements:[REQ-042,REQ-043]

# System evaluates:
ESTIMATED COMPLEXITY: 9/10 (Very Complex)

RECOMMENDATION: Consider splitting this task

SUGGESTED BREAKDOWN:
1. TASK-005.1: Design Event Sourcing architecture (5/10)
2. TASK-005.2: Implement EventStore infrastructure (6/10)
3. TASK-005.3: Implement Order aggregate with events (5/10)

OPTIONS:
[S]plit - Create 3 subtasks (recommended)
[C]reate - Create as-is (complexity 9/10)
[M]odify - Adjust scope
```

#### Stage 2: Implementation Planning (During `/task-work` Phase 2.7)

**When**: After implementation plan created, before coding begins

**Purpose**: Decide review mode (auto-proceed/quick/full)

**Input**: Implementation plan (files, patterns, risks, dependencies)

**Threshold**: Complexity ≥7 requires mandatory human checkpoint (Phase 2.6)

**Example**:
```bash
/task-work TASK-042

# After planning (Phase 2):
Phase 2.7: Complexity Evaluation

COMPLEXITY SCORE: 5/10 (Medium)
FILES: 3 files to create
PATTERNS: Repository, Service (familiar)
DEPENDENCIES: 1 new package
REVIEW MODE: QUICK_OPTIONAL

[Quick checkpoint - Press ENTER to review or wait 30s to auto-proceed]
```

### Complexity Scoring (0-10 Scale)

See [common-thresholds.md](../shared/common-thresholds.md#complexity-scoring-thresholds) for detailed scoring tables.

**Summary**:
- **1-3 (Simple)**: 🟢 Auto-proceed, no review
- **4-6 (Medium)**: 🟡 Quick checkpoint, 30s timeout
- **7-10 (Complex)**: 🔴 Mandatory review or breakdown

### Review Modes by Complexity

**AUTO_PROCEED** (Complexity 1-3):
- No human checkpoint required
- System proceeds directly to Phase 3 (implementation)
- Best for: Simple bug fixes, minor updates, straightforward features

**QUICK_OPTIONAL** (Complexity 4-6):
- Optional 30-second checkpoint
- Press ENTER to review, or auto-proceed after timeout
- Best for: Standard features with clear approach

**FULL_REQUIRED** (Complexity 7-10):
- Mandatory human review
- No timeout, waits for explicit approval
- Best for: Complex features, high-risk changes, unfamiliar patterns

### Common Use Cases

#### Use Case 1: Simple Task (Auto-Proceed)

```bash
/task-work TASK-010  # "Update user profile validation message"

# Phase 2.7 Output:
Complexity: 2/10 (Simple)
Review Mode: AUTO_PROCEED
Files: 1 file to modify
Estimated: 30 minutes

Automatically proceeding to implementation...
```

#### Use Case 2: Medium Task (Quick Checkpoint)

```bash
/task-work TASK-025  # "Add email notification service"

# Phase 2.7 Output:
Complexity: 5/10 (Medium)
Review Mode: QUICK_OPTIONAL
Files: 3 files to create
Estimated: 4 hours

Quick Checkpoint (auto-proceed in 30s):
[ENTER] Review plan  [c] Cancel  [Auto-proceed in: 25s]

# Wait 30s → Auto-proceeds
# OR Press ENTER → Escalates to full review
```

#### Use Case 3: Complex Task (Mandatory Review)

```bash
/task-work TASK-042  # "Implement OAuth2 authentication flow"

# Phase 2.7 Output:
Complexity: 8/10 (Complex)
Review Mode: FULL_REQUIRED
Triggers: Security keywords detected

FULL REVIEW REQUIRED

Complexity Breakdown:
- Files: 6 files to create (3 points)
- Patterns: OAuth2, Token Management (unfamiliar, 2 points)
- Risk: High (security, authentication) (3 points)

[A]pprove  [M]odify  [V]iew Full Plan  [C]ancel

Your choice: _
```

**Learn More**: See "Complete Reference" below for all complexity factors and breakdown strategies.

---

## Complete Reference (30+ minutes)

### Complexity Factor Breakdown

See [common-thresholds.md](../shared/common-thresholds.md#complexity-factor-scoring) for detailed factor scoring.

The system evaluates FOUR factors to calculate total complexity score:

#### Factor 1: File Complexity (0-3 points)

**Simple change** (1 file): +1 point
- Single file modification
- Isolated component change
- Bug fix in one location

**Moderate change** (2-5 files): +2 points
- Multiple related files
- Feature spanning several components
- Service with tests

**Complex change** (6+ files): +3 points
- Architecture-level changes
- Multiple subsystems affected
- New feature with extensive integration

#### Factor 2: Pattern Familiarity (0-2 points)

**Familiar patterns** (all known): +0 points
- Using established project patterns
- Standard CRUD operations
- Common design patterns (Repository, Factory, etc.)

**Mixed familiarity** (some unfamiliar): +1 point
- New pattern being introduced
- Pattern used differently than before
- Adapting external pattern to project

**Unfamiliar patterns** (new to project): +2 points
- Completely new architectural approach
- Experimental pattern
- Complex external pattern (CQRS, Event Sourcing, etc.)

#### Factor 3: Risk Assessment (0-3 points)

**Low risk**: +0 points
- Internal changes only
- Well-tested area
- Easy to rollback

**Medium risk** (external dependencies, moderate changes): +1 point
- External API integration
- Moderate database changes
- Third-party library integration

**High risk** (security, breaking changes, data migration): +3 points
- Security-sensitive changes (auth, encryption)
- Breaking API changes
- Database migrations with data
- Production hotfixes

#### Factor 4: External Dependencies (0-2 points)

**No dependencies**: +0 points
- Using only existing project code
- No new packages required

**1-2 dependencies**: +1 point
- Adding 1-2 new npm/nuget packages
- Minor dependency version updates

**3+ dependencies**: +2 points
- Significant new dependencies
- Major version upgrades
- Complex dependency chains

### Example Complexity Calculations

#### Example 1: Simple Task (Score: 2/10)

**Task**: "Update user profile validation message"

**Calculation**:
```
File Complexity:     1 file = +1 point
Pattern Familiarity: Familiar validation = +0 points
Risk Level:          Low (UI text change) = +0 points
Dependencies:        No new deps = +0 points
─────────────────────────────────────────
TOTAL SCORE: 1/10 → Rounded to 2/10 (Simple)
```

**Review Mode**: AUTO_PROCEED

#### Example 2: Medium Task (Score: 5/10)

**Task**: "Add email notification service"

**Calculation**:
```
File Complexity:     3 files (service, tests, config) = +2 points
Pattern Familiarity: Familiar service pattern = +0 points
Risk Level:          Medium (external email API) = +1 point
Dependencies:        2 new packages (email lib, templates) = +1 point
─────────────────────────────────────────
TOTAL SCORE: 4/10 → Rounded to 5/10 (Medium)
```

**Review Mode**: QUICK_OPTIONAL

#### Example 3: Complex Task (Score: 8/10)

**Task**: "Implement OAuth2 authentication flow"

**Calculation**:
```
File Complexity:     6 files (auth, tokens, middleware, tests) = +3 points
Pattern Familiarity: Unfamiliar OAuth2 pattern = +2 points
Risk Level:          High (security, authentication) = +3 points
Dependencies:        No new deps (built-in) = +0 points
─────────────────────────────────────────
TOTAL SCORE: 8/10 (Complex)
```

**Review Mode**: FULL_REQUIRED

### Automatic Task Breakdown

When complexity ≥7, the system suggests breaking down into smaller subtasks.

#### Breakdown Strategies

See [common-thresholds.md](../shared/common-thresholds.md#breakdown-thresholds) for breakdown thresholds.

**1. No Breakdown** (Complexity 1-3):
```
Original: TASK-010 - Update validation
Breakdown: None needed
Rationale: Simple, single-file change
```

**2. Logical Breakdown** (Complexity 4-6):
```
Original: TASK-020 - Build user dashboard
Breakdown:
├── TASK-020.1: Dashboard UI components
├── TASK-020.2: Dashboard API endpoints
├── TASK-020.3: Dashboard data models
└── TASK-020.4: Dashboard tests
Rationale: Split by logical layers
```

**3. File-Based Breakdown** (Complexity 7-8):
```
Original: TASK-030 - Payment processing system
Breakdown:
├── TASK-030.1: Payment models (3 files)
├── TASK-030.2: Payment gateway (2 files)
├── TASK-030.3: Payment service (2 files)
├── TASK-030.4: Payment API (2 files)
└── TASK-030.5: Payment tests (3 files)
Rationale: Group related files (2-3 files per subtask)
```

**4. Phase-Based Breakdown** (Complexity 9-10):
```
Original: TASK-040 - Multi-tenant architecture
Breakdown:
├── TASK-040.1: Phase 1 - Foundation (models, interfaces)
├── TASK-040.2: Phase 2 - Core Implementation (business logic)
├── TASK-040.3: Phase 3 - Integration (database, APIs)
├── TASK-040.4: Phase 4 - Advanced Features (optimization)
└── TASK-040.5: Phase 5 - Testing & Documentation
Rationale: Sequential implementation phases
```

### Force-Review Triggers

See [common-thresholds.md](../shared/common-thresholds.md#force-review-triggers) for complete trigger list.

Tasks with ANY of these triggers require FULL_REQUIRED review mode regardless of complexity score:

**Security Triggers**:
- Keywords: auth, password, encryption, token, secret, credential
- Changes to authentication/authorization code
- Security-sensitive API endpoints

**Breaking Change Triggers**:
- Public API modifications
- Database schema changes
- Configuration file changes affecting all environments

**Production Triggers**:
- Hotfix tags
- Production deployment flags
- Emergency patches

**User Flags**:
- `--review` command-line option
- Manual escalation request

### Feature-Level Complexity Control

The `/feature-generate-tasks` command integrates complexity evaluation to prevent oversized tasks during generation.

**Feature**: Complexity evaluation during task generation (TASK-008)

**Key Benefits**:
- Catches complex tasks BEFORE they're created
- Automatic breakdown during generation (not mid-implementation)
- Consistent task sizing across feature
- Better sprint planning with right-sized tasks

**Example Usage**:
```bash
/feature-generate-tasks FEAT-001 --threshold 6

# Output:
📋 Complexity-Aware Task Generation

Original Proposed Tasks: 3
After Complexity Evaluation: 8 tasks (5 breakdowns)

🔴 TASK-045 (Original): Complete authentication backend
   Complexity: 9/10 - Auto-broken down into:
   ├── TASK-045.1: JWT authentication endpoint (5/10)
   ├── TASK-045.2: OAuth2 provider integration (6/10)
   └── TASK-045.3: Session management system (5/10)

✅ All generated tasks now have complexity ≤6 (threshold)

📊 Complexity Analysis
Total Tasks: 8 (after breakdown from 3 original)
Complexity Distribution:
  🟢 Simple (1-3): 0 tasks
  🟡 Medium (4-6): 8 tasks
  🔴 Complex (7-10): 0 tasks (all broken down)
Average Complexity: 5.2
Recommended for immediate implementation: ✅ All tasks ready
```

**Interactive Mode**:
```bash
/feature-generate-tasks FEAT-001 --interactive

# Prompts for threshold customization
Enter breakdown threshold (1-10) [default: 7]: 6
Enter max subtasks per task [default: 5]: 4

# Shows breakdown suggestions for borderline tasks
# Allows manual approval/rejection of automatic breakdowns
```

**Threshold Configuration**:
```bash
# Use custom threshold for feature
/feature-generate-tasks FEAT-001 --threshold 8

# Skip complexity check (advanced users)
/feature-generate-tasks FEAT-001 --skip-complexity-check
```

**Integration with Two-Stage System**:
- **Stage 0.5 (Feature Generation)**: Evaluate complexity during task proposal, break down before creation
- **Stage 1 (Task Creation)**: Re-evaluate complexity on manually created tasks, suggest splits
- **Stage 2 (Implementation Planning)**: Final complexity check with detailed plan, determine review mode

This creates a **three-tier safety net** preventing oversized tasks at every creation point.

### Customizing Complexity Thresholds

Override default thresholds in `.claude/settings.json`:

```json
{
  "complexity": {
    "breakdown_threshold": 6,
    "auto_proceed_max": 3,
    "quick_review_max": 6,
    "full_review_min": 7,
    "max_subtasks": 5
  }
}
```

**Command-line overrides**:
```bash
# Use custom threshold for this task
/task-create "Title" --complexity-threshold 8

# Skip complexity check (advanced users only)
/task-work TASK-001 --skip-complexity-check

# Force full review regardless of score
/task-work TASK-001 --review
```

### Task Metadata Schema

Complexity evaluation results are saved to task frontmatter:

```yaml
complexity_evaluation:
  score: 7
  level: "complex"
  review_mode: "FULL_REQUIRED"
  evaluated_at: "2025-10-12T14:30:00Z"
  factor_scores:
    - factor: "file_complexity"
      score: 2
      max_score: 3
      justification: "4-6 files to create"
    - factor: "pattern_familiarity"
      score: 1
      max_score: 2
      justification: "Using familiar REST API patterns"
    - factor: "risk_level"
      score: 2
      max_score: 3
      justification: "External API dependency, moderate risk"
    - factor: "dependencies"
      score: 2
      max_score: 2
      justification: "3+ new dependencies required"
```

---

## Examples (Real-World Scenarios)

### Example 1: Simple Bug Fix (AUTO_PROCEED)

**Task**: TASK-101 - Fix typo in error message

**Complexity Evaluation**:
```
Files: 1 (error_messages.py)
Patterns: String replacement (familiar)
Risk: Low (non-breaking change)
Dependencies: None

Score: 1/10 (Simple)
Review Mode: AUTO_PROCEED
```

**Workflow**:
```bash
/task-work TASK-101

# System output:
Phase 2.7: Complexity Evaluation Complete
Score: 1/10 (Simple)
Auto-proceeding to implementation (no review needed)...

Phase 3: Implementation
[Implementation happens automatically]
```

### Example 2: Standard Feature (QUICK_OPTIONAL)

**Task**: TASK-202 - Add CSV export functionality

**Complexity Evaluation**:
```
Files: 3 (export_service.py, csv_formatter.py, tests)
Patterns: Export pattern (familiar), CSV library (familiar)
Risk: Low (read-only operation)
Dependencies: 1 (csv library already in project)

Score: 4/10 (Medium)
Review Mode: QUICK_OPTIONAL
```

**Workflow**:
```bash
/task-work TASK-202

# System output:
Phase 2.7: Complexity Evaluation Complete
Score: 4/10 (Medium)

Quick Checkpoint (auto-proceed in 30s):
Files: 3 files to create
Estimated: 3 hours
Tests: Included

[ENTER] Review  [c] Cancel  [Auto-proceed in: 28s]

# User waits 30s → Auto-proceeds to Phase 3
```

### Example 3: Complex Architecture Change (FULL_REQUIRED)

**Task**: TASK-303 - Migrate to microservices architecture

**Complexity Evaluation**:
```
Files: 25+ files (multiple services, databases, APIs)
Patterns: Microservices (unfamiliar), Event-Driven (new)
Risk: High (breaking changes, data migration)
Dependencies: 8+ new packages

Score: 10/10 (Very Complex)
Review Mode: FULL_REQUIRED
Triggers: Breaking changes, schema changes
```

**Workflow**:
```bash
/task-work TASK-303

# System output:
Phase 2.7: Complexity Evaluation Complete
Score: 10/10 (Very Complex)

⚠️  RECOMMENDATION: This task should be broken down

Complexity Factors:
🔴 Files: 25+ files (max complexity)
🔴 Patterns: Microservices, Event-Driven (unfamiliar)
🔴 Risk: High (breaking changes, data migration)
🔴 Dependencies: 8+ new packages

FULL REVIEW REQUIRED (no auto-proceed)

Options:
[A]pprove - Proceed with current scope (not recommended)
[S]plit - Break down into subtasks (RECOMMENDED)
[C]ancel - Cancel and redesign

Your choice: _
```

### Example 4: Security-Sensitive Task (Force-Review Trigger)

**Task**: TASK-404 - Update password hashing algorithm

**Complexity Evaluation**:
```
Files: 2 (auth_service.py, tests)
Patterns: Password hashing (familiar)
Risk: High (security-sensitive)
Dependencies: 1 (bcrypt library)

Base Score: 5/10 (Medium)
Force Trigger: Security keyword ("password")
Review Mode: FULL_REQUIRED (escalated from QUICK_OPTIONAL)
```

**Workflow**:
```bash
/task-work TASK-404

# System output:
Phase 2.7: Complexity Evaluation Complete
Base Score: 5/10 (Medium)

🔒 SECURITY TRIGGER DETECTED

Force-Review Trigger: Security keyword ("password")
Review Mode: FULL_REQUIRED (escalated)

This task requires mandatory review regardless of complexity score.

Security Considerations:
- Password storage changes
- Potential impact on existing users
- Requires security review

[A]pprove  [M]odify  [C]ancel

Your choice: _
```

---

## FAQ

### Q: Why two stages of complexity evaluation?

**A**: Stage 1 (during task creation) helps prevent oversized tasks before work begins. Stage 2 (during implementation planning) routes to appropriate review mode based on actual implementation details. This two-stage approach catches complexity issues early AND adapts to implementation realities.

### Q: Can I customize complexity thresholds per project?

**A**: Yes, customize thresholds in `.claude/settings.json`:
```json
{
  "complexity": {
    "breakdown_threshold": 6,
    "auto_proceed_max": 3
  }
}
```

See [Customizing Complexity Thresholds](#customizing-complexity-thresholds) above.

### Q: What if I disagree with the complexity score?

**A**: You have several options:
1. **Use `--complexity-threshold` flag** to adjust threshold for single task
2. **Choose [M]odify during checkpoint** to adjust task scope
3. **Use `--skip-complexity-check`** to bypass evaluation (advanced users)
4. **Update project settings** for permanent threshold changes

### Q: How does complexity affect team velocity?

**A**: Teams using complexity management report:
- **2-4 hours saved per complex task** detected early
- **80% reduction in mid-implementation splits**
- **Average complexity of 4-5** (optimal range)
- **Higher developer confidence** in task sizing

### Q: What happens if I force a complex task without breakdown?

**A**: The system will:
1. Warn you about high complexity
2. Require FULL_REQUIRED review mode
3. Track time spent for velocity analysis
4. If task takes >2x estimate, suggest retroactive breakdown for learning

### Q: Can complexity evaluation handle multi-stack projects?

**A**: Yes, complexity evaluation is stack-agnostic. File counts, pattern familiarity, and risk levels apply across all technology stacks. Stack-specific agents provide appropriate implementation guidance regardless of complexity.

---

## Related Documentation

- [Design-First Workflow](./design-first-workflow.md) - Separate design and implementation for complex tasks
- [Feature Generate Tasks](../../installer/global/commands/feature-generate-tasks.md) - Automatic task generation with complexity control
- [Task Work Command](../../installer/global/commands/task-work.md) - Phase 2.7 complexity evaluation details
- [Common Thresholds](../shared/common-thresholds.md) - Shared quality threshold definitions

---

**Last Updated**: 2025-10-12
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
