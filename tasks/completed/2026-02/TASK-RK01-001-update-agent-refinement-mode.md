---
complexity: 7
dependencies: []
feature_id: FEAT-RK-001
id: TASK-RK01-001
implementation_mode: task-work
parent_review: TASK-REV-RK01
priority: high
status: completed
tags:
- refinement
- completeness-scoring
- agent
task_type: feature
title: Add refinement mode and completeness scoring to requirements-analyst agent
wave: 1
---

# Task: Add Refinement Mode and Completeness Scoring to Requirements Analyst Agent

## Description

Update `installer/global/agents/requirements-analyst.md` and `installer/global/agents/requirements-analyst-ext.md` to support refinement mode with completeness scoring. This is the foundation that `/epic-refine` and `/feature-refine` commands will rely on.

## Files to Modify

- `installer/global/agents/requirements-analyst.md` - Add refinement mode section, completeness scoring logic, updated boundaries
- `installer/global/agents/requirements-analyst-ext.md` - Add Graphiti integration patterns, refinement question templates, sync instructions

## Changes Required

### requirements-analyst.md

1. **Add Refinement Mode Section** (after Primary Responsibilities):
   - Define when refinement mode activates (triggered by `/epic-refine` or `/feature-refine`)
   - Three-phase flow: display current state → targeted questions → change summary
   - Question presentation rules: one at a time, skip/done always available
   - Natural language answer parsing guidance
   - Change summary generation rules

2. **Add Completeness Scoring Logic**:
   - Epic completeness: 9 weighted dimensions (business objective 15%, scope 15%, success criteria 20%, acceptance criteria 15%, risk 10%, constraints 10%, dependencies 5%, stakeholders 5%, organisation 5%)
   - Feature completeness: 7 weighted dimensions (scope within epic 10%, acceptance criteria 25%, requirements traceability 20%, BDD coverage 15%, technical considerations 15%, dependencies 10%, test strategy 5%)
   - Score calculation method with partial credit
   - Score interpretation guide (informational, not gating)

3. **Update Output Format Template**:
   - Add `completeness_score` to frontmatter
   - Add `refinement_history` array structure
   - Add `organisation_pattern` field awareness

4. **Update Boundaries**:
   - ALWAYS: Present refinement questions one at a time with skip/done options
   - ALWAYS: Show before/after completeness scores
   - NEVER: Skip the change summary before applying updates
   - ASK: When refinement answers contradict existing content

### requirements-analyst-ext.md

1. **Add Graphiti Integration Patterns**:
   - Episode schema for epics (from FEAT-RK-001 spec lines 307-330)
   - Episode schema for features (from spec lines 333-357)
   - Group ID strategy (`{project}__requirements`)
   - Sync error handling patterns
   - Standalone mode behavior

2. **Add Refinement Question Templates**:
   - Scope refinement questions with example good answers
   - Success criteria questions with measurable examples
   - Risk assessment questions
   - Dependency discovery questions
   - Organisation pattern assessment questions

## Acceptance Criteria

- [ ] requirements-analyst.md contains refinement mode section with three-phase flow
- [ ] Completeness scoring dimensions match FEAT-RK-001 spec exactly (epic: 9 dimensions, feature: 7 dimensions)
- [ ] Score weights sum to 100% for both epic and feature scoring
- [ ] requirements-analyst-ext.md contains Graphiti episode schemas matching spec
- [ ] Question templates include example good answers and skip guidance
- [ ] Progressive disclosure maintained (core file < 500 lines, extended loads on-demand)

## Test Requirements

- [ ] Verify agent file parses correctly (valid YAML frontmatter)
- [ ] Verify completeness score weights sum to 100%
- [ ] Verify all 9 epic dimensions documented
- [ ] Verify all 7 feature dimensions documented