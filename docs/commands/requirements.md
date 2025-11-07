# Requirements Commands

Commands for gathering, formalizing, and testing requirements.

## /gather-requirements

Interactive Q&A session to capture complete requirements.

**Usage:**
```bash
/gather-requirements [topic]
```

**Output:** `docs/requirements/draft/[topic].md`

[See detailed documentation →](../guides/command_usage_guide.md#gather-requirements)

## /formalize-ears

Convert draft requirements into EARS notation.

**Usage:**
```bash
/formalize-ears
```

**Output:** Individual requirement files (`REQ-001.md`, `REQ-002.md`, etc.)

[See detailed documentation →](../guides/command_usage_guide.md#formalize-ears)

## /generate-bdd

Generate BDD/Gherkin scenarios from requirements.

**Usage:**
```bash
/generate-bdd [FEAT-XXX]
```

**Output:** `docs/bdd/BDD-XXX.feature`

[See detailed documentation →](../guides/command_usage_guide.md#generate-bdd)

For complete command documentation, see the [Command Usage Guide](../guides/command_usage_guide.md).
