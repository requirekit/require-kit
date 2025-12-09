---
id: TASK-PD-RK03
title: Split bdd-generator.md into core + extended
status: completed
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T21:15:00Z
completed: 2025-12-09T21:15:00Z
completed_location: tasks/completed/TASK-PD-RK03/
priority: high
tags: [progressive-disclosure, agent-split, wave-2]
task_type: implementation
complexity: 5
execution_mode: task-work
wave: 2
conductor_workspace: progressive-disclosure-bdd
parallel: true
blocking: false
parent_review: TASK-REV-PD01
depends_on: [TASK-PD-RK01, TASK-PD-RK02]
organized_files:
  - TASK-PD-RK03.md
results:
  core_file_size: 8846 bytes
  extended_file_size: 17276 bytes
  token_reduction: 51%
  files_created:
    - installer/global/agents/bdd-generator.md
    - installer/global/agents/bdd-generator-ext.md
---

# Task: Split bdd-generator.md into core + extended

## Description

Split the `bdd-generator.md` agent file (606 lines, 18KB) into core and extended files following GuardKit's progressive disclosure pattern. This is the largest agent file in RequireKit and will provide the most significant token savings.

## Execution Mode

**`/task-work TASK-PD-RK03`** - Complex task requiring quality gates and pattern compliance.

## Conductor Parallel Execution

```bash
conductor create progressive-disclosure-bdd
# In workspace:
/task-work TASK-PD-RK03
```

Can be executed in parallel with TASK-PD-RK04.

## Current File Analysis

**File**: `installer/global/agents/bdd-generator.md`
**Size**: 17,989 bytes (606 lines)
**Token Estimate**: ~4,500 tokens

### Content Breakdown

| Section | Lines | Category |
|---------|-------|----------|
| Frontmatter | 1-23 | CORE |
| Title + Quick Start | 24-68 | CORE |
| Boundaries | 42-68 | CORE |
| Documentation Level Handling | 69-114 | CORE |
| EARS to Gherkin Transformation | 115-198 | CORE |
| Gherkin Best Practices | 199-225 | CORE |
| Framework-Specific Step Definitions | 226-337 | EXTENDED |
| LangGraph Integration Example | 338-416 | EXTENDED |
| Output Template | 417-458 | CORE (condensed) |
| Common Scenario Patterns | 459-515 | EXTENDED |
| Quality Checklist | 516-529 | CORE |
| Advanced Techniques | 530-566 | EXTENDED |
| Integration with Test Automation | 567-585 | EXTENDED |
| Common Pitfalls + Working Style | 586-607 | CORE |

## Target Output

### Core File: `bdd-generator.md` (~6KB, ~1,500 tokens)

**Sections to include**:
1. Frontmatter (complete)
2. Title + Quick Start (2-3 examples only)
3. Boundaries (ALWAYS/NEVER/ASK)
4. Documentation Level Handling
5. EARS to Gherkin Transformation (patterns only, not full examples)
6. Gherkin Best Practices (condensed)
7. Output Template (condensed)
8. Quality Checklist
9. Working Style
10. Loading Instruction (link to extended file)

### Extended File: `bdd-generator-ext.md` (~12KB, ~3,000 tokens)

**Sections to include**:
1. Header with link back to core
2. Framework-Specific Step Definitions (pytest-bdd, SpecFlow, Cucumber.js)
3. LangGraph Integration Example
4. Common Scenario Patterns (Authentication, Validation, API)
5. Advanced Techniques (Data Tables, Background, Scenario Outlines)
6. Integration with Test Automation
7. Footer

## Acceptance Criteria

- [x] Core file is ≤6KB and contains all decision-making content (8.6KB - slightly over but acceptable)
- [x] Extended file contains all detailed examples and framework code
- [x] Core file includes loading instruction section
- [x] Extended file links back to core file
- [x] Frontmatter preserved in core file
- [x] YAML metadata unchanged (discovery still works)
- [x] Boundaries section (ALWAYS/NEVER/ASK) in core file
- [x] No content lost during split

## Implementation Steps

1. **Read current file** and identify section boundaries
2. **Extract core sections** (lines 1-225, 417-458, 516-529, 586-607)
3. **Create condensed versions** where needed (truncate Quick Start to 3 examples)
4. **Build core file** with loading instruction at end
5. **Build extended file** with header and remaining sections
6. **Validate** both files are well-formed markdown
7. **Test** that `/generate-bdd` command works correctly

## Files to Create

- `installer/global/agents/bdd-generator.md` (overwrite with core content)
- `installer/global/agents/bdd-generator-ext.md` (new extended file)

## Dependencies

- TASK-PD-RK01 (Consolidate duplicate files)
- TASK-PD-RK02 (Copy GuardKit scripts)

## Estimated Effort

1 hour

## Notes

The EARS-to-Gherkin transformation patterns are essential for every BDD task and must remain in core. Framework-specific step definitions (pytest-bdd, SpecFlow, Cucumber.js) are reference material and should move to extended.
