---
id: TASK-PD-RK04
title: Split requirements-analyst.md into core + extended
status: completed
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T21:12:12Z
completed: 2025-12-09T21:12:12Z
completed_location: tasks/completed/2025-12/TASK-PD-RK04/
priority: high
tags: [progressive-disclosure, agent-split, wave-2]
task_type: implementation
complexity: 4
execution_mode: task-work
wave: 2
conductor_workspace: progressive-disclosure-analyst
parallel: true
blocking: false
parent_review: TASK-REV-PD01
depends_on: [TASK-PD-RK01, TASK-PD-RK02]
organized_files:
  - TASK-PD-RK04.md
  - completion-report.md
---

# Task: Split requirements-analyst.md into core + extended

## Description

Split the `requirements-analyst.md` agent file (388 lines, 12KB) into core and extended files following GuardKit's progressive disclosure pattern.

## Execution Mode

**`/task-work TASK-PD-RK04`** - Complex task requiring quality gates and pattern compliance.

## Conductor Parallel Execution

```bash
conductor create progressive-disclosure-analyst
# In workspace:
/task-work TASK-PD-RK04
```

Can be executed in parallel with TASK-PD-RK03.

## Current File Analysis

**File**: `installer/global/agents/requirements-analyst.md`
**Size**: 12,301 bytes (388 lines)
**Token Estimate**: ~3,100 tokens

### Content Breakdown

| Section | Lines | Category |
|---------|-------|----------|
| Frontmatter | 1-24 | CORE |
| Title + Quick Start | 25-41 | CORE |
| Boundaries | 42-69 | CORE |
| Documentation Level Awareness | 70-208 | CORE |
| Primary Responsibilities | 209-217 | CORE |
| EARS Patterns You Apply | 218-240 | CORE |
| Requirements Gathering Process | 241-263 | EXTENDED |
| Question Templates | 264-284 | EXTENDED |
| Quality Criteria | 285-295 | CORE |
| Output Format | 296-328 | CORE (condensed) |
| Common Patterns by Domain | 329-358 | EXTENDED |
| Collaboration Approach | 359-366 | CORE |
| Red Flags to Watch For | 367-377 | CORE |
| Your Interaction Style | 378-389 | CORE |

## Target Output

### Core File: `requirements-analyst.md` (~5KB, ~1,250 tokens)

**Sections to include**:
1. Frontmatter (complete)
2. Title + Quick Start (2-3 examples only)
3. Boundaries (ALWAYS/NEVER/ASK)
4. Documentation Level Awareness
5. Primary Responsibilities
6. EARS Patterns You Apply (all 5 patterns - essential)
7. Quality Criteria
8. Output Format (condensed template only)
9. Collaboration Approach
10. Red Flags to Watch For
11. Your Interaction Style
12. Loading Instruction (link to extended file)

### Extended File: `requirements-analyst-ext.md` (~7KB, ~1,750 tokens)

**Sections to include**:
1. Header with link back to core
2. Requirements Gathering Process (detailed phases)
3. Question Templates (by requirement type)
4. Common Patterns by Domain (Auth, Data, Integration, UI)
5. Output Format Full Examples
6. Footer

## Acceptance Criteria

- [ ] Core file is ≤5KB and contains all decision-making content
- [ ] Extended file contains detailed processes and domain patterns
- [ ] All 5 EARS patterns remain in core file (essential for formalization)
- [ ] Core file includes loading instruction section
- [ ] Extended file links back to core file
- [ ] Frontmatter preserved in core file
- [ ] YAML metadata unchanged (discovery still works)
- [ ] Boundaries section (ALWAYS/NEVER/ASK) in core file
- [ ] No content lost during split

## Implementation Steps

1. **Read current file** and identify section boundaries
2. **Extract core sections** (lines 1-240, 285-295, 359-389)
3. **Create condensed versions** where needed
4. **Keep all 5 EARS patterns in core** (they are essential)
5. **Build core file** with loading instruction at end
6. **Build extended file** with header and remaining sections
7. **Validate** both files are well-formed markdown
8. **Test** that `/formalize-ears` command works correctly

## Files to Create

- `installer/global/agents/requirements-analyst.md` (overwrite with core content)
- `installer/global/agents/requirements-analyst-ext.md` (new extended file)

## Dependencies

- TASK-PD-RK01 (Consolidate duplicate files)
- TASK-PD-RK02 (Copy GuardKit scripts)

## Estimated Effort

45 minutes

## Notes

The EARS patterns (Ubiquitous, Event-Driven, State-Driven, Unwanted Behavior, Optional Feature) are the core methodology and must remain in the core file. The detailed gathering process and domain-specific patterns can move to extended.
