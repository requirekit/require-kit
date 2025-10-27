# Generate BDD Command

Transform EARS requirements into executable BDD/Gherkin scenarios.

## Usage
```
/generate-bdd [requirement-id]
```

## Transformation Process

I'll convert EARS requirements to BDD scenarios:

1. Map EARS patterns to Gherkin structures
2. Create concrete test examples
3. Cover happy path, edge cases, and errors
4. Add appropriate tags and metadata
5. Ensure scenario independence

## Scenario Coverage

For each requirement, I'll generate:
- ✅ Happy path scenarios
- 🔄 Edge case handling
- ❌ Error scenarios
- ⚡ Performance tests (if applicable)
- 🔒 Security tests (if applicable)

## Output Format

```gherkin
Feature: [Feature name]
  As a [role]
  I want [capability]
  So that [benefit]

  Scenario: [Description]
    Given [context]
    When [action]
    Then [outcome]
```

## Reference

This command uses the methodology from:
`~/.agentic-flow/instructions/core/bdd-methodology.md`

Specify which requirements to convert or generate all.
