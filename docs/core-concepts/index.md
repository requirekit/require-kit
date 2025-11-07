# Core Concepts

Understand the fundamentals of RequireKit's requirements management approach.

## Overview

RequireKit uses proven methodologies to transform vague requirements into clear, testable specifications:

- **EARS Notation** for unambiguous requirements
- **BDD/Gherkin** for testable scenarios
- **Epic/Feature Hierarchy** for organization
- **Traceability** for impact analysis

## Concepts

### 📋 [EARS Notation](ears-notation.md)
Five clear patterns for unambiguous requirements: Ubiquitous, Event-Driven, State-Driven, Unwanted Behavior, Optional Feature.

**Use when:** Writing any requirement to ensure clarity and testability.

### ✅ [BDD/Gherkin Scenarios](bdd-scenarios.md)
Automatic generation of testable Given-When-Then scenarios from EARS requirements.

**Use when:** You need acceptance criteria or automated test specifications.

### 🏗️ [Epic/Feature Hierarchy](hierarchy.md)
Structured organization: Epic → Feature → Requirement with full traceability.

**Use when:** Organizing requirements for large projects or complex systems.

### 🔍 [Requirements Traceability](traceability.md)
Clear links from requirements through features to epics, enabling impact analysis and change management.

**Use when:** You need to understand dependencies or assess impact of changes.

## The RequireKit Philosophy

### 1. Requirements First
Start with clear requirements before design or implementation. EARS notation ensures everyone understands what needs to be built.

### 2. Generate, Don't Write
Automatically generate BDD scenarios from requirements. Reduce manual work and ensure consistency.

### 3. Organize Hierarchically
Structure requirements into epics and features. Maintain traceability from strategic goals to implementation details.

### 4. Stay Technology Agnostic
Focus on *what* needs to be built, not *how*. Markdown-driven outputs work with any implementation system.

### 5. Maintain Traceability
Clear links enable impact analysis, change management, and compliance documentation.

## Workflow Overview

```
1. Gather Requirements          2. Formalize with EARS
   (Interactive Q&A)    →           (5 patterns)
         ↓                               ↓
   3. Generate BDD              4. Organize Hierarchy
      (Given-When-Then) →           (Epic/Feature)
         ↓                               ↓
   5. Maintain Traceability     6. Export/Integrate
      (REQ→BDD→FEAT)    →          (PM tools)
```

## Learning Path

### Beginner
Start here if you're new to RequireKit:

1. **[EARS Notation](ears-notation.md)** - Learn the five patterns
2. **[BDD Scenarios](bdd-scenarios.md)** - Understand Given-When-Then
3. **[Try the Quickstart](../getting-started/quickstart.md)** - Hands-on practice

### Intermediate
Build on the basics:

1. **[Epic/Feature Hierarchy](hierarchy.md)** - Organize your requirements
2. **[Requirements Traceability](traceability.md)** - Track dependencies
3. **[Command Reference](../commands/index.md)** - Master all commands

### Advanced
Deep dive into advanced topics:

1. **[Integration with taskwright](../getting-started/integration.md)** - Full workflow
2. **[PM Tool Export](../integration/pm-tools.md)** - Jira, Linear integration
3. **[Examples](../examples/index.md)** - Real-world applications

## Common Questions

### Why EARS notation?

EARS (Easy Approach to Requirements Syntax) provides:
- **Consistency**: Five patterns cover all requirement types
- **Clarity**: Unambiguous structure reduces misunderstanding
- **Testability**: Clear triggers and responses enable verification

### Why BDD/Gherkin?

BDD scenarios provide:
- **Shared understanding**: Given-When-Then is readable by everyone
- **Automated testing**: Scenarios drive test implementation
- **Acceptance criteria**: Clear success definition

### Why Epic/Feature hierarchy?

Hierarchical organization provides:
- **Strategic alignment**: Epics map to business objectives
- **Manageable scope**: Features are implementation units
- **Clear traceability**: Track from strategy to details

### Why technology agnostic?

Markdown outputs enable:
- **Flexibility**: Works with any PM tool or implementation system
- **Version control**: Git-friendly plain text format
- **Future-proof**: Not locked into specific tools

## Next Steps

Choose your path:

**New to RequireKit?**
→ Start with [EARS Notation](ears-notation.md)

**Understand EARS already?**
→ Learn about [BDD Scenarios](bdd-scenarios.md)

**Ready to organize requirements?**
→ Explore [Epic/Feature Hierarchy](hierarchy.md)

**Want to see examples?**
→ Check out [Examples](../examples/index.md)

---

**Need help?** Check the [FAQ](../faq.md) or [Troubleshooting Guide](../troubleshooting/index.md)
