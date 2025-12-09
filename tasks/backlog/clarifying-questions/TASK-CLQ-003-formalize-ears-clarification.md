---
id: TASK-CLQ-003
title: Add Pattern Clarification to /formalize-ears Command
status: backlog
type: enhancement
priority: medium
complexity: 4
created: 2025-12-09T11:00:00Z
wave: 1
parallel_safe: true
execution_method: direct-claude-code
estimated_effort: 0.5-1 day
parent_review: TASK-REV-025
tags: [clarifying-questions, formalize-ears, wave-1, parallel]
files_modified:
  - installer/global/commands/formalize-ears.md
---

# Add Pattern Clarification to /formalize-ears Command

## Objective

Enhance the `/formalize-ears` command to ask clarifying questions when input requirements are ambiguous about which EARS pattern to use, guiding users to select the most appropriate pattern.

## Background

From TASK-REV-025 analysis: Natural language requirements can often be formalized using multiple EARS patterns. For example:

**Input**: "Users should be able to login"

**Could be**:
- **Event-Driven**: "When a user submits credentials, the system shall authenticate..."
- **Ubiquitous**: "The system shall provide login functionality..."
- **State-Driven**: "While a user session is active, the system shall..."

Clarification helps select the most accurate pattern and prompts for missing elements (error conditions, timing constraints).

## Execution Method

**Direct Claude Code** - This is a single-file markdown edit adding a new section.

Do NOT use `/task-work` for this task.

## Implementation

### File to Modify

`installer/global/commands/formalize-ears.md`

### Changes Required

Add a new section after "Input Format" and before "Output Format":

```markdown
## Pattern Clarification (Ambiguity Detection)

When input requirements are ambiguous about EARS pattern type, clarifying questions guide pattern selection.

### Pattern Selection Flow

```
Input: "Users should be able to login"

┌─────────────────────────────────────────────────────────────┐
│ EARS PATTERN CLARIFICATION                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ This requirement could be expressed as multiple patterns.    │
│ Please clarify:                                              │
│                                                              │
│ 1. Is this triggered by a specific user action or event?    │
│    [Y] → Event-Driven: "When X happens, the system shall Y" │
│    [N] → Continue to next question                          │
│                                                              │
│ 2. Is this behavior conditional on system state?            │
│    [Y] → State-Driven: "While X state, the system shall Y"  │
│    [N] → Continue to next question                          │
│                                                              │
│ 3. Is this handling an error or unwanted condition?         │
│    [Y] → Unwanted Behavior: "If X error, then system shall" │
│    [N] → Continue to next question                          │
│                                                              │
│ 4. Is this an optional/configurable feature?                │
│    [Y] → Optional Feature: "Where X enabled, system shall"  │
│    [N] → Ubiquitous: "The system shall Y" (default)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Completeness Questions

After pattern selection, prompt for missing elements:

```
┌─────────────────────────────────────────────────────────────┐
│ REQUIREMENT COMPLETENESS                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ For Event-Driven pattern "When user submits credentials...":│
│                                                              │
│ 1. Are there timing constraints?                            │
│    Example: "...within 1 second"                            │
│    [Enter timing or skip]                                   │
│                                                              │
│ 2. Are there error conditions to capture?                   │
│    Example: "If credentials invalid, then system shall..."  │
│    [Y/N] If yes, we'll create an Unwanted Behavior req      │
│                                                              │
│ 3. Are there boundary conditions?                           │
│    Example: "Maximum 3 login attempts per minute"           │
│    [Enter boundary or skip]                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Pattern Decision Tree

```
                    ┌──────────────────┐
                    │ Analyze Input    │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Triggered by     │
                    │ specific event?  │
                    └────────┬─────────┘
                      Yes    │    No
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌─────────────┐         ┌─────────────┐
        │ Event-Driven│         │ Conditional │
        │   Pattern   │         │ on state?   │
        └─────────────┘         └──────┬──────┘
                                  Yes  │  No
                            ┌──────────┴──────────┐
                            ▼                     ▼
                   ┌─────────────┐       ┌─────────────┐
                   │State-Driven │       │ Handles     │
                   │  Pattern    │       │ errors?     │
                   └─────────────┘       └──────┬──────┘
                                           Yes  │  No
                                     ┌──────────┴──────────┐
                                     ▼                     ▼
                            ┌─────────────┐       ┌─────────────┐
                            │  Unwanted   │       │ Optional    │
                            │  Behavior   │       │ feature?    │
                            └─────────────┘       └──────┬──────┘
                                                    Yes  │  No
                                              ┌──────────┴──────────┐
                                              ▼                     ▼
                                     ┌─────────────┐       ┌─────────────┐
                                     │  Optional   │       │ Ubiquitous  │
                                     │  Feature    │       │  (Default)  │
                                     └─────────────┘       └─────────────┘
```

### Example Clarification Session

```
Input: "Users should be able to login"

Claude: I'll help formalize this requirement. Let me clarify the pattern:

Q1: Is this triggered by a specific user action?
A: Yes, when user submits the login form

Claude: This is an Event-Driven requirement.

Q2: Are there timing constraints?
A: Yes, authentication should complete within 1 second

Q3: Should I also create an error handling requirement?
A: Yes, for invalid credentials

Output:
## REQ-001: User Authentication [Event-Driven]
When a user submits login credentials, the system shall authenticate
the user and establish a session within 1 second.

## REQ-002: Invalid Credentials Handling [Unwanted Behavior]
If a user submits invalid login credentials, then the system shall
display an error message and increment the failed attempt counter.
```

### Skipping Clarification

For direct formalization without clarification:
```bash
# Provide explicit pattern
/formalize-ears "Users login" --pattern event-driven

# Skip clarification and auto-detect
/formalize-ears "Users login" --auto
```
```

## Acceptance Criteria

- [ ] Pattern clarification flow added to formalize-ears.md
- [ ] Decision tree guides pattern selection
- [ ] Completeness questions prompt for timing/errors/boundaries
- [ ] Skip option available for experienced users
- [ ] Example session demonstrates the flow
- [ ] All five EARS patterns covered in decision tree
- [ ] No technology-specific questions

## Testing

Manual verification:
1. Read the updated command file
2. Walk through decision tree with sample requirements
3. Verify each EARS pattern is reachable
4. Verify completeness questions are useful
5. Verify skip options work

## Notes

- Pattern detection should be HELPFUL, not prescriptive
- Users can always override the suggested pattern
- Completeness questions help capture edge cases early
- This is about requirement clarity, not implementation
