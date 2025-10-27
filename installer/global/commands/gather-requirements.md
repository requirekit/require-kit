# Gather Requirements Command

Start an interactive requirements gathering session using the Q&A approach.

## Usage

In Claude Code, type:
```
/gather-requirements
```

## Process

1. **Discovery Phase**: Start with high-level understanding
   - What is the main purpose/goal?
   - Who are the users?
   - What problem does this solve?

2. **Exploration Phase**: Dive into specifics
   - What are the key features?
   - What are the constraints?
   - What are the non-functional requirements?

3. **Validation Phase**: Confirm understanding
   - Review gathered requirements
   - Identify gaps
   - Clarify ambiguities

## Output

Creates a requirements document in `docs/requirements/draft/[feature-name].md` with:
- User stories
- Functional requirements
- Non-functional requirements
- Acceptance criteria
- Dependencies

## Best Practices

1. **Use the 5W1H Framework**:
   - **What**: What capability is needed?
   - **Who**: Who will use this feature?
   - **When**: When will this be used?
   - **Where**: Where in the system does this fit?
   - **Why**: Why is this important?
   - **How**: How should it work?

2. **Progressive Disclosure**:
   - Start broad, then narrow down
   - Don't overwhelm with detailed questions initially
   - Build context before diving deep

3. **Document As You Go**:
   - Capture requirements in draft form
   - Use markdown for clarity
   - Include examples where helpful

## Example Session

```markdown
### Q: What is the main purpose of this feature?
A: To allow users to sync their photos across devices automatically.

### Q: Who are the primary users?
A: Consumers with multiple devices (phone, tablet, computer) who take lots of photos.

### Q: What problem does this solve?
A: Users currently have to manually transfer photos between devices, which is time-consuming and error-prone.

### Q: What are the key capabilities needed?
A: 
- Automatic photo detection on each device
- Background synchronization
- Conflict resolution for duplicates
- Selective sync options
- Storage management

### Q: What are the quality requirements?
A:
- Sync should happen within 5 minutes of photo creation
- No data loss during sync
- Minimal battery impact on mobile devices
- Support for RAW and JPEG formats
```

## Requirements Document Structure

The generated document follows this structure:

```markdown
---
id: REQ-[NUMBER]
title: [Feature Name]
status: draft
created: [DATE]
---

# [Feature Name] Requirements

## Executive Summary
[Brief overview of the feature and its purpose]

## User Stories
- As a [user type], I want to [action] so that [benefit]
- ...

## Functional Requirements
### FR-001: [Requirement Name]
**Description**: [What the system must do]
**Priority**: [High/Medium/Low]
**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

## Non-Functional Requirements
### NFR-001: [Requirement Name]
**Category**: [Performance/Security/Usability/etc]
**Description**: [Quality attribute requirement]
**Metric**: [How to measure]

## Dependencies
- [External systems]
- [APIs]
- [Libraries]

## Assumptions
- [What we're assuming to be true]

## Constraints
- [Technical limitations]
- [Business constraints]
- [Regulatory requirements]

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

## Workflow Integration

After gathering requirements:

1. **Review and Refine**: Read through the draft requirements
2. **Formalize**: Use `/formalize-ears` to convert to EARS notation
3. **Generate Tests**: Use `/generate-bdd` to create test scenarios
4. **Approve**: Move from draft to approved when ready

## Tips for Effective Requirements Gathering

1. **Listen Actively**: Pay attention to what's not being said
2. **Ask "Why" Multiple Times**: Get to the root need
3. **Use Examples**: Concrete scenarios clarify abstract requirements
4. **Validate Understanding**: Restate requirements in your own words
5. **Document Decisions**: Capture not just what, but why
6. **Consider Edge Cases**: What happens when things go wrong?
7. **Think About Data**: What information needs to be stored/processed?
8. **Consider Integration**: How does this fit with existing systems?

## Common Pitfalls to Avoid

- **Solution-First Thinking**: Focus on the problem before jumping to solutions
- **Assumption Making**: Always verify, never assume
- **Incomplete Acceptance Criteria**: Be specific about what "done" means
- **Missing Non-Functional Requirements**: Performance, security, and usability matter
- **Ignoring Constraints**: Technical and business limitations shape solutions
- **Forgetting Maintenance**: Consider long-term support and updates

## Next Steps

Once requirements are gathered:
- Review with stakeholders
- Prioritize features
- Estimate complexity
- Plan implementation sprints
- Create architecture decisions if needed
