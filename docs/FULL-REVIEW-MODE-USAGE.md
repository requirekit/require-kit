# Full Review Mode - Usage Guide

## Overview

Full Review Mode provides comprehensive architectural review checkpoints for complex tasks (complexity score 7-10) or escalated tasks from quick review. This guide explains how to use the full review system effectively.

## When Full Review Activates

Full Review Mode is triggered when:

1. **High Complexity Score**: Task complexity score >= 7/10
2. **Force-Review Triggers**: Security keywords, breaking changes, schema changes, hotfix flag
3. **User Escalation**: User pressed ENTER during quick review (score 4-6)
4. **Explicit Request**: `--review` flag passed to task-work command

## Display Sections

### 1. Header Section
```
Task: TASK-003B-2 - Full Review Mode - Display & Basic Actions
Complexity: 🔴 8/10
⬆️ Escalated from quick review (if applicable)
Estimated Time: ~2-3 hours
```

**What to Look For**:
- Red indicator (🔴) = high complexity (7-10)
- Yellow indicator (🟡) = moderate complexity (4-6)
- Green indicator (🟢) = low complexity (1-3)
- Escalation note if you pressed ENTER from quick review

### 2. Complexity Breakdown
```
📊 COMPLEXITY BREAKDOWN:

  🟡 File Complexity: 2.0/3.0 points
     → 6 files to create/modify (moderate scope)

  🟡 Pattern Familiarity: 1.0/2.0 points
     → Uses Strategy pattern (familiar)

  🔴 Risk Level: 3.0/3.0 points
     → High risk: Authentication changes, Database schema modification

  ⚡ FORCE-REVIEW TRIGGERS:
     - Security Keywords
```

**What to Look For**:
- Red factors (🔴) = high risk/complexity - pay close attention
- Yellow factors (🟡) = moderate concern - review carefully
- Green factors (🟢) = low concern - quick review
- Force-review triggers = mandatory review reasons

### 3. Changes Summary
```
📁 CHANGES SUMMARY:

  Files to Create/Modify: 5
    - installer/global/commands/lib/review_modes.py
    - installer/global/commands/lib/user_interaction.py
    - (etc.)

  External Dependencies: 1
    - pyyaml

  Test Strategy:
    Unit tests for display methods, approval/cancel handlers
```

**What to Look For**:
- File count - more files = higher coordination complexity
- External dependencies - new dependencies require security review
- Test strategy - comprehensive testing planned?

### 4. Risk Assessment
```
⚠️ RISK ASSESSMENT:

  🔴 HIGH: File operation atomicity during task cancellation
     Mitigation: Use atomic write pattern with temp file + os.replace()

  🟡 MEDIUM: YAML frontmatter parsing errors
     Mitigation: Graceful fallback to original content if parsing fails
```

**What to Look For**:
- High risks (🔴) = potential system-breaking issues
- Medium risks (🟡) = potential bugs or degraded functionality
- Low risks (🟢) = minor issues
- Mitigation strategy - is it adequate?

### 5. Implementation Order
```
📋 IMPLEMENTATION ORDER:

  1. Phase 1: Extend ImplementationPlan model (~15 min)
  2. Phase 2: Implement FileOperations utility (~20 min)
  3. Phase 3: Implement FullReviewDisplay (~45 min)
  (etc.)

  Estimated Lines of Code: ~500
```

**What to Look For**:
- Logical ordering - dependencies satisfied?
- Time estimates - realistic for complexity?
- Clear phases - easy to track progress?

### 6. Decision Prompt
```
DECISION OPTIONS:
  [A] Approve  - Proceed with this plan as-is
  [M] Modify   - Interactively edit the plan
  [V] View     - See full implementation plan
  [Q] Question - Ask about plan rationale
  [C] Cancel   - Return task to backlog
```

## Decision Actions

### [A] Approve - Proceed with Plan

**When to Use**:
- Plan looks solid and comprehensive
- Risks are acceptable with mitigations
- Implementation order makes sense
- You're confident in the approach

**What Happens**:
1. Displays: "✅ Plan approved! Proceeding to Phase 3 (Implementation)..."
2. Updates task metadata with approval details
3. Proceeds to Phase 3 (Implementation)
4. Tracks review duration and score

**Metadata Added**:
```yaml
implementation_plan:
  approved: true
  approved_by: user
  approved_at: "2025-10-09T10:30:00Z"
  review_mode: "full_required"  # or "escalated"
  review_duration_seconds: 120
  complexity_score: 8
```

### [C] Cancel - Return to Backlog

**When to Use**:
- Plan reveals task is too complex
- Requirements are unclear or incomplete
- Better approach needed
- Not the right time to implement

**What Happens**:
1. Prompts: "⚠️ Are you sure you want to cancel this task?"
2. Requires confirmation: [y/N]
3. If confirmed:
   - Displays: "❌ Task cancelled. Moving to backlog..."
   - Moves task file from `tasks/in_progress/` to `tasks/backlog/`
   - Updates metadata with cancellation details
   - Exits task-work command cleanly

**Metadata Added**:
```yaml
status: backlog
cancelled: true
cancelled_at: "2025-10-09T10:35:00Z"
cancellation_reason: "user_requested"
```

**Important**: All work completed so far is saved. You can resume later.

### [M] Modify - Edit Plan (Coming Soon)

**Status**: Stub implementation in TASK-003B-2, full implementation in TASK-003B-3

**When to Use**:
- Plan is mostly good but needs adjustments
- Want to add/remove files
- Adjust risk mitigations
- Refine implementation phases

**What Happens** (Current):
- Displays: "⚠️ Modify mode coming soon (TASK-003B-3)"
- Re-prompts for another choice

**What Will Happen** (TASK-003B-3):
- Interactive plan editor
- Modify files, dependencies, phases
- Validate changes
- Save modified plan
- Re-calculate complexity if needed

### [V] View - See Full Plan (Coming Soon)

**Status**: Stub implementation in TASK-003B-2, full implementation in TASK-003B-3

**When to Use**:
- Want to see complete untruncated plan
- Need to review specific details
- Want to copy plan text
- Prefer plain text view

**What Happens** (Current):
- Displays: "⚠️ View mode coming soon (TASK-003B-3)"
- Re-prompts for another choice

**What Will Happen** (TASK-003B-3):
- Display full plan text
- Pagination support for long plans
- Copy to clipboard option
- Return to checkpoint after viewing

### [Q] Question - Ask About Plan (Coming Soon)

**Status**: Stub implementation in TASK-003B-2, full implementation in TASK-003B-4

**When to Use**:
- Unclear about plan rationale
- Want clarification on approach
- Need more context on decisions
- Confused about implementation order

**What Happens** (Current):
- Displays: "⚠️ Q&A mode coming soon (TASK-003B-4)"
- Re-prompts for another choice

**What Will Happen** (TASK-003B-4):
- Interactive Q&A session
- AI-powered explanations
- Clarification of design decisions
- Return to checkpoint after Q&A

## Input Validation

### Valid Inputs
- `A` or `a` → Approve
- `C` or `c` → Cancel
- `M` or `m` → Modify (stub)
- `V` or `v` → View (stub)
- `Q` or `q` → Question (stub)

### Input Handling
- **Case-insensitive**: `A`, `a`, `approve` all work (uses first character)
- **Whitespace trimmed**: ` a ` → `a`
- **Multi-character**: `approve` → `a` (first character only)
- **Empty input**: Shows help and re-prompts
- **Invalid input**: Shows error and re-prompts

### Error Messages
```
❌ Invalid choice: 'x'
Please enter A (Approve), M (Modify), V (View), Q (Question), or C (Cancel)
```

After 3 invalid attempts:
```
⚠️ 3 invalid attempts. Please review options carefully.
```

### Special Keys
- **Ctrl+C**: Treated as cancellation request (same as [C])
- **Empty ENTER**: Shows help message and re-prompts

## Integration with Quick Review

When you press ENTER during quick review (complexity 4-6), you're escalated to full review:

**Escalation Indicator**:
```
⬆️ Escalated from quick review
```

**Preserved Context**:
- Complexity score from Phase 2.7 evaluation
- Implementation plan reference
- Original review mode (quick_optional)

**Metadata Tracking**:
```yaml
escalation:
  from_mode: "quick_optional"
  escalated_at: "2025-10-09T10:15:00Z"
  reason: "user_requested"
```

## Best Practices

### 1. Review All Red Indicators
- Red complexity factors (🔴) need extra attention
- High risks (🔴) must have adequate mitigations
- Red force-review triggers are non-negotiable

### 2. Validate Mitigations
- Check each risk has a concrete mitigation
- Verify mitigations are realistic and sufficient
- Consider if additional mitigations are needed

### 3. Check Implementation Order
- Verify dependencies are satisfied in order
- Confirm time estimates are reasonable
- Look for potential blockers or missing steps

### 4. Consider Alternatives
- Could a simpler approach work?
- Are we over-engineering?
- Is this the right time for this complexity?

### 5. When to Cancel
- Requirements are ambiguous
- Better approach emerges
- Task scope is too large
- Dependencies are missing

### 6. When to Approve
- Plan is comprehensive and clear
- Risks are identified and mitigated
- Implementation order is logical
- You're confident in the approach

## Troubleshooting

### Display Issues

**Terminal Too Narrow**:
- Display adapts to 70-120 columns
- Falls back to 80 if detection fails
- Consider widening terminal for better view

**Missing Data**:
- Display handles missing fields gracefully
- Shows "Not estimated" if duration missing
- Shows generic messages if phases missing

### File Operation Issues

**Task File Not Found**:
- Verify task is in `tasks/in_progress/`
- Check task ID is correct
- Ensure file has proper YAML frontmatter

**Cancellation Fails**:
- Atomic write ensures no partial updates
- Check `tasks/backlog/` directory exists
- Verify write permissions

### Input Issues

**Input Not Recognized**:
- Use single letters: A, C, M, V, Q
- Check for typos
- System is case-insensitive

**Ctrl+C Not Working**:
- First Ctrl+C triggers cancellation prompt
- Confirms with [y/N]
- Second Ctrl+C forces emergency exit

## Examples

### Example 1: Approving a Well-Designed Plan

```
Your choice (A/M/V/Q/C): a

✅ Plan approved!
Proceeding to Phase 3 (Implementation)...
```

### Example 2: Cancelling an Overly Complex Task

```
Your choice (A/M/V/Q/C): c

⚠️ Are you sure you want to cancel this task?
All work completed so far will be saved.

Confirm cancellation? [y/N]: y

❌ Task cancelled. Moving to backlog...
```

### Example 3: Invalid Input with Retry

```
Your choice (A/M/V/Q/C): x

❌ Invalid choice: 'x'
Please enter A (Approve), M (Modify), V (View), Q (Question), or C (Cancel)

Your choice (A/M/V/Q/C): z

❌ Invalid choice: 'z'
Please enter A (Approve), M (Modify), V (View), Q (Question), or C (Cancel)

Your choice (A/M/V/Q/C): a

✅ Plan approved!
```

### Example 4: Stub Action (Modify)

```
Your choice (A/M/V/Q/C): m

⚠️ Modify mode coming soon (TASK-003B-3)
For now, please choose [A]pprove or [C]ancel.

Your choice (A/M/V/Q/C): a

✅ Plan approved!
```

## Future Enhancements (TASK-003B-3, TASK-003B-4)

1. **Plan Modification** (TASK-003B-3)
   - Interactive editing of files, dependencies, phases
   - Validation of modified plan
   - Re-calculation of complexity score

2. **Plan Viewing** (TASK-003B-3)
   - Full untruncated plan display
   - Pagination for long plans
   - Copy to clipboard

3. **Q&A Mode** (TASK-003B-4)
   - AI-powered plan explanations
   - Clarification of design decisions
   - Interactive question-answer session

## Related Documentation

- `TASK-003B-2-IMPLEMENTATION-SUMMARY.md` - Implementation details
- `installer/global/commands/lib/review_modes.py` - Source code
- `tests/integration/test_full_review_demo.py` - Usage examples

---

**Last Updated**: 2025-10-09
**Version**: 1.0 (TASK-003B-2)
