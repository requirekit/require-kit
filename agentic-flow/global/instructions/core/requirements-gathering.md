# Requirements Gathering Guide

## Interactive Q&A Process

This guide helps conduct effective requirements gathering sessions that lead to clear EARS requirements and BDD scenarios.

## Question Framework

### Phase 1: Discovery (High-Level)
Start with broad questions to understand the context:

1. **Purpose**
   - What problem are we solving?
   - Why is this important now?
   - What happens if we don't solve it?

2. **Users**
   - Who will use this feature?
   - What are their goals?
   - What is their technical expertise?

3. **Success**
   - How will we measure success?
   - What are the key metrics?
   - What is the minimum acceptable outcome?

### Phase 2: Exploration (Detailed)
Drill into specifics:

1. **Functionality**
   - What specific actions can users take?
   - What are the system's responses?
   - What data is involved?

2. **Scenarios**
   - What is the happy path?
   - What could go wrong?
   - What are the edge cases?

3. **Constraints**
   - What are the technical limitations?
   - What are the business rules?
   - What are the compliance requirements?

### Phase 3: Validation
Confirm understanding:

1. **Completeness**
   - Have we covered all user types?
   - Are all scenarios addressed?
   - Any missing requirements?

2. **Clarity**
   - Are requirements unambiguous?
   - Can they be tested?
   - Are success criteria measurable?

3. **Feasibility**
   - Are requirements technically possible?
   - Do we have the resources?
   - What are the risks?

## Question Templates by Domain

### Authentication & Security
- How do users prove their identity?
- What happens on failed authentication?
- How long do sessions last?
- What security standards apply?
- How do we handle password reset?

### Data Management
- What data do we collect?
- How is it validated?
- Where is it stored?
- Who can access it?
- How long do we keep it?

### User Interface
- What information is displayed?
- How do users interact?
- What feedback is provided?
- How do we handle errors?
- What about accessibility?

### Performance
- How fast must it respond?
- How many concurrent users?
- What is acceptable downtime?
- Peak load expectations?
- Graceful degradation strategy?

## Documentation Template

```markdown
## Requirements Gathering Session
**Date**: [Date]
**Participants**: [Names]
**Feature**: [Feature name]

### Context
[Background and purpose]

### Key Findings

#### Users & Goals
- Primary users: [Description]
- User goals: [List]
- Success metrics: [Metrics]

#### Functional Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

#### Non-Functional Requirements
- Performance: [Criteria]
- Security: [Requirements]
- Usability: [Standards]

#### Scenarios Identified
1. **Happy Path**: [Description]
2. **Edge Case 1**: [Description]
3. **Error Case 1**: [Description]

### Open Questions
- [ ] [Question 1]
- [ ] [Question 2]

### Next Steps
- [ ] Formalize to EARS notation
- [ ] Create BDD scenarios
- [ ] Review with stakeholders
```

## Best Practices

### Do's
✅ Ask open-ended questions initially
✅ Use the "5 Whys" technique
✅ Provide examples to clarify
✅ Document assumptions
✅ Confirm understanding with summaries
✅ Focus on user outcomes, not solutions

### Don'ts
❌ Lead with technical solutions
❌ Make assumptions without confirming
❌ Skip edge cases and errors
❌ Ignore non-functional requirements
❌ Accept vague requirements
❌ Forget about maintenance and operations

## Output Checklist

After gathering requirements, ensure you have:
- [ ] Clear problem statement
- [ ] Identified all user types
- [ ] Documented success criteria
- [ ] Listed functional requirements
- [ ] Specified non-functional requirements
- [ ] Identified test scenarios
- [ ] Noted constraints and assumptions
- [ ] Flagged risks and open questions
