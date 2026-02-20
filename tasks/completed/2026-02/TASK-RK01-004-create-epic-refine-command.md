---
complexity: 7
dependencies:
- TASK-RK01-001
- TASK-RK01-002
feature_id: FEAT-RK-001
id: TASK-RK01-004
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: high
status: completed
tags:
- epic-refine
- refinement
- command
task_type: feature
title: Create /epic-refine command
wave: 2
---

# Task: Create /epic-refine Command

## Description

Create the `/epic-refine` command definition at `installer/global/commands/epic-refine.md`. This is the primary new command - an interactive, guided refinement of existing epics with completeness scoring, targeted questions, and change summaries.

## Files to Create

- `installer/global/commands/epic-refine.md` - Epic refinement command definition

## Changes Required

Follow the established command file pattern (see `epic-create.md` for reference). The command must implement:

### Phase 1: Current State Display
- Load epic markdown file by ID
- Parse frontmatter and content sections
- Calculate completeness score (using 9-dimension model from requirements-analyst)
- Display completeness assessment with visual indicators (check, warning, cross)
- Show refinement recommendations based on gaps

### Phase 2: Targeted Questions
- Questions organised by category (scope, success criteria, acceptance criteria, dependencies, risks, constraints, organisation)
- Present weakest categories first
- One question at a time with clear prompts
- Include example good answers with each question
- Skip and done always available
- [REFINE] prefix and visual separators for mode clarity
- Natural language accepted for all answers
- Confirm what was captured after each answer

### Phase 3: Change Summary and Commit
- Display all changes before writing
- Before/after completeness score
- Apply changes options: Yes (update + Graphiti push), No (discard), Edit (manual adjust)
- Update markdown in-place
- Append `refinement_history` entry to frontmatter
- Push to Graphiti if enabled (graceful degradation)

### Arguments
```bash
/epic-refine <epic-id> [options]
/epic-refine EPIC-001
/epic-refine EPIC-001 --focus scope
/epic-refine EPIC-001 --focus criteria
/epic-refine EPIC-001 --focus risks
/epic-refine EPIC-001 --quick
```

### Organisation Awareness
- Detect large direct-pattern epics (8+ tasks) and suggest adding features
- Detect single-feature epics and suggest flattening to direct
- Detect mixed pattern and suggest consolidation

### UX Design (James's Problem)
- Clear mode indicators: `[REFINE]` prefix, visual separators
- One question at a time (never a list)
- Natural language answers
- Skip and done always available
- Show what changed after each answer

## Acceptance Criteria

- [ ] Command file follows established pattern (usage, examples, process, output format)
- [ ] Three-phase flow implemented (display → questions → summary)
- [ ] Questions presented one at a time with skip/done options
- [ ] `--focus` flag restricts questions to a single category
- [ ] `--quick` flag skips prompts and applies AI-suggested improvements
- [ ] Completeness score calculated before and after refinement
- [ ] `refinement_history` appended to frontmatter
- [ ] Graphiti push after markdown update (graceful degradation)
- [ ] [REFINE] prefix and visual separators for mode clarity
- [ ] Works in both Claude Code and Claude Desktop
- [ ] Organisation pattern assessment included in question categories

## Test Requirements

- [ ] Verify command file has valid structure
- [ ] Verify all question categories from spec are covered
- [ ] Verify refinement_history schema matches spec
- [ ] Verify --focus flag documented for each category