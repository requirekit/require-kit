---
id: TASK-CLQ-001
title: Add Clarifying Questions to /epic-create Command
status: completed
type: enhancement
priority: high
complexity: 3
created: 2025-12-09T11:00:00Z
completed: 2025-12-10T06:33:00Z
wave: 1
parallel_safe: true
execution_method: direct-claude-code
estimated_effort: 0.5 day
parent_review: TASK-REV-025
tags: [clarifying-questions, epic-create, wave-1, parallel]
files_modified:
  - installer/global/commands/epic-create.md
---

# Add Clarifying Questions to /epic-create Command

## Objective

Enhance the `/epic-create` command to ask clarifying questions before creating an epic, ensuring better-scoped epics with clear success criteria and stakeholder identification.

## Background

From TASK-REV-025 analysis: Epic creation benefits from clarification because user intent may be ambiguous when only a title is provided. Clarifying questions help capture:
- Scope boundaries (prevent scope creep)
- Success criteria (measurable outcomes)
- Stakeholders (accountability)
- Timeline constraints (planning)

## Execution Method

**Direct Claude Code** - This is a single-file markdown edit adding a new section.

Do NOT use `/task-work` for this task.

## Implementation

### File to Modify

`installer/global/commands/epic-create.md`

### Changes Required

Add a new section after the "Examples" section and before "Epic Structure":

```markdown
## Clarifying Questions (Interactive Mode)

When creating an epic interactively, the following questions help ensure a well-scoped epic:

### 1. Scope Boundary
```
What is explicitly OUT OF SCOPE for this epic?
[Helps prevent scope creep and sets clear boundaries]

Examples:
- "Mobile app support (web only for now)"
- "Third-party integrations"
- "Advanced analytics"
```

### 2. Success Criteria
```
What measurable outcomes define success for this epic?
[Provide 2-3 specific, measurable criteria]

Examples:
- "User registration rate increases by 20%"
- "Page load time under 2 seconds"
- "Zero critical security vulnerabilities"
```

### 3. Stakeholders
```
Who are the key stakeholders for this epic?

- Product Owner: [Name or role]
- Engineering Lead: [Name or role]
- Design Lead: [Name or role]
- Other: [Name/role if applicable]
```

### 4. Timeline Constraints
```
Are there timeline constraints or dependencies?

Options:
- Quarter target (e.g., "Q1-2024")
- Specific deadline (e.g., "2024-03-15")
- Dependency (e.g., "After EPIC-002 completes")
- Flexible (no hard constraints)
```

### 5. PM Tool Export (Optional)
```
Should this epic sync to external PM tools?

Options:
- Jira (project key: ___)
- Linear (team: ___)
- GitHub Projects (repo: ___)
- Azure DevOps (project: ___)
- None (local only)
```

### Skipping Clarification

For quick epic creation without clarification:
```bash
# Direct creation with all parameters
/epic-create "Title" priority:high quarter:Q1-2024 stakeholder:"Team Lead"

# Or use --quick flag to skip questions
/epic-create "Title" --quick
```

### Clarification Output

Answers are stored in the epic frontmatter:
```yaml
clarification:
  out_of_scope: ["Mobile support", "Third-party integrations"]
  success_criteria:
    - "User registration +20%"
    - "Page load <2s"
  stakeholders:
    product_owner: "Sarah Chen"
    engineering_lead: "Mike Johnson"
  timeline: "Q1-2024"
  pm_tools: ["jira"]
```
```

### Integration Point

Update the "Process" or workflow section to mention:
```markdown
## Process

1. **Clarification** (interactive mode): Answer scoping questions
2. **Validation**: Verify epic structure
3. **Creation**: Generate epic file
4. **Export** (optional): Sync to PM tools
```

## Acceptance Criteria

- [ ] New "Clarifying Questions" section added to epic-create.md
- [ ] Questions focus on requirements (what/why), not implementation (how)
- [ ] Skip option available for quick creation
- [ ] Answers stored in frontmatter for traceability
- [ ] Examples provided for each question
- [ ] No technology-specific questions (preserves tech-agnostic principle)

## Testing

Manual verification:
1. Read the updated command file
2. Verify questions are clear and useful
3. Verify skip option is documented
4. Verify frontmatter storage format is valid YAML

## Notes

- Questions should be OPTIONAL - users can skip for quick creation
- Focus on VALUE - each question should improve epic quality
- Keep to 5 questions max to avoid question fatigue
- All questions must be technology-agnostic
