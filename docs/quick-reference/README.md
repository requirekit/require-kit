# Quick Reference Cards

Fast-access documentation for common Agentecflow Lite workflows and concepts. Each card is designed to fit on a single screen for easy reference during development.

## Available Cards

### Core Workflows
- **[task-work-cheat-sheet.md](task-work-cheat-sheet.md)** - Complete `/task-work` command reference
  - All phases (1-5.5) with decision points
  - All flags (--design-only, --implement-only, --micro)
  - State transitions and common errors

### Complexity Management
- **[complexity-guide.md](complexity-guide.md)** - Task complexity evaluation guide
  - Scoring factors and thresholds
  - Breakdown strategies by complexity level
  - Examples for each complexity tier

### Quality Assurance
- **[quality-gates-card.md](quality-gates-card.md)** - Quality gates reference
  - All gates with pass/fail thresholds
  - Phase 4.5 fix loop flowchart
  - Escalation paths for blocked tasks

### Advanced Workflows
- **[design-first-workflow-card.md](design-first-workflow-card.md)** - Design-first workflow guide
  - When to use --design-only vs --implement-only
  - State prerequisites and transitions
  - Common patterns (architect handoff, multi-day tasks)

## Navigation by Workflow Phase

### Planning Phase (Pre-Implementation)
1. [Complexity Guide](complexity-guide.md) - Evaluate task complexity before creation
2. [Design-First Workflow](design-first-workflow-card.md) - Choose workflow mode

### Implementation Phase
1. [Task Work Cheat Sheet](task-work-cheat-sheet.md) - Execute implementation workflow
2. [Quality Gates](quality-gates-card.md) - Understand quality requirements

### Review Phase
1. [Quality Gates](quality-gates-card.md) - Verify all gates passed
2. [Task Work Cheat Sheet](task-work-cheat-sheet.md) - Understand state transitions

## Path Conventions

All quick reference cards link to full documentation using these conventions:

- **Commands**: `installer/global/commands/{command-name}.md`
- **Agents**: `installer/global/agents/{agent-name}.md`
- **Workflows**: `docs/guides/{workflow-name}.md`
- **Patterns**: `docs/patterns/{pattern-name}.md`

## Usage Tips

**Print-Friendly**: Each card is ≤150 lines and designed for standard terminal viewing.

**Cross-References**: Cards link to full documentation for detailed information.

**Progressive Detail**: Cards provide quick reference first, then link to comprehensive guides.

**Terminal Access**: Display cards in terminal using `cat` or `less`:
```bash
# View in terminal
cat docs/quick-reference/task-work-cheat-sheet.md

# View with pager
less docs/quick-reference/complexity-guide.md
```

## Contributing

When adding new quick reference cards:
1. Follow the 5-section template (Overview, Quick Reference, Decision Guide, Examples, See Also)
2. Keep cards ≤150 lines for printability
3. Use simple text diagrams (arrows, indentation) not complex ASCII art
4. Cross-reference to full documentation (don't duplicate content)
5. Update this README with navigation entries
