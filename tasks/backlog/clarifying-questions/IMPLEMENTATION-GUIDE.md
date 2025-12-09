# Implementation Guide: Clarifying Questions Enhancement

## Execution Strategy

This guide details how to implement the clarifying questions enhancement for RequireKit, including which tasks use `/task-work` vs direct Claude Code, and how to parallelize using Conductor workspaces.

## Task Execution Methods

### Method Legend

| Method | When to Use | Tools |
|--------|-------------|-------|
| **Direct Claude Code** | Simple markdown edits, documentation updates | Read, Edit, Write |
| **/task-work** | Complex logic, multiple files, testing required | Full workflow with quality gates |
| **Conductor Parallel** | Independent tasks that can run simultaneously | Multiple Claude Code instances |

### Task-by-Task Execution Method

| Task | Method | Rationale |
|------|--------|-----------|
| TASK-CLQ-001 | **Direct Claude Code** | Single file edit, adding markdown section |
| TASK-CLQ-002 | **Direct Claude Code** | Single file edit, adding markdown section |
| TASK-CLQ-003 | **Direct Claude Code** | Single file edit, adding markdown section |
| TASK-CLQ-004 | **Direct Claude Code** | Documentation update |
| TASK-CLQ-005 | **/task-work** | Integration testing, multiple scenarios |

**Rationale**: Tasks 001-004 are straightforward markdown additions to command specification files. They don't require the full `/task-work` workflow with quality gates, architectural review, or test enforcement. Task 005 (integration testing) benefits from the structured `/task-work` approach.

---

## Wave 1: Core Enhancements (PARALLEL)

**Execution**: Run TASK-CLQ-001, 002, 003 in parallel using Conductor workspaces.

### Conductor Setup

```bash
# Terminal 1: Epic Create Enhancement
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
claude
# Then: "Implement TASK-CLQ-001 - Add clarification to /epic-create"

# Terminal 2: Feature Create Enhancement
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
claude
# Then: "Implement TASK-CLQ-002 - Add clarification to /feature-create"

# Terminal 3: Formalize EARS Enhancement
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit
claude
# Then: "Implement TASK-CLQ-003 - Add pattern clarification to /formalize-ears"
```

### Why Parallel is Safe

- Each task modifies a **different file**:
  - TASK-CLQ-001 → `installer/global/commands/epic-create.md`
  - TASK-CLQ-002 → `installer/global/commands/feature-create.md`
  - TASK-CLQ-003 → `installer/global/commands/formalize-ears.md`
- No shared dependencies between tasks
- No database or state conflicts
- Git can merge changes cleanly

### Wave 1 Completion Criteria

- [ ] All three command files updated
- [ ] Each file has new "Clarifying Questions" section
- [ ] Questions are technology-agnostic (requirements-focused)
- [ ] No conflicts when merging branches

**Estimated Time**: 0.5-1 day (parallel execution)

---

## Wave 2: Documentation (SEQUENTIAL)

**Execution**: Run after Wave 1 completes. Single task, direct Claude Code.

### Execution Command

```bash
claude
# Then: "Implement TASK-CLQ-004 - Document clarification philosophy"
```

### Why Sequential

- Depends on Wave 1 being complete (needs to reference actual implementation)
- Single file modification
- Quick task (0.25 day)

### Wave 2 Completion Criteria

- [ ] INTEGRATION-GUIDE.md updated with clarification philosophy
- [ ] Table showing which commands have clarification
- [ ] Explanation of technology-agnostic principle

**Estimated Time**: 0.25 day

---

## Wave 3: Integration Testing (SEQUENTIAL)

**Execution**: Run after Wave 2 completes. Use `/task-work` for structured testing.

### Execution Command

```bash
/task-work TASK-CLQ-005
```

### Why /task-work

- Requires systematic testing of multiple scenarios
- Benefits from quality gates and checkpoints
- Should validate full workflow: epic → feature → requirements → EARS → BDD
- May uncover integration issues requiring fixes

### Wave 3 Test Scenarios

1. **Epic Creation Flow**
   - Run `/epic-create "Test Epic"`
   - Verify clarification questions appear
   - Verify epic file created with answers

2. **Feature Creation Flow**
   - Run `/feature-create "Test Feature" epic:EPIC-XXX`
   - Verify clarification questions appear
   - Verify feature links to epic correctly

3. **EARS Formalization Flow**
   - Run `/formalize-ears` with ambiguous input
   - Verify pattern selection questions appear
   - Verify correct EARS pattern generated

4. **End-to-End Workflow**
   - Create epic → create feature → gather requirements → formalize EARS → generate BDD
   - Verify clarifications enhance (not block) workflow
   - Verify technology-agnostic questions throughout

### Wave 3 Completion Criteria

- [ ] All test scenarios pass
- [ ] No workflow blockers introduced
- [ ] Clarifications add value without friction
- [ ] Documentation accurate

**Estimated Time**: 0.5 day

---

## Execution Timeline

```
Day 1 (Morning)
├── Wave 1 Start (Parallel)
│   ├── Workspace 1: TASK-CLQ-001 (epic-create)
│   ├── Workspace 2: TASK-CLQ-002 (feature-create)
│   └── Workspace 3: TASK-CLQ-003 (formalize-ears)
│
Day 1 (Afternoon)
├── Wave 1 Complete
├── Merge all changes
└── Wave 2: TASK-CLQ-004 (documentation)

Day 2 (Morning)
├── Wave 3: TASK-CLQ-005 (integration testing)
└── Final review and completion
```

**Total**: 1.75-2.25 days

---

## Quality Checklist

### Before Marking Complete

- [ ] All command files have clarification sections
- [ ] Questions are requirements-focused, not implementation-focused
- [ ] No technology-specific questions (JWT, Redux, etc.)
- [ ] Documentation updated
- [ ] Integration tests pass
- [ ] Workflow remains smooth (clarifications don't block progress)

### Review Criteria

Each clarification section should:
1. Have 3-5 focused questions (avoid question fatigue)
2. Include sensible defaults or skip options
3. Focus on WHAT and WHY, not HOW
4. Produce better epic/feature/requirement specifications

---

## Rollback Plan

If issues arise:

1. **Single Task Issue**: Revert specific file changes
2. **Wave 1 Integration Issue**: Revert all three command files
3. **Philosophy Misalignment**: Review against TASK-REV-025 recommendations

Git commands for rollback:
```bash
# Revert specific file
git checkout HEAD~1 -- installer/global/commands/epic-create.md

# Revert all Wave 1 changes
git checkout HEAD~1 -- installer/global/commands/
```

---

## Post-Implementation

After all waves complete:

1. **Update TASK-REV-025** status to `COMPLETED`
2. **Create follow-up tasks** if additional enhancements identified
3. **Consider**: Should clarification be added to other commands later?
4. **Monitor**: User feedback on clarification usefulness
