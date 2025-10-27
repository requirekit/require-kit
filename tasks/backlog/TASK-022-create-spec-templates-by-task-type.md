---
id: TASK-022
title: Create Spec Templates by Task Type for Requirements Gathering
status: backlog
priority: medium
created: 2025-10-16T10:55:00Z
labels: [enhancement, sdd-alignment, requirements, templates]
estimated_effort: 6-8 hours
complexity_estimate: 5

# Source
source: spectrum-driven-development-analysis.md
recommendation: Priority 2 - Medium Impact, Medium Effort
sdd_alignment: Spec Flexibility

# Requirements
requirements:
  - REQ-SDD-013: Specialized templates for different task types
  - REQ-SDD-014: Reduce over-specification for simple tasks
  - REQ-SDD-015: Appropriate detail level per task category
---

# Create Spec Templates by Task Type for Requirements Gathering

## Problem Statement

Same verbose requirements process for all task types (bug fixes, features, refactors, docs). Different task types need different levels of detail and focus areas.

## Solution Overview

Create specialized requirement templates for different task types:
- **bug-fix**: Minimal spec (current vs expected behavior)
- **feature**: Comprehensive spec (EARS notation, BDD scenarios)
- **refactor**: Architecture-focused (design goals, constraints)
- **documentation**: User-centric (audience, format, examples)
- **performance**: Metrics-focused (current vs target performance)
- **security**: Threat-focused (vulnerabilities, mitigations)

## Acceptance Criteria

### 1. Template System
- [ ] Template selection via `--type` flag
- [ ] 6 specialized templates (bug-fix, feature, refactor, docs, performance, security)
- [ ] Template-specific Q&A workflows
- [ ] Appropriate word count limits per template

### 2. Bug Fix Template
- [ ] Current behavior (broken)
- [ ] Expected behavior (fixed)
- [ ] Steps to reproduce
- [ ] Priority level
- [ ] Root cause (if known)
- [ ] Word limit: ≤200 words

### 3. Feature Template
- [ ] Full EARS notation
- [ ] BDD scenarios
- [ ] User stories
- [ ] Non-functional requirements
- [ ] Word limit: ≤800 words

### 4. Refactor Template
- [ ] Current architecture
- [ ] Design goals
- [ ] Constraints/requirements
- [ ] Success criteria
- [ ] Word limit: ≤500 words

### 5. Documentation Template
- [ ] Target audience
- [ ] Documentation format
- [ ] Key sections/examples
- [ ] Success criteria
- [ ] Word limit: ≤400 words

### 6. Performance Template
- [ ] Current performance metrics
- [ ] Target performance metrics
- [ ] Bottlenecks identified
- [ ] Success criteria
- [ ] Word limit: ≤300 words

### 7. Security Template
- [ ] Vulnerability description
- [ ] Threat model
- [ ] Mitigation strategy
- [ ] Acceptance criteria
- [ ] Word limit: ≤400 words

## Implementation Plan

### Phase 1: Template Data Models (2 hours)
```python
# File: installer/global/commands/lib/requirement_templates/__init__.py

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TemplateQuestion:
    id: str
    text: str
    required: bool = True
    multiline: bool = False
    examples: List[str] = None

@dataclass
class RequirementTemplate:
    type: str
    name: str
    description: str
    word_limit: int
    questions: List[TemplateQuestion]
    output_format: str

    def generate_requirement(self, answers: Dict[str, str]) -> str:
        """Generate requirement from template and answers."""
        return self.output_format.format(**answers)
```

### Phase 2: Bug Fix Template (1 hour)
```json
// File: installer/global/commands/lib/requirement_templates/bug-fix.json

{
  "type": "bug-fix",
  "name": "Bug Fix",
  "description": "Minimal specification for bug fixes",
  "word_limit": 200,
  "questions": [
    {
      "id": "bug_description",
      "text": "What is the bug?",
      "required": true,
      "examples": ["User can't log in with valid credentials", "Payment fails on checkout"]
    },
    {
      "id": "expected_behavior",
      "text": "What is the expected behavior?",
      "required": true,
      "examples": ["User should receive JWT token and be logged in"]
    },
    {
      "id": "actual_behavior",
      "text": "What is the actual behavior?",
      "required": true,
      "examples": ["User receives 'Invalid credentials' error even with correct password"]
    },
    {
      "id": "steps_to_reproduce",
      "text": "Steps to reproduce?",
      "required": true,
      "multiline": true,
      "examples": ["1. Navigate to /login\\n2. Enter valid email and password\\n3. Click Login\\n4. Observe error"]
    },
    {
      "id": "priority",
      "text": "Priority (low/medium/high/critical)?",
      "required": true,
      "examples": ["high"]
    },
    {
      "id": "root_cause",
      "text": "Root cause (if known)?",
      "required": false,
      "examples": ["Password hashing comparison uses wrong algorithm"]
    }
  ],
  "output_format": "## {requirement_id}: {bug_description}\n\n**Type**: Bug Fix\n**Priority**: {priority}\n**Template**: Minimal Specification\n\n**Current Behavior** (broken):\n  {actual_behavior}\n\n**Expected Behavior** (fixed):\n  {expected_behavior}\n\n**Steps to Reproduce**:\n{steps_to_reproduce}\n\n**Root Cause** (if known):\n  {root_cause}\n\n**Acceptance Criteria**:\n  ✅ Bug is fixed and behavior matches expected\n  ✅ No regression in related functionality\n  ✅ Tests added to prevent recurrence"
}
```

### Phase 3: Feature Template (1 hour)
```json
// File: installer/global/commands/lib/requirement_templates/feature.json

{
  "type": "feature",
  "name": "Feature",
  "description": "Comprehensive specification for new features",
  "word_limit": 800,
  "questions": [
    {
      "id": "feature_purpose",
      "text": "What is the main purpose/goal of this feature?",
      "required": true,
      "multiline": true
    },
    {
      "id": "target_users",
      "text": "Who are the primary users?",
      "required": true
    },
    {
      "id": "problem_solved",
      "text": "What problem does this solve?",
      "required": true,
      "multiline": true
    },
    {
      "id": "key_capabilities",
      "text": "What are the key capabilities needed?",
      "required": true,
      "multiline": true
    },
    {
      "id": "constraints",
      "text": "What are the constraints or non-functional requirements?",
      "required": false,
      "multiline": true
    },
    {
      "id": "success_criteria",
      "text": "How will success be measured?",
      "required": true,
      "multiline": true
    }
  ],
  "output_format": "## {requirement_id}: {feature_title}\n\n**Type**: Feature\n**Template**: Comprehensive Specification\n\n**Purpose/Goal**:\n{feature_purpose}\n\n**Target Users**:\n{target_users}\n\n**Problem Solved**:\n{problem_solved}\n\n**Key Capabilities**:\n{key_capabilities}\n\n**Constraints**:\n{constraints}\n\n**Success Criteria**:\n{success_criteria}\n\n**EARS Notation** (to be formalized):\nWhen [trigger], the system shall [response]\n\n**BDD Scenarios** (to be generated):\nScenarios will be generated via /generate-bdd"
}
```

### Phase 4: Refactor Template (1 hour)
```json
// File: installer/global/commands/lib/requirement_templates/refactor.json

{
  "type": "refactor",
  "name": "Refactor",
  "description": "Architecture-focused specification for refactoring",
  "word_limit": 500,
  "questions": [
    {
      "id": "current_architecture",
      "text": "Describe the current architecture/design",
      "required": true,
      "multiline": true
    },
    {
      "id": "design_goals",
      "text": "What are the design goals of this refactor?",
      "required": true,
      "multiline": true,
      "examples": ["Improve testability", "Reduce coupling", "Improve performance"]
    },
    {
      "id": "constraints",
      "text": "What constraints must be maintained?",
      "required": true,
      "multiline": true,
      "examples": ["Backward compatibility", "No API changes", "Zero downtime"]
    },
    {
      "id": "success_criteria",
      "text": "How will success be measured?",
      "required": true,
      "multiline": true,
      "examples": ["Code coverage >80%", "Cyclomatic complexity <10", "No performance regression"]
    }
  ],
  "output_format": "## {requirement_id}: {refactor_title}\n\n**Type**: Refactor\n**Template**: Architecture-Focused\n\n**Current Architecture**:\n{current_architecture}\n\n**Design Goals**:\n{design_goals}\n\n**Constraints**:\n{constraints}\n\n**Success Criteria**:\n{success_criteria}\n\n**Acceptance Criteria**:\n  ✅ All tests pass after refactor\n  ✅ No functional changes (behavior preserved)\n  ✅ Design goals achieved\n  ✅ Constraints respected"
}
```

### Phase 5: Documentation, Performance, Security Templates (1.5 hours)
```json
// File: installer/global/commands/lib/requirement_templates/documentation.json
{
  "type": "documentation",
  "name": "Documentation",
  "description": "User-centric specification for documentation",
  "word_limit": 400,
  "questions": [
    {
      "id": "target_audience",
      "text": "Who is the target audience?",
      "required": true,
      "examples": ["Developers", "End users", "System administrators"]
    },
    {
      "id": "documentation_format",
      "text": "What format should the documentation be in?",
      "required": true,
      "examples": ["Markdown guide", "API reference", "Tutorial", "FAQ"]
    },
    {
      "id": "key_sections",
      "text": "What are the key sections or topics to cover?",
      "required": true,
      "multiline": true
    },
    {
      "id": "examples_needed",
      "text": "What examples should be included?",
      "required": false,
      "multiline": true
    }
  ],
  "output_format": "## {requirement_id}: {documentation_title}\n\n**Type**: Documentation\n**Template**: User-Centric\n\n**Target Audience**: {target_audience}\n**Format**: {documentation_format}\n\n**Key Sections**:\n{key_sections}\n\n**Examples**:\n{examples_needed}\n\n**Success Criteria**:\n  ✅ Documentation is clear and concise\n  ✅ All key sections covered\n  ✅ Examples are accurate and helpful\n  ✅ Target audience can understand and use"
}

// File: installer/global/commands/lib/requirement_templates/performance.json
{
  "type": "performance",
  "name": "Performance",
  "description": "Metrics-focused specification for performance improvements",
  "word_limit": 300,
  "questions": [
    {
      "id": "current_metrics",
      "text": "What are the current performance metrics?",
      "required": true,
      "examples": ["API response time: 500ms", "Page load time: 3 seconds"]
    },
    {
      "id": "target_metrics",
      "text": "What are the target performance metrics?",
      "required": true,
      "examples": ["API response time: <100ms", "Page load time: <1 second"]
    },
    {
      "id": "bottlenecks",
      "text": "What bottlenecks have been identified?",
      "required": false,
      "examples": ["Database queries N+1 problem", "Unoptimized image loading"]
    }
  ],
  "output_format": "## {requirement_id}: {performance_title}\n\n**Type**: Performance\n**Template**: Metrics-Focused\n\n**Current Performance**:\n{current_metrics}\n\n**Target Performance**:\n{target_metrics}\n\n**Bottlenecks**:\n{bottlenecks}\n\n**Success Criteria**:\n  ✅ Target metrics achieved\n  ✅ No functional regressions\n  ✅ Performance improvements sustained over time"
}

// File: installer/global/commands/lib/requirement_templates/security.json
{
  "type": "security",
  "name": "Security",
  "description": "Threat-focused specification for security improvements",
  "word_limit": 400,
  "questions": [
    {
      "id": "vulnerability",
      "text": "Describe the vulnerability or security concern",
      "required": true,
      "multiline": true
    },
    {
      "id": "threat_model",
      "text": "What is the threat model?",
      "required": true,
      "multiline": true,
      "examples": ["SQL injection attack", "XSS vulnerability", "Authentication bypass"]
    },
    {
      "id": "mitigation_strategy",
      "text": "What is the mitigation strategy?",
      "required": true,
      "multiline": true,
      "examples": ["Parameterized queries", "Input sanitization", "Multi-factor authentication"]
    }
  ],
  "output_format": "## {requirement_id}: {security_title}\n\n**Type**: Security\n**Template**: Threat-Focused\n\n**Vulnerability**:\n{vulnerability}\n\n**Threat Model**:\n{threat_model}\n\n**Mitigation Strategy**:\n{mitigation_strategy}\n\n**Success Criteria**:\n  ✅ Vulnerability is fixed\n  ✅ Security tests pass\n  ✅ No new vulnerabilities introduced\n  ✅ Complies with security standards (OWASP, etc.)"
}
```

### Phase 6: Command Integration (1.5 hours)
```markdown
# File: installer/global/commands/gather-requirements.md

## Template-Based Requirements Gathering (NEW)

### Usage

```bash
/gather-requirements --type [template-name]
```

### Available Templates

- **bug-fix** (≤200 words): Minimal spec for bug fixes
- **feature** (≤800 words): Comprehensive spec for new features
- **refactor** (≤500 words): Architecture-focused for refactoring
- **documentation** (≤400 words): User-centric for docs
- **performance** (≤300 words): Metrics-focused for performance
- **security** (≤400 words): Threat-focused for security

### Example: Bug Fix Template

```bash
/gather-requirements --type bug-fix

Selected template: Bug Fix (minimal specification)

Q1: What is the bug?
> User can't log in with valid credentials

Q2: What is the expected behavior?
> User should receive JWT token and be logged in

Q3: What is the actual behavior?
> User receives "Invalid credentials" error even with correct password

Q4: Steps to reproduce?
> 1. Navigate to /login
> 2. Enter valid email and password
> 3. Click "Login"
> 4. Observe error message

Q5: Priority (low/medium/high/critical)?
> high

Q6: Root cause (if known)? [optional]
> Password hashing comparison uses wrong algorithm

Generating bug fix requirement...

## REQ-BUG-012: User Can't Log In with Valid Credentials

**Type**: Bug Fix
**Priority**: High
**Template**: Minimal Specification

**Current Behavior** (broken):
  User receives "Invalid credentials" error even with correct password

**Expected Behavior** (fixed):
  User should receive JWT token and be logged in

**Steps to Reproduce**:
  1. Navigate to /login
  2. Enter valid email and password
  3. Click "Login"
  4. Observe error message

**Root Cause** (if known):
  Password hashing comparison uses wrong algorithm

**Acceptance Criteria**:
  ✅ Bug is fixed and behavior matches expected
  ✅ No regression in related functionality
  ✅ Tests added to prevent recurrence

**Word Count**: 89/200 ✅
```
```

### Phase 7: Testing (1 hour)
```python
# File: tests/integration/test_requirement_templates.py

def test_bug_fix_template():
    answers = {
        "requirement_id": "REQ-BUG-001",
        "bug_description": "User can't log in",
        "expected_behavior": "User should be logged in",
        "actual_behavior": "User sees error",
        "steps_to_reproduce": "1. Navigate to /login\\n2. Enter credentials\\n3. Click login",
        "priority": "high",
        "root_cause": "Wrong password algorithm"
    }

    template = load_template("bug-fix")
    requirement = template.generate_requirement(answers)

    assert "REQ-BUG-001" in requirement
    assert "User can't log in" in requirement
    assert "Priority: high" in requirement
    assert len(requirement.split()) < 200  # Word limit check

def test_feature_template():
    # Test feature template with comprehensive spec
    pass

def test_refactor_template():
    # Test refactor template with architecture focus
    pass
```

## Files to Create

### Template Files
- `installer/global/commands/lib/requirement_templates/__init__.py`
- `installer/global/commands/lib/requirement_templates/bug-fix.json`
- `installer/global/commands/lib/requirement_templates/feature.json`
- `installer/global/commands/lib/requirement_templates/refactor.json`
- `installer/global/commands/lib/requirement_templates/documentation.json`
- `installer/global/commands/lib/requirement_templates/performance.json`
- `installer/global/commands/lib/requirement_templates/security.json`

### Test Files
- `tests/unit/test_requirement_templates.py`
- `tests/integration/test_requirement_templates.py`

### Modified Files
- `installer/global/commands/gather-requirements.md` (add --type flag)

## Success Metrics

- **Template Usage**: 80% of requirements use appropriate template
- **Specification Quality**: Improved clarity and appropriate detail level
- **Word Count Reduction**: 40-60% for bug fixes, 20-30% for features
- **Developer Satisfaction**: Faster requirements gathering

## Related Tasks

- TASK-019: Concise Mode for EARS
- TASK-021: Requirement Versioning

## Dependencies

- None (standalone enhancement)

## Notes

- Templates are JSON-based for easy customization
- Teams can create custom templates
- Template selection is optional (standard workflow still available)
- Consider adding template validation and linting
