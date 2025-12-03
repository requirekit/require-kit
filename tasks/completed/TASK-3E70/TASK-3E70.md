---
id: TASK-3E70
title: Verify RequireKit Agent Usage - Duplication Analysis
status: completed
created: 2025-12-03T16:35:00Z
updated: 2025-12-03T17:10:00Z
completed: 2025-12-03T17:10:00Z
completed_location: tasks/completed/TASK-3E70/
priority: high
tags: [architecture, review, agent-consolidation, duplication-analysis]
task_type: review
decision_required: true
complexity: 5
related_tasks: [TASK-SHA-001, TASK-ARCH-DC05]
review_results:
  mode: architectural
  depth: standard
  score: 95
  findings_count: 6
  recommendations_count: 4
  decision: implement
  implementation_task: TASK-8632
  report_path: .claude/reviews/TASK-3E70-review-report.md
  completed_at: 2025-12-03T17:00:00Z
---

# Task: Verify RequireKit Agent Usage - Duplication Analysis

## Review Status: COMPLETE

**See full report**: [.claude/reviews/TASK-3E70-review-report.md](../../.claude/reviews/TASK-3E70-review-report.md)

---

## Key Finding

**RequireKit does NOT use the 5 agents identified in the similarity report.**

All 5 agents are vestigial copies from shared development history. They are NOT invoked by any RequireKit commands or workflows.

---

## Agent Usage Matrix (Final)

| Agent | In Installer | Referenced by Commands | Invoked by Commands | **Verdict** |
|-------|-------------|----------------------|--------------------|----|
| architectural-reviewer | ✅ | ❌ | ❌ | **UNUSED - SAFE TO REMOVE** |
| test-orchestrator | ✅ | ❌ | ❌ | **UNUSED - SAFE TO REMOVE** |
| task-manager | ✅ | ❌ | ❌ | **UNUSED - SAFE TO REMOVE** |
| code-reviewer | ✅ | ❌ | ❌ | **UNUSED - SAFE TO REMOVE** |
| test-verifier | ✅ | ❌ | ❌ | **UNUSED - SAFE TO REMOVE** |
| bdd-generator | ✅ | ✅ | ✅ | **USED - KEEP** |
| requirements-analyst | ✅ | ✅ | ✅ | **USED - KEEP** |

---

## Evidence Summary

1. **CLAUDE.md explicitly lists only 2 agents**: `bdd-generator` and `requirements-analyst`
2. **No command references**: Grep of all 12 commands found NO references to the 5 agents
3. **No subagent_type usage**: RequireKit commands don't spawn subagents via Task tool
4. **task-manager is a GuardKit copy**: References other agents but is itself never invoked

---

## Acceptance Criteria Status

- [x] Exhaustive search of all RequireKit source files completed
- [x] Each command file manually reviewed for agent usage
- [x] Document which agents are actively used (with evidence)
- [x] Document which agents are unused/vestigial (with evidence)
- [x] Provide per-agent recommendation: keep, consolidate, or remove
- [ ] Update TASK-ARCH-DC05 with definitive findings (pending)

---

## Recommendations

### Safe Removal List (5 agents)
Remove from `installer/global/agents/`:
- `architectural-reviewer.md`
- `test-orchestrator.md`
- `task-manager.md`
- `code-reviewer.md`
- `test-verifier.md`

Remove from `.claude/agents/`:
- `test-orchestrator.md`
- `task-manager.md`
- `code-reviewer.md`
- `test-verifier.md`

### Keep List (2 agents)
- `bdd-generator.md` - Core to BDD generation workflow
- `requirements-analyst.md` - Core to EARS formalization workflow

---

## Decision Checkpoint

| Option | Description |
|--------|-------------|
| **[A]ccept** | Archive this review task as complete |
| **[I]mplement** | Create task to remove the 5 unused agents |
| **[R]evise** | Request deeper analysis |
| **[C]ancel** | Discard findings |

---

## Background

A similarity analysis (TASK-SHA-001) identified the following agents as having some level of duplication between RequireKit and GuardKit:

| Agent | Similarity | Category |
|-------|------------|----------|
| test-orchestrator | 74% | Manual Review (50-80%) |
| architectural-reviewer | 72% | Manual Review (50-80%) |
| task-manager | 64% | Manual Review (50-80%) |
| code-reviewer | 61% | Manual Review (50-80%) |
| test-verifier | 47% | Low Similarity (<50%) |

## Objective

Verify whether RequireKit **actually uses** these agents in its workflows, or if they are vestigial/unused code that could be safely removed or consolidated.

**CRITICAL**: Do NOT remove any agents that are actively used. This review must provide definitive evidence before any consolidation decisions.

## Key Paths Checked

### Source Locations (RequireKit Repo)
- **Commands**: `installer/global/commands/` (12 commands)
- **Agents (source)**: `installer/global/agents/` (7 agents)
- **Local dev agents**: `.claude/agents/` (8 agents)

### Installation Location (Runtime)
- **Installed agents**: `~/.agentecflow/agents/` (all agents installed)

## Research Questions - ANSWERED

### 1. Agent Presence Analysis
- [x] Which of these 5 agents exist in `installer/global/agents/`? **ALL 5**
- [x] Which are installed to `~/.agentecflow/agents/`? **ALL 5**
- [x] Are there discrepancies between source and installed versions? **architectural-reviewer missing from .claude/agents/**

### 2. Command Usage Analysis (CRITICAL)
- [x] Search ALL commands in `installer/global/commands/` for agent references - **NONE FOUND**
- [x] Check for `subagent_type` parameter usage - **NONE FOUND**
- [x] Check for Task tool invocations with these agent types - **NONE FOUND**
- [x] Check for any agent name mentions in command documentation - **ONLY README EXAMPLES**

### 3. Workflow Integration
- [x] Are these agents part of the core RequireKit workflow? **NO**
- [x] Do epic/feature commands use any of these agents? **NO**
- [x] Do they serve a purpose specific to requirements management? **NO**

### 4. Cross-Package Analysis
- [x] If agents ARE used, is usage identical to GuardKit or divergent? **N/A - NOT USED**
- [x] Are there RequireKit-specific customizations? **NO - COPIES FROM GUARDKIT**
- [x] Could functionality be delegated to GuardKit if both packages are installed? **YES - RECOMMENDED**

## Notes

- RequireKit-only agents (bdd-generator, requirements-analyst) are NOT in scope
- Focus is on the 5 agents identified in the similarity report
- This is a review/analysis task - no implementation changes should be made
- Review complete with HIGH confidence level
