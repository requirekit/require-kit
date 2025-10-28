# Task Work - Unified Implementation Command

## Command Syntax

```bash
/task-work TASK-XXX [--design-only | --implement-only | --micro] [other-flags...]
```

## Feature Detection and Package Integration

The `/task-work` command automatically detects which Agentecflow packages are installed and adapts its workflow accordingly, enabling **bidirectional optional integration** between taskwright and require-kit.

### Installation Scenarios

| Installed Packages | Available Features | Unavailable Features |
|-------------------|-------------------|----------------------|
| **taskwright only** | ✅ Standard mode<br>✅ TDD mode<br>✅ Quality gates<br>✅ Stack templates | ❌ BDD mode<br>❌ EARS requirements loading<br>❌ Epic/Feature context |
| **require-kit only** | ⚠️ Not applicable | ℹ️ Install taskwright for task execution |
| **Both installed** | ✅ All modes (standard, TDD, BDD)<br>✅ EARS requirements<br>✅ BDD scenarios<br>✅ Epic/Feature context<br>✅ Full traceability | None - full integration |

### Automatic Detection

The command uses `feature_detection.py` library to detect installed packages:

```python
from lib.feature_detection import (
    is_taskwright_installed,
    is_require_kit_installed,
    supports_requirements,
    supports_bdd,
    get_available_features
)

# Check what features are available
features = get_available_features()
# Returns: {
#   "task_management": True/False,
#   "requirements_engineering": True/False,
#   "bdd_generation": True/False,
#   ...
# }
```

### Graceful Degradation

**When require-kit is not installed:**
- ✅ Task execution continues normally
- ℹ️ EARS requirements not loaded (uses task description only)
- ℹ️ BDD scenarios not loaded
- ℹ️ Epic/Feature context not loaded
- ⚠️ BDD mode blocked with clear error message

**Example output (taskwright only):**
```
ℹ️  Package Detection
- taskwright: ✅ installed (v1.0.0)
- require-kit: ❌ not installed

📋 Task Context
- Description: Loaded ✅
- Acceptance Criteria: Loaded ✅
- Requirements (EARS): Skipped (install require-kit for this)
- BDD Scenarios: Skipped (install require-kit for this)
- Epic/Feature Context: Skipped (install require-kit for this)

Continuing with available context...
```

### Mode Availability

**BDD Mode requires require-kit:**
```bash
/task-work TASK-042 --mode=bdd

# If require-kit not installed:
❌ BDD mode requires require-kit

You requested: /task-work TASK-042 --mode=bdd
Available modes: standard, tdd

Options:
1. Install require-kit for BDD support:
   cd require-kit && ./installer/scripts/install.sh

2. Use alternative mode:
   /task-work TASK-042 --mode=tdd

3. Use standard mode:
   /task-work TASK-042 --mode=standard
```

### Integration Suggestions

When task references unavailable features:
```
⚠️  Task TASK-042 references features that cannot be loaded

Referenced in task metadata:
- Epic: EPIC-001
- Requirements: [REQ-005, REQ-006]
- BDD Scenarios: FEAT-001

These require require-kit to be installed.

To enable full context loading:
  cd require-kit
  ./installer/scripts/install.sh

Continue with task description only? [Y/n]
```

## Micro-Task Mode (NEW - TASK-020)

The task-work command now supports a `--micro` flag for streamlined execution of trivial tasks (typo fixes, documentation updates, cosmetic changes) that don't require full architectural review.

### Flag: --micro

**Purpose**: Lightweight workflow for trivial tasks, completing in 3-5 minutes vs 15+ minutes.

**Criteria for micro-tasks** (ALL must be true):
- Complexity: 1/10 (single file, <1 hour, low risk)
- Files: Single file modification (or documentation-only)
- Risk: No high-risk keywords (security, schema, breaking changes, API changes)
- Estimated time: <1 hour

**Phases executed**:
- Phase 1: Load Task Context
- Phase 3: Implementation (simplified)
- Phase 4: Quick Testing (compilation + tests only, no coverage)
- Phase 4.5: Fix Loop (1 attempt max, vs 3 in standard)
- Phase 5: Quick Review (lint only, skip SOLID/DRY/YAGNI)

**Phases skipped**:
- Phase 2: Implementation Planning
- Phase 2.5A: Pattern Suggestion
- Phase 2.5B: Architectural Review
- Phase 2.6: Human Checkpoint
- Phase 2.7: Complexity Evaluation
- Phase 5.5: Plan Audit (no plan in micro-task mode)

**Quality gates** (micro-task specific):
- Compilation: REQUIRED (same as standard)
- Tests Pass: REQUIRED (same as standard)
- Coverage: SKIPPED (not required for micro-tasks)
- Architectural Review: SKIPPED
- Code Review: LIGHTWEIGHT (lint only)

**Auto-detection**: System automatically suggests `--micro` flag when task qualifies:
- Analyzes task metadata (title, description, estimated effort)
- Detects high-risk keywords (security, database, API, etc.)
- Shows suggestion with 10-second timeout
- User can accept suggestion or continue with full workflow

**Validation**: If `--micro` flag is used but task doesn't qualify, escalates to full workflow with warning.

**Example** (micro-task success):
```bash
/task-work TASK-047 --micro

Micro-Task Mode Enabled

Phase 1: Load Task Context
  Task: Fix typo in error message
  File: src/services/AuthService.py
  Change: 'occured' → 'occurred'

Phase 3: Implementation
  Updated src/services/AuthService.py:45
  Changed error message

Phase 4: Quick Testing
  Compilation: PASSED
  Tests: 5/5 PASSED (coverage skipped)

Phase 5: Quick Review
  Lint: PASSED (no issues)

Task State: BACKLOG → IN_REVIEW
Duration: 2 minutes 34 seconds
```

**Example** (auto-detection):
```bash
/task-work TASK-047

Detected micro-task (confidence: 95%)
This task appears to be trivial (complexity 1/10, single file, <1 hour).

Suggest using: /task-work TASK-047 --micro
Saves ~12 minutes by skipping optional phases.

Auto-apply micro-mode? [y/N] (10s timeout): _
```

**Example** (escalation):
```bash
/task-work TASK-048 --micro

Task does not qualify as micro-task:
  - Complexity: 5/10 (threshold: 1/10)
  - High-risk keywords detected: authentication, database
  - Estimated effort: 4 hours (threshold: <1 hour)

Escalating to full workflow...

Phase 1: Load Task Context
Phase 2: Implementation Planning
Phase 2.5B: Architectural Review
...
(continues with full workflow)
```

**Documentation-only exception**: Tasks affecting only documentation files (.md, .txt, .rst) automatically qualify for micro-task mode, even if they affect multiple files.

**Use cases**:
- Typo fixes in code or documentation
- Comment updates and documentation improvements
- Cosmetic changes (formatting, whitespace)
- Simple configuration changes
- Minor UI text updates
- Small refactoring (variable renaming, etc.)

**NOT for**:
- Security-related changes (authentication, authorization, encryption)
- Database schema changes (migrations, table alterations)
- API changes (breaking changes, new endpoints)
- External integrations (third-party APIs, webhooks)
- Multi-file refactoring
- Complex business logic changes

## Design-First Workflow Flags (TASK-006)

The task-work command now supports optional flags for design-first workflow, enabling flexible execution modes based on task complexity and team collaboration needs.

### Flag: --design-only

**Purpose**: Execute design phases only, stop at approval checkpoint.

**Phases executed**:
- Phase 1: Load Task Context
- Phase 2: Implementation Planning
- Phase 2.5A: Pattern Suggestion (if Design Patterns MCP available)
- Phase 2.5B: Architectural Review
- Phase 2.7: Complexity Evaluation & Plan Persistence
- Phase 2.8: Human Checkpoint (mandatory for design-only)

**Phases skipped**:
- Phase 3: Implementation
- Phase 4: Testing
- Phase 4.5: Fix Loop
- Phase 5: Code Review

**Outcome**: Task moves to `design_approved` state with saved implementation plan.

**Use cases**:
- Complex tasks (complexity ≥ 7) requiring upfront design approval
- Multi-day tasks where design and implementation happen on different days
- Architect-led design with developer-led implementation
- High-risk changes (security, breaking changes, schema changes)
- Unclear requirements needing design exploration

**Example**:
```bash
/task-work TASK-006 --design-only
```

### Flag: --implement-only

**Purpose**: Execute implementation phases using previously approved design.

**Prerequisite**: Task MUST be in `design_approved` state (approved via --design-only).

**Phases executed**:
- Phase 3: Implementation (using saved plan)
- Phase 4: Testing
- Phase 4.5: Fix Loop (ensure tests pass)
- Phase 5: Code Review

**Phases skipped**:
- Phase 1-2.8 (uses saved design from --design-only run)

**Outcome**: Task moves to `in_review` state (if quality gates pass) or `blocked` (if tests fail).

**Use cases**:
- Implementing previously approved designs
- Continuing work after design approval on different day
- Different person implementing than who designed
- Multi-day task workflow (design Day 1, implement Day 2)

**Example**:
```bash
/task-work TASK-006 --implement-only
```

### No Flags (Default Behavior - Unchanged)

**Purpose**: Execute complete workflow in single session.

**Phases executed**: All phases in sequence (1 → 2 → 2.5A → 2.5B → 2.7 → 2.8 → 3 → 4 → 4.5 → 5)

**Phase 2.8 checkpoint**: Triggered based on complexity evaluation (auto-proceed for 1-3, optional for 4-6, mandatory for 7-10).

**Use cases**:
- Simple to medium tasks (complexity 1-6)
- Straightforward implementation with clear approach
- Single developer handling both design and implementation
- Design and implementation can happen in same session
- Low-risk changes

**Example**:
```bash
/task-work TASK-006
```

### Flag Validation Rules

**Mutual Exclusivity**: --design-only and --implement-only cannot be used together.

```bash
# ❌ Invalid usage
/task-work TASK-006 --design-only --implement-only

# Error message:
❌ Error: Cannot use both --design-only and --implement-only flags together

Choose one workflow mode:
  --design-only     Execute design phases only (Phases 1-2.8)
  --implement-only  Execute implementation phases only (Phases 3-5)
  (no flags)        Execute complete workflow (default)
```

**State Validation**: --implement-only requires task to be in `design_approved` state.

```bash
# ❌ Invalid usage (task not in design_approved state)
/task-work TASK-006 --implement-only

# Error message:
❌ Cannot execute --implement-only workflow

Task TASK-006 is in 'backlog' state.
Required state: design_approved

To approve design first, run:
  /task-work TASK-006 --design-only

Or run complete workflow without flags:
  /task-work TASK-006
```

### New Task State: design_approved

Tasks can now be in a `design_approved` state:
- **Location**: `tasks/design_approved/{task_id}.md`
- **Purpose**: Indicates design has been approved and is ready for implementation
- **Metadata**: Includes saved implementation plan, architectural review scores, complexity evaluation

### Design Metadata Schema

When using --design-only, the following metadata is saved to task frontmatter:

```yaml
design:
  status: approved  # pending, approved, rejected, n/a
  approved_at: "2025-10-11T14:30:00Z"
  approved_by: "human"  # or "auto" for simple tasks
  implementation_plan_version: "v1"
  architectural_review_score: 85
  complexity_score: 7
  design_session_id: "design-TASK-006-20251011143000"
  design_notes: "Architectural review passed, ready for implementation"
```

### Implementation Plan Storage

Design plans are saved to:
```
docs/state/{task_id}/implementation_plan.json
```

This file contains:
- Files to create/modify
- External dependencies
- Estimated duration and LOC
- Implementation phases
- Test strategy
- Risk mitigations
- Architectural review results

## Context7 MCP Integration (Library Documentation)

During task implementation, **automatically use Context7 MCP** to retrieve up-to-date library documentation when implementing with specific libraries or frameworks.

### When to Use Context7

Context7 should be invoked automatically during these phases:

1. **Phase 2: Implementation Planning**
   - When selecting libraries or frameworks for the implementation
   - When planning API usage patterns
   - When determining best practices for a library

2. **Phase 3: Implementation**
   - When implementing features using specific libraries
   - When unfamiliar with a library's API
   - When library documentation is needed for correct usage
   - When implementing patterns specific to a framework (React hooks, FastAPI patterns, etc.)

3. **Phase 4: Testing**
   - When writing tests using testing frameworks (pytest, Vitest, xUnit)
   - When setting up test fixtures or mocks
   - When implementing test patterns specific to the stack

### Context7 Workflow

**Step 1: Resolve Library ID**

Always resolve library name to Context7-compatible ID first:

```python
# Use mcp__context7__resolve-library-id tool
mcp__context7__resolve_library_id("react")
# Returns: /facebook/react or /facebook/react/v18.2.0
```

**Step 2: Get Library Documentation**

Use resolved ID to fetch documentation:

```python
# Use mcp__context7__get-library-docs tool
mcp__context7__get_library_docs(
  context7CompatibleLibraryID="/facebook/react",
  topic="hooks",              # Optional: focus area
  tokens=5000                 # Optional: max tokens (default: 5000)
)
```

### Examples by Stack

**React/TypeScript:**
- Libraries: "react", "next.js", "tailwindcss", "vitest", "playwright"
- Topics: "hooks", "routing", "styling", "testing"

**Python:**
- Libraries: "fastapi", "pytest", "pydantic", "langchain", "streamlit"
- Topics: "dependency-injection", "testing", "validation", "agents"

**.NET MAUI:**
- Libraries: "maui", "xamarin", "xunit", "moq"
- Topics: "mvvm", "data-binding", "navigation", "testing"

**TypeScript API:**
- Libraries: "nestjs", "typeorm", "jest", "supertest"
- Topics: "dependency-injection", "decorators", "testing", "validation"

### Integration Points in task-work Workflow

**Phase 2: Implementation Planning**
```
When task requires library usage:
1. Identify required libraries from requirements
2. Use Context7 to resolve library IDs
3. Fetch documentation for implementation approach
4. Incorporate library best practices into implementation plan
```

**Phase 3: Implementation**
```
When implementing with unfamiliar library APIs:
1. Use Context7 to get current documentation
2. Focus documentation on relevant topics (use `topic` parameter)
3. Implement according to latest library patterns
4. Verify implementation matches library best practices
```

**Phase 4: Testing**
```
When writing tests:
1. Use Context7 to get testing framework docs
2. Focus on testing patterns and assertions
3. Implement tests using framework best practices
```

### Best Practices

1. **Always resolve library ID first** - Don't assume library path format
2. **Use topic parameter** - Narrow documentation to relevant sections
3. **Limit token usage** - Default 5000 tokens is usually sufficient
4. **Cache library IDs** - Reuse resolved IDs within same task session
5. **Version awareness** - Use specific versions when available (/library/vX.Y.Z)
6. **Framework-specific patterns** - Always check library-specific patterns for the stack

### Error Handling

If Context7 library is not found:
- Proceed with general knowledge
- Document that library docs were unavailable
- Note in implementation for human review

### When NOT to Use Context7

- Standard language features (JavaScript, Python syntax)
- Well-established patterns (SOLID principles)
- General software engineering concepts
- Standard library functions (already in training data)

---

## 🎯 EXECUTION PROTOCOL - START HERE IMMEDIATELY

When user runs `/task-work TASK-XXX [flags]`, **EXECUTE THIS EXACT SEQUENCE**:

### Step 0: Parse and Validate Flags (NEW - Required for design-first workflow)

**PARSE** command-line flags from user input:
```python
# Extract flags from command
design_only = "--design-only" in user_input or "-d" in user_input
implement_only = "--implement-only" in user_input or "-i" in user_input
```

**VALIDATE** flag mutual exclusivity:
```python
from installer.global.commands.lib.flag_validator import validate_flags

flags = {
    "design_only": design_only,
    "implement_only": implement_only,
    # ... other flags
}

try:
    validate_flags(flags)
except FlagConflictError as e:
    print(str(e))
    exit(1)
```

**DISPLAY** active flags (if any):
```python
if design_only:
    print("🎨 Workflow Mode: DESIGN-ONLY (Phases 1-2.8)")
    print("   Task will stop at design approval checkpoint\n")
elif implement_only:
    print("🚀 Workflow Mode: IMPLEMENT-ONLY (Phases 3-5)")
    print("   Using previously approved design\n")
else:
    print("🔄 Workflow Mode: STANDARD (All phases)")
    print("   Complete workflow with complexity-based checkpoints\n")
```

**PROCEED** to Step 1 with flag context.

### Step 1: Load Task Context (REQUIRED - Multi-phase file resolution)

This step implements robust file resolution supporting descriptive filenames and automatic state detection.

#### Phase 1.1: Parse and Validate Task ID

**EXTRACT** task ID from user command:
```python
task_id = extract_task_id(user_input)  # e.g., "TASK-XXX" from "/task-work TASK-XXX"
```

**VALIDATE** task ID format:
- Must match pattern: `TASK-[A-Z0-9-]+` (e.g., TASK-001, TASK-BUG-001, TASK-003B-2)
- Reject if invalid: "Invalid task ID format: {task_id}. Expected format: TASK-XXX"

**DISPLAY**: "Loading task {task_id}..."

#### Phase 1.2: Multi-State File Search

**SEARCH** for task file across multiple states using glob patterns:

Search order (priority from highest to lowest):
1. `tasks/in_progress/{task_id}*.md` (expected location for active tasks)
2. `tasks/backlog/{task_id}*.md` (may need to transition to in_progress)
3. `tasks/blocked/{task_id}*.md` (may need to unblock and continue)
4. `tasks/in_review/{task_id}*.md` (edge case: re-work after review)

**Implementation pattern**:
```python
search_states = [
    ("in_progress", "tasks/in_progress"),
    ("backlog", "tasks/backlog"),
    ("blocked", "tasks/blocked"),
    ("in_review", "tasks/in_review")
]

matches = []
for state_name, state_dir in search_states:
    # Use Glob tool with pattern: {state_dir}/{task_id}*.md
    files = glob(f"{state_dir}/{task_id}*.md")
    for file in files:
        matches.append({
            "path": file,
            "state": state_name,
            "filename": extract_filename(file)
        })

    # Stop searching if found (priority order)
    if matches:
        break
```

**IMPORTANT**: Use Glob tool for file pattern matching, NOT bash find commands.

#### Phase 1.3: Handle Search Results

**CASE A: No matches found**
```python
if len(matches) == 0:
    # Task file not found in any state
    **DISPLAY** error report:
    ```
    ❌ Error: Task file not found

    Task ID: {task_id}
    Searched locations:
      - tasks/in_progress/{task_id}*.md
      - tasks/backlog/{task_id}*.md
      - tasks/blocked/{task_id}*.md
      - tasks/in_review/{task_id}*.md

    Possible causes:
    1. Task ID is incorrect or misspelled
    2. Task file has been deleted
    3. Task has been completed and archived

    Suggestions:
    - Verify task ID: /task-status (lists all tasks)
    - Check completed tasks: ls tasks/completed/
    - Create new task: /task-create "Task title"
    ```
    **EXIT** with error code
```

**CASE B: Single match found**
```python
if len(matches) == 1:
    task_file = matches[0]
    current_state = task_file["state"]
    file_path = task_file["path"]

    **DISPLAY**: "✅ Found: {task_file['filename']} (state: {current_state})"

    # Proceed to Phase 1.4 (automatic state transition if needed)
```

**CASE C: Multiple matches found**
```python
if len(matches) > 1:
    # Multiple files match the pattern (edge case: duplicates)
    **DISPLAY** error report:
    ```
    ⚠️  Warning: Multiple task files found

    Task ID: {task_id}
    Matches:
    {for each match:}
      {index}. {match['filename']} (state: {match['state']})

    This is unexpected and indicates duplicate task files.

    Recommendations:
    1. Review the duplicate files manually
    2. Delete or rename the incorrect file(s)
    3. Ensure only one file per task ID exists

    Locations:
    {for each match:}
      {match['path']}
    ```
    **EXIT** with error code
```

#### Phase 1.4: Automatic State Transition (if needed)

**IF** current_state != "in_progress":

```python
# Task file found in non-active state, needs transition
**DISPLAY** state transition prompt:
```
🔄 Task State Transition Required

Task: {task_id}
Current State: {current_state}
Required State: IN_PROGRESS (for task-work to execute)

File: {file_path}

Automatic transition will:
1. Move file: {current_state}/{filename} → in_progress/{filename}
2. Update task metadata (status, updated timestamp)
3. Preserve all task content and history

Proceed with state transition? [Y/n]:
```

**WAIT** for user confirmation (default: Yes after 5 seconds)

**IF** user confirms (or timeout):
    1. **READ** task file to extract frontmatter and content
    2. **UPDATE** frontmatter metadata:
       ```yaml
       status: in_progress
       updated: {current_timestamp_iso8601}
       previous_state: {current_state}
       state_transition_reason: "Automatic transition for task-work execution"
       ```
    3. **WRITE** updated file to `tasks/in_progress/{filename}`
    4. **DELETE** old file from `tasks/{current_state}/{filename}`
    5. **DISPLAY**: "✅ Transitioned {task_id} from {current_state} to IN_PROGRESS"
    6. **UPDATE** variables:
       ```python
       file_path = f"tasks/in_progress/{filename}"
       current_state = "in_progress"
       ```

**IF** user declines:
    **DISPLAY**: "❌ State transition declined. Cannot execute task-work on {current_state} tasks."
    **EXIT** with error code

**ELSE** (already in_progress):
    # No transition needed, proceed directly
    **DISPLAY**: "✅ Task is already IN_PROGRESS"

#### Phase 1.5: Load Task Context (Enhanced with Feature Detection)

**STEP 1: Detect Installed Packages**

**IMPORT** feature detection library:
```python
from lib.feature_detection import (
    is_require_kit_installed,
    supports_requirements,
    supports_bdd,
    get_available_features
)
```

**CHECK** package availability:
```python
has_require_kit = is_require_kit_installed()
features = get_available_features()
```

**STEP 2: Read Task File**

**READ** task file from final location: `{file_path}`

**STEP 3: Extract Context (Conditional Loading)**

**EXTRACT** required context with conditional loading:
```python
task_context = {
    "task_id": task_id,
    "file_path": file_path,
    "state": current_state,

    # From frontmatter (always loaded)
    "title": frontmatter.title,
    "priority": frontmatter.priority,
    "assignee": frontmatter.assignee,

    # From content (always loaded)
    "acceptance_criteria": extract_acceptance_criteria(content),
    "description": extract_description(content),
    "implementation_notes": extract_implementation_notes(content),

    # Conditional fields (only if require-kit installed)
    "requirements": [],
    "bdd_scenarios": [],
    "epic": None,
    "feature": None,
    "requirements_loaded": False,
    "epic_feature_loaded": False
}

# Load require-kit features if available
if has_require_kit and supports_requirements():
    task_context["requirements"] = frontmatter.requirements or []
    task_context["bdd_scenarios"] = frontmatter.bdd_scenarios or []
    task_context["epic"] = frontmatter.epic
    task_context["feature"] = frontmatter.feature
    task_context["requirements_loaded"] = True
    task_context["epic_feature_loaded"] = True
```

**STEP 4: Validate Context**

**VALIDATE** essential fields exist:
- `title`: Must be present
- `acceptance_criteria`: At least one criterion required
- Conditional validation:
  - IF require-kit installed: Check if requirements/bdd_scenarios referenced but empty
  - IF not installed: Warn if frontmatter references these fields

**STEP 5: Display Context Summary**

**DISPLAY** loaded context summary with package status:
```
📋 Task Context Loaded

ℹ️  Package Detection:
- taskwright: ✅ installed
- require-kit: {✅ installed | ❌ not installed}

ID: {task_id}
Title: {title}
State: {state}
Priority: {priority}

{If require-kit installed:}
Requirements: {len(requirements)} linked ({', '.join(requirements[:3])}{' ...' if len > 3})
BDD Scenarios: {len(bdd_scenarios)} linked
Epic: {epic or 'None'}
Feature: {feature or 'None'}

{If require-kit NOT installed:}
Requirements: Skipped (install require-kit for EARS requirements)
BDD Scenarios: Skipped (install require-kit for BDD scenarios)
Epic/Feature: Skipped (install require-kit for hierarchy context)

Acceptance Criteria: {len(acceptance_criteria)} items
```

**STEP 6: Check for Unavailable Feature References**

**IF** require-kit NOT installed AND task references require-kit features:
```python
if not has_require_kit:
    referenced_features = []
    if frontmatter.epic:
        referenced_features.append(f"Epic: {frontmatter.epic}")
    if frontmatter.requirements:
        referenced_features.append(f"Requirements: {frontmatter.requirements}")
    if frontmatter.bdd_scenarios:
        referenced_features.append(f"BDD Scenarios: {frontmatter.bdd_scenarios}")

    if referenced_features:
        **DISPLAY** warning:
        ```
        ⚠️  Task {task_id} references features that cannot be loaded

        Referenced in task metadata:
        {for feature in referenced_features: print(f"- {feature}")}

        These require require-kit to be installed.

        To enable full context loading:
          cd require-kit
          ./installer/scripts/install.sh

        Continue with task description only? [Y/n]
        ```

        **WAIT** for user confirmation (default: Yes after 5 seconds)

        **IF** user declines:
            **DISPLAY**: "Task execution cancelled. Install require-kit or remove references from task metadata."
            **EXIT** with error code
```

**PROCEED** to Step 2 (Detect Technology Stack)

### Step 2: Detect Technology Stack (REQUIRED - 10 seconds)

**READ** `.claude/settings.json` and extract `project.template` value.

If file exists: Use `project.template` value
If file not exists: Set stack to "default"

**DISPLAY**: "🔍 Detected stack: {stack}"

### Step 3: Select Agents for Stack (REQUIRED - 5 seconds)

Based on detected stack, **MAP** to agents using this table:

| Stack | Analysis | Planning | Arch Review | Implementation | Testing | Review |
|-------|----------|----------|-------------|----------------|---------|--------|
| **maui** | requirements-analyst | maui-usecase-specialist | architectural-reviewer | maui-usecase-specialist | dotnet-testing-specialist | code-reviewer |
| **react** | requirements-analyst | react-state-specialist | architectural-reviewer | react-state-specialist | react-testing-specialist | code-reviewer |
| **python** | requirements-analyst | python-api-specialist | architectural-reviewer | python-api-specialist | python-testing-specialist | code-reviewer |
| **python-mcp** | requirements-analyst | python-mcp-specialist | architectural-reviewer | python-mcp-specialist | python-testing-specialist | code-reviewer |
| **typescript-api** | requirements-analyst | nestjs-api-specialist | architectural-reviewer | typescript-domain-specialist | nodejs-testing-specialist | code-reviewer |
| **dotnet-microservice** | requirements-analyst | dotnet-api-specialist | architectural-reviewer | dotnet-domain-specialist | dotnet-testing-specialist | code-reviewer |
| **default** | requirements-analyst | software-architect | architectural-reviewer | task-manager | test-verifier | code-reviewer |

**DISPLAY**: "🤖 Selected agents: [list agent names]"

### Step 4: INVOKE TASK TOOL FOR EACH PHASE (REQUIRED - DO NOT SKIP)

**⚠️ CRITICAL: YOU MUST USE THE TASK TOOL. DO NOT ATTEMPT TO DO THE WORK YOURSELF.**

#### Phase 1: Requirements Analysis (Enhanced with Feature Detection)

**STEP 1: Validate Mode Requirements**

**IF** mode == 'bdd':
```python
from lib.feature_detection import supports_bdd

if not supports_bdd():
    **DISPLAY** error:
    ```
    ❌ BDD mode requires require-kit

    You requested: /task-work {task_id} --mode=bdd
    Available modes: standard, tdd

    Options:
    1. Install require-kit for BDD support:
       cd require-kit && ./installer/scripts/install.sh

    2. Use alternative mode:
       /task-work {task_id} --mode=tdd

    3. Use standard mode:
       /task-work {task_id} --mode=standard
    ```
    **EXIT** with error code

# Check if task has BDD scenarios linked
if not task_context.get("bdd_scenarios"):
    **DISPLAY** error:
    ```
    ❌ BDD mode requires linked BDD scenarios

    Task {task_id} has no linked BDD scenarios.

    Options:
    1. Generate BDD scenarios first:
       /generate-bdd {task_id}

    2. Use alternative mode:
       /task-work {task_id} --mode=standard
    ```
    **EXIT** with error code
```

**STEP 2: Invoke Requirements Analysis**

**INVOKE** Task tool:
```
subagent_type: "requirements-analyst"
description: "Analyze requirements for TASK-XXX"
prompt: "Analyze task TASK-XXX requirements and acceptance criteria.
         Extract key functional requirements, non-functional requirements,
         and testable acceptance criteria for {stack} implementation.
         Identify any gaps or ambiguities that need clarification.

         {If require-kit installed and requirements linked:}
         EARS Requirements Available:
         {Load and include EARS requirements from linked REQ-XXX files}

         {If BDD mode and scenarios linked:}
         BDD Scenarios Available:
         {Load and include BDD scenarios from linked BDD-XXX files}

         {If epic/feature context available:}
         Epic/Feature Context:
         Epic: {epic_id} - {epic_title}
         Feature: {feature_id} - {feature_title}

         {If require-kit NOT installed:}
         Note: Using task description and acceptance criteria only.
         EARS requirements and BDD scenarios not available (require-kit not installed)."
```

**WAIT** for agent to complete before proceeding.

#### Phase 2: Implementation Planning

**INVOKE** Task tool:
```
subagent_type: "{selected_planning_agent_from_table}"
description: "Plan implementation for TASK-XXX"
prompt: "Design {stack} implementation approach for TASK-XXX.
         Include architecture decisions, pattern selection, and component structure.
         Consider {stack}-specific best practices and testing strategies.
         Output: Implementation plan with file structure and key components."
```

**WAIT** for agent to complete before proceeding.

#### Phase 2.5A: Pattern Suggestion (NEW - Recommend design patterns)

**IF** Design Patterns MCP is available (check for mcp__design-patterns tools):

**QUERY** Design Patterns MCP using problem description from implementation plan:
```
Use find_patterns or search_patterns to query:
- Problem description from task requirements
- Constraints extracted from EARS requirements (performance, scalability, security)
- Technology stack context

Example query:
"I need a pattern for handling external API failures gracefully with timeout constraints under 200ms"

Parse MCP response to extract:
- Recommended patterns (with confidence scores)
- Pattern categories (Resilience, Performance, etc.)
- Why each pattern is recommended
- Implementation guidance for {stack}
```

**DISPLAY** pattern recommendations (if any found):
```
🎯 Design Pattern Recommendations

Based on task requirements and constraints:

1. **Circuit Breaker Pattern** (Confidence: 95%)
   Category: Resilience
   Why: Handles external API failures, enforces timeout constraints
   Stack guidance: {stack-specific implementation notes from MCP}

2. **Retry Pattern** (Confidence: 82%)
   Category: Resilience
   Why: Handles transient failures, works with Circuit Breaker
   Stack guidance: {stack-specific implementation notes from MCP}

[Additional patterns if relevant...]
```

**IF** no Design Patterns MCP available, skip to Phase 2.5B.

#### Phase 2.5B: Architectural Review (Catch design issues early)

**INVOKE** Task tool:
```
subagent_type: "architectural-reviewer"
description: "Review architecture for TASK-XXX"
prompt: "Review the implementation plan from Phase 2 for TASK-XXX.
         Evaluate against SOLID principles, DRY principle, and YAGNI principle.
         Check for: single responsibility, proper abstraction, unnecessary complexity.
         Score each principle (0-100) and provide specific recommendations.

         PATTERN CONTEXT (if Design Patterns MCP was queried):
         {Include pattern recommendations from Phase 2.5A}
         - Validate if suggested patterns are appropriate
         - Check if implementation plan aligns with pattern best practices
         - Identify if patterns are over-engineered for the requirements

         Approval thresholds:
         - ≥80/100: Auto-approve (proceed to Phase 3)
         - 60-79/100: Approve with recommendations
         - <60/100: Reject (revise design)
         Output: Architectural review report with approval decision."
```

**WAIT** for agent to complete before proceeding.

#### Phase 2.7: Complexity Evaluation (NEW - Auto-proceed mode routing)

**INVOKE** Task tool:
```
subagent_type: "complexity-evaluator"
description: "Evaluate implementation complexity for TASK-XXX"
prompt: "Evaluate implementation complexity for TASK-XXX using the implementation plan from Phase 2.

         Extract and analyze:
         - File count (files to create/modify)
         - Design patterns mentioned
         - External dependencies (APIs, databases, services)
         - Risk indicators (security, schema changes, performance)

         Calculate complexity score (1-10 scale) based on:
         - File complexity factor (0-3 points)
         - Pattern familiarity factor (0-2 points)
         - Risk level factor (0-3 points)

         Detect force-review triggers:
         - User flag (--review)
         - Security keywords
         - Breaking changes
         - Schema changes
         - Hotfix

         Route to review mode:
         - Score 1-3: AUTO_PROCEED (display summary, proceed to Phase 3)
         - Score 4-6: QUICK_OPTIONAL (offer optional checkpoint)
         - Score 7-10 or triggers: FULL_REQUIRED (mandatory Phase 2.6)

         Output: ComplexityScore with routing decision and human-readable summary."
```

**WAIT** for agent to complete before proceeding.

**EVALUATE** complexity evaluation result:

```python
complexity_result = extract_complexity_result(phase_27_output)
review_mode = complexity_result.review_mode  # AUTO_PROCEED, QUICK_OPTIONAL, or FULL_REQUIRED
```

**IF** review_mode == AUTO_PROCEED:
- Display complexity summary
- Automatically proceed to Phase 3 (no human intervention)

**ELSE IF** review_mode == QUICK_OPTIONAL:
- Display complexity summary with optional checkpoint prompt
- Offer user choice: [A]pprove, [R]eview, [Enter] to auto-approve
- Default to proceed after 10 seconds timeout
- If user chooses [R]eview, proceed to Phase 2.6

**ELSE IF** review_mode == FULL_REQUIRED:
- Display detailed complexity summary
- Mandatory Phase 2.6 human checkpoint (see below)

#### Phase 2.6: Human Checkpoint (Optional - Triggered by complexity evaluation or critical tasks)

**NOTE**: This phase is now triggered by Phase 2.7 complexity evaluation:
- **Mandatory**: If complexity score 7-10 OR force-review triggers detected
- **Optional**: If complexity score 4-6 AND user chooses to review
- **Skipped**: If complexity score 1-3 (auto-proceed)

**Human checkpoint is triggered by Phase 2.7 complexity evaluation**:

```python
# Automatic triggers from Phase 2.7
if complexity_result.review_mode == FULL_REQUIRED:
    trigger_checkpoint = True
    checkpoint_reason = "Complexity score 7-10 or force-review triggers"
elif complexity_result.review_mode == QUICK_OPTIONAL and user_chose_review:
    trigger_checkpoint = True
    checkpoint_reason = "User requested review (optional)"
else:
    trigger_checkpoint = False  # AUTO_PROCEED - skip to Phase 3
```

**IF TRIGGERED**, display interactive checkpoint:

```
═══════════════════════════════════════════════════════
🔍 PHASE 2.6 - HUMAN CHECKPOINT REQUIRED
═══════════════════════════════════════════════════════

TASK: {TASK-ID} - {Title}

COMPLEXITY EVALUATION (Phase 2.7):
  Score: {complexity_score}/10 ({review_mode})
  Triggers: {List of force-review triggers}
  Reason: {checkpoint_reason}

ARCHITECTURAL REVIEW (Phase 2.5B):
  Score: {arch_score}/100 ({arch_status})
  Issues: {issue_count}
  {List of critical issues and recommendations}

ESTIMATED FIX TIME: {minutes} minutes (design adjustment)

OPTIONS:
1. [A]pprove - Proceed with current design
2. [R]evise - Apply recommendations and re-review
3. [V]iew - Show full architectural review report
4. [C]omplexity - Show detailed complexity breakdown
5. [D]iscuss - Escalate to software-architect

Your choice (A/R/V/C/D):
═══════════════════════════════════════════════════════
```

**WAIT** for human decision:
- **Approve**: Continue to Phase 3 (implementation)
- **Revise**: Loop back to Phase 2 (planning) with feedback
- **View**: Display full architectural review report, then prompt again
- **Complexity**: Display detailed complexity breakdown, then prompt again
- **Discuss**: Invoke software-architect agent for consultation

**IF NOT TRIGGERED** (auto-proceed from Phase 2.7):
- Display complexity summary (score 1-3)
- Automatically proceed to Phase 3 with no human intervention

#### Phase 2.7: Implementation Plan Generation & Complexity Evaluation (ENHANCED)

**PURPOSE**: Generate structured implementation plan and evaluate complexity to route to appropriate review mode

**ENHANCEMENTS (TASK-027 - Markdown Plans)**:
- **Dual Format Support**: Generates both Markdown (`implementation_plan.md`) and JSON (`implementation_plan.json`) formats
- **Human-Readable Plans**: Markdown format improves readability for Phase 2.8 checkpoint display
- **Backward Compatibility**: JSON format preserved for automated processing
- **Git-Friendly**: Markdown plans are easier to review in version control diffs
- **Plan Location**: Both files saved to `docs/state/{task_id}/`

**INVOKE** Task tool:
```
subagent_type: "task-manager"
description: "Generate implementation plan and evaluate complexity for TASK-XXX"
prompt: "Execute Phase 2.7 for TASK-XXX:

         STEP 1: PARSE IMPLEMENTATION PLAN
         - Parse Phase 2 planning output into structured ImplementationPlan
         - Extract: files to create/modify, patterns, dependencies, risks, phases
         - Use stack-specific parser if available, fallback to generic
         - Save to: docs/state/{task_id}/implementation_plan.json

         STEP 2: CALCULATE COMPLEXITY SCORE
         - Use ComplexityCalculator to evaluate plan (1-10 scale)
         - Factors: file count, pattern familiarity, risk level, dependencies
         - Save to: docs/state/{task_id}/complexity_score.json

         STEP 3: DETECT FORCE-REVIEW TRIGGERS
         - Security keywords (auth, password, encryption, etc.)
         - Schema changes (database migrations)
         - Breaking changes (public API modifications)
         - User flag (--review command-line option)
         - Hotfix or production tags

         STEP 4: DETERMINE REVIEW MODE
         - Score 1-3 + no triggers → AUTO_PROCEED
         - Score 4-6 + no triggers → QUICK_OPTIONAL
         - Score 7-10 OR any trigger → FULL_REQUIRED

         STEP 5: RETURN RESULTS
         - ComplexityScore with review_mode
         - ImplementationPlan path
         - Force triggers list (if any)

         Stack: {detected_stack}
         Phase 2 Output: {phase_2_planning_output}
         Task Metadata: {task_frontmatter}"
```

**WAIT** for agent to complete before proceeding.

**EXTRACT** Phase 2.7 results:
```python
complexity_score = extract_complexity_score(phase_27_output)
review_mode = complexity_score.review_mode  # AUTO_PROCEED | QUICK_OPTIONAL | FULL_REQUIRED
plan_path = f"docs/state/{task_id}/implementation_plan.json"
triggers = complexity_score.forced_review_triggers
```

**DISPLAY** Phase 2.7 summary:
```
Phase 2.7 Complete: Plan Generated & Complexity Evaluated

Plan saved: {plan_path}
Complexity Score: {complexity_score.total_score}/10 ({complexity_score.level})
Review Mode: {review_mode}
{If triggers: "Force Triggers: " + ", ".join(triggers)}
```

#### Phase 2.8: Human Plan Checkpoint (ENHANCED - Rich Display & Interactive Modification)

**PURPOSE**: Route to appropriate review based on complexity score from Phase 2.7, with rich visual display and interactive plan modification capabilities.

**ENHANCEMENTS (TASK-028, TASK-029)**:
- **Rich Visual Display**: Human-readable plan summary with file changes, dependencies, risks, effort
- **Markdown & JSON Support**: Loads plans from both `implementation_plan.md` and `implementation_plan.json`
- **Interactive Modification**: [M]odify option for adjusting plan before implementation
- **Version Management**: Automatic plan versioning with timestamped backups
- **Undo Support**: Revert to previous plan versions during modification

**ROUTE** based on review_mode from Phase 2.7:

**IF** review_mode == AUTO_PROCEED:
```
Display auto-proceed summary:

  Auto-Proceed Mode (Low Complexity)

  Complexity: {score}/10 (Simple task)
  Files: {file_count} file(s)
  Tests: {test_count} tests planned
  Estimated: ~{duration} minutes

  Automatically proceeding to implementation (no review needed)...

Update task metadata:
  auto_approved: true
  approved_by: "system"
  approved_at: {current_timestamp}
  review_mode: "auto_proceed"

Proceed immediately to Phase 3 (Implementation)
```

**ELSE IF** review_mode == QUICK_OPTIONAL:

**INVOKE** Task tool:
```
subagent_type: "task-manager"
description: "Execute quick review checkpoint for TASK-XXX"
prompt: "Execute Phase 2.8 Quick Review for TASK-XXX:

         STEP 1: LOAD CONTEXT
         - Load ImplementationPlan from {plan_path}
         - Load ComplexityScore from complexity_score.json
         - Extract summary information

         STEP 2: DISPLAY QUICK REVIEW CARD
         - Complexity score and level
         - File count summary
         - Pattern summary
         - Estimated duration
         - Brief risk summary (if any)

         STEP 3: START 10-SECOND COUNTDOWN
         - Use QuickReviewHandler from review_modes.py
         - Display countdown timer (10...9...8...)
         - Listen for user input:
           * ENTER pressed → Return 'escalate' (escalate to full review)
           * 'c' pressed → Return 'cancel' (cancel task, move to backlog)
           * Timeout (no input) → Return 'timeout' (auto-approve, proceed to Phase 3)

         STEP 4: UPDATE TASK METADATA
         - Record review decision
         - Update timestamps
         - Set proceed_to_phase_3 flag accordingly

         Return result: {'action': 'timeout'|'escalate'|'cancel', 'duration': seconds}"
```

**WAIT** for result

**IF** result.action == 'timeout':
  - **DISPLAY**: "Quick review timed out. Auto-approving task..."
  - **UPDATE** task metadata: `auto_approved: true, approved_by: "timeout", review_mode: "quick_optional"`
  - **PROCEED** to Phase 3 (Implementation)

**ELSE IF** result.action == 'escalate':
  - **DISPLAY**: "Escalating to full review mode..."
  - **UPDATE** review_mode to FULL_REQUIRED
  - **SET** escalated flag: true
  - **FALL THROUGH** to FULL_REQUIRED handling below

**ELSE IF** result.action == 'cancel':
  - **DISPLAY**: "Task cancelled by user"
  - **UPDATE** task metadata: `cancelled: true, cancelled_at: {timestamp}, cancelled_reason: "User cancelled during quick review"`
  - **MOVE** task file from in_progress/ to backlog/
  - **EXIT** task-work command

**ELSE IF** review_mode == FULL_REQUIRED (OR escalated from QUICK_OPTIONAL):

**STEP 1: LOAD PLAN AND DISPLAY ENHANCED CHECKPOINT (TASK-028)**

Load implementation plan from either:
- `docs/state/{task_id}/implementation_plan.md` (Markdown format - TASK-027)
- `docs/state/{task_id}/implementation_plan.json` (JSON format - legacy)

**Display rich visual checkpoint**:

```
═══════════════════════════════════════════════════════════════
🎯 PHASE 2.8 - IMPLEMENTATION PLAN CHECKPOINT
═══════════════════════════════════════════════════════════════

TASK: TASK-042 - Implement user authentication API

COMPLEXITY: 7/10 (High - Full review required)

📁 FILES TO CREATE (5 files):
   1. src/auth/login.py           - Login endpoint handler
   2. src/auth/session.py         - Session management
   3. src/auth/validator.py       - Input validation
   4. tests/test_login.py         - Login endpoint tests
   5. tests/test_session.py       - Session management tests

📦 EXTERNAL DEPENDENCIES (3 new packages):
   • bcrypt - Password hashing
   • PyJWT - JWT token generation
   • redis - Session storage

⚠️  RISKS IDENTIFIED (2 risks):
   🟡 MEDIUM - External dependency on Redis server
   🔴 HIGH - Security: Password storage and session tokens

⏱️  ESTIMATED EFFORT:
   • Duration: 8 hours
   • Lines of Code: ~450 lines
   • Complexity: High (7/10)

🏗️  IMPLEMENTATION PHASES:
   Phase 1: Models and validation (2h)
   Phase 2: Authentication logic (3h)
   Phase 3: Session management (2h)
   Phase 4: Testing (1h)

📊 ARCHITECTURAL REVIEW:
   Overall Score: 85/100 (Approved with recommendations)
   SOLID: 88/100
   DRY: 82/100
   YAGNI: 85/100

OPTIONS:
  [A]pprove  - Proceed with current plan
  [M]odify   - Edit plan before implementation (TASK-029)
  [V]iew     - Show complete plan in pager
  [C]ancel   - Cancel task, return to backlog

Your choice [A/M/V/C]:
═══════════════════════════════════════════════════════════════
```

**STEP 2: HANDLE USER DECISION**

**IF** user selects [A]pprove:
  - **DISPLAY**: "Plan approved. Proceeding to implementation..."
  - **UPDATE** task metadata: `approved: true, approved_by: "user", approved_at: {timestamp}, review_mode: "full_required"`
  - **IF** escalated: Also update `escalated: true`
  - **PROCEED** to Phase 3 (Implementation)

**ELSE IF** user selects [M]odify (TASK-029 - Interactive Plan Modification):

  **ENTER MODIFICATION LOOP**:

  ```
  ═══════════════════════════════════════════════════════════════
  📝 PLAN MODIFICATION MODE
  ═══════════════════════════════════════════════════════════════

  Select what to modify:
    1. Files - Add/remove files to create or modify
    2. Dependencies - Add/remove/update external dependencies
    3. Risks - Add/remove/modify risks and mitigations
    4. Effort - Adjust duration or complexity estimates
    5. [U]ndo - Revert to previous version
    6. [D]one - Save changes and return to checkpoint
    7. [C]ancel - Discard changes

  Choice [1-4/U/D/C]:
  ```

  **Modification Options**:

  **1. Modify Files**:
  ```
  Current files to create (5):
    1. src/auth/login.py
    2. src/auth/session.py
    3. src/auth/validator.py
    4. tests/test_login.py
    5. tests/test_session.py

  Actions:
    [A]dd file - Add new file to plan
    [R]emove file - Remove file from plan
    [B]ack - Return to modification menu

  Choice [A/R/B]:
  ```

  **2. Modify Dependencies**:
  ```
  Current dependencies (3):
    1. bcrypt - Password hashing
    2. PyJWT - JWT token generation
    3. redis - Session storage

  Actions:
    [A]dd dependency - Add new package
    [R]emove dependency - Remove package
    [M]odify dependency - Change version or justification
    [B]ack - Return to modification menu

  Choice [A/R/M/B]:
  ```

  **3. Modify Risks**:
  ```
  Current risks (2):
    1. 🟡 MEDIUM - External dependency on Redis server
    2. 🔴 HIGH - Security: Password storage and session tokens

  Actions:
    [A]dd risk - Add new risk
    [R]emove risk - Remove risk
    [M]odify risk - Change severity or mitigation
    [B]ack - Return to modification menu

  Choice [A/R/M/B]:
  ```

  **4. Modify Effort**:
  ```
  Current estimates:
    Duration: 8 hours
    Lines of Code: ~450 lines
    Complexity: 7/10 (High)

  Enter new values (or press Enter to keep):
    Duration [8h]: 10h
    LOC [~450]: ~500
    Complexity [7]: 8

  Updated estimates:
    Duration: 10 hours (+25%)
    Lines of Code: ~500 lines (+11%)
    Complexity: 8/10 (High)

  Confirm changes? [y/n]:
  ```

  **Version Management**:
  - Automatically saves plan versions: `implementation_plan_v1.json`, `implementation_plan_v2.json`, etc.
  - Each modification creates timestamped backup
  - [U]ndo option reverts to previous version
  - Plan history tracked in task metadata

  **After Modifications Complete**:
  - Save updated plan to `implementation_plan.md` and `implementation_plan.json`
  - Recalculate complexity score based on new plan
  - Update architectural review if significant changes
  - Return to Phase 2.8 checkpoint display with updated plan
  - Prompt user again: [A]pprove / [M]odify / [V]iew / [C]ancel

  **Modification Metadata** (saved to task frontmatter):
  ```yaml
  plan_modifications:
    - version: 1
      timestamp: "2025-10-19T14:30:00Z"
      changes:
        - category: "dependencies"
          action: "added"
          detail: "Added redis-py package"
        - category: "effort"
          action: "modified"
          detail: "Increased duration from 8h to 10h"
      complexity_before: 7
      complexity_after: 8
    current_version: 1
  ```

**ELSE IF** user selects [V]iew:
  - Display complete plan in pager (less/more command)
  - Return to checkpoint prompt after viewing

**ELSE IF** user selects [C]ancel:
  - **CONFIRM**: "Are you sure you want to cancel? [y/n]:"
  - **IF** confirmed:
    - **DISPLAY**: "Task cancelled by user"
    - **UPDATE** task metadata: `cancelled: true, cancelled_at: {timestamp}, cancelled_reason: "User cancelled during full review"`
    - **MOVE** task file from in_progress/ to backlog/
    - **EXIT** task-work command

#### Phase 2.9: Workflow Routing (NEW - Design-First Workflow Support)

**PURPOSE**: Route to appropriate workflow based on flags from Step 0

**EVALUATE** workflow mode:

```python
# Check which workflow to execute
if design_only:
    # DESIGN-ONLY workflow: Stop here, save design, move to design_approved state
    workflow_mode = "design_only"
elif implement_only:
    # IMPLEMENT-ONLY workflow: Verify prerequisites, skip to Phase 3
    workflow_mode = "implement_only"
else:
    # STANDARD workflow: Continue to Phase 3 as normal
    workflow_mode = "standard"
```

**PATH A: DESIGN-ONLY Workflow** (--design-only flag):

```python
if workflow_mode == "design_only":
    print("\n🎨 Design-Only Workflow Complete")
    print("=" * 67)

    # Import plan persistence module
    from installer.global.commands.lib.plan_persistence import save_plan

    # Save implementation plan to disk
    plan_data = {
        "files_to_create": extract_files_to_create(phase_2_output),
        "files_to_modify": extract_files_to_modify(phase_2_output),
        "external_dependencies": extract_dependencies(phase_2_output),
        "estimated_duration": extract_duration(phase_2_output),
        "estimated_loc": extract_loc(phase_2_output),
        "phases": extract_phases(phase_2_output),
        "test_summary": extract_test_summary(phase_2_output),
        "risks": extract_risks(phase_2_output)
    }

    architectural_review = {
        "overall_score": arch_score,
        "status": arch_status,
        "principles": {
            "solid": solid_score,
            "dry": dry_score,
            "yagni": yagni_score
        },
        "recommendations": arch_recommendations
    }

    plan_path = save_plan(task_id, plan_data, architectural_review)
    print(f"✅ Implementation plan saved: {plan_path}")

    # Update task frontmatter with design metadata
    design_metadata = {
        "status": "approved",
        "approved_at": datetime.now().isoformat(),
        "approved_by": "human",  # or "auto" if auto-approved
        "implementation_plan_version": "v1",
        "architectural_review_score": arch_score,
        "complexity_score": complexity_score.total_score,
        "design_session_id": f"design-{task_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "design_notes": "Design approved via --design-only workflow"
    }

    # Add design section to task frontmatter
    # ... (update task file with design metadata)

    # Move task to design_approved state
    # ... (move file from current state to tasks/design_approved/)

    # Display success report
    print("\n✅ Design Phase Complete - " + task_id)
    print()
    print("🎨 Design Approval Summary:")
    print(f"- Architectural Review: {arch_score}/100 ({arch_status})")
    print(f"- Complexity Score: {complexity_score.total_score}/10 ({complexity_score.level})")
    print(f"- Approval Status: APPROVED")
    print(f"- Approved By: {design_metadata['approved_by']}")
    print(f"- Approved At: {design_metadata['approved_at']}")
    print()
    print("📋 Implementation Plan:")
    print(f"- Files to create: {len(plan_data['files_to_create'])}")
    print(f"- External dependencies: {len(plan_data['external_dependencies'])}")
    print(f"- Estimated duration: {plan_data['estimated_duration']}")
    print(f"- Estimated LOC: {plan_data.get('estimated_loc', 'N/A')}")
    print()
    print("🔄 State Transition:")
    print(f"From: {current_state}")
    print("To: DESIGN_APPROVED")
    print("Reason: Design approved via --design-only workflow")
    print()
    print("📋 Next Steps:")
    print("1. Review the saved implementation plan")
    print("2. Schedule implementation session")
    print(f"3. Run: /task-work {task_id} --implement-only")
    print()
    print("💾 Design artifacts saved to task metadata")

    # EXIT - Do not proceed to Phase 3
    exit(0)
```

**PATH B: IMPLEMENT-ONLY Workflow** (--implement-only flag):

```python
elif workflow_mode == "implement_only":
    print("\n🚀 Implement-Only Workflow: Loading Approved Design")
    print("=" * 67)

    # Import phase execution module
    from installer.global.commands.lib.phase_execution import execute_implementation_phases, StateValidationError
    from installer.global.commands.lib.plan_persistence import load_plan, plan_exists

    # Verify task is in design_approved state
    if current_state != "design_approved":
        raise StateValidationError(
            f"❌ Cannot execute --implement-only workflow\n\n"
            f"Task {task_id} is in '{current_state}' state.\n"
            f"Required state: design_approved\n\n"
            f"To approve design first, run:\n"
            f"  /task-work {task_id} --design-only\n\n"
            f"Or run complete workflow without flags:\n"
            f"  /task-work {task_id}"
        )

    # Verify design metadata exists
    design_metadata = task_context.get("design", {})
    if not design_metadata or design_metadata.get("status") != "approved":
        raise PhaseExecutionError(
            f"❌ Design metadata missing or invalid for {task_id}\n\n"
            f"Task is in design_approved state, but design metadata is incomplete.\n"
            f"Re-run design phase: /task-work {task_id} --design-only"
        )

    # Verify implementation plan exists
    if not plan_exists(task_id):
        raise PhaseExecutionError(
            f"❌ Implementation plan not found for {task_id}\n\n"
            f"Design was approved but plan file is missing.\n"
            f"Re-run design phase: /task-work {task_id} --design-only"
        )

    # Load implementation plan
    saved_plan = load_plan(task_id)
    plan_data = saved_plan["plan"]

    # Display implementation start context
    print()
    print(f"TASK: {task_id} - {task_context['title']}")
    print()
    print("APPROVED DESIGN:")
    print(f"  Design approved: {design_metadata.get('approved_at', 'unknown')}")
    print(f"  Approved by: {design_metadata.get('approved_by', 'unknown')}")
    print(f"  Architectural score: {design_metadata.get('architectural_review_score', 'N/A')}/100")
    print(f"  Complexity score: {design_metadata.get('complexity_score', 'N/A')}/10")
    print()
    print("IMPLEMENTATION PLAN:")
    print(f"  Files to create: {len(plan_data.get('files_to_create', []))}")
    print(f"  External dependencies: {len(plan_data.get('external_dependencies', []))}")
    print(f"  Estimated duration: {plan_data.get('estimated_duration', 'N/A')}")
    print(f"  Test strategy: {plan_data.get('test_summary', 'N/A')}")
    print()
    print("Beginning implementation phases (3 → 4 → 4.5 → 5)...")
    print("=" * 67)
    print()

    # Move task from design_approved to in_progress
    # ... (move file from tasks/design_approved/ to tasks/in_progress/)

    # SKIP Phases 1-2.8, jump directly to Phase 3
    # (Phases 1-2.8 results are already in saved_plan)

    # Continue to Phase 3 with loaded plan
    # ... (Phase 3 execution continues below)
```

**PATH C: STANDARD Workflow** (no flags):

```python
else:  # workflow_mode == "standard"
    print("\n🔄 Standard Workflow: Proceeding to Implementation")
    print("Design phases complete, continuing to implementation...\n")

    # No special handling needed - continue to Phase 3 as normal
    # This is the existing behavior (backward compatible)
```

#### Phase 3: Implementation

**INVOKE** Task tool:
```
subagent_type: "{selected_implementation_agent_from_table}"
description: "Implement TASK-XXX"
prompt: "Implement TASK-XXX following {stack} best practices and planned architecture.
         Use patterns identified in planning phase.
         Create production-quality code with proper error handling.
         Follow {stack}-specific conventions and patterns.
         Prepare codebase for comprehensive testing."
```

**WAIT** for agent to complete before proceeding.

#### Phase 4: Testing

**CRITICAL**: Refer to test-orchestrator.md for mandatory compilation verification before testing.

**INVOKE** Task tool:
```
subagent_type: "{selected_testing_agent_from_table}"
description: "Generate and execute tests for TASK-XXX"
prompt: "Create comprehensive test suite for TASK-XXX implementation.
         Include: unit tests, integration tests, edge cases.
         Target: 80%+ line coverage, 75%+ branch coverage.
         Use {stack}-specific testing frameworks and patterns.

         🚨 MANDATORY COMPILATION CHECK (See test-orchestrator.md):
         1. MUST verify code COMPILES/BUILDS successfully BEFORE running tests
         2. If compilation fails, report errors immediately with file:line details
         3. ONLY proceed to test execution if compilation succeeds with zero errors
         4. Use stack-specific build commands (see test-orchestrator.md for details)

         EXECUTE the test suite and report detailed results:
         - Build/compilation status (MUST be success before tests run)
         - Test execution results (passed/failed counts)
         - Coverage metrics (line and branch percentages)
         - Detailed failure information for any failing tests

         Cross-reference: installer/global/agents/test-orchestrator.md (MANDATORY RULE #1)"
```

**WAIT** for agent to complete before proceeding.

#### Phase 4.5: Fix Loop (Ensure All Tests Pass)

🚨 **ABSOLUTE REQUIREMENT - ZERO TOLERANCE FOR TEST FAILURES** 🚨

The task-work command has **ZERO TOLERANCE** for compilation errors or test failures.
This phase MUST NOT complete until:
- Code compiles with ZERO errors (100% build success)
- ALL tests pass (100% test pass rate)
- NO tests are skipped, ignored, or commented out

**Cross-reference**: See test-orchestrator.md for quality gate enforcement details.

**EVALUATE** test results from Phase 4:

```python
compilation_errors = extract_compilation_errors(phase_4_output)
test_failures = extract_test_failures(phase_4_output)
coverage = extract_coverage(phase_4_output)

max_attempts = 3
attempt = 1
```

**WHILE** (compilation_errors > 0 OR test_failures > 0) AND attempt <= max_attempts:

1. **DISPLAY** Failure Report:
   ```
   ⚠️  TESTS FAILING - Entering Fix Loop (Attempt {attempt}/3)

   Compilation Errors: {count}
   {List of compilation errors with file:line}

   Test Failures: {count}
   {List of failing tests with assertion details}

   Initiating automatic fix cycle...
   ```

2. **INVOKE** Task tool to fix issues:
   ```
   subagent_type: "{selected_implementation_agent_from_table}"
   description: "Fix test failures for TASK-XXX (Attempt {attempt})"
   prompt: "Fix the failing tests for TASK-XXX.

            COMPILATION ERRORS ({count}):
            {list_of_compilation_errors_with_file_line}

            TEST FAILURES ({count}):
            {list_of_test_failures_with_details}

            CRITICAL INSTRUCTIONS:
            1. Fix ALL compilation errors FIRST - code must build
            2. Run the build command to verify compilation succeeds
            3. Fix failing test assertions by correcting the implementation
            4. Ensure code behavior matches test expectations
            5. Do NOT modify tests unless they're provably incorrect
            6. Do NOT skip, comment out, or ignore failing tests
            7. Do NOT mark tests with [Ignore] or skip attributes

            SUCCESS CRITERIA:
            - Zero compilation errors
            - All tests pass (100%)
            - No tests skipped or ignored

            You MUST achieve passing tests before completing."
   ```

3. **WAIT** for fix to complete

4. **RE-INVOKE** Phase 4 Testing:
   ```
   subagent_type: "{selected_testing_agent_from_table}"
   description: "Re-run tests for TASK-XXX after fixes (Attempt {attempt})"
   prompt: "Re-execute the complete test suite for TASK-XXX after fixes.

            VERIFY:
            1. Code compiles/builds successfully (no errors)
            2. All tests execute without errors
            3. All tests pass (no failures)
            4. Coverage meets thresholds (≥80% line, ≥75% branch)

            Report detailed results including:
            - Build/compilation status
            - Test pass/fail counts
            - Coverage percentages
            - Any remaining failures"
   ```

5. **WAIT** for test execution to complete

6. **RE-EVALUATE** results:
   ```python
   compilation_errors = extract_compilation_errors(retest_output)
   test_failures = extract_test_failures(retest_output)
   attempt += 1
   ```

7. **IF** compilation_errors == 0 AND test_failures == 0:
   ```
   ✅ All tests passing! Proceeding to code review.
   ```
   **BREAK** out of loop → Proceed to Phase 5

8. **ELSE IF** attempt > max_attempts:
   ```
   ❌ CRITICAL: Unable to achieve passing tests after 3 attempts

   Final Status:
   - Compilation Errors: {count}
   - Test Failures: {count}
   - Coverage: {percentage}%

   Task moved to BLOCKED state with detailed diagnostics.
   Manual intervention required.

   Diagnostics have been saved to task file.
   ```
   **BREAK** out of loop → Move to BLOCKED state

9. **ELSE**:
   **CONTINUE** loop (attempt next fix)

**END WHILE**

**Result of Phase 4.5**:
- ✅ **SUCCESS**: All tests passing → Proceed to Phase 5
- ❌ **BLOCKED**: Max attempts exhausted → Move to BLOCKED state, skip Phase 5

#### Phase 5: Code Review

**ONLY EXECUTE IF Phase 4.5 succeeded (all tests passing)**

**INVOKE** Task tool:
```
subagent_type: "code-reviewer"
description: "Review TASK-XXX implementation"
prompt: "Review TASK-XXX implementation for quality and best practices.
         Check: code quality, test coverage, error handling, documentation.
         Verify {stack}-specific patterns are correctly applied.
         Provide actionable feedback if improvements needed.
         Confirm readiness for IN_REVIEW state or identify blockers."
```

**WAIT** for agent to complete before proceeding.

#### Phase 5.5: Plan Audit (Hubbard's Step 6)

**NEW PHASE** - Implements John Hubbard's Step 6 (Audit) from his proven 6-step workflow.

**When to execute:**
- Always execute after Phase 5 (Code Review)
- Only if implementation plan exists (skip for tasks without plans)
- Applies to both --implement-only and standard workflows
- NOT executed in --micro mode

**Objective:**
Verify that actual implementation matches the approved architectural plan. Catch scope creep, validate complexity estimates, and ensure AI followed instructions.

**Research Support:**
- John Hubbard's 6-step workflow: "Audit - check the code against Plan.md"
- ThoughtWorks research: "Agent frequently doesn't follow all instructions" - Birgitta Böckeler
- Closes critical gap in AI-Engineer Lite identified in SDD research analysis

**Process:**
1. **Load saved implementation plan** from `docs/state/{task_id}/implementation_plan.md`
2. **Analyze actual implementation:**
   - Scan for created/modified files
   - Count lines of code (LOC)
   - Extract dependencies from package files (requirements.txt, package.json, *.csproj)
   - Calculate implementation duration (if available in metadata)
3. **Compare planned vs actual:**
   - **Files**: List extra files, missing files
   - **Dependencies**: List extra deps, missing deps
   - **LOC**: Calculate % variance
   - **Duration**: Calculate % variance
4. **Generate audit report** with severity (low/medium/high)
5. **Display report and prompt** for human decision

**Severity Calculation:**
- **Low**: <10% variance, 0 extra files, all metrics within acceptable range
- **Medium**: 10-30% variance, 1-2 extra files, or 1-2 extra dependencies
- **High**: >30% variance, 3+ extra files, 3+ extra dependencies, or major deviations

**Human Decision Options:**
- **[A]pprove**: Accept implementation as-is, proceed to IN_REVIEW
  - Updates task metadata with audit results
  - Non-blocking default (allows unattended operation)
- **[R]evise**: Request removal of scope creep, transition to BLOCKED
  - Requires manual intervention to remove extra files/dependencies
  - Task cannot proceed until revised
- **[E]scalate**: Create follow-up task, proceed to IN_REVIEW with warning
  - Acknowledges complexity underestimation
  - Creates tracking task for scope creep investigation
  - Current task completes but flagged for analysis
- **[C]ancel**: Block task completion, transition to BLOCKED
  - Complete rejection of implementation
  - Requires full rework

**Timeout Behavior:**
- 30-second timeout for human response
- **Auto-approves if no input** (non-blocking default)
- Allows unattended operation while preserving human control option
- Audit report saved to `docs/state/{task_id}/plan_audit_report.json`

**Metrics Tracking:**
Audit outcomes are tracked in `docs/state/plan_audit_metrics.json` for:
- **Complexity model improvement**: Use LOC/duration variances to refine estimates
- **Scope creep pattern detection**: Identify common sources of extra files/deps
- **Estimation accuracy refinement**: Create feedback loop for better planning

**Example Output:**
```
======================================================================
PLAN AUDIT - TASK-042
======================================================================

PLANNED IMPLEMENTATION:
  Files: 5 files (245 lines)
  Dependencies: 2 (axios, bcrypt)
  Duration: 4 hours

ACTUAL IMPLEMENTATION:
  Files: 7 files (380 lines)
  Dependencies: 3 (axios, bcrypt, lodash)
  Duration: 6 hours

DISCREPANCIES:
  🔴 2 extra file(s) not in plan
      - src/utils/helpers.ts
      - src/utils/validators.ts

  🟡 1 extra dependenc(ies) not in plan
      - lodash

  🔴 LOC variance: +55.1% (245 → 380 lines)

  🟡 Duration variance: +50.0% (4.0h → 6.0h)

SEVERITY: 🔴 HIGH

RECOMMENDATIONS:
  1. Review extra files for scope creep: src/utils/helpers.ts, src/utils/validators.ts
  2. Justify extra dependencies: lodash
  3. Understand why LOC exceeded estimate by 55%

OPTIONS:
  [A]pprove - Accept implementation as-is, update plan retroactively
  [R]evise - Request removal of scope creep items
  [E]scalate - Mark as complex, create follow-up task
  [C]ancel - Block task completion

Choice [A]pprove/[R]evise/[E]scalate/[C]ancel (30s timeout = auto-approve): _
```

**Implementation:**
Phase 5.5 is implemented in `installer/global/commands/lib/phase_execution.py`:
- Function: `execute_phase_5_5_plan_audit(task_id, task_context)`
- Core logic: `installer/global/commands/lib/plan_audit.py`
- Metrics tracking: `installer/global/commands/lib/metrics/plan_audit_metrics.py`

**Skip Behavior:**
If no implementation plan exists (e.g., task created before Phase 2.7 was implemented), Phase 5.5 is automatically skipped:
```
⚠️  No implementation plan found - skipping audit
```

**Success Criteria:**
- Audit completes in < 5 seconds
- Discrepancies accurately detected
- Human decision properly handled
- Task metadata updated correctly
- Metrics tracked for future improvement

**Error Handling:**
- If plan doesn't exist: Skip audit, proceed to IN_REVIEW
- If audit fails: Log error, default to approve (non-blocking)
- If decision timeout: Auto-approve with warning

**Benefits:**
- ✅ Catches scope creep automatically (saves review time)
- ✅ Validates complexity estimates (improves future planning)
- ✅ Ensures AI follows plan (detects hallucinations)
- ✅ Closes Hubbard's Step 6 gap (100% workflow alignment)
- ✅ Creates feedback loop for estimation improvement

### Step 5: Evaluate Quality Gates (REQUIRED)

**Note**: Phase 4.5 (Fix Loop) already enforces test compilation and passing. This step evaluates final quality metrics.

Based on final results after Phase 4.5, **EVALUATE**:

| Gate | Threshold | Result |
|------|-----------|--------|
| Code compiles | 100% | ✅ or ❌ (Phase 4.5 enforced) |
| All tests passing | 100% | ✅ or ❌ (Phase 4.5 enforced) |
| Line coverage | ≥ 80% | ✅ or ❌ |
| Branch coverage | ≥ 75% | ✅ or ❌ |
| Test execution time | < 30s | ✅ or ⚠️ |

### Step 6: Determine Next State (REQUIRED)

🚨 **CRITICAL ENFORCEMENT LOGIC - NO EXCEPTIONS** 🚨

Based on Phase 4.5 results and quality gates, the following logic MUST be enforced:

**BLOCKING LOGIC** (explicit Python pseudocode to prevent IN_REVIEW with failures):

```python
# ABSOLUTE REQUIREMENT: Task CANNOT move to IN_REVIEW unless ALL conditions met
def determine_next_state(phase_45_results, coverage_results):
    """
    Determines next task state with ZERO TOLERANCE for failures.

    Returns:
        state: "in_review" | "blocked" | "in_progress"
        reason: Human-readable explanation
    """
    compilation_errors = phase_45_results.compilation_errors
    test_failures = phase_45_results.test_failures
    test_pass_rate = phase_45_results.passed / phase_45_results.total
    line_coverage = coverage_results.lines
    branch_coverage = coverage_results.branches

    # GATE 1: Compilation must succeed (MANDATORY)
    if compilation_errors > 0:
        return "blocked", f"BLOCKED: {compilation_errors} compilation errors remain after 3 fix attempts"

    # GATE 2: All tests must pass - NO EXCEPTIONS (MANDATORY)
    if test_failures > 0 or test_pass_rate < 1.0:
        return "blocked", f"BLOCKED: {test_failures} test failures remain (pass rate: {test_pass_rate*100:.1f}%)"

    # GATE 3: Coverage thresholds must be met (MANDATORY)
    if line_coverage < 80:
        # Re-invoke testing agent to add more tests
        return "in_progress", f"Coverage too low ({line_coverage}%), generating additional tests"

    if branch_coverage < 75:
        # Re-invoke testing agent to add more tests
        return "in_progress", f"Branch coverage too low ({branch_coverage}%), generating additional tests"

    # ALL GATES PASSED - ONLY path to IN_REVIEW
    return "in_review", "All quality gates passed: 100% tests passing, coverage thresholds met"
```

**STATE TRANSITION RULES**:

- ✅ **Phase 4.5 SUCCESS (all tests passing) + Coverage ≥ thresholds**:
  → Move task to `tasks/in_review/TASK-XXX.md`
  → All quality gates passed, ready for human review
  → **This is the ONLY path to IN_REVIEW state**

- ⚠️ **Phase 4.5 SUCCESS but coverage below threshold**:
  → Keep task in `tasks/in_progress/TASK-XXX.md`
  → **RE-INVOKE** testing agent to add more tests
  → Do NOT proceed until coverage threshold met
  → Loop back to Phase 4
  → **MUST NOT move to IN_REVIEW**

- ❌ **Phase 4.5 BLOCKED (max fix attempts exhausted with failures)**:
  → Move task to `tasks/blocked/TASK-XXX.md`
  → Include detailed diagnostics in task file:
    - Compilation errors (if any)
    - Test failure details
    - Fix attempts made
    - Recommended next steps
  → Notify that manual intervention required
  → **MUST NOT move to IN_REVIEW**

### Step 7: Generate Report (REQUIRED)

**OUTPUT** comprehensive report based on outcome:

#### Success Report (All Tests Passing)

```
✅ Task Work Complete - TASK-XXX

🔍 Stack: {detected_stack}
🤖 Agents Used: {list_of_agents}
⏱️  Duration: {total_duration}

📊 Test Results:
- Compilation: ✅ Success
- Total Tests: {total_tests}
- Passed: {passed_tests} ✅ (100%)
- Failed: 0
- Skipped: 0
- Coverage: {coverage_percentage}% (line), {branch_percentage}% (branch)

🔧 Fix Loop Summary:
- Initial test run: {initial_failures} failures
- Fix attempts: {fix_attempts_made}
- Final result: All tests passing ✅

📈 Quality Gates:
✅ Code compiles
✅ All tests passing (100%)
✅ Line coverage ({coverage}% ≥ 80%)
✅ Branch coverage ({branch}% ≥ 75%)
{performance_status} Test execution time ({time}s)

🔄 State Transition:
From: IN_PROGRESS
To: IN_REVIEW
Reason: All quality gates passed

📋 Next Steps:
- Human review of implementation
- Merge to main branch if approved
- Deploy to staging environment
```

#### Blocked Report (Tests Still Failing)

```
❌ Task Work Blocked - TASK-XXX

🔍 Stack: {detected_stack}
🤖 Agents Used: {list_of_agents}
⏱️  Duration: {total_duration}

📊 Final Test Results:
- Compilation: {compilation_status}
- Total Tests: {total_tests}
- Passed: {passed_tests}
- Failed: {failed_tests} ❌
- Skipped: {skipped_tests}
- Coverage: {coverage_percentage}%

🔧 Fix Loop Summary:
- Initial failures: {initial_failures}
- Fix attempts made: 3/3 (max reached)
- Remaining issues: {remaining_issues}

❌ Remaining Compilation Errors ({count}):
{list_of_compilation_errors}

❌ Remaining Test Failures ({count}):
{list_of_test_failures}

📈 Quality Gates:
{compile_status} Code compiles
❌ Tests passing ({failed} failures)
{coverage_status} Coverage thresholds

🔄 State Transition:
From: IN_PROGRESS
To: BLOCKED
Reason: Unable to achieve passing tests after 3 fix attempts

📋 Required Actions:
1. Review compilation errors (if any) and fix manually
2. Review test failure details and diagnose root cause
3. Check for missing dependencies or configuration issues
4. Verify test specifications are correct
5. Consider if architectural changes are needed
6. Re-run /task-work once issues are manually resolved

💡 Recommendations:
{specific_recommendations_based_on_error_patterns}
```

### Step 8: Commit State Files to Git (REQUIRED for Conductor Support)

**CRITICAL**: After completing all phases and generating the report, commit all state files to git. This ensures that state is preserved across git worktrees (used by Conductor.build for parallel development).

**EXECUTE** the following Python code:

```python
from installer.global.commands.lib.git_state_helper import commit_state_files

# Commit all state files for this task
# This includes:
# - docs/state/{task_id}/implementation_plan.md
# - docs/state/{task_id}/audit_report.json (if Phase 5.5 executed)
# - Any other state files created during workflow

try:
    commit_state_files(
        task_id="{task_id}",
        message=f"Save implementation state for {task_id} (workflow complete)"
    )
    print("✅ State files committed to git")
except Exception as e:
    # Don't fail workflow if git commit fails
    # (may not be in a git repo, or git may not be available)
    print(f"⚠️  Warning: Could not commit state files: {e}")
    print("   (This is non-critical - workflow can continue)")
```

**Why this is needed:**

- **Conductor.build** uses git worktrees for parallel development
- Each worktree has its own working directory but shares the same git repository
- State files in `docs/state/` MUST be committed to be visible across all worktrees
- Without this step, state loss occurs when switching between worktrees

**When to skip:**

- Only skip if not in a git repository (e.g., running in a sandboxed environment)
- Error handling ensures workflow continues even if git commit fails

**What gets committed:**

- All files in `docs/state/{task_id}/` directory
- Commit message includes task ID for traceability
- Does NOT push to remote (that's a separate operation)

---

## 📚 ADDITIONAL CONTEXT (Reference Only - Execute Above First)

### Development Modes

The command supports multiple development modes via `--mode` flag:

#### Standard Mode (Default)
```bash
/task-work TASK-XXX
```
- Implementation and tests together
- Fastest approach for straightforward features
- All 5 phases execute in sequence

#### TDD Mode
```bash
/task-work TASK-XXX --mode=tdd
```
- RED: Testing agent generates failing tests first
- GREEN: Implementation agent writes minimal code to pass
- REFACTOR: Implementation agent improves code quality
- Best for complex business logic

#### BDD Mode
```bash
/task-work TASK-XXX --mode=bdd
```
- Starts from Gherkin scenarios
- BDD generator creates step definitions
- Implementation agent satisfies scenarios
- Best for user-facing features

### Stack-Specific Agent Details

#### MAUI Stack Agents
- **maui-usecase-specialist**: UseCase pattern with Either monad
- **maui-viewmodel-specialist**: MVVM with RelayCommand
- **dotnet-testing-specialist**: xUnit with FluentAssertions

#### React Stack Agents
- **react-state-specialist**: Hooks, context, state management
- **react-testing-specialist**: React Testing Library, Vitest

#### Python Stack Agents
- **python-api-specialist**: FastAPI, Pydantic, async patterns
- **python-testing-specialist**: pytest, pytest-asyncio, fixtures

#### Python MCP Stack Agents
- **python-mcp-specialist**: MCP server architecture, tool/resource registration, LangGraph integration
- **python-testing-specialist**: pytest, pytest-asyncio, MCP client testing

#### TypeScript API Stack Agents
- **nestjs-api-specialist**: NestJS, dependency injection, decorators
- **typescript-domain-specialist**: Domain modeling, Result patterns
- **nodejs-testing-specialist**: Jest, Supertest, integration tests

#### .NET Microservice Stack Agents
- **dotnet-api-specialist**: FastEndpoints, REPR pattern, middleware
- **dotnet-domain-specialist**: DDD, Either monad, domain events
- **dotnet-testing-specialist**: xUnit, WebApplicationFactory, Testcontainers

### Usage Examples

#### Basic Usage
```bash
# Automatic stack detection and full workflow
/task-work TASK-042
```

#### With Options
```bash
# TDD mode with higher coverage threshold
/task-work TASK-042 --mode=tdd --coverage-threshold=90

# Fix only mode (for blocked tasks)
/task-work TASK-042 --fix-only

# With progress sync to epic/feature
/task-work TASK-042 --sync-progress

# Include full epic/feature context
/task-work TASK-042 --with-context
```

### Technology Detection Priority

1. **Primary**: Read `project.template` from `.claude/settings.json`
2. **Fallback**: Auto-detect from project files:
   - `*.csproj` with `Microsoft.Maui` → maui
   - `*.csproj` with `FastEndpoints` → dotnet-microservice
   - `package.json` with `react` → react
   - `package.json` with `@nestjs` → typescript-api
   - `requirements.txt` or `pyproject.toml` with `mcp` dependency → python-mcp
   - `requirements.txt` or `pyproject.toml` → python
3. **Default**: Use generic agents (software-architect, task-manager, test-verifier)

### Quality Gate Details

#### Tests Passing (Required)
- All test cases must pass
- No skipped tests allowed
- No test errors or warnings

#### Line Coverage (Required ≥ 80%)
- Percentage of code lines executed during tests
- Excludes generated code, interfaces
- Calculated by stack-specific coverage tool

#### Branch Coverage (Required ≥ 75%)
- Percentage of conditional branches tested
- Both true and false paths must be covered
- Critical for logic-heavy code

#### Performance (Warning if > 30s)
- Total test suite execution time
- Warning only, doesn't block
- Suggests optimization if exceeded

### Error Handling

#### Scenario: BDD Mode Without require-kit
```
❌ BDD mode requires require-kit

You requested: /task-work TASK-042 --mode=bdd
Available modes: standard, tdd

Current installation:
- taskwright: ✅ installed
- require-kit: ❌ not installed

Options:
1. Install require-kit for BDD support:
   cd require-kit && ./installer/scripts/install.sh

2. Use alternative mode:
   /task-work TASK-042 --mode=tdd

3. Use standard mode:
   /task-work TASK-042 --mode=standard
```

#### Scenario: Task References Unavailable Features
```
⚠️  Task TASK-042 references features that cannot be loaded

Referenced in task metadata:
- Epic: EPIC-001
- Requirements: [REQ-005, REQ-006]
- BDD Scenarios: FEAT-001

These require require-kit to be installed.

Current installation:
- taskwright: ✅ installed
- require-kit: ❌ not installed

To enable full context loading:
  cd require-kit
  ./installer/scripts/install.sh

Continue with task description only? [Y/n]
```

#### Scenario: Task Not Found
```
❌ Error: Task TASK-XXX not found
Location checked: tasks/in_progress/TASK-XXX.md
Action: Verify task ID or check task state (backlog/blocked/completed)
```

#### Scenario: Tests Failing
```
❌ Task TASK-XXX - Tests Failed

Failed Tests:
1. test_feature_validation (line 45)
   Expected: ValidationError
   Actual: None

Action: Review implementation and run:
/task-work TASK-XXX --fix-only
```

#### Scenario: Low Coverage
```
⚠️  Task TASK-XXX - Coverage Below Threshold

Current: 72%
Required: 80%

Uncovered:
- feature_service.py lines 45-52 (error handling)
- feature_service.py lines 78-85 (edge case)

Action: Testing agent will generate additional tests automatically
```

### Advanced Options

```bash
# Dry run (show plan without executing)
/task-work TASK-XXX --dry-run

# Watch mode (continuous testing)
/task-work TASK-XXX --watch

# Parallel test execution
/task-work TASK-XXX --parallel

# Skip specific phase
/task-work TASK-XXX --skip-review

# Force specific agent
/task-work TASK-XXX --implementation-agent=custom-specialist
```

### Integration with External Tools

When task metadata includes external tool references:

```yaml
# In task frontmatter
external_tools:
  jira: PROJ-123
  linear: PROJECT-456
  github: #789
```

After successful completion, automatically sync:
- Update Jira sub-task status to "In Review"
- Update Linear issue progress to 100%
- Update GitHub issue with test results

### File Locations

```
tasks/
├── backlog/         # New tasks (BACKLOG state)
├── in_progress/     # Active work (IN_PROGRESS state)
├── in_review/       # Passed quality gates (IN_REVIEW state)
├── blocked/         # Failed quality gates (BLOCKED state)
└── completed/       # Finished tasks (COMPLETED state)
```

### Success Metrics

After running `/task-work`:
- ✅ All agents invoked automatically
- ✅ No manual intervention required
- ✅ Quality gates enforced consistently
- ✅ State transitions handled automatically
- ✅ Comprehensive report generated

### Troubleshooting

**Problem**: Agents not invoked
- **Cause**: Command reading stopped before execution protocol
- **Fix**: Ensure execution protocol is first content Claude sees

**Problem**: Wrong agents selected
- **Cause**: Stack detection failed or incorrect settings
- **Fix**: Verify `.claude/settings.json` has correct `project.template`

**Problem**: Task tool not found
- **Cause**: Claude Code version doesn't support Task tool
- **Fix**: Update Claude Code to latest version

**Problem**: Agent not found
- **Cause**: Stack-specific agent doesn't exist
- **Fix**: System falls back to default agents automatically

### Best Practices

1. **Always start with `/task-work`** - Don't manually implement
2. **Trust the agents** - They're specialized for their domains
3. **Review quality gate failures** - They indicate real issues
4. **Use appropriate mode** - TDD for logic, BDD for features
5. **Keep tasks focused** - One feature per task works best

### Migration from Previous System

If you previously used separate commands:
- ❌ `/task-implement` → Use `/task-work`
- ❌ `/task-test` → Use `/task-work`
- ❌ Manual quality checks → Automatic in `/task-work`

### Command Philosophy

**"Implementation and testing are inseparable"**

This command embodies quality-first development by:
- Combining implementation with test creation
- Automatically running tests after implementation
- Enforcing quality gates before state transitions
- Supporting multiple development methodologies

Part of the streamlined 3-command workflow:
1. `/task-create` - Define the work
2. `/task-work` - Build and verify (THIS COMMAND)
3. `/task-complete` - Ship it

---

## ⚠️ CRITICAL REMINDER

**DO NOT ATTEMPT TO IMPLEMENT THE TASK YOURSELF**

This command requires **Task tool invocations for each phase**. Your role is to:
1. ✅ Detect the stack
2. ✅ Select the correct agents
3. ✅ Invoke Task tool for each phase
4. ✅ Aggregate results and generate report

**DO NOT**:
- ❌ Write implementation code directly
- ❌ Write test code directly
- ❌ Skip agent invocations
- ❌ Attempt to do all phases yourself

The agents are specialized and will produce better results than doing it yourself.
