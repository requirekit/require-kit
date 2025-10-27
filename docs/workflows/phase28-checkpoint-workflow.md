# Phase 2.8 Checkpoint Workflow

## Overview

Phase 2.8 is the **human checkpoint** in the task-work implementation workflow where developers review the generated implementation plan before code execution begins. This checkpoint provides an enhanced display of plan details, enabling informed decision-making about whether to proceed, modify, or cancel implementation.

**Key Features:**
- **Enhanced Plan Summary**: Displays files, dependencies, risks, and effort estimates in digestible format
- **Intelligent Formatting**: Truncates long lists while showing critical information
- **Complexity-Based Triggering**: Checkpoint behavior adapts based on task complexity
- **Integration with Markdown Plans**: Works seamlessly with human-readable plan format

**When This Phase Executes:**
- After Phase 2 (Implementation Planning) completes
- After Phase 2.7 (Complexity Evaluation) determines review mode
- Before Phase 3 (Implementation) begins

**Purpose:**
- Validate plan accuracy and completeness
- Catch design issues before implementation
- Provide opportunity for plan adjustments
- Enable human oversight at critical decision point

## Prerequisites

**Required:**
- Task with completed implementation plan (Phase 2)
- Understanding of review modes (AUTO_PROCEED, QUICK_OPTIONAL, FULL_REQUIRED)

**Recommended:**
- Familiarity with Markdown plan format
- Understanding of task complexity scoring (0-10 scale)
- Awareness of modification options (see [Plan Modification Workflow](./plan-modification-workflow.md))

**System State:**
- Task in `IN_PROGRESS` state
- Implementation plan saved (`.claude/task-plans/{task_id}-implementation-plan.md`)
- Complexity evaluation complete (Phase 2.7)

## Enhanced Display Features

### Plan Summary Sections

The checkpoint displays four key sections of the implementation plan:

#### 1. Files to Create/Modify
**Format:**
```
FILES TO CREATE/MODIFY:
  📄 src/auth/jwt_service.py (80 lines)
     Purpose: JWT token generation and validation

  📄 src/api/auth_endpoints.py (60 lines)
     Purpose: Authentication API endpoints

  📄 tests/test_jwt_service.py (45 lines)
     Purpose: Unit tests for JWT service

  📄 tests/test_auth_endpoints.py (35 lines)
     Purpose: Integration tests for auth API

  📄 src/auth/__init__.py (10 lines)
     Purpose: Package initialization

  ... and 3 more files
```

**Display Rules:**
- First 5 files shown with full details
- Remaining files shown as count ("+N more files")
- Files sorted by estimated LOC (largest first)
- Purpose included for clarity

#### 2. Dependencies
**Format:**
```
DEPENDENCIES:
  📦 pyjwt (2.8.0+)
     Purpose: JWT token creation and validation

  📦 python-dotenv (1.0.0+)
     Purpose: Environment variable management

  📦 redis (5.0.0+)
     Purpose: Token blacklist storage

  ... and 2 more dependencies
```

**Display Rules:**
- First 3 dependencies shown with versions
- Remaining shown as count ("+N more dependencies")
- Purpose/justification included
- External services highlighted separately

#### 3. Risks and Mitigations
**Format:**
```
RISKS IDENTIFIED:
  🔴 CRITICAL: JWT secret management
     Mitigation: Use environment variables, never commit secrets

  🟡 MEDIUM: Token refresh race conditions
     Mitigation: Implement token versioning and atomic updates

  🟢 LOW: Performance overhead of token validation
     Mitigation: Add Redis caching layer for decoded tokens
```

**Display Rules:**
- ALL risks shown (not truncated)
- Sorted by severity: CRITICAL → HIGH → MEDIUM → LOW
- Severity color-coded (🔴 🟠 🟡 🟢)
- Mitigation strategy for each risk

#### 4. Effort Estimates
**Format:**
```
EFFORT ESTIMATE:
  📊 Complexity: 7/10 (Complex)
  ⏱️  Duration: 4 hours
  📝 Lines of Code: ~287
  📈 Confidence: Medium (multiple new dependencies)
```

**Display Rules:**
- Complete effort section (never truncated)
- Complexity score with level (Simple/Medium/Complex/Very Complex)
- Estimated duration and LOC
- Confidence level and justification

### Review Mode Display

The checkpoint displays different information based on review mode:

#### AUTO_PROCEED (Complexity 1-3)
**No checkpoint displayed** - system proceeds directly to implementation.

**Rationale:** Simple tasks with clear approach don't need human review.

#### QUICK_OPTIONAL (Complexity 4-6)
```
═══════════════════════════════════════════════════════
PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT (QUICK REVIEW)
═══════════════════════════════════════════════════════

[Plan summary displayed]

⏱️  AUTO-PROCEED in 30 seconds (press any key to review)

OPTIONS:
[A] Approve - Proceed to implementation
[M] Modify - Edit plan interactively
[V] View - Show full plan details
[C] Cancel - Return to backlog

Your choice (A/M/V/C):
```

**Behavior:**
- 30-second countdown timer
- Auto-proceeds if no input
- Can interrupt timer to review/modify

#### FULL_REQUIRED (Complexity 7-10)
```
═══════════════════════════════════════════════════════
PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT (FULL REVIEW)
═══════════════════════════════════════════════════════

[Plan summary displayed]

⚠️  MANDATORY REVIEW REQUIRED (Complexity 7/10)

OPTIONS:
[A] Approve - Proceed to implementation
[M] Modify - Edit plan interactively
[V] View - Show full plan details
[S] Simplify - Break down into smaller tasks
[C] Cancel - Return to backlog

Your choice (A/M/V/S/C):
```

**Behavior:**
- No timeout - waits for human input
- Additional [S]implify option for task breakdown
- Mandatory review for complex tasks

## Step-by-Step Workflow

### Step 1: Task-Work Executes Phase 2
```bash
/task-work TASK-042
```

System generates implementation plan and saves to:
`.claude/task-plans/TASK-042-implementation-plan.md`

### Step 2: System Evaluates Complexity (Phase 2.7)

```
COMPLEXITY EVALUATION:
  Score: 7/10 (Complex)
  Review Mode: FULL_REQUIRED

COMPLEXITY FACTORS:
  🔴 Files: 8 files to create (3 points)
  🟡 Patterns: Mixed familiar/unfamiliar (1 point)
  🔴 Risk: Security-sensitive (JWT management) (3 points)
  🟢 Dependencies: 3 new dependencies (0 points)
```

### Step 3: Checkpoint Triggered (if Required)

Based on complexity score:
- **1-3**: No checkpoint (AUTO_PROCEED)
- **4-6**: Quick checkpoint with 30s timeout
- **7-10**: Full mandatory checkpoint

### Step 4: Plan Summary Displayed

System formats and displays plan summary with:
- Files (first 5, truncated if more)
- Dependencies (first 3, truncated if more)
- Risks (all, sorted by severity)
- Effort (complete estimate)

### Step 5: Human Reviews Information

Developer examines:
- ✅ Are all necessary files included?
- ✅ Are dependencies correct and minimal?
- ✅ Are risks identified and mitigated?
- ✅ Is effort estimate reasonable?

### Step 6: Human Chooses Action

Available options:
- **[A] Approve**: Plan looks good, proceed
- **[M] Modify**: Make adjustments (see [Plan Modification Workflow](./plan-modification-workflow.md))
- **[V] View**: Show full plan in default editor
- **[S] Simplify**: Break down task (complexity 7-10 only)
- **[C] Cancel**: Major issues, return to backlog

## Decision Points

### When to Approve

**Approve when:**
- ✅ All necessary files are included
- ✅ Dependencies are correct and justified
- ✅ Risks are identified with reasonable mitigations
- ✅ Effort estimate aligns with task complexity
- ✅ No obvious design flaws or missing components

**Action:** Select `[A] Approve` to proceed to Phase 3 (Implementation)

### When to Modify

**Modify when:**
- ⚠️ Missing 1-2 files (e.g., forgot test file)
- ⚠️ Unnecessary dependency included
- ⚠️ Risk missing or severity incorrect
- ⚠️ Effort estimate slightly off

**Action:** Select `[M] Modify` to enter interactive modification mode (see [Plan Modification Workflow](./plan-modification-workflow.md))

### When to View Full Plan

**View when:**
- 🔍 Need to see complete file list (truncated display)
- 🔍 Want to review full dependency details
- 🔍 Need to examine implementation phases
- 🔍 Truncation hides critical information

**Action:** Select `[V] View` to open full Markdown plan in default editor

### When to Simplify

**Simplify when:**
- 🔴 Complexity 7-10 feels too large
- 🔴 Multiple unrelated concerns in one task
- 🔴 Clear logical breakpoints exist
- 🔴 Effort estimate exceeds comfort level

**Action:** Select `[S] Simplify` to get task breakdown suggestions

### When to Cancel

**Cancel when:**
- ❌ Major design flaws identified
- ❌ Wrong approach entirely
- ❌ Missing critical requirements
- ❌ Need to rethink architecture

**Action:** Select `[C] Cancel` to return task to backlog with notes

## Examples

### Example 1: Simple Task (AUTO_PROCEED)

**Task:** Add logging to existing function

**Complexity:** 2/10 (Simple)

**Result:**
```
COMPLEXITY: 2/10 (Simple)
REVIEW MODE: AUTO_PROCEED

Proceeding directly to implementation...
```

**No checkpoint displayed** - system proceeds to Phase 3.

---

### Example 2: Medium Task (QUICK_OPTIONAL)

**Task:** Implement user profile update endpoint

**Complexity:** 5/10 (Medium)

**Checkpoint Display:**
```
═══════════════════════════════════════════════════════
PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT (QUICK REVIEW)
═══════════════════════════════════════════════════════

TASK: TASK-042 - Implement user profile update endpoint

COMPLEXITY: 5/10 (Medium)

FILES TO CREATE/MODIFY:
  📄 src/api/profile_endpoints.py (85 lines)
     Purpose: Profile update API endpoint

  📄 src/services/profile_service.py (120 lines)
     Purpose: Profile validation and update logic

  📄 tests/test_profile_endpoints.py (60 lines)
     Purpose: Integration tests for profile API

DEPENDENCIES:
  📦 pydantic (2.0.0+)
     Purpose: Request/response validation

RISKS IDENTIFIED:
  🟡 MEDIUM: Concurrent profile updates
     Mitigation: Optimistic locking with version field

EFFORT ESTIMATE:
  📊 Complexity: 5/10 (Medium)
  ⏱️  Duration: 2.5 hours
  📝 Lines of Code: ~265
  📈 Confidence: High (familiar patterns)

⏱️  AUTO-PROCEED in 30 seconds (press any key to review)

OPTIONS:
[A] Approve - Proceed to implementation
[M] Modify - Edit plan interactively
[V] View - Show full plan details
[C] Cancel - Return to backlog

Your choice (A/M/V/C):
```

**Developer Action:** Reviews quickly, presses `A` to approve.

**Alternative:** If no input, auto-proceeds after 30 seconds.

---

### Example 3: Complex Task (FULL_REQUIRED)

**Task:** Implement JWT authentication system

**Complexity:** 7/10 (Complex)

**Checkpoint Display:**
```
═══════════════════════════════════════════════════════
PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT (FULL REVIEW)
═══════════════════════════════════════════════════════

TASK: TASK-042 - Implement JWT authentication system

COMPLEXITY: 7/10 (Complex)
ARCHITECTURAL REVIEW: 85/100 (APPROVED with recommendations)

FILES TO CREATE/MODIFY:
  📄 src/auth/jwt_service.py (80 lines)
     Purpose: JWT token generation and validation

  📄 src/api/auth_endpoints.py (60 lines)
     Purpose: Authentication API endpoints

  📄 src/auth/token_blacklist.py (45 lines)
     Purpose: Token revocation management

  📄 tests/test_jwt_service.py (50 lines)
     Purpose: Unit tests for JWT service

  📄 tests/test_auth_endpoints.py (40 lines)
     Purpose: Integration tests for auth API

  ... and 3 more files

DEPENDENCIES:
  📦 pyjwt (2.8.0+)
     Purpose: JWT token creation and validation

  📦 python-dotenv (1.0.0+)
     Purpose: Environment variable management

  📦 redis (5.0.0+)
     Purpose: Token blacklist storage

RISKS IDENTIFIED:
  🔴 CRITICAL: JWT secret management
     Mitigation: Use environment variables, never commit secrets

  🟡 MEDIUM: Token refresh race conditions
     Mitigation: Implement token versioning and atomic updates

  🟢 LOW: Performance overhead of token validation
     Mitigation: Add Redis caching layer for decoded tokens

EFFORT ESTIMATE:
  📊 Complexity: 7/10 (Complex)
  ⏱️  Duration: 4 hours
  📝 Lines of Code: ~287
  📈 Confidence: Medium (security-sensitive, multiple dependencies)

ARCHITECTURAL RECOMMENDATIONS:
  - Consider token revocation strategy for logout
  - Add rate limiting to auth endpoints
  - Implement token refresh endpoint

⚠️  MANDATORY REVIEW REQUIRED (Complexity 7/10)

OPTIONS:
[A] Approve - Proceed to implementation
[M] Modify - Edit plan interactively
[V] View - Show full plan details
[S] Simplify - Break down into smaller tasks
[C] Cancel - Return to backlog

Your choice (A/M/V/S/C):
```

**Developer Action:**

1. **Reviews plan carefully**
2. **Notices missing refresh endpoint** (mentioned in recommendations but not in files)
3. **Chooses `[M] Modify`** to add file
4. **After modification, plan redisplays** with new file included
5. **Chooses `[A] Approve`** to proceed

## Troubleshooting

### Issue: Missing Plan File

**Error:**
```
❌ Implementation plan not found: .claude/task-plans/TASK-042-implementation-plan.md

Attempting graceful recovery...
✅ Generated minimal plan from task description
```

**Resolution:**
- System generates basic plan from task frontmatter
- Checkpoint displays with available information
- Recommend using `[M] Modify` to enhance plan

---

### Issue: Invalid Plan Format

**Error:**
```
⚠️  Plan format validation failed (not valid Markdown)

Falling back to JSON plan format...
```

**Resolution:**
- System attempts to parse plan as JSON
- If successful, displays JSON content in checkpoint
- If failed, displays raw text and recommends manual edit

---

### Issue: Timeout in QUICK Mode

**Behavior:**
```
⏱️  AUTO-PROCEED in 30 seconds...
⏱️  10 seconds...
⏱️  5 seconds...
⏱️  0 seconds - Proceeding to implementation
```

**Resolution:**
- System automatically approves and proceeds
- No action required (intentional auto-proceed)
- To prevent: Press any key during countdown to interrupt

---

### Issue: Truncated Display Hides Critical Info

**Problem:** Important files/dependencies hidden in "+N more" truncation

**Solution:**
1. Select `[V] View` to open full plan
2. Review complete file/dependency lists
3. Return to checkpoint and choose action
4. Alternatively, select `[M] Modify` to make changes based on truncated view

## Related Workflows

- **[Plan Modification Workflow](./plan-modification-workflow.md)** - How to modify plans at checkpoint
- **[Complexity Management Workflow](./complexity-management-workflow.md)** - How complexity determines review mode
- **[Design-First Workflow](./design-first-workflow.md)** - Using `--design-only` for checkpoint-only execution
- **[Markdown Plans Workflow](./markdown-plans-workflow.md)** - Understanding plan format and structure

## FAQ

### Q: Can I skip the checkpoint?

**A:** Only for simple tasks (complexity 1-3) where AUTO_PROCEED mode applies. For medium tasks (4-6), you can let the 30-second timeout expire for auto-approval. Complex tasks (7-10) require mandatory review.

---

### Q: What if the plan is too long to read in the checkpoint display?

**A:** Use `[V] View` to open the full Markdown plan in your default editor. Review at your own pace, then return to the checkpoint to choose your action.

---

### Q: How do I modify the plan?

**A:** Select `[M] Modify` at the checkpoint. This enters interactive modification mode where you can add/remove files, dependencies, risks, or adjust effort estimates. See [Plan Modification Workflow](./plan-modification-workflow.md) for details.

---

### Q: What happens if I timeout in QUICK mode?

**A:** The system automatically approves the plan and proceeds to implementation (Phase 3). This is intentional behavior for medium-complexity tasks where the plan is likely good enough to proceed.

---

### Q: Can I edit the plan file directly instead of using [M] Modify?

**A:** Yes, but it's not recommended during an active task-work session. The checkpoint works with the saved plan file, so direct edits won't be reflected until you restart the task. For safety, use `[M] Modify` or `[C] Cancel` → manual edit → restart task-work.

---

### Q: What information is shown for different review modes?

**A:**
- **AUTO_PROCEED (1-3):** No checkpoint displayed
- **QUICK_OPTIONAL (4-6):** Summary with 30s timeout, options A/M/V/C
- **FULL_REQUIRED (7-10):** Summary with mandatory review, options A/M/V/S/C (includes Simplify)
