# Plan Modification Workflow

## Overview

The Plan Modification Workflow enables **interactive editing of implementation plans** at the Phase 2.8 checkpoint, providing developers with fine-grained control over plan details before code execution begins. This workflow supports adding, removing, or modifying files, dependencies, risks, and effort estimates through a structured, version-controlled process.

**Key Features:**
- **4 Modification Categories**: Files, Dependencies, Risks, Effort
- **Automatic Version Management**: Every modification creates timestamped backup
- **Undo Functionality**: Revert changes with multi-level undo support
- **Checkpoint Loop Integration**: Modified plans redisplay at checkpoint for review
- **Validation and Error Recovery**: Syntax validation with correction prompts

**When This Workflow Activates:**
- At Phase 2.8 checkpoint when `[M] Modify` option is selected
- After plan summary is displayed
- Before implementation (Phase 3) begins

**Purpose:**
- Make small adjustments without full plan regeneration
- Add missing files or dependencies identified during review
- Adjust risk assessments or effort estimates
- Maintain plan accuracy with version history

## Prerequisites

**Required:**
- At Phase 2.8 checkpoint with plan summary displayed
- Implementation plan exists (`.claude/task-plans/{task_id}-implementation-plan.md`)

**Recommended:**
- Understanding of plan structure (files, dependencies, risks, effort)
- Awareness of modification categories and syntax
- Familiarity with checkpoint loop (modify → redisplay → approve/modify again)

**System State:**
- Task in `IN_PROGRESS` state
- Checkpoint displaying plan summary
- Modification option `[M]` available

## 4 Modification Categories

### 1. Files Modification

**What You Can Modify:**
- Add files to create/modify list
- Remove files from plan
- Change file purposes/descriptions
- Adjust line-of-code estimates for files

**When to Use:**
- Missing test file identified during review
- Unnecessary file included in plan
- File purpose needs clarification
- LOC estimate seems off

**Modification Syntax:**

**Add File:**
```
ADD: path/to/file.py (80 lines) - Purpose description
```

**Remove File:**
```
REMOVE: path/to/file.py
```

**Modify File:**
```
MODIFY: path/to/file.py
  Purpose: Updated purpose description
  LOC: 120
```

**Examples:**

**Add missing test file:**
```
ADD: tests/test_authentication.py (50 lines) - Unit tests for authentication service
```

**Remove unnecessary file:**
```
REMOVE: src/utils/deprecated_helper.py
```

**Update file purpose:**
```
MODIFY: src/api/auth_endpoints.py
  Purpose: Authentication endpoints with rate limiting
```

---

### 2. Dependencies Modification

**What You Can Modify:**
- Add new dependencies (libraries, tools, external services)
- Remove unnecessary dependencies
- Modify dependency versions or specifications
- Change dependency purposes/justifications

**When to Use:**
- Missing library identified (e.g., forgot logging library)
- Included dependency not actually needed
- Version constraint too strict/loose
- Purpose needs clarification

**Modification Syntax:**

**Add Dependency:**
```
ADD: package-name (version-spec) - Purpose description
```

**Remove Dependency:**
```
REMOVE: package-name
```

**Modify Dependency:**
```
MODIFY: package-name
  Version: updated-version-spec
  Purpose: Updated purpose description
```

**Examples:**

**Add logging library:**
```
ADD: structlog (23.1.0+) - Structured logging with context
```

**Remove unused package:**
```
REMOVE: unused-legacy-lib
```

**Update version constraint:**
```
MODIFY: pyjwt
  Version: 2.8.0+
  Purpose: JWT creation and validation (updated to latest stable)
```

---

### 3. Risks Modification

**What You Can Modify:**
- Add new risks with severity level (LOW/MEDIUM/HIGH/CRITICAL)
- Remove addressed or invalid risks
- Modify risk severity or mitigation strategy
- Update risk descriptions

**When to Use:**
- Security concern identified during review
- Risk listed but already mitigated elsewhere
- Severity assessment incorrect
- Mitigation strategy needs improvement

**Modification Syntax:**

**Add Risk:**
```
ADD: [SEVERITY] Risk description
  Mitigation: Mitigation strategy
```

**Remove Risk:**
```
REMOVE: Risk description (partial match OK)
```

**Modify Risk:**
```
MODIFY: Risk description (partial match)
  Severity: NEW_SEVERITY
  Mitigation: Updated mitigation strategy
```

**Severity Levels:**
- `CRITICAL` 🔴: System security, data loss, production outage
- `HIGH` 🟠: Major functionality impact, performance degradation
- `MEDIUM` 🟡: Moderate impact, workarounds available
- `LOW` 🟢: Minor inconvenience, edge cases

**Examples:**

**Add security risk:**
```
ADD: [CRITICAL] SQL injection vulnerability in user input
  Mitigation: Use parameterized queries, validate all input
```

**Remove addressed risk:**
```
REMOVE: Token refresh race conditions
```

**Update risk severity:**
```
MODIFY: Performance overhead
  Severity: LOW
  Mitigation: Add Redis caching layer (reduced from MEDIUM)
```

---

### 4. Effort Modification

**What You Can Modify:**
- Estimated duration (hours)
- Expected lines of code
- Complexity score (0-10 scale)
- Confidence level and justification

**When to Use:**
- Duration estimate seems too optimistic/pessimistic
- LOC estimate doesn't match file count
- Complexity score feels off
- Confidence level needs adjustment

**Modification Syntax:**

**Modify Duration:**
```
DURATION: 6 hours (reason: additional complexity identified)
```

**Modify LOC:**
```
LOC: 350 (reason: additional files added)
```

**Modify Complexity:**
```
COMPLEXITY: 8 (reason: security requirements increase complexity)
```

**Modify Confidence:**
```
CONFIDENCE: Low (reason: unfamiliar authentication patterns)
```

**Examples:**

**Increase duration:**
```
DURATION: 5 hours (reason: added token refresh endpoint)
```

**Reduce LOC estimate:**
```
LOC: 200 (reason: removed unnecessary utility file)
```

**Adjust complexity:**
```
COMPLEXITY: 6 (reason: risk mitigation reduces overall complexity)
```

## Step-by-Step Workflow

### Step 1: Review Plan Summary at Checkpoint

```
═══════════════════════════════════════════════════════
PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT
═══════════════════════════════════════════════════════

[Plan summary displayed with files, dependencies, risks, effort]

OPTIONS:
[A] Approve - Proceed to implementation
[M] Modify - Edit plan interactively  ← Select this option
[V] View - Show full plan details
[C] Cancel - Return to backlog

Your choice (A/M/V/C):
```

### Step 2: Choose [M]odify Option

```
Your choice: M

Entering interactive modification mode...
```

### Step 3: Modification Menu Displayed

```
═══════════════════════════════════════════════════════
PLAN MODIFICATION MODE
═══════════════════════════════════════════════════════

What would you like to modify?

[1] Files - Add, remove, or edit planned files
[2] Dependencies - Change dependencies or versions
[3] Risks - Add risk mitigations or change risk levels
[4] Effort - Adjust duration, LOC, or complexity estimates

[S] Save & Review - Save changes and return to checkpoint
[U] Undo - Revert last modification
[C] Cancel - Discard all changes and return to checkpoint

Your choice (1-4/S/U/C):
```

### Step 4: Select Modification Category

**Example: Select `[1] Files`**

```
Your choice: 1

═══════════════════════════════════════════════════════
FILES MODIFICATION
═══════════════════════════════════════════════════════

Current Files (8 total):
  1. src/auth/jwt_service.py (80 lines)
  2. src/api/auth_endpoints.py (60 lines)
  3. src/auth/token_blacklist.py (45 lines)
  4. tests/test_jwt_service.py (50 lines)
  5. tests/test_auth_endpoints.py (40 lines)
  ... and 3 more

Actions:
[A] Add file
[R] Remove file
[M] Modify file details

[B] Back to modification menu

Your choice (A/R/M/B):
```

### Step 5: Enter Modification

**Example: Add missing file**

```
Your choice: A

Enter file details (format: path (LOC) - purpose):
> src/auth/token_refresh.py (55 lines) - Token refresh endpoint implementation

✅ File added: src/auth/token_refresh.py (55 lines)

What would you like to do next?
[A] Add another file
[R] Remove a file
[M] Modify file details
[B] Back to modification menu

Your choice:
```

### Step 6: Validation and Update

```
Your choice: B

Validating modifications...
✅ 1 file added
✅ Plan updated successfully

Creating backup: .claude/plans/backups/plan-TASK-042-v2-20251019143000.md
```

### Step 7: Automatic Backup Created

**Backup Location:** `.claude/plans/backups/`

**Backup Naming:** `plan-TASK-042-v{N}-{timestamp}.md`

**Backup Contains:**
- Complete plan before modification
- Metadata: modification timestamp, modified by, change summary

### Step 8: Loop Back to Checkpoint

```
Returning to checkpoint with updated plan...

═══════════════════════════════════════════════════════
PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT
═══════════════════════════════════════════════════════

[Updated plan summary displayed - includes new file]

FILES TO CREATE/MODIFY:
  📄 src/auth/jwt_service.py (80 lines)
  📄 src/api/auth_endpoints.py (60 lines)
  📄 src/auth/token_blacklist.py (45 lines)
  📄 src/auth/token_refresh.py (55 lines)  ← NEW
  📄 tests/test_jwt_service.py (50 lines)
  ... and 3 more files

OPTIONS:
[A] Approve - Proceed to implementation
[M] Modify - Edit plan interactively (again)
[V] View - Show full plan details
[C] Cancel - Return to backlog

Your choice (A/M/V/C):
```

### Step 9: Review Changes and Approve

Developer sees updated plan with new file included.

```
Your choice: A

✅ Plan approved - Proceeding to Phase 3 (Implementation)
```

### Step 10: Implementation Proceeds

System executes Phase 3 with modified plan, creating all files including the newly added `token_refresh.py`.

## Version Management

### Automatic Backups

**When Backups Are Created:**
- Every time a modification is saved
- Before any destructive operation (remove, modify)
- Automatically on first modification in a session

**Backup Location:**
```
.claude/plans/backups/
├── plan-TASK-042-v1-20251019142500.md  (original)
├── plan-TASK-042-v2-20251019143000.md  (after adding file)
├── plan-TASK-042-v3-20251019143200.md  (after adding dependency)
└── plan-TASK-042-v4-20251019143500.md  (after adjusting effort)
```

**Backup Naming Convention:**
```
plan-{task_id}-v{version_number}-{timestamp}.md
```

**Backup Metadata:**
Each backup includes frontmatter:
```yaml
---
version: 2
modified_at: 2025-10-19T14:30:00Z
modified_by: human
previous_version: v1
changes:
  - Added file: src/auth/token_refresh.py
  - Justification: Missing refresh endpoint identified at checkpoint
---
```

### Modification History

**Tracked Information:**
- Who modified (human/AI)
- What changed (diff summary)
- When modified (ISO 8601 timestamp)
- Why modified (justification/notes)

**History Display:**
```
MODIFICATION HISTORY:

v1 → v2 (2025-10-19 14:30:00 by human)
  + Added file: src/auth/token_refresh.py (55 lines)
  Reason: Missing refresh endpoint identified at checkpoint

v2 → v3 (2025-10-19 14:32:00 by human)
  + Added dependency: redis (5.0.0+)
  Reason: Token blacklist requires Redis storage

v3 → v4 (2025-10-19 14:35:00 by human)
  ~ Modified effort: Duration 4h → 5h
  Reason: Additional file and dependency increase complexity
```

## Undo Functionality

### [U]ndo Option

**What It Does:**
- Reverts the last modification
- Restores previous plan version from backup
- Can be used multiple times to step back through history

**When to Use:**
- Made a mistake in last modification
- Want to try different approach
- Need to backtrack to earlier plan state

**How It Works:**

### Step 1: Make Modification (Accidentally Wrong)

```
[M] Modify → Files → Add
Added: src/utils/unnecessary_helper.py

Wait, that file isn't actually needed...
```

### Step 2: Return to Modification Menu

```
[B] Back to modification menu

What would you like to modify?
[1] Files
[2] Dependencies
[3] Risks
[4] Effort

[S] Save & Review
[U] Undo  ← Select this option
[C] Cancel

Your choice:
```

### Step 3: Undo Last Change

```
Your choice: U

⚠️  UNDO CONFIRMATION
You are about to revert the last modification:
  - Added file: src/utils/unnecessary_helper.py (30 lines)

This will restore plan version v2 (previous version).

Are you sure? (y/n):
```

### Step 4: Confirm Undo

```
Your choice: y

✅ Modification reverted
✅ Restored plan version v2

Current plan state:
  - Files: 8 (back to original count)
  - Version: v2
  - Last modification: Added dependency redis (5.0.0+)
```

### Step 5: Continue Modifying or Save

```
What would you like to modify?
[1] Files
[2] Dependencies
[3] Risks
[4] Effort

[S] Save & Review  ← Can now save clean version
[U] Undo (can undo again to v1 if needed)
[C] Cancel
```

### Undo Limitations

**Can Undo:**
- ✅ Last modification (most recent)
- ✅ Multiple modifications (step back through history)
- ✅ Any category (files, dependencies, risks, effort)

**Cannot Undo:**
- ❌ After leaving modification mode ([S] Save & Review)
- ❌ After checkpoint approval ([A] Approve)
- ❌ Original plan (v1 always preserved)

**Warning on Last Version:**
```
⚠️  WARNING: This is the last undo available.
Undoing will restore the original plan (v1).
All modifications will be lost.

Are you sure? (y/n):
```

## Decision Framework

### When to Modify (vs Other Options)

**Modify when:**
- ✅ Small adjustments needed (1-3 changes)
- ✅ Missing file/dependency identified
- ✅ Risk severity incorrect
- ✅ Effort estimate slightly off
- ✅ Can fix in <5 minutes

**Approve when:**
- ✅ Plan is correct and complete
- ✅ No changes needed
- ✅ Ready to proceed to implementation

**Cancel when:**
- ❌ Major design flaws
- ❌ Multiple significant issues
- ❌ Need to rethink approach
- ❌ Would take >10 minutes to modify

**View when:**
- 🔍 Need complete file/dependency list
- 🔍 Truncated display hides important info
- 🔍 Want to review full plan before deciding

## Examples

### Example 1: Add Missing Test File

**Checkpoint Display:**
```
FILES TO CREATE/MODIFY:
  📄 src/auth/jwt_service.py (80 lines)
  📄 src/api/auth_endpoints.py (60 lines)
  📄 tests/test_jwt_service.py (50 lines)

⚠️  Notice: Missing integration tests for auth endpoints
```

**Modification Flow:**

1. **Select [M] Modify**

2. **Select [1] Files → [A] Add file**

3. **Enter file details:**
   ```
   > tests/test_auth_endpoints.py (40 lines) - Integration tests for authentication API
   ```

4. **System confirms:**
   ```
   ✅ File added: tests/test_auth_endpoints.py (40 lines)
   ```

5. **Select [B] Back → [S] Save & Review**

6. **Plan redisplays at checkpoint with new file:**
   ```
   FILES TO CREATE/MODIFY:
     📄 src/auth/jwt_service.py (80 lines)
     📄 src/api/auth_endpoints.py (60 lines)
     📄 tests/test_jwt_service.py (50 lines)
     📄 tests/test_auth_endpoints.py (40 lines)  ← NEW
   ```

7. **Select [A] Approve**

---

### Example 2: Remove Unnecessary Dependency

**Checkpoint Display:**
```
DEPENDENCIES:
  📦 pyjwt (2.8.0+) - JWT token creation
  📦 python-dotenv (1.0.0+) - Environment variables
  📦 legacy-crypto-lib (1.5.0) - Unused legacy library
```

**Modification Flow:**

1. **Select [M] Modify**

2. **Select [2] Dependencies → [R] Remove**

3. **System shows dependency list:**
   ```
   Select dependency to remove:
   1. pyjwt (2.8.0+)
   2. python-dotenv (1.0.0+)
   3. legacy-crypto-lib (1.5.0)

   Your choice (1-3):
   ```

4. **Select `3` (legacy-crypto-lib)**

5. **System confirms:**
   ```
   ✅ Dependency removed: legacy-crypto-lib
   ```

6. **Select [B] Back → [S] Save & Review**

7. **Plan redisplays without legacy library:**
   ```
   DEPENDENCIES:
     📦 pyjwt (2.8.0+) - JWT token creation
     📦 python-dotenv (1.0.0+) - Environment variables
   ```

8. **Select [A] Approve**

---

### Example 3: Multiple Modifications with Undo

**Scenario:** Developer makes several changes, then realizes one was wrong.

**Modification Flow:**

1. **Modify effort (increase duration):**
   ```
   [M] Modify → [4] Effort → DURATION: 6 hours
   ✅ Duration updated to 6 hours (v2)
   ```

2. **Add new file:**
   ```
   [M] Modify → [1] Files → [A] Add
   > src/utils/experimental_feature.py (30 lines) - Experimental optimization
   ✅ File added (v3)
   ```

3. **Review updated plan at checkpoint:**
   ```
   Wait, that experimental feature shouldn't be in this task...
   ```

4. **Return to modification mode:**
   ```
   [M] Modify
   ```

5. **Undo last change:**
   ```
   [U] Undo
   ⚠️  Revert: Added file src/utils/experimental_feature.py?
   > y
   ✅ Restored to v2 (effort modification only)
   ```

6. **Save and review:**
   ```
   [S] Save & Review
   ```

7. **Plan shows only effort change (experimental file removed):**
   ```
   EFFORT ESTIMATE:
     ⏱️  Duration: 6 hours (updated)  ← Kept

   FILES: (experimental_feature.py removed)  ← Undone
   ```

8. **Approve clean plan:**
   ```
   [A] Approve
   ```

## Troubleshooting

### Issue: Invalid Modification Syntax

**Error:**
```
❌ Invalid file syntax: missing LOC estimate

Expected format:
  ADD: path/to/file.py (80 lines) - Purpose description

Please try again:
```

**Resolution:**
- System prompts for correction
- Provides example format
- Validates on re-entry

---

### Issue: Conflicting Modifications

**Error:**
```
❌ Conflict detected: File already exists in plan
  Trying to add: src/auth/jwt_service.py
  Already in plan: src/auth/jwt_service.py (80 lines)

Use [M]odify instead of [A]dd to change existing files.
```

**Resolution:**
- Use correct action ([M]odify vs [A]dd)
- System prevents duplicate entries
- Suggests appropriate action

---

### Issue: Lost Changes

**Problem:** Accidentally canceled without saving modifications.

**Recovery:**
```
⚠️  You have unsaved modifications:
  - Added file: src/auth/token_refresh.py
  - Modified effort: Duration 4h → 5h

These changes will be lost if you cancel.

Options:
[S] Save & Review - Save changes and return to checkpoint
[D] Discard - Cancel without saving
[B] Back - Return to modification mode

Your choice (S/D/B):
```

**Best Practice:** Always use `[S] Save & Review` before leaving modification mode.

---

### Issue: Version Management Problems

**Problem:** Can't find backup or version history.

**Solution:**
1. Check `.claude/plans/backups/` directory
2. Backups are named: `plan-{task_id}-v{N}-{timestamp}.md`
3. Latest version is always in `.claude/task-plans/`
4. Use `[U]ndo` to restore from backups automatically

## Related Workflows

- **[Phase 2.8 Checkpoint Workflow](./phase28-checkpoint-workflow.md)** - Understanding the checkpoint display and when to modify
- **[Complexity Management Workflow](./complexity-management-workflow.md)** - How task complexity affects checkpoint behavior
- **[Markdown Plans Workflow](./markdown-plans-workflow.md)** - Plan format and structure details
- **[Design-First Workflow](./design-first-workflow.md)** - Using design-only mode with modification

## FAQ

### Q: Can I modify multiple categories at once?

**A:** No, modifications are sequential. You modify one category, save, review the updated plan, then modify another category if needed. This ensures each change is validated and tracked properly.

---

### Q: What if I make a mistake during modification?

**A:** Use the `[U]ndo` option to revert the last modification. You can undo multiple times to step back through the modification history. All versions are backed up automatically.

---

### Q: How many times can I undo?

**A:** You can undo back to the original plan (v1). Each modification creates a new version, and undo steps back one version at a time. The original plan is always preserved.

---

### Q: Can I edit the plan file directly instead of using [M] Modify?

**A:** Not during an active task-work session. The checkpoint works with the saved plan file, so direct edits won't be reflected until you restart task-work. For safety and version control, use `[M] Modify` during the session. If you prefer manual editing, select `[C] Cancel` at checkpoint, edit the plan file directly, then restart `/task-work`.

---

### Q: Where are backups stored?

**A:** All backups are stored in `.claude/plans/backups/` with versioned, timestamped filenames:
```
plan-{task_id}-v{version_number}-{timestamp}.md
```

Example: `plan-TASK-042-v2-20251019143000.md`

---

### Q: What happens to modification history when I approve the plan?

**A:** The modification history is saved in the task frontmatter and all backup versions are preserved in `.claude/plans/backups/`. You can always review the complete modification history even after task completion.

---

### Q: Can I modify a plan after approving it?

**A:** Not during the same task-work session. Once you approve and proceed to Phase 3 (Implementation), the plan is locked for that run. If you discover issues during implementation, use `/task-refine` after completion or cancel the task-work session and restart with a modified plan.
