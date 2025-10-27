---
id: TASK-024
title: Add Compliance Scorecard to Task Completion
status: backlog
priority: low
created: 2025-10-16T11:05:00Z
labels: [enhancement, sdd-alignment, quality, compliance]
estimated_effort: 12-16 hours
complexity_estimate: 7

# Source
source: spectrum-driven-development-analysis.md
recommendation: Priority 3 - High Impact, High Effort
sdd_alignment: Quality Enhancement

# Requirements
requirements:
  - REQ-SDD-019: Quantify requirement compliance
  - REQ-SDD-020: Measure scope creep percentage
  - REQ-SDD-021: Provide compliance scoring
---

# Add Compliance Scorecard to Task Completion

## Problem Statement

No quantitative measure of requirement compliance at task completion. Developers don't know if implementation fully matches requirements or contains scope creep.

## Solution Overview

Add compliance analysis to `/task-complete` command that:
- Measures requirements coverage (% implemented)
- Detects scope creep (% beyond requirements)
- Calculates test coverage of requirements
- Provides overall compliance score (0-100)
- Offers interactive remediation options

## Acceptance Criteria

### 1. Requirements Coverage Analysis
- [ ] Parse all requirements linked to task
- [ ] Verify each requirement is implemented
- [ ] Report coverage: X% (target: 100%)
- [ ] List missing requirements (if any)

### 2. Scope Creep Detection
- [ ] Identify code not linked to requirements
- [ ] Calculate scope creep percentage
- [ ] Flag unspecified features
- [ ] Report: Y% scope creep (target: 0%)

### 3. Test Coverage of Requirements
- [ ] Map tests to requirements
- [ ] Calculate requirement test coverage
- [ ] Report: Z% requirements tested (target: 100%)
- [ ] Identify untested requirements

### 4. Compliance Scoring
- [ ] Requirements Implemented: X/100
- [ ] Scope Creep: -Y points
- [ ] Test Coverage: Z/100
- [ ] Quality Gates: Pass/Fail
- [ ] Overall Compliance: Total/100

### 5. Interactive Remediation
- [ ] [A]pprove & Complete (if compliance ≥90)
- [ ] [F]ix Scope Creep (remove unspecified features)
- [ ] [C]reate Requirements (approve scope creep)
- [ ] [B]lock (if compliance <60)

## Implementation Plan

### Phase 1: Compliance Data Model (2 hours)
```python
# File: installer/global/commands/lib/compliance_scorer.py

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class RequirementCoverage:
    requirement_id: str
    requirement_text: str
    implemented: bool
    implementation_location: str  # File:line
    test_coverage: bool
    tests: List[str]

@dataclass
class ScopeCreepItem:
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    estimated_lines: int

@dataclass
class ComplianceScorecard:
    task_id: str
    requirements_total: int
    requirements_implemented: int
    requirements_coverage_pct: float
    scope_creep_items: List[ScopeCreepItem]
    scope_creep_pct: float
    test_coverage_pct: float
    quality_gates_passed: bool
    overall_compliance_score: int

    def display(self):
        """Display compliance scorecard."""
        print(f"""
Compliance Scorecard
═══════════════════════════════════════════════════════

Requirements Coverage
  ✅ REQ-042.1: JWT token generation (Implemented: AuthService.cs:42)
  ✅ REQ-042.2: 24-hour expiration (Implemented: TokenConfig.cs:15)
  ✅ REQ-042.3: User claims (Implemented: AuthService.cs:45-46)
  ✅ REQ-042.4: HS256 signature (Implemented: AuthService.cs:50)
  ✅ REQ-042.5: Logging (Implemented: Logger.cs:89)

  Requirements Implemented: {self.requirements_coverage_pct}% ({self.requirements_implemented}/{self.requirements_total}) ✅

Scope Creep Analysis
  ❌ Token refresh mechanism (AuthService.cs:67)
     - Not in requirements
     - 34 lines of code
     - Action: Create REQ-043 or remove

  ❌ Rate limiting middleware (Startup.cs:34)
     - Not in requirements
     - 28 lines of code
     - Action: Create REQ-044 or remove

  Implementation Beyond Requirements: {self.scope_creep_pct}% ⚠️

Test Coverage
  ✅ Unit tests cover all requirements: 98% (18/18 tests passing)
  ✅ BDD scenarios executed: 100% (5/5 scenarios passing)
  ✅ Integration tests: 100% (3/3 tests passing)

  Test Coverage of Requirements: {self.test_coverage_pct}% ✅

Quality Metrics
  ✅ Code quality: 92/100 (SonarQube)
  ✅ Security scan: No vulnerabilities
  ✅ Performance: All endpoints <100ms
  ✅ Architectural review: 85/100

Overall Compliance Score
═══════════════════════════════════════════════════════
  Requirements Coverage:        {self.requirements_coverage_pct}% ✅
  Scope Creep:                   -{self.scope_creep_pct}% ⚠️
  Test Coverage:                 {self.test_coverage_pct}% ✅
  Quality Gates:                100% ✅

  TOTAL COMPLIANCE: {self.overall_compliance_score}/100 {'✅' if self.overall_compliance_score >= 90 else '⚠️'}

Recommendations:
  1. Create REQ-043 for token refresh (or remove feature)
  2. Create REQ-044 for rate limiting (or remove feature)
  3. Add integration test for claim validation (improve to 100%)
""")
```

### Phase 2: Requirements Coverage Analysis (3 hours)
```python
# File: installer/global/commands/lib/requirement_coverage_analyzer.py

import ast
import re
from pathlib import Path
from typing import List, Tuple

class RequirementCoverageAnalyzer:
    def analyze_coverage(self, task_id: str) -> List[RequirementCoverage]:
        """Analyze implementation coverage of requirements."""

        # Load requirements
        requirements = self.load_requirements(task_id)

        # Get implementation files
        impl_files = self.get_implementation_files(task_id)

        # Map requirements to implementation
        coverage = []
        for req in requirements:
            impl_location = self.find_implementation(req, impl_files)
            tests = self.find_tests_for_requirement(req)

            coverage.append(RequirementCoverage(
                requirement_id=req.id,
                requirement_text=req.text,
                implemented=impl_location is not None,
                implementation_location=impl_location or "NOT FOUND",
                test_coverage=len(tests) > 0,
                tests=tests
            ))

        return coverage

    def find_implementation(self, requirement, impl_files: List[Path]) -> str:
        """Find where requirement is implemented."""

        # Strategy 1: Look for requirement ID in comments
        for file in impl_files:
            content = file.read_text()
            if requirement.id in content:
                # Find line number
                for i, line in enumerate(content.split('\n'), 1):
                    if requirement.id in line:
                        return f"{file.name}:{i}"

        # Strategy 2: Semantic search for requirement keywords
        keywords = self.extract_keywords(requirement.text)
        for file in impl_files:
            content = file.read_text()
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    # Found potential implementation
                    return f"{file.name} (semantic match)"

        return None

    def extract_keywords(self, requirement_text: str) -> List[str]:
        """Extract key terms from requirement."""
        # Extract action verbs and nouns
        words = requirement_text.lower().split()
        keywords = [w for w in words if len(w) > 4 and w not in ['shall', 'system', 'should']]
        return keywords[:5]  # Top 5 keywords
```

### Phase 3: Scope Creep Detection (3 hours)
```python
# File: installer/global/commands/lib/scope_creep_detector.py

class ScopeCreepDetector:
    def detect_scope_creep(
        self,
        task_id: str,
        requirements: List[Requirement],
        impl_files: List[Path]
    ) -> List[ScopeCreepItem]:
        """Detect code not linked to any requirement."""

        scope_creep_items = []

        for file in impl_files:
            content = file.read_text()

            # Parse code (language-specific)
            if file.suffix == '.py':
                creep = self._detect_python_scope_creep(file, content, requirements)
            elif file.suffix in ['.cs', '.java']:
                creep = self._detect_csharp_scope_creep(file, content, requirements)
            elif file.suffix in ['.js', '.ts']:
                creep = self._detect_javascript_scope_creep(file, content, requirements)
            else:
                creep = []

            scope_creep_items.extend(creep)

        return scope_creep_items

    def _detect_python_scope_creep(
        self,
        file: Path,
        content: str,
        requirements: List[Requirement]
    ) -> List[ScopeCreepItem]:
        """Detect scope creep in Python code."""

        creep_items = []
        tree = ast.parse(content)

        # Check each function/method
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function is linked to requirement
                if not self._is_linked_to_requirement(node, requirements, content):
                    # Potential scope creep
                    creep_items.append(ScopeCreepItem(
                        file_path=str(file),
                        line_number=node.lineno,
                        code_snippet=ast.get_source_segment(content, node)[:100],
                        description=f"Function '{node.name}' not linked to any requirement",
                        estimated_lines=self._count_lines(node)
                    ))

        return creep_items

    def _is_linked_to_requirement(
        self,
        node: ast.AST,
        requirements: List[Requirement],
        content: str
    ) -> bool:
        """Check if code node is linked to a requirement."""

        # Strategy 1: Check for requirement ID in comments/docstrings
        if hasattr(node, 'body') and node.body:
            first_stmt = node.body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Str):
                docstring = first_stmt.value.s
                for req in requirements:
                    if req.id in docstring:
                        return True

        # Strategy 2: Check for [GENERATED] annotation with requirement ID
        source_segment = ast.get_source_segment(content, node)
        for req in requirements:
            if f"[GENERATED] From {req.id}" in source_segment:
                return True

        # Strategy 3: Semantic match with requirement keywords
        for req in requirements:
            keywords = self.extract_keywords(req.text)
            for keyword in keywords:
                if keyword.lower() in ast.get_source_segment(content, node).lower():
                    return True  # Likely linked

        return False  # Not linked to any requirement
```

### Phase 4: Test Coverage Analysis (2 hours)
```python
# File: installer/global/commands/lib/test_coverage_analyzer.py

class TestCoverageAnalyzer:
    def analyze_test_coverage(
        self,
        requirements: List[Requirement],
        test_files: List[Path]
    ) -> Dict[str, List[str]]:
        """Map tests to requirements."""

        requirement_tests = {}

        for req in requirements:
            tests = self.find_tests_for_requirement(req, test_files)
            requirement_tests[req.id] = tests

        return requirement_tests

    def find_tests_for_requirement(
        self,
        requirement: Requirement,
        test_files: List[Path]
    ) -> List[str]:
        """Find tests that cover a specific requirement."""

        tests = []

        for test_file in test_files:
            content = test_file.read_text()

            # Strategy 1: Look for requirement ID in test names/comments
            if requirement.id in content:
                # Extract test names
                test_names = self._extract_test_names(test_file, content)
                tests.extend([f"{test_file.name}::{test}" for test in test_names])

            # Strategy 2: Semantic match with requirement keywords
            keywords = self.extract_keywords(requirement.text)
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    test_names = self._extract_test_names(test_file, content)
                    tests.extend([f"{test_file.name}::{test}" for test in test_names if keyword.lower() in test.lower()])

        return list(set(tests))  # Deduplicate

    def _extract_test_names(self, test_file: Path, content: str) -> List[str]:
        """Extract test function/method names from test file."""

        if test_file.suffix == '.py':
            return self._extract_python_test_names(content)
        elif test_file.suffix in ['.cs']:
            return self._extract_csharp_test_names(content)
        elif test_file.suffix in ['.js', '.ts']:
            return self._extract_javascript_test_names(content)
        return []

    def _extract_python_test_names(self, content: str) -> List[str]:
        """Extract Python test names (functions starting with test_)."""
        tree = ast.parse(content)
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
```

### Phase 5: Compliance Scoring (2 hours)
```python
# File: installer/global/commands/lib/compliance_scorer.py

class ComplianceScorer:
    def calculate_compliance(
        self,
        task_id: str,
        requirements_coverage: List[RequirementCoverage],
        scope_creep_items: List[ScopeCreepItem],
        total_lines: int
    ) -> ComplianceScorecard:
        """Calculate overall compliance score."""

        # Requirements coverage
        requirements_implemented = sum(1 for r in requirements_coverage if r.implemented)
        requirements_total = len(requirements_coverage)
        requirements_coverage_pct = (requirements_implemented / requirements_total * 100) if requirements_total > 0 else 0

        # Scope creep
        scope_creep_lines = sum(item.estimated_lines for item in scope_creep_items)
        scope_creep_pct = (scope_creep_lines / total_lines * 100) if total_lines > 0 else 0

        # Test coverage
        requirements_tested = sum(1 for r in requirements_coverage if r.test_coverage)
        test_coverage_pct = (requirements_tested / requirements_total * 100) if requirements_total > 0 else 0

        # Quality gates (from existing system)
        quality_gates_passed = self.check_quality_gates(task_id)

        # Overall compliance
        overall_score = int(
            (requirements_coverage_pct * 0.4) +  # 40% weight
            (max(0, 100 - scope_creep_pct) * 0.3) +  # 30% weight
            (test_coverage_pct * 0.2) +  # 20% weight
            (100 if quality_gates_passed else 0) * 0.1  # 10% weight
        )

        return ComplianceScorecard(
            task_id=task_id,
            requirements_total=requirements_total,
            requirements_implemented=requirements_implemented,
            requirements_coverage_pct=requirements_coverage_pct,
            scope_creep_items=scope_creep_items,
            scope_creep_pct=scope_creep_pct,
            test_coverage_pct=test_coverage_pct,
            quality_gates_passed=quality_gates_passed,
            overall_compliance_score=overall_score
        )
```

### Phase 6: Interactive Remediation (2 hours)
```python
# File: installer/global/commands/lib/compliance_remediator.py

class ComplianceRemediator:
    def handle_compliance(self, scorecard: ComplianceScorecard):
        """Handle compliance results with interactive remediation."""

        scorecard.display()

        if scorecard.overall_compliance_score >= 90:
            choice = input("\n[A]pprove & Complete  [V]iew Details  [C]ancel\nYour choice: ")
        elif scorecard.overall_compliance_score >= 60:
            choice = input("\n[A]pprove & Complete  [F]ix Scope Creep  [C]reate Requirements  [C]ancel\nYour choice: ")
        else:
            print("\n⚠️  Compliance too low (<60). Task cannot be completed.")
            choice = input("\n[F]ix Scope Creep  [C]reate Requirements  [B]lock Task  [C]ancel\nYour choice: ")

        if choice.upper() == 'A':
            self.approve_and_complete(scorecard.task_id)
        elif choice.upper() == 'F':
            self.fix_scope_creep(scorecard.scope_creep_items)
        elif choice.upper() == 'C' and "Create" in choice:
            self.create_requirements_for_scope_creep(scorecard.scope_creep_items)
        elif choice.upper() == 'B':
            self.block_task(scorecard.task_id, "Compliance too low")
        elif choice.upper() == 'V':
            self.view_details(scorecard)

    def fix_scope_creep(self, scope_creep_items: List[ScopeCreepItem]):
        """Remove scope creep from implementation."""
        for item in scope_creep_items:
            print(f"\nRemoving scope creep: {item.description}")
            # Remove code from file
            self.remove_code_block(item.file_path, item.line_number, item.estimated_lines)

        print(f"\n✅ Removed {len(scope_creep_items)} scope creep items")

    def create_requirements_for_scope_creep(self, scope_creep_items: List[ScopeCreepItem]):
        """Create new requirements for scope creep features."""
        for item in scope_creep_items:
            print(f"\nCreating requirement for: {item.description}")
            # Auto-generate requirement draft
            req_id = self.create_requirement_draft(item)
            print(f"  Created: {req_id}")

        print(f"\n✅ Created {len(scope_creep_items)} requirement drafts")
```

### Phase 7: Integration with Task Complete (2 hours)
```markdown
# File: installer/global/commands/task-complete.md

## Compliance Analysis (NEW)

Before completing task, run compliance analysis:

1. **Requirements Coverage Analysis**
   - Verify all requirements implemented
   - Report coverage percentage

2. **Scope Creep Detection**
   - Identify unspecified features
   - Calculate scope creep percentage

3. **Test Coverage Analysis**
   - Map tests to requirements
   - Report test coverage percentage

4. **Compliance Scoring**
   - Calculate overall compliance score
   - Display scorecard

5. **Interactive Remediation**
   - If compliance ≥90: Approve & Complete
   - If compliance 60-89: Fix Scope Creep or Create Requirements
   - If compliance <60: Block task until fixed

**Example**:
```bash
/task-complete TASK-042 --interactive

Running compliance analysis...

[Compliance Scorecard displayed]

Overall Compliance: 98/100 ✅

[A]pprove & Complete  [V]iew Details  [C]ancel
Your choice: A

✅ Task TASK-042 completed with 98/100 compliance
```
```

### Phase 8: Testing (2 hours)
```python
# File: tests/integration/test_compliance_scoring.py

def test_full_compliance():
    # Task with 100% requirements coverage, 0% scope creep
    task = create_test_task_with_full_compliance()

    scorecard = ComplianceScorer().calculate_compliance(
        task.id,
        task.requirements_coverage,
        [],  # No scope creep
        1000  # Total lines
    )

    assert scorecard.requirements_coverage_pct == 100
    assert scorecard.scope_creep_pct == 0
    assert scorecard.overall_compliance_score >= 95

def test_scope_creep_detection():
    # Task with scope creep
    task = create_test_task_with_scope_creep()

    scorecard = ComplianceScorer().calculate_compliance(
        task.id,
        task.requirements_coverage,
        [ScopeCreepItem(...)],  # 20% scope creep
        1000
    )

    assert scorecard.scope_creep_pct > 0
    assert scorecard.overall_compliance_score < 90

def test_remediation_workflow():
    # Test fixing scope creep
    scorecard = ComplianceScorecard(...)
    remediator = ComplianceRemediator()

    # Simulate fixing scope creep
    remediator.fix_scope_creep(scorecard.scope_creep_items)

    # Recalculate compliance
    new_scorecard = ComplianceScorer().calculate_compliance(...)
    assert new_scorecard.scope_creep_pct == 0
    assert new_scorecard.overall_compliance_score >= 90
```

## Files to Create/Modify

### New Files
- `installer/global/commands/lib/compliance_scorer.py`
- `installer/global/commands/lib/requirement_coverage_analyzer.py`
- `installer/global/commands/lib/scope_creep_detector.py`
- `installer/global/commands/lib/test_coverage_analyzer.py`
- `installer/global/commands/lib/compliance_remediator.py`
- `tests/unit/test_compliance_scorer.py`
- `tests/integration/test_compliance_scoring.py`

### Modified Files
- `installer/global/commands/task-complete.md` (add compliance analysis)
- `installer/global/agents/code-reviewer.md` (integrate compliance scoring)

## Success Metrics

- **Compliance Detection Accuracy**: ≥95% correct detection
- **Scope Creep Identification**: ≥90% accuracy
- **Remediation Success Rate**: ≥80% tasks fixed via remediation
- **Developer Satisfaction**: Improved quality awareness

## Related Tasks

- TASK-018: Spec Drift Detection (shares scope creep logic)
- TASK-023: Spec Regeneration (uses compliance scoring)

## Dependencies

- None (standalone enhancement, but complements TASK-018)

## Notes

- Compliance scoring is quantitative (0-100 scale)
- Thresholds: ≥90 (excellent), 60-89 (acceptable), <60 (blocked)
- Scope creep detection uses AST analysis and semantic matching
- Consider language-specific parsers for better accuracy
- Integration with SonarQube/CodeClimate for code quality metrics
