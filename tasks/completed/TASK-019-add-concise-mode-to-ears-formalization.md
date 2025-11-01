---
id: TASK-019
title: Add Concise Mode Flag to EARS Requirements Formalization
status: backlog
priority: high
created: 2025-10-16T10:40:00Z
labels: [enhancement, sdd-alignment, requirements, brevity]
estimated_effort: 2-3 hours
complexity_estimate: 3

# Source
source: spectrum-driven-development-analysis.md
recommendation: Priority 1 - High Impact, Low Effort
sdd_alignment: Spec Conciseness

# Requirements
requirements:
  - REQ-SDD-004: Avoid over-verbose specifications
  - REQ-SDD-005: Provide concise requirement mode
  - REQ-SDD-006: Enforce word count constraints
---

# Add Concise Mode Flag to EARS Requirements Formalization

## Problem Statement

EARS notation can become verbose, leading to over-specification that consumes excessive AI tokens and reduces readability. No current mechanism to enforce brevity.

## Solution Overview

Add `--concise` flag to `/formalize-ears` command that:
- Limits requirements to ≤500 words
- Focuses on "what" not "how"
- Uses bullet points over paragraphs
- Provides word count tracking

## Acceptance Criteria

### 1. Concise Flag Implementation
- [ ] Add `--concise` parameter to `/formalize-ears` command
- [ ] Enforce 500-word limit per requirement
- [ ] Generate bullet-point format (not paragraphs)
- [ ] Display word count: X/500

### 2. Concise Guidelines
- [ ] Focus on behavior, not implementation
- [ ] Omit obvious details
- [ ] Use action verbs (validate, generate, return, log)
- [ ] Avoid redundant explanations

### 3. Validation
- [ ] Reject requirements >500 words in concise mode
- [ ] Suggest splitting into multiple requirements if too complex
- [ ] Provide word count feedback

### 4. Default Mode Unchanged
- [ ] Standard mode (no flag) remains verbose
- [ ] Backward compatibility maintained
- [ ] Concise mode is opt-in

## Implementation Plan

### Phase 1: Command Enhancement (1 hour)
```markdown
# File: installer/global/commands/formalize-ears.md

## Command Syntax

```bash
/formalize-ears [--concise] [--max-words N]
```

## Flags

### --concise
Generates concise EARS requirements with ≤500 word limit.
- Uses bullet points
- Focuses on "what" not "how"
- Omits implementation details

### --max-words N
Custom word limit (default: 500 in concise mode, unlimited in standard mode).

## Examples

### Concise Mode
```bash
/formalize-ears --concise

## REQ-042: User Authentication

**Type**: Event-Driven
**Constraint**: ≤500 words

When valid credentials submitted, system shall:
- Validate against auth service
- Generate JWT (24h expiry)
- Return token in response
- Log event

**Word Count**: 47/500 ✅
```

### Standard Mode
```bash
/formalize-ears

## REQ-042: User Authentication

**Type**: Event-Driven

When a user submits valid login credentials through the authentication endpoint,
the system shall perform the following sequence of operations:

1. Validate the provided credentials against the authentication service...
(continues with detailed explanation)

**Word Count**: 347 (no limit)
```
```

### Phase 2: Agent Integration (1 hour)
```markdown
# File: installer/global/agents/requirements-analyst.md

## Concise Mode Guidelines (when --concise flag used)

When generating concise requirements:

1. **Word Budget**: ≤500 words per requirement
2. **Format**: Bullet points, not paragraphs
3. **Focus**: What the system shall do (behavior)
4. **Omit**: How it's implemented (technical details)
5. **Action Verbs**: validate, generate, return, log, create, update, delete
6. **Avoid**:
   - Implementation details (unless critical)
   - Redundant explanations
   - Obvious context
   - Filler words

## Word Count Tracking

Display word count after each requirement:
- ✅ X/500 (within limit)
- ⚠️  X/500 (approaching limit, 450-500)
- ❌ X/500 (over limit, requires splitting)
```

### Phase 3: Validation Logic (30 minutes)
```python
# File: installer/global/commands/lib/requirement_validator.py

def validate_concise_requirement(text: str, max_words: int = 500) -> ValidationResult:
    """Validate requirement against concise mode constraints."""

    word_count = len(text.split())

    if word_count > max_words:
        return ValidationResult(
            valid=False,
            word_count=word_count,
            message=f"❌ Requirement exceeds {max_words} words ({word_count}/{max_words}). "
                    f"Consider splitting into multiple requirements."
        )

    if word_count >= max_words * 0.9:  # 450+ words
        return ValidationResult(
            valid=True,
            word_count=word_count,
            message=f"⚠️  Approaching word limit ({word_count}/{max_words}). "
                    f"Consider condensing further."
        )

    return ValidationResult(
        valid=True,
        word_count=word_count,
        message=f"✅ {word_count}/{max_words}"
    )
```

### Phase 4: Testing (30 minutes)
- Unit tests for word count validation
- Integration tests with requirements-analyst agent
- Test cases: within limit, approaching limit, over limit

## Files to Create/Modify

### New Files
- `installer/global/commands/lib/requirement_validator.py`
- `tests/unit/test_requirement_validator.py`

### Modified Files
- `installer/global/commands/formalize-ears.md` (add --concise flag)
- `installer/global/agents/requirements-analyst.md` (add concise guidelines)

## Example Output

### Before (Standard Mode - Verbose)
```markdown
## REQ-042: User Authentication

**Type**: Event-Driven

When a user submits valid login credentials through the authentication endpoint,
the system shall perform the following comprehensive sequence of operations to
ensure secure and reliable authentication:

1. The system shall validate the provided credentials against the authentication
   service using industry-standard validation protocols.
2. Upon successful validation, the system shall generate a JSON Web Token (JWT)
   with a 24-hour expiration period to maintain security while balancing user
   convenience.
3. The system shall return the generated token in the response payload to enable
   the client application to maintain an authenticated session.
4. The system shall log the successful authentication event with appropriate
   metadata for security auditing and compliance purposes.

**Word Count**: 124
```

### After (Concise Mode)
```markdown
## REQ-042: User Authentication

**Type**: Event-Driven
**Constraint**: ≤500 words

When valid credentials submitted, system shall:
- Validate against auth service
- Generate JWT (24h expiry)
- Return token in response
- Log authentication event

**Acceptance Criteria**:
- ✅ Valid credentials → JWT token
- ✅ Invalid credentials → 401 error
- ✅ Token expires after 24h
- ✅ All auth events logged

**Word Count**: 47/500 ✅
```

## Success Metrics

- **Word Count Reduction**: 50-70% reduction in concise mode
- **Readability**: Improved (measured by developer feedback)
- **AI Token Savings**: 40-60% reduction in token usage
- **Time Savings**: 30-40% faster requirement review

## Related Tasks

- TASK-021: Spec Templates by Type
- TASK-018: Spec Drift Detection

## Dependencies

- None (standalone enhancement)

## Notes

- Concise mode is opt-in (backward compatible)
- Can combine with other flags: `/formalize-ears --concise --max-words 300`
- Consider adding presets: `--ultra-concise` (250 words), `--standard-concise` (500 words)
