# Debug - Systematic Bug Investigation and Root Cause Analysis

## Command
```bash
/debug [TASK-XXX] [--issue "description"] [--logs path/to/logs]
```

## Purpose
Systematically investigate and resolve bugs using evidence-based root cause analysis. Invokes the debugging-specialist agent to apply a methodical debugging approach.

## When to Use

Use `/debug` when:
- Tests are failing and root cause is unclear
- Bug reports indicate unexpected behavior
- Intermittent issues that are hard to reproduce
- Performance degradation or resource leaks
- After deployment issues in production

## Arguments

- `TASK-XXX` (optional): Task ID associated with the bug
- `--issue` (optional): Brief description of the problem
- `--logs` (optional): Path to log files or error output

## Examples

### Debug a Failing Task
```bash
/debug TASK-034 --issue "UI not updating after navigation"
```

### Debug with Log Files
```bash
/debug TASK-042 --logs output/debug.log --issue "Crash on barcode scan"
```

### Debug a General Issue (No Task)
```bash
/debug --issue "Memory leak in product list view"
```

### Debug from Error Output
```bash
/debug TASK-015 --issue "ObjectDisposedException in ScanningEngine"
```

## Execution Flow

When you run `/debug`, Claude Code will:

### 1. Gather Initial Context (30 seconds)

**If TASK-XXX provided:**
- Read task file from `tasks/in_progress/TASK-XXX.md`
- Extract requirements and acceptance criteria
- Identify recent code changes related to task

**If --logs provided:**
- Read log files
- Extract error messages and stack traces
- Identify timestamps and patterns

**If --issue provided:**
- Parse issue description
- Identify affected components
- Formulate initial hypotheses

### 2. Invoke Debugging Specialist

Claude Code will use the Task tool to invoke the debugging-specialist agent:

```
subagent_type: "debugging-specialist"
description: "Debug issue: {issue description}"
prompt: "Systematically debug the following issue: {issue description}

Context:
- Task: {TASK-XXX if provided}
- Error logs: {log content if provided}
- Recent changes: {git log output}

Follow the systematic debugging methodology:
1. Evidence Gathering - Collect error context, stack traces, reproduction steps
2. Hypothesis Formation - Analyze errors and form testable hypotheses
3. Targeted Investigation - Add strategic logging, inspect state
4. Root Cause Identification - Trace data flow, document evidence
5. Implement Minimal Fix - Fix root cause, not symptoms
6. Verify Fix - Create regression tests, run test suite

Output:
- Root cause analysis document
- Proposed fix with explanation
- Regression tests to prevent recurrence
- Updated task documentation"
```

### 3. Review Debugging Results

The debugging-specialist agent will provide:

```markdown
# Root Cause Analysis

## Summary
{One-sentence root cause}

## Evidence
- {Error messages, stack traces, logs}
- {Investigation findings}
- {Hypothesis testing results}

## Root Cause
{Detailed explanation with data flow analysis}

## Proposed Fix
{Code changes with rationale}

## Verification Plan
- {Regression tests}
- {Manual testing steps}
- {Prevention recommendations}
```

### 4. Apply Fix (Interactive)

Claude Code will present the proposed fix and ask:

```
═══════════════════════════════════════════════════════
🔍 ROOT CAUSE IDENTIFIED
═══════════════════════════════════════════════════════

ISSUE: {issue description}
ROOT CAUSE: {summary}

PROPOSED FIX:
{File changes summary}

VERIFICATION:
- {Test plan}
- {Manual steps}

OPTIONS:
1. [A]pply Fix - Apply the proposed changes
2. [R]eview Details - View full root cause analysis
3. [M]odify - Discuss alternative approaches
4. [S]kip - Document findings without applying fix

Your choice (A/R/M/S):
═══════════════════════════════════════════════════════
```

**User choices:**
- **Apply**: Implement the fix, create regression tests, update task
- **Review**: Show full root cause analysis document
- **Modify**: Discuss alternative fixes or refinements
- **Skip**: Document findings for manual resolution later

### 5. Post-Fix Verification

**If fix is applied:**

1. **Run Tests**
   ```bash
   # Technology-specific test command
   dotnet test  # .NET
   pytest       # Python
   npm test     # TypeScript/React
   ```

2. **Verify Build**
   ```bash
   # Ensure code compiles without errors
   dotnet build    # .NET
   python -m py_compile src/**/*.py  # Python
   npm run build   # TypeScript/React
   ```

3. **Check Coverage**
   ```bash
   # Verify regression test added
   dotnet test --collect:"XPlat Code Coverage"
   pytest --cov
   npm test -- --coverage
   ```

4. **Update Documentation**
   - Add root cause analysis to `docs/debugging/TASK-XXX-root-cause.md`
   - Update task file with fix details
   - Document prevention recommendations

## Output

The `/debug` command produces:

### 1. Root Cause Analysis Document
```
docs/debugging/TASK-XXX-root-cause.md
```

Contains:
- Issue summary and reproduction steps
- Investigation timeline
- Evidence gathered
- Root cause explanation
- Fix description
- Verification results
- Prevention recommendations

### 2. Regression Tests
```
tests/regression/test_task_xxx_fix.py
```

Test that:
- Reproduces the bug (would fail before fix)
- Passes after fix
- Prevents future regressions
- Documents expected behavior

### 3. Updated Task File
```
tasks/in_progress/TASK-XXX.md
```

Additions:
```markdown
## Debugging Session

**Issue**: {description}
**Root Cause**: {summary}
**Fix Applied**: {commit hash}
**Documentation**: [Root Cause Analysis](../../docs/debugging/TASK-XXX-root-cause.md)
**Regression Test**: tests/regression/test_task_xxx_fix.py
**Verified**: {date}
```

## Integration with task-work

The debugging-specialist is automatically invoked during `task-work` when:

**Phase 4.5: Test Enforcement** - If tests fail after fix attempts:

```yaml
Test Failure Handling:
  attempt_1: "Run tests"
  result_1: "FAIL"
  action_1: "Auto-fix compilation/import errors"

  attempt_2: "Run tests again"
  result_2: "FAIL"
  action_2: "Invoke debugging-specialist for root cause analysis"

  attempt_3: "Apply debugging-specialist fix and retest"
  result_3: "PASS or FAIL"

  if result_3 == "FAIL":
    action_final: "Mark task as BLOCKED, document investigation"
```

## Debugging Workflow Diagram

```
User runs /debug
       ↓
[1. Gather Context]
   - Read task file
   - Parse error logs
   - Review recent git changes
       ↓
[2. Invoke debugging-specialist]
   - Evidence gathering
   - Hypothesis formation
   - Targeted investigation
   - Root cause identification
   - Propose minimal fix
       ↓
[3. Present Findings]
   - Show root cause analysis
   - Display proposed fix
   - Request user approval
       ↓
[4. Apply Fix (if approved)]
   - Implement code changes
   - Create regression tests
   - Update documentation
       ↓
[5. Verify Fix]
   - Run test suite
   - Verify build succeeds
   - Check code coverage
   - Manual verification steps
       ↓
[6. Complete]
   - Update task status
   - Commit changes
   - Generate summary report
```

## Success Criteria

A debugging session is successful when:

```yaml
Evidence:
  - Root cause clearly identified with supporting evidence
  - Reproduction steps documented and verified
  - Fix addresses root cause, not symptoms

Fix Quality:
  - Minimal code changes (only what's necessary)
  - Follows architectural principles (SOLID, DRY)
  - No regressions introduced
  - All existing tests still pass

Testing:
  - Regression test added and passing
  - Test coverage maintained or improved
  - Manual verification completed

Documentation:
  - Root cause analysis document created
  - Task file updated with findings
  - Prevention recommendations documented
  - Team knowledge base updated
```

## Best Practices

### 1. Always Reproduce First
```bash
# Don't attempt a fix until you can reliably reproduce the bug
/debug TASK-042 --issue "Intermittent crash" --logs debug.log

# The debugging-specialist will focus on reproduction before fixing
```

### 2. Provide Maximum Context
```bash
# Good - Includes task, specific error, and logs
/debug TASK-034 --issue "ObjectDisposedException in ProcessScanAsync after navigation" --logs android-debug.log

# Less helpful - Vague description, no context
/debug --issue "Something's broken"
```

### 3. Review Before Applying
```bash
# Always review the root cause analysis before applying fixes
# Use [R]eview option to understand the investigation
# Ensures you learn from the debugging process
```

### 4. Verify Thoroughly
```bash
# After fix is applied, manually verify:
1. Build succeeds
2. All tests pass (including new regression test)
3. Original reproduction steps no longer trigger bug
4. No new issues introduced
```

### 5. Document for Team
```bash
# Share findings with team
- Add to team knowledge base
- Update common issues documentation
- Discuss in code review
- Consider architectural improvements
```

## Technology-Specific Debugging

The debugging-specialist adapts to your technology stack:

### .NET MAUI
```bash
/debug TASK-034 --issue "RX stream not firing after navigation"

# Specialist will investigate:
- Observable subscription lifecycle
- ViewModel disposal patterns
- RefCount() behavior
- MVVM binding issues
- Platform-specific lifecycle events
```

### Python
```bash
/debug TASK-015 --issue "Async function blocking event loop"

# Specialist will investigate:
- Event loop conflicts
- Blocking calls in async functions
- Task cancellation handling
- Import and dependency issues
```

### TypeScript/React
```bash
/debug TASK-022 --issue "Infinite re-render loop in component"

# Specialist will investigate:
- useEffect dependencies
- State update patterns
- Stale closures
- Memory leaks from listeners
```

## Common Use Cases

### 1. Test Failures After Implementation
```bash
# Scenario: Implemented feature but tests failing
/debug TASK-018 --issue "Integration tests failing after user service refactor"

# Result: Identifies dependency injection configuration error
```

### 2. Production Bug Report
```bash
# Scenario: User reports issue in production
/debug --issue "Crash when scanning barcode with special characters" --logs prod-error.log

# Result: Identifies input validation gap, proposes fix with regex pattern
```

### 3. Performance Degradation
```bash
# Scenario: App became slow after recent changes
/debug TASK-025 --issue "Product list loading takes 30+ seconds"

# Result: Identifies N+1 query problem, proposes eager loading solution
```

### 4. Intermittent Failures
```bash
# Scenario: Test fails randomly in CI/CD
/debug TASK-031 --issue "Random test failures in LoginViewModelTests"

# Result: Identifies race condition in async test, proposes deterministic timing
```

### 5. Memory Leaks
```bash
# Scenario: App memory usage grows over time
/debug --issue "Memory leak when navigating between product list and details"

# Result: Identifies undisposed RX subscriptions, proposes proper cleanup
```

## Troubleshooting

### "Cannot reproduce the bug"
```
If debugging-specialist cannot reproduce:
1. Provide more detailed steps
2. Include environment details (device, OS version, etc.)
3. Add logs from when bug occurred
4. Try to identify what conditions are required
5. Consider if bug is truly intermittent (timing-dependent)
```

### "Fix didn't resolve the issue"
```
If proposed fix doesn't work:
1. Verify fix was applied correctly
2. Check if there are multiple root causes
3. Review if symptoms vs root cause were confused
4. Gather additional evidence with fix in place
5. Re-invoke /debug with updated information
```

### "Tests still failing after fix"
```
If tests fail after applying fix:
1. Check if fix introduced regressions
2. Verify all dependencies are correct
3. Review test expectations (may need updating)
4. Check if multiple issues exist
5. Re-run debugging session focusing on test failures
```

## Tips for Effective Debugging

1. **Start with evidence, not assumptions**
   - Gather logs, stack traces, reproduction steps
   - Let data guide hypothesis formation

2. **Form testable hypotheses**
   - Predict what evidence would confirm/refute
   - Test one hypothesis at a time

3. **Fix root cause, not symptoms**
   - Understand WHY the bug happens
   - Address fundamental issue

4. **Always add regression tests**
   - Prevent bug from returning
   - Document expected behavior

5. **Learn from debugging sessions**
   - Build mental library of common patterns
   - Share knowledge with team
   - Improve architecture to prevent similar bugs

## Related Commands

- `/task-work` - Main implementation command (includes automatic debugging on test failure)
- `/task-status` - Check if task is BLOCKED due to debugging issues
- `/task-complete` - Complete task after successful debugging and fix verification

## Notes

- The debugging-specialist uses a systematic, evidence-based approach
- Fixes are minimal and focused on root causes
- All fixes include regression tests
- Documentation is automatically generated
- Integration with existing task workflow is seamless

**Remember**: Good debugging is about systematic investigation, not random changes. Trust the process, gather evidence, and fix root causes.
