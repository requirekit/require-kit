# Progressive Disclosure Implementation Guide

## Quick Reference

### Execution Order

```
Wave 1 (Sequential) ──────────────────────────────────────────────────────┐
│  TASK-PD-RK01: Consolidate duplicates [Direct] (15 min)                │
│  TASK-PD-RK02: Copy GuardKit scripts [Direct] (15 min)                 │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
Wave 2 (Parallel) ────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │ Workspace: p-d-bdd          │  │ Workspace: p-d-analyst          │  │
│  │ TASK-PD-RK03                │  │ TASK-PD-RK04                    │  │
│  │ Split bdd-generator.md      │  │ Split requirements-analyst.md   │  │
│  │ [/task-work] (1 hour)       │  │ [/task-work] (45 min)           │  │
│  └─────────────────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
Wave 3 (Parallel) ────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │ Workspace: p-d-test-bdd     │  │ Workspace: p-d-test-ears        │  │
│  │ TASK-PD-RK05                │  │ TASK-PD-RK06                    │  │
│  │ Test /generate-bdd          │  │ Test /formalize-ears            │  │
│  │ [Direct] (30 min)           │  │ [Direct] (30 min)               │  │
│  └─────────────────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
Wave 4 (Sequential) ──────────────────────────────────────────────────────┐
│  TASK-PD-RK07: Update documentation [Direct] (30 min)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Task Execution Commands

### Wave 1: Foundation

```bash
# No Conductor needed - execute sequentially

# TASK-PD-RK01: Consolidate duplicates
# Execute directly in Claude Code - compare and consolidate agent files

# TASK-PD-RK02: Copy GuardKit scripts
# Execute directly in Claude Code - copy and adapt scripts
```

### Wave 2: Agent Splitting (Parallel)

```bash
# Terminal 1: BDD Generator
conductor create progressive-disclosure-bdd
cd $(conductor path progressive-disclosure-bdd)
/task-work TASK-PD-RK03

# Terminal 2: Requirements Analyst
conductor create progressive-disclosure-analyst
cd $(conductor path progressive-disclosure-analyst)
/task-work TASK-PD-RK04
```

### Wave 3: Testing (Parallel)

```bash
# Terminal 1: BDD Testing
conductor create progressive-disclosure-test-bdd
cd $(conductor path progressive-disclosure-test-bdd)
# Execute TASK-PD-RK05 test scenarios manually

# Terminal 2: EARS Testing
conductor create progressive-disclosure-test-ears
cd $(conductor path progressive-disclosure-test-ears)
# Execute TASK-PD-RK06 test scenarios manually
```

### Wave 4: Documentation

```bash
# No Conductor needed
# Execute TASK-PD-RK07 directly in main workspace
```

## Conductor Workspace Cleanup

After completion:

```bash
conductor delete progressive-disclosure-bdd
conductor delete progressive-disclosure-analyst
conductor delete progressive-disclosure-test-bdd
conductor delete progressive-disclosure-test-ears
```

## File Changes Summary

### Created Files

| File | Wave | Source |
|------|------|--------|
| `installer/global/lib/agent_enhancement/__init__.py` | 1 | New |
| `installer/global/lib/agent_enhancement/models.py` | 1 | GuardKit |
| `installer/global/lib/agent_enhancement/applier.py` | 1 | GuardKit (modified) |
| `installer/global/lib/agent_enhancement/boundary_utils.py` | 1 | GuardKit |
| `installer/global/lib/utils/__init__.py` | 1 | New |
| `installer/global/lib/utils/file_io.py` | 1 | GuardKit |
| `installer/global/agents/bdd-generator-ext.md` | 2 | New (split) |
| `installer/global/agents/requirements-analyst-ext.md` | 2 | New (split) |

### Modified Files

| File | Wave | Change |
|------|------|--------|
| `installer/global/agents/bdd-generator.md` | 2 | Trimmed to core |
| `installer/global/agents/requirements-analyst.md` | 2 | Trimmed to core |
| `CLAUDE.md` | 4 | Add progressive disclosure section |
| `README.md` | 4 | Add feature mention |
| `installer/README.md` | 4 | Add agent file list |

### Possibly Removed Files

| File | Wave | Reason |
|------|------|--------|
| `.claude/agents/bdd-generator.md` | 1 | Consolidated to global |
| `.claude/agents/requirements-analyst.md` | 1 | Consolidated to global |

## Verification Checklist

### After Wave 1
- [ ] No duplicate agent files
- [ ] GuardKit scripts copied to `installer/global/lib/`
- [ ] Python packages importable

### After Wave 2
- [ ] Core files are ≤6KB
- [ ] Extended files contain detailed examples
- [ ] Loading instructions in core files
- [ ] No content lost

### After Wave 3
- [ ] `/generate-bdd` produces valid Gherkin
- [ ] `/formalize-ears` produces valid EARS
- [ ] Extended content loads when requested
- [ ] No quality regression

### After Wave 4
- [ ] Documentation updated
- [ ] All file references correct
- [ ] Conductor workspaces cleaned up

## Rollback Plan

If issues are discovered:

1. **Git reset** to pre-implementation state:
   ```bash
   git checkout HEAD~N -- installer/global/agents/
   ```

2. **Restore original files** from backup (if created)

3. **Remove new files**:
   ```bash
   rm installer/global/agents/*-ext.md
   rm -rf installer/global/lib/agent_enhancement/
   rm -rf installer/global/lib/utils/
   ```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Token savings | ≥30% | Compare before/after file sizes |
| Command functionality | 100% | All tests pass |
| Quality regression | 0 | Manual review of output |
| Implementation time | ≤4 hours | Wall clock with parallelization |
