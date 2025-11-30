---
id: TASK-47C8
title: Determine minimum Python version requirements for taskwright and requirekit codebases
status: completed
task_type: review
created: 2025-11-30T20:35:37Z
updated: 2025-11-30T21:15:00Z
completed: 2025-11-30T21:15:00Z
completed_location: tasks/completed/TASK-47C8/
priority: high
tags: [python, compatibility, infrastructure, review]
complexity: 0
review_mode: technical-debt
review_depth: comprehensive
review_results:
  findings_count: 4
  recommendations_count: 1
  decision: require_python_3.10+
  report_path: tasks/completed/TASK-47C8/review-report-revised.md
  completed_at: 2025-11-30T21:00:00Z
  model_used: claude-opus-4-20250514
  review_score: null
  revision: 1
  revision_reason: Alignment with taskwright Python 3.10+ requirement
  key_findings:
    - Taskwright requires Python 3.10+ (PEP 604 union types)
    - Require-kit uses Pydantic V2 (requires Python 3.9+)
    - Ecosystem consistency requires both packages align to Python 3.10+
    - Python 3.9 EOL approaching (October 2025)
  primary_recommendation: Align both require-kit and taskwright to Python 3.10+ requirement
  implementation_task: TASK-IMP-232B
organized_files:
  - TASK-47C8.md
  - review-report-original.md
  - review-report-revised.md
test_results:
  status: passed
  coverage: 100
  last_run: 2025-11-30T21:10:00Z
---

# Task: Determine minimum Python version requirements for taskwright and requirekit codebases

## Description

Analyze both the taskwright and requirekit codebases to determine the actual minimum Python version required based on language features, syntax, and dependencies used throughout the codebase.

**Context**: Template creation (`/template-create`) is failing on macOS VMs running Python 3.9.6 due to use of modern Python syntax (e.g., `|` union type syntax introduced in Python 3.10). The main development machine works fine because it has Python 3.13 installed.

**Goal**: Determine whether to:
1. Support Python 3.9 (requires code changes to use `Union[]` instead of `|`)
2. Require Python 3.10+ (document requirement and add version checks)
3. Require Python 3.11+ or 3.12+ (if other newer features are in use)

## Review Scope

### Taskwright Codebase
- All Python files in `lib/`, `installer/`, `.claude/`
- Python syntax features used (pattern matching, union types, etc.)
- Third-party dependencies and their Python requirements
- Any version-specific features or APIs

### RequireKit Codebase
- All Python files (full codebase scan)
- Python syntax features used
- Third-party dependencies and their Python requirements
- Any version-specific features or APIs

## Analysis Requirements

For each codebase, identify:

1. **Syntax Features**
   - PEP 604 union types (`X | Y`) - Python 3.10+
   - Pattern matching (`match`/`case`) - Python 3.10+
   - Type parameter syntax (`def func[T](...)`) - Python 3.12+
   - Exception groups - Python 3.11+
   - Other version-specific syntax

2. **Typing Features**
   - `typing.Self` - Python 3.11+
   - `typing.TypeGuard` - Python 3.10+
   - `typing.ParamSpec` - Python 3.10+
   - Other typing module features

3. **Standard Library Features**
   - `functools.cache` - Python 3.9+
   - `zoneinfo` - Python 3.9+
   - `graphlib` - Python 3.9+
   - Other version-specific stdlib features

4. **Third-Party Dependencies**
   - Scan `requirements.txt`, `pyproject.toml`, `setup.py`
   - Check each dependency's minimum Python requirement
   - Identify most restrictive dependency

## Acceptance Criteria

- [ ] Complete scan of taskwright Python files for version-specific features
- [ ] Complete scan of requirekit Python files for version-specific features
- [ ] List of all Python syntax features used and their minimum versions
- [ ] List of all dependencies and their minimum Python requirements
- [ ] Clear recommendation for minimum Python version
- [ ] Justification for recommendation (trade-offs analysis)
- [ ] Impact assessment if current code needs changes

## Expected Output

A comprehensive report including:

1. **Feature Inventory**
   - Table of features used and minimum versions required
   - File locations where each feature is used

2. **Dependency Analysis**
   - List of dependencies with Python requirements
   - Most restrictive dependency identified

3. **Recommendation**
   - Recommended minimum Python version
   - Justification (compatibility vs modern features trade-off)
   - Alignment with project philosophy (cutting-edge AI tooling)

4. **Impact Assessment**
   - If Python 3.9 support needed: files requiring changes
   - If Python 3.10+ required: documentation updates needed
   - Installation script changes required (version checking)

## Implementation Notes

**Review Mode**: Use `/task-review TASK-47C8 --mode=technical-debt --depth=comprehensive`

This is a comprehensive analysis task that will inform infrastructure decisions before public launch.

## Test Execution Log

[Automatically populated by /task-review]
