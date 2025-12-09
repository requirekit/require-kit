---
id: TASK-PD-RK07
title: Update RequireKit documentation
status: completed
created: 2025-12-09T11:00:00Z
updated: 2025-12-09T22:30:00Z
completed: 2025-12-09T22:30:00Z
priority: medium
tags: [progressive-disclosure, documentation, wave-4]
task_type: implementation
complexity: 2
execution_mode: direct
wave: 4
conductor_workspace: null
parallel: false
blocking: false
parent_review: TASK-REV-PD01
depends_on: [TASK-PD-RK05, TASK-PD-RK06]
---

# Task: Update RequireKit documentation

## Description

Update RequireKit documentation to reflect the progressive disclosure implementation. Add guidance on when and how to load extended agent content.

## Execution Mode

**Direct Claude Code** - Documentation updates, no code generation needed.

## Files to Update

### 1. CLAUDE.md (root)

Add section about progressive disclosure:

```markdown
## Progressive Disclosure

RequireKit uses progressive disclosure to optimize context window usage while maintaining comprehensive documentation.

### How It Works

Agent files are split into:
1. **Core files** (`{name}.md`): Essential content always loaded
   - Quick Start examples
   - Boundaries (ALWAYS/NEVER/ASK)
   - EARS patterns
   - Core capabilities

2. **Extended files** (`{name}-ext.md`): Detailed reference loaded on-demand
   - Framework-specific examples
   - Domain patterns
   - Advanced techniques
   - Troubleshooting

### Loading Extended Content

When implementing detailed code or needing framework-specific guidance:

```bash
# For BDD generator extended content
cat agents/bdd-generator-ext.md

# For requirements analyst extended content
cat agents/requirements-analyst-ext.md
```

### Benefits

- **30%+ token reduction** in typical tasks
- **Faster responses** from reduced context
- **Same comprehensive content** available when needed
```

### 2. README.md (root)

Add brief mention in Features section:

```markdown
### Efficient Context Management

RequireKit uses progressive disclosure to keep context lean:
- Core agent content always loaded (~30% of original)
- Extended examples available on-demand
- Framework-specific step definitions in extended files
```

### 3. installer/README.md

Add note about extended files:

```markdown
### Agent Files

The installer distributes both core and extended agent files:
- `bdd-generator.md` - Core BDD generation (always loaded)
- `bdd-generator-ext.md` - Extended examples (on-demand)
- `requirements-analyst.md` - Core EARS formalization (always loaded)
- `requirements-analyst-ext.md` - Extended gathering processes (on-demand)
```

## Acceptance Criteria

- [x] CLAUDE.md updated with progressive disclosure section
- [x] README.md updated with feature mention
- [x] installer/README.md updated with agent file list
- [x] Documentation is consistent across all files
- [x] No broken links or references
- [x] Aligns with GuardKit's progressive disclosure documentation style

## Implementation Steps

1. Read current CLAUDE.md and identify insertion point
2. Add Progressive Disclosure section after "Core Principles" or "Workflow Overview"
3. Update README.md Features section
4. Update installer documentation
5. Verify all file references are correct
6. Check for consistency with GuardKit documentation

## Dependencies

- TASK-PD-RK05 (Test /generate-bdd) - Must pass before documenting
- TASK-PD-RK06 (Test /formalize-ears) - Must pass before documenting

## Estimated Effort

30 minutes

## Notes

Keep documentation concise. The goal is to inform users about progressive disclosure without overwhelming them. Focus on:
1. What it is (split files)
2. Why it matters (token efficiency)
3. How to use it (cat command)
