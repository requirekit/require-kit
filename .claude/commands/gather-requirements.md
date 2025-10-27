# Gather Requirements Command

Start an interactive requirements gathering session to elicit and document system requirements.

## Command
```
/gather-requirements [feature-name]
```

## Process

### Phase 1: Discovery (High-Level)
I'll ask broad questions to understand:
- The problem you're solving
- Who will use this feature
- Key business goals
- Success criteria

### Phase 2: Exploration (Detailed)
We'll drill down into:
- Specific user actions
- System responses
- Error conditions
- Performance requirements
- Security needs

### Phase 3: Validation
I'll confirm:
- All scenarios are covered
- Requirements are testable
- No conflicts exist
- Acceptance criteria are clear

## Interactive Q&A Format

I'll guide you through a conversation like this:

```
Q: What is the main purpose of this feature?
A: [Your response]

Q: Who are the primary users?
A: [Your response]

Q: What triggers this behavior?
A: [Your response]

Q: What should happen when [specific scenario]?
A: [Your response]
```

## What You'll Get

After our session, I'll provide:
1. Natural language requirements summary
2. Identified constraints and assumptions
3. Acceptance criteria
4. Ready for EARS formalization

## Tips for Best Results

- Be specific with examples
- Mention edge cases you're aware of
- Include performance expectations
- Describe error scenarios
- Mention security concerns

## Example Session

```
Claude: Let's gather requirements for your feature. What problem are we solving?

You: We need a user authentication system for our web app.

Claude: Great! Who will be using this authentication system?

You: Both regular users and administrators, with different access levels.

Claude: What authentication methods should we support?

You: Email/password primarily, with optional 2FA.

Claude: What should happen when a user fails to login multiple times?

You: Lock the account after 3 failed attempts for 15 minutes.

[continues...]
```

## Next Steps

After gathering requirements:
1. Run `/formalize-ears` to convert to EARS notation
2. Run `/generate-bdd` to create test scenarios
3. Begin implementation with clear specifications

Start by telling me: **What feature would you like to gather requirements for?**
