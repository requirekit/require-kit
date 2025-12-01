---
id: TASK-REV-5E0E
title: Review require-kit symlink architecture vs taskwright issues
status: completed
created: 2025-12-01T00:00:00Z
updated: 2025-12-01T07:50:00Z
completed: 2025-12-01T07:50:00Z
priority: high
tags: [review, architecture-review, symlink, installation, cross-environment]
complexity: 5
task_type: review
decision_required: true
review_results:
  mode: architectural
  depth: standard
  completed_at: 2025-12-01T07:45:00Z
  findings_count: 3
  recommendations_count: 3
  decision: accepted
  decision_rationale: "No critical issues found. Copy-first pattern is fundamentally sound and portable."
  technical_debt_score: 1.5
  priority_1_effort_hours: 0
  priority_2_effort_hours: 0
  priority_3_effort_hours: 4
  total_effort_hours: 4
  report_path: .claude/reviews/TASK-REV-5E0E-architectural-review.md
  user_decision: accept
  user_decision_timestamp: 2025-12-01T07:50:00Z
related_tasks:
  - taskwright:TASK-BUG-D8F3 (symlink regression diagnosis)
  - taskwright:TASK-BUG-D8F3-technical-debt-report (architectural issues)
---

# Task: Review require-kit symlink architecture vs taskwright issues

## Description

Taskwright discovered critical architectural issues with their `/template-create` command that uses symlinks to Python orchestrator scripts. The symlinks encode hard-coded repository paths, causing complete command failure when:
- Repository is in different location (VM, different user, Conductor worktrees)
- Installation performed from different machine
- Repository moved after installation

**This review task will analyze whether require-kit has similar architectural vulnerabilities.**

## Background: Taskwright Issues Identified

### Primary Issue: Hard-coded Repository Paths in Symlinks

**Taskwright's broken pattern:**
```bash
~/.agentecflow/bin/template-create-orchestrator
  → /Users/richardwoollcott/Projects/appmilla_github/taskwright/installer/global/commands/lib/template_create_orchestrator.py
```

**Problem:** Symlink encodes specific user and project location, breaking on VM or different environments.

### Secondary Issues Found

| Issue | Severity | Impact |
|-------|----------|--------|
| **Python 3.14 version mismatch** | LOW | Minor compatibility risk |
| **No symlink integrity validation** | MEDIUM | Silent failures |
| **Path resolution ambiguity** | HIGH | Blocks cross-environment usage |
| **Poor error messages** | LOW | UX degradation |

### Taskwright's Recommended Fix

**Option 1 (PREFERRED)**: Replace symlinks with script copies
- ✅ Works everywhere (no path dependencies)
- ✅ Consistent with existing command pattern
- ✅ Conductor-compatible
- ❌ Scripts not auto-updated (must re-run install.sh)

**Option 2**: Use environment variable `$TASKWRIGHT_HOME`
- ✅ Portable symlinks
- ❌ Requires shell configuration
- ❌ Fragile (variable must be set correctly)

## Investigation Scope

### 1. Analyze require-kit Installation Architecture

**Review Areas:**
- [ ] How does `installer/scripts/install.sh` handle Python library files?
- [ ] Are there any symlinks that encode absolute paths?
- [ ] How are command markdown files installed?
- [ ] How are agent markdown files installed?
- [ ] Are there any Python command orchestrators (like taskwright's template-create)?

**Initial Observations (to be verified):**

From preliminary analysis of [install.sh](../../../installer/scripts/install.sh):
1. **Library files**: Copied directly via `cp -r` (line 438), NOT symlinked ✅
2. **Command files**: Symlinks created but only for .md files (lines 388-398) ⚠️
3. **Agent files**: Symlinks created but only for .md files (lines 417-427) ⚠️
4. **No Python orchestrators**: No evidence of Python command scripts requiring symlinks ✅

### 2. Compare Installation Patterns

**Taskwright Pattern (BROKEN):**
```bash
# Creates symlinks to Python scripts in source repository
~/.agentecflow/bin/template-create-orchestrator
  → ~/Projects/appmilla_github/taskwright/installer/global/commands/lib/template_create_orchestrator.py
```

**require-kit Pattern (to be analyzed):**
```bash
# Appears to copy library files directly
~/.agentecflow/lib/feature_detection.py (COPIED from source)
~/.agentecflow/lib/utils/*.py (COPIED from source)

# Symlinks for markdown files only (verify if this is problematic)
~/.agentecflow/commands/gather-requirements.md
  → require-kit/gather-requirements.md
```

**Key Questions:**
1. Do markdown file symlinks have the same hard-coded path issue?
2. Are markdown files executed or just read by Claude Code?
3. If just read, is path resolution different from Python script execution?

### 3. Check for Symlink Validation

**Verification Tasks:**
- [ ] Does install.sh validate symlinks after creation?
- [ ] Does `require-kit doctor` (if exists) check symlink integrity?
- [ ] Are there any post-installation validation checks?
- [ ] What happens if symlink target is missing?

### 4. Test Cross-Environment Scenarios

**Test Matrix:**

| Environment | Scenario | Expected Result | Status |
|-------------|----------|-----------------|--------|
| **Dev machine** | Install.sh → commands work | ✅ Works | ⚠️ VERIFY |
| **Different location** | Clone to ~/require-kit → install | ✅ Works | ⚠️ TEST NEEDED |
| **Different user** | Install as different user | ✅ Works | ⚠️ TEST NEEDED |
| **Conductor worktree** | Use in Conductor worktree | ✅ Works | ⚠️ TEST NEEDED |
| **After repo move** | Move repo after installation | ✅ Works or clear error | ⚠️ TEST NEEDED |
| **VM environment** | Install on different machine | ✅ Works | ⚠️ TEST NEEDED |

### 5. Analyze Command Execution Pattern

**Critical Analysis:**
- [ ] How do require-kit commands get invoked in Claude Code?
- [ ] Are markdown files executed or parsed?
- [ ] If symlinks break, what error messages appear?
- [ ] Is there any Python script invocation via symlinks?

### 6. Review Python Version Handling

**Verification:**
- [ ] Does require-kit handle Python 3.14+ gracefully?
- [ ] Are version checks aligned with taskwright (3.10+)?
- [ ] Are pre-release Python versions detected and warned?

## Acceptance Criteria

### Must Complete
- [ ] Complete architectural analysis of all symlink usage
- [ ] Identify any hard-coded path dependencies
- [ ] Document current installation pattern vs taskwright pattern
- [ ] Test at least 3 cross-environment scenarios
- [ ] Determine if require-kit has same issues as taskwright

### Decision Points
- [ ] Does require-kit need the same fix as taskwright?
- [ ] Are markdown file symlinks a problem?
- [ ] Should we switch to copy-based installation?
- [ ] Do we need symlink integrity validation?

### Deliverables
- [ ] Technical debt report (similar to taskwright's)
- [ ] Risk assessment (HIGH/MEDIUM/LOW for each finding)
- [ ] Recommended fixes with priority levels
- [ ] Test results from cross-environment validation
- [ ] Decision on whether to implement preventive fixes

## Expected Findings

### Hypothesis 1: No Critical Issues (LIKELY)

**Evidence so far:**
- Library files are copied, not symlinked
- No Python command orchestrators detected
- Only .md files use symlinks (different execution model)

**If confirmed:**
- Document why require-kit is NOT affected
- Add validation to prevent future issues
- Update documentation with architectural notes

### Hypothesis 2: Minor Issues with Markdown Symlinks (POSSIBLE)

**Potential problems:**
- Markdown symlinks still encode absolute paths
- Could break if repo moved after installation
- Error messages might be unclear

**If confirmed:**
- Assess severity (MEDIUM or LOW)
- Consider preventive fixes
- Add symlink validation to install.sh

### Hypothesis 3: Critical Issues Found (UNLIKELY)

**If discovered:**
- Prioritize as P1 (same as taskwright)
- Implement same fix pattern (copy vs symlink)
- Add validation and testing
- Update documentation

## Related Documentation

### Taskwright References
- [TASK-BUG-D8F3](file:///Users/richardwoollcott/Projects/appmilla_github/taskwright/tasks/completed/TASK-BUG-D8F3-diagnose-template-create-regression.md) - Original bug diagnosis
- [Technical Debt Report](file:///Users/richardwoollcott/Projects/appmilla_github/taskwright/.claude/reviews/TASK-BUG-D8F3-technical-debt-report.md) - Comprehensive analysis

### require-kit References
- [install.sh](../../../installer/scripts/install.sh) - Installation script
- [CLAUDE.md](../../../CLAUDE.md) - Project documentation
- [INTEGRATION-GUIDE.md](../../../docs/INTEGRATION-GUIDE.md) - Integration patterns

## Technical Debt Score (To Be Determined)

**Scoring Criteria (from taskwright pattern):**
- Hard-coded paths: 0-3 points
- Symlink validation: 0-2 points
- Error messages: 0-1 points
- Cross-environment testing: 0-2 points
- Python version handling: 0-2 points

**Total Debt Score**: TBD (0-10 scale)
- 0-2: Minimal debt (cosmetic improvements only)
- 3-5: Moderate debt (preventive fixes recommended)
- 6-8: Significant debt (fixes needed)
- 9-10: Critical debt (immediate fixes required)

## Review Workflow

1. **Use `/task-review TASK-REV-5E0E --mode=architectural`**
   - Systematic analysis of installation architecture
   - Comparison with taskwright patterns
   - Cross-environment testing

2. **Decision Checkpoint**
   - [A]ccept - No issues found, document and close
   - [I]mplement - Create implementation task for fixes
   - [R]evise - Need deeper analysis
   - [C]ancel - Not applicable

3. **If [I]mplement chosen:**
   - Create fix task with priority level
   - Align with taskwright fix pattern
   - Test across environments

## Success Metrics

### Primary Metrics
- **Completeness**: All investigation areas covered
- **Accuracy**: Findings verified with tests
- **Clarity**: Clear recommendations with priority levels
- **Actionability**: Concrete next steps identified

### Quality Gates
- ✅ All symlink usage documented
- ✅ Cross-environment scenarios tested
- ✅ Comparison with taskwright complete
- ✅ Risk assessment completed
- ✅ Recommendations prioritized

## Timeline Estimate

- **Investigation**: 2-3 hours
- **Testing**: 1-2 hours
- **Report writing**: 1 hour
- **Total**: 4-6 hours

## Next Steps

1. Execute review using `/task-review TASK-REV-5E0E --mode=architectural`
2. Document findings in technical debt report
3. Make decision at checkpoint
4. Create implementation task if needed (Priority TBD based on findings)
5. Update require-kit documentation with architectural notes

---

## Implementation Notes

This is a **review task** - no implementation should occur until analysis is complete and decision is made at checkpoint.

**CRITICAL**: Use `/task-review` command, NOT `/task-work`, to ensure proper review workflow and decision checkpoint.
