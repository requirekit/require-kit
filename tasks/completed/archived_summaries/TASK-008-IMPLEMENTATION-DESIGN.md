# TASK-008: Python Implementation Design
## Feature-Generate-Tasks Enhancement for Complexity Control

**Document Version:** 1.0
**Date:** 2025-10-11
**Status:** Design Phase (Phase 2)

---

## Executive Summary

This document defines the comprehensive Python implementation approach for enhancing `/feature-generate-tasks` with complexity-based task breakdown. The design leverages existing complexity evaluation modules from TASK-005/006 and integrates 4 breakdown strategies to prevent task explosion while maintaining implementation quality.

**Key Design Principles:**
- ✅ **Reuse existing complexity infrastructure** (complexity_calculator.py, complexity_factors.py, complexity_models.py)
- ✅ **Modular architecture** with clear separation of concerns
- ✅ **Performance target**: < 30 seconds for 20 tasks
- ✅ **Test coverage**: ≥ 80% line coverage
- ✅ **Type safety**: Comprehensive type hints throughout
- ✅ **Error resilience**: Graceful degradation on failures

---

## 1. Module Architecture

### 1.1 Existing Modules (REUSE)

#### `/installer/global/commands/lib/complexity_calculator.py`
**Purpose:** Core complexity calculation engine
**Reuse Strategy:** Import and use `ComplexityCalculator` class directly
**Key Classes:**
- `ComplexityCalculator`: Main calculation orchestrator
- Score aggregation (1-10 scale)
- Review mode determination (AUTO_PROCEED, QUICK_OPTIONAL, FULL_REQUIRED)

**Integration Point:**
```python
from installer.global.commands.lib.complexity_calculator import ComplexityCalculator
from installer.global.commands.lib.complexity_models import EvaluationContext, ImplementationPlan
from installer.global.commands.lib.complexity_factors import DEFAULT_FACTORS
```

#### `/installer/global/commands/lib/complexity_factors.py`
**Purpose:** Individual complexity scoring factors
**Reuse Strategy:** Use DEFAULT_FACTORS (3 core factors)
**Key Factors:**
- `FileComplexityFactor`: 0-3 points based on file count
- `PatternFamiliarityFactor`: 0-2 points based on design patterns
- `RiskLevelFactor`: 0-3 points based on risk indicators

#### `/installer/global/commands/lib/complexity_models.py`
**Purpose:** Type-safe data models
**Reuse Strategy:** Extend with new models for task breakdown
**Key Models:**
- `ComplexityScore`: Aggregate score with metadata
- `FactorScore`: Individual factor results
- `ImplementationPlan`: Parsed plan structure
- `EvaluationContext`: Evaluation context container

### 1.2 New Modules (CREATE)

#### `/installer/global/commands/lib/task_breakdown.py`
**Purpose:** Core task breakdown logic with 4 strategies
**Estimated LOC:** 400-500 lines
**Key Classes:**

```python
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class BreakdownStrategy(Enum):
    """Task breakdown strategies based on complexity."""
    NO_BREAKDOWN = "no_breakdown"           # Score 1-3: Keep as single task
    LOGICAL_UNITS = "logical_units"         # Score 4-6: Break by logical components
    FILE_BASED = "file_based"               # Score 7-8: One sub-task per file group
    PHASE_BASED = "phase_based"             # Score 9-10: Break by implementation phases

@dataclass(frozen=True)
class SubTask:
    """Represents a generated sub-task."""
    sub_task_id: str                        # e.g., TASK-001.2.05.A
    title: str
    description: str
    complexity_score: int                   # 1-10 scale
    estimated_duration: str                 # e.g., "2-3 hours"
    dependencies: List[str]                 # List of sub-task IDs
    files: List[str]                        # Files involved
    type: str                               # 'ui', 'api', 'test', 'doc'

@dataclass
class BreakdownResult:
    """Result of task breakdown analysis."""
    original_task_id: str
    original_complexity: int
    strategy_used: BreakdownStrategy
    sub_tasks: List[SubTask]
    breakdown_justification: str
    statistics: Dict[str, Any]              # avg complexity, distribution

class TaskBreakdownEngine:
    """Orchestrates task breakdown based on complexity scores."""

    def __init__(self, complexity_calculator: ComplexityCalculator):
        self.complexity_calculator = complexity_calculator
        self.strategy_selector = BreakdownStrategySelector()

    def analyze_and_breakdown(
        self,
        task_id: str,
        task_description: str,
        implementation_plan: ImplementationPlan,
        context: EvaluationContext
    ) -> BreakdownResult:
        """
        Analyze task complexity and apply appropriate breakdown strategy.

        Flow:
        1. Calculate complexity score
        2. Select breakdown strategy
        3. Apply strategy to generate sub-tasks
        4. Calculate statistics
        5. Return structured result
        """
        pass
```

#### `/installer/global/commands/lib/breakdown_strategies.py`
**Purpose:** Implementation of 4 breakdown strategies
**Estimated LOC:** 500-600 lines
**Key Classes:**

```python
from abc import ABC, abstractmethod
from typing import List, Protocol

class BreakdownStrategyProtocol(Protocol):
    """Protocol for breakdown strategy implementations."""

    def can_handle(self, complexity_score: int) -> bool:
        """Check if this strategy handles the given complexity."""
        ...

    def breakdown(
        self,
        task_id: str,
        implementation_plan: ImplementationPlan,
        context: EvaluationContext
    ) -> List[SubTask]:
        """Execute breakdown strategy."""
        ...

class NoBreakdownStrategy:
    """Strategy for simple tasks (score 1-3) - no breakdown needed."""

    SCORE_RANGE = (1, 3)

    def can_handle(self, complexity_score: int) -> bool:
        return self.SCORE_RANGE[0] <= complexity_score <= self.SCORE_RANGE[1]

    def breakdown(self, task_id: str, plan: ImplementationPlan,
                  context: EvaluationContext) -> List[SubTask]:
        """Return empty list - task stays as-is."""
        return []

class LogicalUnitsStrategy:
    """Strategy for moderate tasks (score 4-6) - break by logical components."""

    SCORE_RANGE = (4, 6)

    def breakdown(self, task_id: str, plan: ImplementationPlan,
                  context: EvaluationContext) -> List[SubTask]:
        """
        Break into logical units:
        1. Parse implementation plan for logical components
        2. Identify: Setup, Core Logic, Error Handling, Testing
        3. Generate sub-tasks maintaining dependencies
        """
        pass

class FileBasedStrategy:
    """Strategy for complex tasks (score 7-8) - one sub-task per file group."""

    SCORE_RANGE = (7, 8)

    def breakdown(self, task_id: str, plan: ImplementationPlan,
                  context: EvaluationContext) -> List[SubTask]:
        """
        Break by file groups:
        1. Group related files (e.g., model + service + tests)
        2. Create sub-task per group
        3. Maintain file dependencies
        """
        pass

class PhaseBasedStrategy:
    """Strategy for very complex tasks (score 9-10) - break by phases."""

    SCORE_RANGE = (9, 10)

    def breakdown(self, task_id: str, plan: ImplementationPlan,
                  context: EvaluationContext) -> List[SubTask]:
        """
        Break by implementation phases:
        1. Phase 1: Data models and interfaces
        2. Phase 2: Core business logic
        3. Phase 3: Integration and error handling
        4. Phase 4: Testing and documentation
        """
        pass

class BreakdownStrategySelector:
    """Selects appropriate strategy based on complexity score."""

    def __init__(self):
        self.strategies = [
            NoBreakdownStrategy(),
            LogicalUnitsStrategy(),
            FileBasedStrategy(),
            PhaseBasedStrategy()
        ]

    def select_strategy(self, complexity_score: int) -> BreakdownStrategyProtocol:
        """Select strategy based on score."""
        for strategy in self.strategies:
            if strategy.can_handle(complexity_score):
                return strategy
        raise ValueError(f"No strategy for complexity score: {complexity_score}")
```

#### `/installer/global/commands/lib/duplicate_detector.py`
**Purpose:** Detect duplicate tasks before creation
**Estimated LOC:** 150-200 lines
**Key Classes:**

```python
from dataclasses import dataclass
from typing import List, Set, Optional
import difflib

@dataclass
class DuplicateMatch:
    """Represents a potential duplicate task."""
    task_id: str
    similarity_score: float                 # 0.0-1.0
    matching_fields: List[str]              # ['title', 'description', 'files']
    reason: str

class DuplicateDetector:
    """Detects potential duplicate tasks using similarity analysis."""

    SIMILARITY_THRESHOLD = 0.85             # 85% similarity = potential duplicate
    TITLE_WEIGHT = 0.4
    DESCRIPTION_WEIGHT = 0.3
    FILES_WEIGHT = 0.3

    def __init__(self):
        self.existing_tasks = self._load_existing_tasks()

    def check_for_duplicates(
        self,
        proposed_task: SubTask,
        existing_tasks: List[SubTask]
    ) -> Optional[DuplicateMatch]:
        """
        Check if proposed task duplicates an existing task.

        Algorithm:
        1. Compare title similarity (Levenshtein distance)
        2. Compare description similarity (TF-IDF cosine similarity)
        3. Compare file overlap (Jaccard index)
        4. Aggregate weighted score
        5. Return match if above threshold
        """
        pass

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate title similarity using SequenceMatcher."""
        return difflib.SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

    def _calculate_file_overlap(self, files1: List[str], files2: List[str]) -> float:
        """Calculate Jaccard index for file lists."""
        set1, set2 = set(files1), set(files2)
        if not set1 and not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
```

#### `/installer/global/commands/lib/visualization.py`
**Purpose:** Terminal output formatting and visualization
**Estimated LOC:** 200-250 lines
**Key Classes:**

```python
from typing import List, Dict
from enum import Enum

class ComplexityColor(Enum):
    """Terminal color codes for complexity visualization."""
    LOW = "\033[92m"        # Green (1-3)
    MEDIUM = "\033[93m"     # Yellow (4-6)
    HIGH = "\033[91m"       # Red (7-10)
    RESET = "\033[0m"

class TaskVisualization:
    """Handles terminal output formatting."""

    def display_breakdown_result(self, result: BreakdownResult) -> None:
        """
        Display formatted breakdown result with:
        - Original task info
        - Complexity score with color coding
        - Strategy used
        - Generated sub-tasks (hierarchical)
        - Statistics summary
        """
        pass

    def display_complexity_distribution(
        self,
        sub_tasks: List[SubTask]
    ) -> None:
        """
        Display ASCII bar chart of complexity distribution:

        Complexity Distribution:
        🟢 Low (1-3):    ████████ 40% (4 tasks)
        🟡 Medium (4-6): ████████████ 50% (5 tasks)
        🔴 High (7-10):  ██ 10% (1 task)

        Average Complexity: 4.2
        """
        pass

    def format_sub_task_tree(self, sub_tasks: List[SubTask]) -> str:
        """
        Format sub-tasks as dependency tree:

        TASK-001.2.05 (Complexity: 8) → 4 sub-tasks
        ├── TASK-001.2.05.A: Setup data models (🟢 2)
        ├── TASK-001.2.05.B: Implement business logic (🟡 5)
        ├── TASK-001.2.05.C: Add error handling (🟢 3)
        └── TASK-001.2.05.D: Create tests (🟡 4)
        """
        pass
```

#### `/installer/global/commands/lib/feature_generator.py`
**Purpose:** Main feature-generate-tasks command implementation
**Estimated LOC:** 300-400 lines
**Key Classes:**

```python
from typing import Optional, List
import argparse

class FeatureTaskGenerator:
    """Main command implementation for /feature-generate-tasks."""

    def __init__(self):
        self.complexity_calculator = ComplexityCalculator(DEFAULT_FACTORS)
        self.breakdown_engine = TaskBreakdownEngine(self.complexity_calculator)
        self.duplicate_detector = DuplicateDetector()
        self.visualizer = TaskVisualization()

    def generate_tasks(
        self,
        feature_id: str,
        options: Dict[str, Any]
    ) -> None:
        """
        Main entry point for task generation.

        Flow:
        1. Load feature specification
        2. Parse requirements and BDD scenarios
        3. Generate initial task list
        4. For each task:
           a. Evaluate complexity
           b. Apply breakdown strategy
           c. Check for duplicates
           d. Generate sub-tasks
        5. Visualize results
        6. Create task files
        7. Update feature metadata
        """
        pass

    def _parse_feature(self, feature_id: str) -> FeatureSpec:
        """Parse feature markdown file."""
        pass

    def _generate_initial_tasks(self, feature: FeatureSpec) -> List[Task]:
        """Generate initial task list from requirements."""
        pass

    def _process_task(self, task: Task) -> BreakdownResult:
        """Process single task with complexity analysis."""
        pass
```

---

## 2. Complexity Integration

### 2.1 Data Flow Diagram

```
┌────────────────────────────────────────────────────────┐
│         Feature-Generate-Tasks Command                  │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  1. Parse Feature Specification                         │
│     - Load feature markdown                             │
│     - Extract requirements, BDD scenarios               │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  2. Generate Initial Tasks                              │
│     - Requirements → Implementation tasks               │
│     - BDD scenarios → Testing tasks                     │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼ (For each task)
┌────────────────────────────────────────────────────────┐
│  3. Create Implementation Plan (from task description)  │
│     - Parse files to create                             │
│     - Identify patterns                                 │
│     - Extract risk indicators                           │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  4. Evaluate Complexity (REUSE complexity_calculator)   │
│     - FileComplexityFactor (0-3 points)                 │
│     - PatternFamiliarityFactor (0-2 points)             │
│     - RiskLevelFactor (0-3 points)                      │
│     Result: ComplexityScore (1-10 scale)                │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  5. Select Breakdown Strategy                           │
│     - Score 1-3: NoBreakdownStrategy                    │
│     - Score 4-6: LogicalUnitsStrategy                   │
│     - Score 7-8: FileBasedStrategy                      │
│     - Score 9-10: PhaseBasedStrategy                    │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  6. Apply Breakdown Strategy                            │
│     - Generate sub-tasks                                │
│     - Assign complexity to each sub-task                │
│     - Establish dependencies                            │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  7. Check for Duplicates (duplicate_detector)           │
│     - Compare with existing tasks                       │
│     - Flag potential duplicates                         │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  8. Visualize Results (visualization)                   │
│     - Display complexity distribution                   │
│     - Show sub-task hierarchy                           │
│     - Print statistics                                  │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│  9. Create Task Files                                   │
│     - Generate markdown task files                      │
│     - Update feature metadata                           │
│     - Link to epic/feature                              │
└────────────────────────────────────────────────────────┘
```

### 2.2 Complexity Score Mapping to Strategies

| Complexity Score | Review Mode      | Breakdown Strategy    | Rationale                          |
|------------------|------------------|-----------------------|------------------------------------|
| 1-3              | AUTO_PROCEED     | NO_BREAKDOWN          | Simple, manageable as single task  |
| 4-6              | QUICK_OPTIONAL   | LOGICAL_UNITS         | Moderate, break into components    |
| 7-8              | FULL_REQUIRED    | FILE_BASED            | Complex, organize by file groups   |
| 9-10             | FULL_REQUIRED    | PHASE_BASED           | Very complex, sequential phases    |

### 2.3 Error Handling Strategy

```python
class ComplexityEvaluationError(Exception):
    """Base exception for complexity evaluation errors."""
    pass

class BreakdownStrategyError(ComplexityEvaluationError):
    """Raised when breakdown strategy fails."""
    pass

# Error handling in feature_generator.py
def _process_task(self, task: Task) -> BreakdownResult:
    """Process task with graceful error handling."""
    try:
        # Calculate complexity
        complexity_score = self.complexity_calculator.calculate(context)
    except Exception as e:
        logger.error(f"Complexity calculation failed for {task.id}: {e}")
        # Fail-safe: Assume high complexity (score=8)
        complexity_score = ComplexityScore(
            total_score=8,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=ReviewMode.FULL_REQUIRED,
            calculation_timestamp=datetime.now(),
            metadata={"error": str(e), "failsafe": True}
        )

    try:
        # Apply breakdown
        result = self.breakdown_engine.analyze_and_breakdown(...)
    except BreakdownStrategyError as e:
        logger.error(f"Breakdown failed for {task.id}: {e}")
        # Fail-safe: Return original task (no breakdown)
        result = BreakdownResult(
            original_task_id=task.id,
            original_complexity=complexity_score.total_score,
            strategy_used=BreakdownStrategy.NO_BREAKDOWN,
            sub_tasks=[],
            breakdown_justification=f"Breakdown failed: {e}",
            statistics={}
        )

    return result
```

---

## 3. Task Breakdown Algorithms

### 3.1 Strategy 1: No Breakdown (Score 1-3)

**Use Case:** Simple tasks with low complexity
**Algorithm:**
```python
def breakdown(self, task_id: str, plan: ImplementationPlan,
              context: EvaluationContext) -> List[SubTask]:
    """No breakdown - return empty list."""
    logger.info(f"Task {task_id} is simple (score 1-3), no breakdown needed")
    return []
```

**Example:**
- **Task:** "Update user profile validation regex"
- **Complexity:** 2 (1 file, no patterns, low risk)
- **Breakdown:** None (stays as single task)

### 3.2 Strategy 2: Logical Units (Score 4-6)

**Use Case:** Moderate tasks requiring component separation
**Algorithm:**
```python
def breakdown(self, task_id: str, plan: ImplementationPlan,
              context: EvaluationContext) -> List[SubTask]:
    """
    Break into logical units:
    1. Setup/Infrastructure
    2. Core Implementation
    3. Error Handling
    4. Testing
    """
    sub_tasks = []

    # Component 1: Setup
    if self._has_setup_work(plan):
        sub_tasks.append(SubTask(
            sub_task_id=f"{task_id}.A",
            title=f"Setup infrastructure for {task_id}",
            description=self._extract_setup_description(plan),
            complexity_score=2,
            estimated_duration="1-2 hours",
            dependencies=[],
            files=self._filter_setup_files(plan.files_to_create),
            type='infrastructure'
        ))

    # Component 2: Core Logic
    sub_tasks.append(SubTask(
        sub_task_id=f"{task_id}.B",
        title=f"Implement core logic for {task_id}",
        description=self._extract_core_logic(plan),
        complexity_score=4,
        estimated_duration="3-4 hours",
        dependencies=[f"{task_id}.A"] if sub_tasks else [],
        files=self._filter_core_files(plan.files_to_create),
        type='implementation'
    ))

    # Component 3: Error Handling
    sub_tasks.append(SubTask(
        sub_task_id=f"{task_id}.C",
        title=f"Add error handling for {task_id}",
        description="Implement validation and error recovery",
        complexity_score=3,
        estimated_duration="2 hours",
        dependencies=[f"{task_id}.B"],
        files=self._filter_error_handling_files(plan.files_to_create),
        type='error_handling'
    ))

    # Component 4: Testing
    sub_tasks.append(SubTask(
        sub_task_id=f"{task_id}.D",
        title=f"Create tests for {task_id}",
        description="Implement unit and integration tests",
        complexity_score=3,
        estimated_duration="2-3 hours",
        dependencies=[f"{task_id}.B", f"{task_id}.C"],
        files=self._filter_test_files(plan.files_to_create),
        type='testing'
    ))

    return sub_tasks
```

**Example:**
- **Task:** "Implement user authentication API"
- **Complexity:** 5 (4 files, moderate patterns, moderate risk)
- **Breakdown:**
  - TASK-001.2.05.A: Setup authentication infrastructure (🟢 2)
  - TASK-001.2.05.B: Implement core authentication logic (🟡 4)
  - TASK-001.2.05.C: Add error handling and validation (🟢 3)
  - TASK-001.2.05.D: Create authentication tests (🟢 3)

### 3.3 Strategy 3: File-Based (Score 7-8)

**Use Case:** Complex tasks with many files
**Algorithm:**
```python
def breakdown(self, task_id: str, plan: ImplementationPlan,
              context: EvaluationContext) -> List[SubTask]:
    """
    Break by file groups:
    1. Group related files (model + service + controller)
    2. Create one sub-task per group
    3. Maintain dependencies between groups
    """
    # Group files by domain/layer
    file_groups = self._group_files_by_domain(plan.files_to_create)

    sub_tasks = []
    previous_sub_task_id = None

    for i, (group_name, files) in enumerate(file_groups.items()):
        sub_task_id = f"{task_id}.{chr(65 + i)}"  # A, B, C, ...

        # Calculate complexity for this file group
        group_complexity = min(len(files) * 2, 6)  # 2 points per file, max 6

        dependencies = []
        if previous_sub_task_id and self._has_dependency(group_name):
            dependencies.append(previous_sub_task_id)

        sub_tasks.append(SubTask(
            sub_task_id=sub_task_id,
            title=f"Implement {group_name} ({len(files)} files)",
            description=f"Create {', '.join(files)}",
            complexity_score=group_complexity,
            estimated_duration=f"{len(files) * 2}-{len(files) * 3} hours",
            dependencies=dependencies,
            files=files,
            type=self._infer_type(group_name)
        ))

        previous_sub_task_id = sub_task_id

    return sub_tasks

def _group_files_by_domain(self, files: List[str]) -> Dict[str, List[str]]:
    """
    Group files by domain/layer:
    - Data models: *Model.py, *Entity.py, *Schema.py
    - Services: *Service.py, *Repository.py
    - Controllers: *Controller.py, *Endpoint.py
    - Tests: test_*.py, *_test.py
    """
    groups = {
        'data_models': [],
        'services': [],
        'controllers': [],
        'tests': []
    }

    for file in files:
        if any(file.endswith(suffix) for suffix in ['Model.py', 'Entity.py', 'Schema.py']):
            groups['data_models'].append(file)
        elif any(file.endswith(suffix) for suffix in ['Service.py', 'Repository.py']):
            groups['services'].append(file)
        elif any(file.endswith(suffix) for suffix in ['Controller.py', 'Endpoint.py']):
            groups['controllers'].append(file)
        elif 'test' in file.lower():
            groups['tests'].append(file)
        else:
            groups.setdefault('other', []).append(file)

    # Remove empty groups
    return {k: v for k, v in groups.items() if v}
```

**Example:**
- **Task:** "Build complete order management system"
- **Complexity:** 8 (9 files, moderate patterns, high risk)
- **Breakdown:**
  - TASK-001.3.02.A: Implement data models (3 files) (🟡 6)
  - TASK-001.3.02.B: Implement services (3 files) (🟡 6)
  - TASK-001.3.02.C: Implement API endpoints (2 files) (🟡 4)
  - TASK-001.3.02.D: Create tests (1 file) (🟢 2)

### 3.4 Strategy 4: Phase-Based (Score 9-10)

**Use Case:** Very complex tasks requiring sequential phases
**Algorithm:**
```python
def breakdown(self, task_id: str, plan: ImplementationPlan,
              context: EvaluationContext) -> List[SubTask]:
    """
    Break by implementation phases:
    Phase 1: Foundation (data models, interfaces)
    Phase 2: Business Logic (core functionality)
    Phase 3: Integration (external systems, error handling)
    Phase 4: Testing & Documentation
    """
    phases = [
        {
            'name': 'Foundation',
            'suffix': 'A',
            'description': 'Create data models and interfaces',
            'files': self._filter_foundation_files(plan.files_to_create),
            'complexity': 5,
            'duration': '4-6 hours',
            'dependencies': []
        },
        {
            'name': 'Business Logic',
            'suffix': 'B',
            'description': 'Implement core business functionality',
            'files': self._filter_business_logic_files(plan.files_to_create),
            'complexity': 7,
            'duration': '8-10 hours',
            'dependencies': [f"{task_id}.A"]
        },
        {
            'name': 'Integration',
            'suffix': 'C',
            'description': 'Integrate with external systems and add error handling',
            'files': self._filter_integration_files(plan.files_to_create),
            'complexity': 6,
            'duration': '6-8 hours',
            'dependencies': [f"{task_id}.B"]
        },
        {
            'name': 'Testing & Documentation',
            'suffix': 'D',
            'description': 'Create comprehensive tests and documentation',
            'files': self._filter_test_files(plan.files_to_create),
            'complexity': 5,
            'duration': '4-6 hours',
            'dependencies': [f"{task_id}.B", f"{task_id}.C"]
        }
    ]

    sub_tasks = []
    for phase in phases:
        if not phase['files']:  # Skip empty phases
            continue

        sub_tasks.append(SubTask(
            sub_task_id=f"{task_id}.{phase['suffix']}",
            title=f"Phase {phase['suffix']}: {phase['name']}",
            description=phase['description'],
            complexity_score=phase['complexity'],
            estimated_duration=phase['duration'],
            dependencies=phase['dependencies'],
            files=phase['files'],
            type='phase'
        ))

    return sub_tasks
```

**Example:**
- **Task:** "Implement complete payment processing system"
- **Complexity:** 10 (12+ files, advanced patterns, critical risk)
- **Breakdown:**
  - TASK-001.4.01.A: Phase A - Foundation (data models, interfaces) (🟡 5)
  - TASK-001.4.01.B: Phase B - Business Logic (payment processing) (🔴 7)
  - TASK-001.4.01.C: Phase C - Integration (Stripe, webhooks) (🟡 6)
  - TASK-001.4.01.D: Phase D - Testing & Documentation (🟡 5)

### 3.5 Sub-Task ID Generation

**Format:** `TASK-{epic}.{feature}.{task}.{sub}`
**Examples:**
- `TASK-001.2.05.A` - Epic 001, Feature 2, Task 05, Sub-task A
- `TASK-001.2.05.B` - Epic 001, Feature 2, Task 05, Sub-task B
- `TASK-002.1.03.C` - Epic 002, Feature 1, Task 03, Sub-task C

**Implementation:**
```python
def generate_sub_task_id(parent_task_id: str, sub_index: int) -> str:
    """
    Generate sub-task ID from parent task ID.

    Args:
        parent_task_id: e.g., "TASK-001.2.05"
        sub_index: 0-based index (0=A, 1=B, 2=C, ...)

    Returns:
        Sub-task ID: e.g., "TASK-001.2.05.A"
    """
    suffix = chr(65 + sub_index)  # A, B, C, ...
    return f"{parent_task_id}.{suffix}"
```

---

## 4. Visualization & Output

### 4.1 Terminal Output Examples

#### Example 1: No Breakdown (Score 1-3)
```
🔍 Analyzing Task Complexity: TASK-001.2.05
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Complexity Evaluation
├── File Complexity: 0/3 (1 file)
├── Pattern Familiarity: 0/2 (no patterns)
└── Risk Level: 0/3 (low risk)

Total Complexity: 🟢 2/10 (LOW)
Review Mode: AUTO_PROCEED

✅ Breakdown Strategy: NO_BREAKDOWN
   Justification: Task is simple and manageable as-is

📋 Task remains as single unit:
   TASK-001.2.05: Update user profile validation regex
   Complexity: 🟢 2 | Duration: 1-2 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Analysis complete - no breakdown required
```

#### Example 2: Logical Units (Score 4-6)
```
🔍 Analyzing Task Complexity: TASK-001.2.06
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Complexity Evaluation
├── File Complexity: 1/3 (4 files)
├── Pattern Familiarity: 1/2 (Strategy pattern)
└── Risk Level: 2/3 (authentication, security)

Total Complexity: 🟡 5/10 (MEDIUM)
Review Mode: QUICK_OPTIONAL

🔧 Breakdown Strategy: LOGICAL_UNITS
   Justification: Moderate complexity - break into logical components

📋 Generated Sub-Tasks (4):

TASK-001.2.06 → 4 logical units
├── TASK-001.2.06.A: Setup authentication infrastructure
│   ├── Complexity: 🟢 2 | Duration: 1-2 hours
│   ├── Files: config/auth_config.py
│   └── Dependencies: None
│
├── TASK-001.2.06.B: Implement core authentication logic
│   ├── Complexity: 🟡 4 | Duration: 3-4 hours
│   ├── Files: services/auth_service.py, models/user_model.py
│   └── Dependencies: TASK-001.2.06.A
│
├── TASK-001.2.06.C: Add error handling and validation
│   ├── Complexity: 🟢 3 | Duration: 2 hours
│   ├── Files: validators/auth_validator.py
│   └── Dependencies: TASK-001.2.06.B
│
└── TASK-001.2.06.D: Create authentication tests
    ├── Complexity: 🟢 3 | Duration: 2-3 hours
    ├── Files: tests/test_auth_service.py
    └── Dependencies: TASK-001.2.06.B, TASK-001.2.06.C

📊 Statistics:
├── Average Complexity: 3.0
├── Total Duration: 8-11 hours
└── Complexity Distribution:
    🟢 Low (1-3):    ███████ 75% (3 tasks)
    🟡 Medium (4-6): ██ 25% (1 task)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Analysis complete - 4 sub-tasks generated
```

#### Example 3: File-Based (Score 7-8)
```
🔍 Analyzing Task Complexity: TASK-001.3.02
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Complexity Evaluation
├── File Complexity: 3/3 (9 files)
├── Pattern Familiarity: 1/2 (Repository pattern)
└── Risk Level: 2/3 (database, transactions)

Total Complexity: 🔴 8/10 (HIGH)
Review Mode: FULL_REQUIRED

📦 Breakdown Strategy: FILE_BASED
   Justification: Complex task - organize by file groups

📋 Generated Sub-Tasks (4):

TASK-001.3.02 → 4 file groups
├── TASK-001.3.02.A: Implement data models (3 files)
│   ├── Complexity: 🟡 6 | Duration: 6-9 hours
│   ├── Files:
│   │   • models/order_model.py
│   │   • models/order_item_model.py
│   │   • schemas/order_schema.py
│   └── Dependencies: None
│
├── TASK-001.3.02.B: Implement services (3 files)
│   ├── Complexity: 🟡 6 | Duration: 6-9 hours
│   ├── Files:
│   │   • services/order_service.py
│   │   • repositories/order_repository.py
│   │   • services/inventory_service.py
│   └── Dependencies: TASK-001.3.02.A
│
├── TASK-001.3.02.C: Implement API endpoints (2 files)
│   ├── Complexity: 🟡 4 | Duration: 4-6 hours
│   ├── Files:
│   │   • api/order_controller.py
│   │   • api/order_routes.py
│   └── Dependencies: TASK-001.3.02.B
│
└── TASK-001.3.02.D: Create tests (1 file)
    ├── Complexity: 🟢 2 | Duration: 2-3 hours
    ├── Files:
    │   • tests/test_order_service.py
    └── Dependencies: TASK-001.3.02.B, TASK-001.3.02.C

📊 Statistics:
├── Average Complexity: 4.5
├── Total Duration: 18-27 hours
└── Complexity Distribution:
    🟢 Low (1-3):    ██ 25% (1 task)
    🟡 Medium (4-6): ███████ 75% (3 tasks)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Analysis complete - 4 sub-tasks generated
```

#### Example 4: Phase-Based (Score 9-10)
```
🔍 Analyzing Task Complexity: TASK-001.4.01
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Complexity Evaluation
├── File Complexity: 3/3 (12 files)
├── Pattern Familiarity: 2/2 (CQRS, Event Sourcing)
└── Risk Level: 3/3 (payment, security, external API)

Total Complexity: 🔴 10/10 (CRITICAL)
Review Mode: FULL_REQUIRED

🎯 Breakdown Strategy: PHASE_BASED
   Justification: Critical complexity - sequential implementation phases

📋 Generated Sub-Tasks (4):

TASK-001.4.01 → 4 implementation phases
├── TASK-001.4.01.A: Phase A - Foundation
│   ├── Description: Create data models and interfaces
│   ├── Complexity: 🟡 5 | Duration: 4-6 hours
│   ├── Files (4):
│   │   • models/payment_model.py
│   │   • models/transaction_model.py
│   │   • interfaces/payment_gateway.py
│   │   • schemas/payment_schema.py
│   └── Dependencies: None
│
├── TASK-001.4.01.B: Phase B - Business Logic
│   ├── Description: Implement core payment processing
│   ├── Complexity: 🔴 7 | Duration: 8-10 hours
│   ├── Files (4):
│   │   • services/payment_service.py
│   │   • services/transaction_service.py
│   │   • handlers/payment_handler.py
│   │   • validators/payment_validator.py
│   └── Dependencies: TASK-001.4.01.A
│
├── TASK-001.4.01.C: Phase C - Integration
│   ├── Description: Integrate with Stripe and webhooks
│   ├── Complexity: 🟡 6 | Duration: 6-8 hours
│   ├── Files (3):
│   │   • integrations/stripe_gateway.py
│   │   • webhooks/payment_webhook.py
│   │   • services/notification_service.py
│   └── Dependencies: TASK-001.4.01.B
│
└── TASK-001.4.01.D: Phase D - Testing & Documentation
    ├── Description: Create comprehensive tests and docs
    ├── Complexity: 🟡 5 | Duration: 4-6 hours
    ├── Files (1):
    │   • tests/test_payment_integration.py
    └── Dependencies: TASK-001.4.01.B, TASK-001.4.01.C

📊 Statistics:
├── Average Complexity: 5.75
├── Total Duration: 22-30 hours
└── Complexity Distribution:
    🟡 Medium (4-6): ███████ 75% (3 tasks)
    🔴 High (7-10):  ██ 25% (1 task)

⚠️  CRITICAL TASK WARNING
This task requires sequential implementation and careful review at each phase.
Recommend human checkpoint before proceeding to Phase B.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Analysis complete - 4 sub-tasks generated
```

### 4.2 Color Coding Implementation

```python
class ComplexityColor(Enum):
    """ANSI color codes for terminal output."""
    LOW = "\033[92m"        # Green (1-3)
    MEDIUM = "\033[93m"     # Yellow (4-6)
    HIGH = "\033[91m"       # Red (7-10)
    BOLD = "\033[1m"
    RESET = "\033[0m"

def colorize_complexity(score: int) -> str:
    """Apply color coding to complexity score."""
    if score <= 3:
        emoji = "🟢"
        color = ComplexityColor.LOW.value
    elif score <= 6:
        emoji = "🟡"
        color = ComplexityColor.MEDIUM.value
    else:
        emoji = "🔴"
        color = ComplexityColor.HIGH.value

    return f"{emoji} {color}{score}{ComplexityColor.RESET.value}"
```

---

## 5. File Structure

### 5.1 New Files to Create

```
installer/global/commands/lib/
├── task_breakdown.py                    (400-500 LOC) ⭐ NEW
├── breakdown_strategies.py              (500-600 LOC) ⭐ NEW
├── duplicate_detector.py                (150-200 LOC) ⭐ NEW
├── visualization.py                     (200-250 LOC) ⭐ NEW
└── feature_generator.py                 (300-400 LOC) ⭐ NEW

Total New LOC: ~1,800-2,200 lines
```

### 5.2 Existing Files to Reuse (NO MODIFICATION)

```
installer/global/commands/lib/
├── complexity_calculator.py             (349 LOC) ✅ REUSE AS-IS
├── complexity_factors.py                (266 LOC) ✅ REUSE AS-IS
└── complexity_models.py                 (224 LOC) ✅ REUSE AS-IS
```

### 5.3 Integration Point (Shell Script - MINIMAL MODIFICATION)

```bash
# installer/global/commands/feature-generate-tasks.sh
#!/bin/bash

# Existing script... (keep as-is)

# ADD: Call Python implementation
python3 installer/global/commands/lib/feature_generator.py \
    --feature-id "$FEATURE_ID" \
    --interactive "$INTERACTIVE" \
    --types "$TASK_TYPES" \
    --export "$EXPORT_TOOLS"
```

### 5.4 Test Files Structure

```
tests/
├── test_task_breakdown.py               (300-400 LOC)
├── test_breakdown_strategies.py         (400-500 LOC)
├── test_duplicate_detector.py           (200-250 LOC)
├── test_visualization.py                (150-200 LOC)
└── test_feature_generator.py            (300-400 LOC)

Total Test LOC: ~1,350-1,750 lines
```

---

## 6. Testing Strategy

### 6.1 Unit Tests

#### test_task_breakdown.py
```python
import pytest
from installer.global.commands.lib.task_breakdown import (
    TaskBreakdownEngine,
    BreakdownResult,
    SubTask,
    BreakdownStrategy
)
from installer.global.commands.lib.complexity_calculator import ComplexityCalculator
from installer.global.commands.lib.complexity_models import (
    EvaluationContext,
    ImplementationPlan
)

class TestTaskBreakdownEngine:
    """Test suite for TaskBreakdownEngine."""

    @pytest.fixture
    def breakdown_engine(self):
        """Create breakdown engine fixture."""
        calculator = ComplexityCalculator()
        return TaskBreakdownEngine(calculator)

    @pytest.fixture
    def simple_context(self) -> EvaluationContext:
        """Create simple task context (score 1-3)."""
        plan = ImplementationPlan(
            task_id="TASK-001.2.05",
            files_to_create=["utils/validator.py"],
            patterns_used=[],
            external_dependencies=[],
            estimated_loc=50,
            risk_indicators=[],
            raw_plan="Update validation regex"
        )
        return EvaluationContext(
            task_id="TASK-001.2.05",
            technology_stack="python",
            implementation_plan=plan,
            task_metadata={},
            user_flags={}
        )

    @pytest.fixture
    def moderate_context(self) -> EvaluationContext:
        """Create moderate task context (score 4-6)."""
        plan = ImplementationPlan(
            task_id="TASK-001.2.06",
            files_to_create=[
                "services/auth_service.py",
                "models/user_model.py",
                "validators/auth_validator.py",
                "tests/test_auth_service.py"
            ],
            patterns_used=["Strategy"],
            external_dependencies=["jwt"],
            estimated_loc=300,
            risk_indicators=["authentication"],
            raw_plan="Implement authentication service with JWT"
        )
        return EvaluationContext(
            task_id="TASK-001.2.06",
            technology_stack="python",
            implementation_plan=plan,
            task_metadata={},
            user_flags={}
        )

    def test_no_breakdown_for_simple_task(
        self,
        breakdown_engine: TaskBreakdownEngine,
        simple_context: EvaluationContext
    ):
        """Test that simple tasks (score 1-3) are not broken down."""
        result = breakdown_engine.analyze_and_breakdown(
            task_id=simple_context.task_id,
            task_description="Update validation regex",
            implementation_plan=simple_context.implementation_plan,
            context=simple_context
        )

        assert result.strategy_used == BreakdownStrategy.NO_BREAKDOWN
        assert len(result.sub_tasks) == 0
        assert result.original_complexity <= 3

    def test_logical_units_for_moderate_task(
        self,
        breakdown_engine: TaskBreakdownEngine,
        moderate_context: EvaluationContext
    ):
        """Test that moderate tasks (score 4-6) use logical units strategy."""
        result = breakdown_engine.analyze_and_breakdown(
            task_id=moderate_context.task_id,
            task_description="Implement authentication",
            implementation_plan=moderate_context.implementation_plan,
            context=moderate_context
        )

        assert result.strategy_used == BreakdownStrategy.LOGICAL_UNITS
        assert len(result.sub_tasks) > 0
        assert result.original_complexity in range(4, 7)

        # Verify sub-task IDs follow pattern
        for sub_task in result.sub_tasks:
            assert sub_task.sub_task_id.startswith("TASK-001.2.06.")
            assert sub_task.sub_task_id[-1] in "ABCDEFGH"

    def test_sub_task_complexity_reduced(
        self,
        breakdown_engine: TaskBreakdownEngine,
        moderate_context: EvaluationContext
    ):
        """Test that sub-tasks have lower complexity than parent."""
        result = breakdown_engine.analyze_and_breakdown(
            task_id=moderate_context.task_id,
            task_description="Implement authentication",
            implementation_plan=moderate_context.implementation_plan,
            context=moderate_context
        )

        if result.sub_tasks:
            max_sub_complexity = max(st.complexity_score for st in result.sub_tasks)
            assert max_sub_complexity < result.original_complexity

    def test_statistics_calculation(
        self,
        breakdown_engine: TaskBreakdownEngine,
        moderate_context: EvaluationContext
    ):
        """Test that statistics are correctly calculated."""
        result = breakdown_engine.analyze_and_breakdown(
            task_id=moderate_context.task_id,
            task_description="Implement authentication",
            implementation_plan=moderate_context.implementation_plan,
            context=moderate_context
        )

        if result.sub_tasks:
            stats = result.statistics
            assert 'average_complexity' in stats
            assert 'total_duration' in stats
            assert 'complexity_distribution' in stats

            # Verify average calculation
            avg = sum(st.complexity_score for st in result.sub_tasks) / len(result.sub_tasks)
            assert abs(stats['average_complexity'] - avg) < 0.01
```

#### test_breakdown_strategies.py
```python
import pytest
from installer.global.commands.lib.breakdown_strategies import (
    NoBreakdownStrategy,
    LogicalUnitsStrategy,
    FileBasedStrategy,
    PhaseBasedStrategy,
    BreakdownStrategySelector
)
from installer.global.commands.lib.complexity_models import (
    ImplementationPlan,
    EvaluationContext
)

class TestBreakdownStrategySelector:
    """Test suite for strategy selection."""

    @pytest.fixture
    def selector(self):
        return BreakdownStrategySelector()

    @pytest.mark.parametrize("score,expected_strategy", [
        (1, NoBreakdownStrategy),
        (3, NoBreakdownStrategy),
        (4, LogicalUnitsStrategy),
        (6, LogicalUnitsStrategy),
        (7, FileBasedStrategy),
        (8, FileBasedStrategy),
        (9, PhaseBasedStrategy),
        (10, PhaseBasedStrategy),
    ])
    def test_strategy_selection_by_score(
        self,
        selector: BreakdownStrategySelector,
        score: int,
        expected_strategy: type
    ):
        """Test correct strategy is selected for each complexity score."""
        strategy = selector.select_strategy(score)
        assert isinstance(strategy, expected_strategy)

class TestLogicalUnitsStrategy:
    """Test suite for logical units breakdown."""

    @pytest.fixture
    def strategy(self):
        return LogicalUnitsStrategy()

    @pytest.fixture
    def context(self) -> EvaluationContext:
        plan = ImplementationPlan(
            task_id="TASK-001.2.06",
            files_to_create=[
                "services/auth_service.py",
                "models/user_model.py",
                "validators/auth_validator.py",
                "tests/test_auth_service.py"
            ],
            patterns_used=["Strategy"],
            raw_plan="Implement authentication service"
        )
        return EvaluationContext(
            task_id="TASK-001.2.06",
            technology_stack="python",
            implementation_plan=plan
        )

    def test_logical_breakdown_creates_components(
        self,
        strategy: LogicalUnitsStrategy,
        context: EvaluationContext
    ):
        """Test that logical units strategy creates component sub-tasks."""
        sub_tasks = strategy.breakdown(
            task_id="TASK-001.2.06",
            plan=context.implementation_plan,
            context=context
        )

        assert len(sub_tasks) > 0

        # Verify component types
        types = {st.type for st in sub_tasks}
        assert 'implementation' in types or 'infrastructure' in types
        assert 'testing' in types

    def test_sub_tasks_have_dependencies(
        self,
        strategy: LogicalUnitsStrategy,
        context: EvaluationContext
    ):
        """Test that sub-tasks maintain proper dependencies."""
        sub_tasks = strategy.breakdown(
            task_id="TASK-001.2.06",
            plan=context.implementation_plan,
            context=context
        )

        # Later sub-tasks should depend on earlier ones
        for i, sub_task in enumerate(sub_tasks[1:], start=1):
            # Check if at least one dependency exists
            assert len(sub_task.dependencies) > 0

class TestFileBasedStrategy:
    """Test suite for file-based breakdown."""

    @pytest.fixture
    def strategy(self):
        return FileBasedStrategy()

    @pytest.fixture
    def context(self) -> EvaluationContext:
        plan = ImplementationPlan(
            task_id="TASK-001.3.02",
            files_to_create=[
                "models/order_model.py",
                "models/order_item_model.py",
                "schemas/order_schema.py",
                "services/order_service.py",
                "repositories/order_repository.py",
                "api/order_controller.py",
                "api/order_routes.py",
                "tests/test_order_service.py"
            ],
            patterns_used=["Repository"],
            raw_plan="Implement order management system"
        )
        return EvaluationContext(
            task_id="TASK-001.3.02",
            technology_stack="python",
            implementation_plan=plan
        )

    def test_file_grouping(
        self,
        strategy: FileBasedStrategy,
        context: EvaluationContext
    ):
        """Test that files are correctly grouped by domain."""
        sub_tasks = strategy.breakdown(
            task_id="TASK-001.3.02",
            plan=context.implementation_plan,
            context=context
        )

        # Verify file groups exist
        assert len(sub_tasks) > 0

        # Verify each sub-task has files
        for sub_task in sub_tasks:
            assert len(sub_task.files) > 0
```

#### test_duplicate_detector.py
```python
import pytest
from installer.global.commands.lib.duplicate_detector import (
    DuplicateDetector,
    DuplicateMatch
)
from installer.global.commands.lib.task_breakdown import SubTask

class TestDuplicateDetector:
    """Test suite for duplicate detection."""

    @pytest.fixture
    def detector(self):
        return DuplicateDetector()

    @pytest.fixture
    def existing_task(self) -> SubTask:
        return SubTask(
            sub_task_id="TASK-001.2.05.A",
            title="Implement user authentication",
            description="Create JWT-based authentication service",
            complexity_score=5,
            estimated_duration="4 hours",
            dependencies=[],
            files=["services/auth_service.py", "models/user_model.py"],
            type="implementation"
        )

    def test_exact_duplicate_detected(
        self,
        detector: DuplicateDetector,
        existing_task: SubTask
    ):
        """Test that exact duplicates are detected."""
        proposed_task = SubTask(
            sub_task_id="TASK-001.2.06.A",
            title="Implement user authentication",  # Same title
            description="Create JWT-based authentication service",  # Same description
            complexity_score=5,
            estimated_duration="4 hours",
            dependencies=[],
            files=["services/auth_service.py", "models/user_model.py"],  # Same files
            type="implementation"
        )

        match = detector.check_for_duplicates(proposed_task, [existing_task])

        assert match is not None
        assert match.similarity_score >= 0.85
        assert existing_task.sub_task_id in match.task_id

    def test_similar_title_detected(
        self,
        detector: DuplicateDetector,
        existing_task: SubTask
    ):
        """Test that similar titles trigger duplicate detection."""
        proposed_task = SubTask(
            sub_task_id="TASK-001.2.06.A",
            title="Implement user auth system",  # Similar but not exact
            description="Different description",
            complexity_score=5,
            estimated_duration="4 hours",
            dependencies=[],
            files=["other_file.py"],
            type="implementation"
        )

        match = detector.check_for_duplicates(proposed_task, [existing_task])

        # Should detect similarity due to title overlap
        if match:
            assert match.similarity_score > 0.5

    def test_different_task_not_duplicate(
        self,
        detector: DuplicateDetector,
        existing_task: SubTask
    ):
        """Test that unrelated tasks are not flagged as duplicates."""
        proposed_task = SubTask(
            sub_task_id="TASK-001.2.07.A",
            title="Implement email service",  # Completely different
            description="Create email notification system",
            complexity_score=3,
            estimated_duration="2 hours",
            dependencies=[],
            files=["services/email_service.py"],
            type="implementation"
        )

        match = detector.check_for_duplicates(proposed_task, [existing_task])

        assert match is None or match.similarity_score < 0.85
```

### 6.2 Integration Tests

#### test_feature_generator.py
```python
import pytest
import tempfile
import shutil
from pathlib import Path
from installer.global.commands.lib.feature_generator import FeatureTaskGenerator

class TestFeatureTaskGenerator:
    """End-to-end integration tests."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing."""
        workspace = tempfile.mkdtemp()
        yield Path(workspace)
        shutil.rmtree(workspace)

    @pytest.fixture
    def sample_feature(self, temp_workspace: Path):
        """Create sample feature file."""
        feature_dir = temp_workspace / "docs" / "features"
        feature_dir.mkdir(parents=True)

        feature_file = feature_dir / "FEAT-001.2-user-authentication.md"
        feature_file.write_text("""
# FEAT-001.2: User Authentication

## Description
Implement JWT-based authentication system

## Requirements
- REQ-001: Secure login endpoint
- REQ-002: Token validation
- REQ-003: Session management

## BDD Scenarios
- BDD-001: Successful login flow
- BDD-002: Invalid credentials handling
        """)

        return feature_file

    def test_full_generation_flow(
        self,
        temp_workspace: Path,
        sample_feature: Path
    ):
        """Test complete task generation flow."""
        generator = FeatureTaskGenerator()

        # Generate tasks
        result = generator.generate_tasks(
            feature_id="FEAT-001.2",
            options={
                'interactive': False,
                'types': 'all',
                'export': None
            }
        )

        # Verify tasks were created
        task_dir = temp_workspace / "tasks" / "backlog"
        assert task_dir.exists()

        task_files = list(task_dir.glob("TASK-*.md"))
        assert len(task_files) > 0

    def test_complexity_based_breakdown(
        self,
        temp_workspace: Path,
        sample_feature: Path
    ):
        """Test that tasks are broken down based on complexity."""
        generator = FeatureTaskGenerator()

        result = generator.generate_tasks(
            feature_id="FEAT-001.2",
            options={'interactive': False}
        )

        # Verify sub-tasks were generated for complex tasks
        task_files = list((temp_workspace / "tasks" / "backlog").glob("TASK-*.*.*.*.md"))

        # Should have some sub-tasks (format: TASK-X.X.XX.X)
        # This depends on complexity evaluation
```

### 6.3 Mock Strategy

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock
from installer.global.commands.lib.complexity_calculator import ComplexityCalculator
from installer.global.commands.lib.complexity_models import ComplexityScore, ReviewMode

@pytest.fixture
def mock_complexity_calculator():
    """Mock complexity calculator for testing."""
    mock = Mock(spec=ComplexityCalculator)

    def calculate_side_effect(context):
        # Return different scores based on file count
        file_count = len(context.implementation_plan.files_to_create)

        if file_count <= 2:
            score = 2
            mode = ReviewMode.AUTO_PROCEED
        elif file_count <= 5:
            score = 5
            mode = ReviewMode.QUICK_OPTIONAL
        elif file_count <= 8:
            score = 8
            mode = ReviewMode.FULL_REQUIRED
        else:
            score = 10
            mode = ReviewMode.FULL_REQUIRED

        return ComplexityScore(
            total_score=score,
            factor_scores=[],
            forced_review_triggers=[],
            review_mode=mode,
            calculation_timestamp=datetime.now(),
            metadata={}
        )

    mock.calculate.side_effect = calculate_side_effect
    return mock
```

### 6.4 Coverage Targets

| Module | Line Coverage | Branch Coverage | Notes |
|--------|---------------|-----------------|-------|
| task_breakdown.py | ≥ 85% | ≥ 75% | Core logic - high coverage required |
| breakdown_strategies.py | ≥ 80% | ≥ 70% | Strategy implementations |
| duplicate_detector.py | ≥ 85% | ≥ 75% | Critical for preventing duplicates |
| visualization.py | ≥ 70% | ≥ 60% | UI-focused - lower threshold acceptable |
| feature_generator.py | ≥ 80% | ≥ 70% | Integration module |

**Overall Target:** ≥ 80% line coverage, ≥ 70% branch coverage

---

## 7. Implementation Phases

### Phase 1: Foundation (4-6 hours)
**Goal:** Core data structures and integration with existing complexity system

**Tasks:**
1. Create `task_breakdown.py` with data models:
   - `BreakdownStrategy` enum
   - `SubTask` dataclass
   - `BreakdownResult` dataclass
   - `TaskBreakdownEngine` class skeleton

2. Integration with existing modules:
   - Import `ComplexityCalculator`
   - Import `ComplexityModels`
   - Import `DEFAULT_FACTORS`

3. Unit tests for data models:
   - Test data model creation
   - Test data validation

**Deliverables:**
- `/installer/global/commands/lib/task_breakdown.py` (150-200 LOC)
- `/tests/test_task_breakdown.py` (100-150 LOC)

**Dependencies:** None (uses existing modules)

---

### Phase 2: Strategy Implementation (8-12 hours)
**Goal:** Implement 4 breakdown strategies

**Tasks:**
1. Create `breakdown_strategies.py`:
   - `BreakdownStrategyProtocol`
   - `NoBreakdownStrategy` (simplest)
   - `BreakdownStrategySelector`

2. Implement `LogicalUnitsStrategy`:
   - Component identification
   - Dependency tracking
   - File assignment

3. Implement `FileBasedStrategy`:
   - File grouping by domain
   - Group complexity calculation
   - Sequential dependencies

4. Implement `PhaseBasedStrategy`:
   - Phase definition
   - File filtering by phase
   - Phase dependencies

5. Comprehensive unit tests for each strategy

**Deliverables:**
- `/installer/global/commands/lib/breakdown_strategies.py` (500-600 LOC)
- `/tests/test_breakdown_strategies.py` (400-500 LOC)

**Dependencies:** Phase 1 completed

---

### Phase 3: Duplicate Detection (4-6 hours)
**Goal:** Prevent duplicate task creation

**Tasks:**
1. Create `duplicate_detector.py`:
   - `DuplicateMatch` dataclass
   - `DuplicateDetector` class
   - Similarity algorithms (Levenshtein, Jaccard)

2. Implement detection logic:
   - Title similarity
   - Description similarity
   - File overlap calculation
   - Weighted aggregation

3. Unit tests for duplicate detection:
   - Exact duplicates
   - Similar tasks
   - False negatives

**Deliverables:**
- `/installer/global/commands/lib/duplicate_detector.py` (150-200 LOC)
- `/tests/test_duplicate_detector.py` (200-250 LOC)

**Dependencies:** Phase 1 completed

---

### Phase 4: Visualization (4-6 hours)
**Goal:** Terminal output formatting

**Tasks:**
1. Create `visualization.py`:
   - `ComplexityColor` enum
   - `TaskVisualization` class
   - ASCII art formatting

2. Implement display methods:
   - `display_breakdown_result()`
   - `display_complexity_distribution()`
   - `format_sub_task_tree()`

3. Terminal output testing:
   - Color code validation
   - Format verification
   - Edge cases (0 sub-tasks, 20+ sub-tasks)

**Deliverables:**
- `/installer/global/commands/lib/visualization.py` (200-250 LOC)
- `/tests/test_visualization.py` (150-200 LOC)

**Dependencies:** Phase 1 completed

---

### Phase 5: Feature Generator Integration (6-8 hours)
**Goal:** Command implementation and end-to-end integration

**Tasks:**
1. Create `feature_generator.py`:
   - `FeatureTaskGenerator` class
   - Feature parsing
   - Task generation orchestration
   - File creation

2. Integration with all components:
   - ComplexityCalculator
   - TaskBreakdownEngine
   - DuplicateDetector
   - Visualization

3. Command-line argument parsing
4. Error handling and logging
5. End-to-end integration tests

**Deliverables:**
- `/installer/global/commands/lib/feature_generator.py` (300-400 LOC)
- `/tests/test_feature_generator.py` (300-400 LOC)
- Shell script integration

**Dependencies:** Phases 1-4 completed

---

### Phase 6: Testing & Documentation (4-6 hours)
**Goal:** Achieve ≥80% coverage and complete documentation

**Tasks:**
1. Run full test suite with coverage
2. Add tests for edge cases
3. Performance testing (20 tasks < 30s)
4. Create usage examples
5. Update command documentation

**Deliverables:**
- Test coverage report (≥80%)
- Performance benchmarks
- Usage documentation

**Dependencies:** Phase 5 completed

---

## 8. External Dependencies

### 8.1 Python Standard Library (No Installation Required)

```python
# Standard library imports
import logging
import re
import difflib
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any, Protocol
from abc import ABC, abstractmethod
```

**No external packages required** - all functionality uses Python standard library.

### 8.2 Internal Dependencies (Already Available)

```python
# Existing complexity evaluation modules
from installer.global.commands.lib.complexity_calculator import ComplexityCalculator
from installer.global.commands.lib.complexity_factors import DEFAULT_FACTORS
from installer.global.commands.lib.complexity_models import (
    ComplexityScore,
    FactorScore,
    ReviewMode,
    ImplementationPlan,
    EvaluationContext
)
```

---

## 9. Performance Considerations

### 9.1 Performance Target

**Requirement:** Process 20 tasks in < 30 seconds
**Breakdown:** ~1.5 seconds per task

### 9.2 Optimization Strategies

#### Strategy 1: Lazy Loading
```python
class FeatureTaskGenerator:
    def __init__(self):
        # Lazy initialization
        self._complexity_calculator = None
        self._breakdown_engine = None

    @property
    def complexity_calculator(self):
        if self._complexity_calculator is None:
            self._complexity_calculator = ComplexityCalculator(DEFAULT_FACTORS)
        return self._complexity_calculator
```

#### Strategy 2: Caching
```python
from functools import lru_cache

class DuplicateDetector:
    @lru_cache(maxsize=128)
    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Cached similarity calculation."""
        return difflib.SequenceMatcher(None, title1.lower(), title2.lower()).ratio()
```

#### Strategy 3: Batch Processing
```python
def generate_tasks_batch(self, tasks: List[Task]) -> List[BreakdownResult]:
    """Process multiple tasks efficiently."""
    results = []
    for task in tasks:
        # No I/O blocking - all in-memory operations
        result = self._process_task(task)
        results.append(result)
    return results
```

### 9.3 Performance Testing

```python
# tests/test_performance.py
import time
import pytest

def test_performance_20_tasks():
    """Verify 20 tasks processed in < 30 seconds."""
    generator = FeatureTaskGenerator()

    # Create 20 sample tasks
    tasks = [create_sample_task(i) for i in range(20)]

    start_time = time.time()
    results = generator.generate_tasks_batch(tasks)
    end_time = time.time()

    duration = end_time - start_time

    assert duration < 30.0, f"Processing took {duration}s (target: <30s)"
    assert len(results) == 20
```

---

## 10. Python Best Practices

### 10.1 Type Hints (Comprehensive)

```python
from typing import List, Optional, Dict, Any, Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class SubTask:
    """Type-safe sub-task model."""
    sub_task_id: str
    title: str
    description: str
    complexity_score: int
    estimated_duration: str
    dependencies: List[str]
    files: List[str]
    type: str

def analyze_and_breakdown(
    self,
    task_id: str,
    task_description: str,
    implementation_plan: ImplementationPlan,
    context: EvaluationContext
) -> BreakdownResult:
    """
    Fully type-hinted method signature.

    Args:
        task_id: Unique task identifier
        task_description: Human-readable description
        implementation_plan: Parsed implementation plan
        context: Evaluation context with metadata

    Returns:
        Breakdown result with sub-tasks and statistics
    """
    pass
```

### 10.2 Dataclasses for Data Structures

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass(frozen=True)  # Immutable by default
class BreakdownResult:
    """Breakdown analysis result."""
    original_task_id: str
    original_complexity: int
    strategy_used: BreakdownStrategy
    sub_tasks: List[SubTask]
    breakdown_justification: str
    statistics: Dict[str, Any] = field(default_factory=dict)
```

### 10.3 Logging for Debugging

```python
import logging

logger = logging.getLogger(__name__)

class TaskBreakdownEngine:
    def analyze_and_breakdown(self, ...):
        logger.info(f"Analyzing task {task_id} for breakdown")

        try:
            complexity_score = self.complexity_calculator.calculate(context)
            logger.debug(f"Complexity calculated: {complexity_score.total_score}")
        except Exception as e:
            logger.error(f"Complexity calculation failed: {e}", exc_info=True)
            # Handle error...

        logger.info(f"Breakdown complete: {len(result.sub_tasks)} sub-tasks generated")
        return result
```

### 10.4 Clear Error Messages

```python
class TaskBreakdownError(Exception):
    """Base exception for task breakdown errors."""
    pass

class InvalidComplexityScoreError(TaskBreakdownError):
    """Raised when complexity score is invalid."""
    def __init__(self, score: int):
        super().__init__(
            f"Invalid complexity score: {score}. "
            f"Expected value between 1-10."
        )

class BreakdownStrategyNotFoundError(TaskBreakdownError):
    """Raised when no strategy matches the complexity score."""
    def __init__(self, score: int):
        super().__init__(
            f"No breakdown strategy found for complexity score: {score}. "
            f"Valid range is 1-10."
        )
```

### 10.5 Pytest Fixtures

```python
# tests/conftest.py
import pytest
from installer.global.commands.lib.complexity_calculator import ComplexityCalculator
from installer.global.commands.lib.task_breakdown import TaskBreakdownEngine

@pytest.fixture(scope="session")
def complexity_calculator():
    """Session-scoped complexity calculator."""
    return ComplexityCalculator()

@pytest.fixture
def breakdown_engine(complexity_calculator):
    """Function-scoped breakdown engine."""
    return TaskBreakdownEngine(complexity_calculator)

@pytest.fixture
def sample_implementation_plan():
    """Sample implementation plan for testing."""
    return ImplementationPlan(
        task_id="TASK-001.2.05",
        files_to_create=["service.py", "model.py"],
        patterns_used=["Repository"],
        raw_plan="Implement user service"
    )
```

---

## 11. Architectural Decisions

### Decision 1: Reuse vs Rebuild Complexity Evaluation

**Decision:** REUSE existing complexity_calculator.py, complexity_factors.py, complexity_models.py

**Rationale:**
- ✅ Already implements 3 core factors (file, pattern, risk)
- ✅ Scoring logic proven in TASK-005/006
- ✅ Saves 500+ LOC of reimplementation
- ✅ Maintains consistency across codebase

**Alternative Considered:** Rebuild simplified version
**Rejected Because:** Unnecessary duplication, no performance benefit

---

### Decision 2: Breakdown Strategy Pattern

**Decision:** Use Strategy Pattern with 4 concrete implementations

**Rationale:**
- ✅ Clear separation of concerns
- ✅ Easy to test independently
- ✅ Extensible (can add more strategies later)
- ✅ Follows Open/Closed Principle

**Alternative Considered:** Single monolithic breakdown method
**Rejected Because:** Hard to test, violates SRP, not extensible

---

### Decision 3: Sub-Task ID Format

**Decision:** `TASK-{epic}.{feature}.{task}.{sub}` (e.g., TASK-001.2.05.A)

**Rationale:**
- ✅ Maintains hierarchy visibility
- ✅ Prevents ID collisions
- ✅ Sorts naturally in file systems
- ✅ Human-readable

**Alternative Considered:** UUID-based IDs
**Rejected Because:** Not human-readable, loses hierarchy context

---

### Decision 4: Duplicate Detection Algorithm

**Decision:** Weighted similarity scoring (title 40%, description 30%, files 30%)

**Rationale:**
- ✅ Balances different signal strengths
- ✅ Title is strongest duplicate indicator
- ✅ Files provide concrete evidence
- ✅ Threshold (85%) prevents false positives

**Alternative Considered:** Exact match only
**Rejected Because:** Misses near-duplicates with slight wording differences

---

### Decision 5: No External Dependencies

**Decision:** Use Python standard library only (no pip install required)

**Rationale:**
- ✅ Zero installation friction
- ✅ No version conflicts
- ✅ Faster execution (no import overhead)
- ✅ Easier to maintain

**Alternative Considered:** Use libraries (nltk for NLP, pandas for stats)
**Rejected Because:** Overkill for requirements, adds complexity

---

## 12. Risk Assessment & Mitigation

### Risk 1: Complexity Calculation Failures

**Risk:** ComplexityCalculator may fail on edge cases
**Likelihood:** Low (proven in TASK-005/006)
**Impact:** Medium (blocks breakdown)

**Mitigation:**
```python
try:
    complexity_score = self.complexity_calculator.calculate(context)
except Exception as e:
    logger.error(f"Complexity calculation failed: {e}")
    # Fail-safe: Assume moderate complexity (score=5)
    complexity_score = create_failsafe_score(context, score=5)
```

---

### Risk 2: Breakdown Strategy Selection Errors

**Risk:** No strategy matches complexity score
**Likelihood:** Very Low (all scores 1-10 covered)
**Impact:** High (breaks feature generation)

**Mitigation:**
```python
try:
    strategy = self.strategy_selector.select_strategy(score)
except ValueError as e:
    logger.error(f"Strategy selection failed: {e}")
    # Fail-safe: Use NoBreakdownStrategy (keep as single task)
    strategy = NoBreakdownStrategy()
```

---

### Risk 3: Performance Degradation (>30s for 20 tasks)

**Risk:** Complex calculations slow down processing
**Likelihood:** Low (mostly in-memory operations)
**Impact:** Medium (user experience)

**Mitigation:**
- Caching similarity calculations
- Lazy loading of modules
- Batch processing optimization
- Performance tests in CI

---

### Risk 4: Duplicate Detection False Positives

**Risk:** Legitimate tasks flagged as duplicates
**Likelihood:** Low (85% threshold is conservative)
**Impact:** Low (user can override)

**Mitigation:**
- Tunable similarity threshold (can adjust if needed)
- Clear justification in duplicate match
- Interactive mode allows user override

---

### Risk 5: Sub-Task ID Collisions

**Risk:** Generated IDs conflict with existing tasks
**Likelihood:** Very Low (hierarchical numbering)
**Impact:** High (breaks task tracking)

**Mitigation:**
```python
def generate_sub_task_id(parent_id: str, index: int) -> str:
    """Generate unique sub-task ID with collision check."""
    sub_id = f"{parent_id}.{chr(65 + index)}"

    # Verify uniqueness
    if task_exists(sub_id):
        raise TaskIDCollisionError(f"Sub-task ID already exists: {sub_id}")

    return sub_id
```

---

## 13. Success Criteria

### Functional Requirements
- ✅ **FR-001:** Evaluate complexity using existing calculator (TASK-005)
- ✅ **FR-002:** Select breakdown strategy based on score (1-3, 4-6, 7-8, 9-10)
- ✅ **FR-003:** Generate sub-tasks with unique hierarchical IDs
- ✅ **FR-004:** Detect duplicate tasks with 85% similarity threshold
- ✅ **FR-005:** Display terminal output with color-coded complexity
- ✅ **FR-006:** Calculate statistics (average, distribution)

### Non-Functional Requirements
- ✅ **NFR-001:** Process 20 tasks in < 30 seconds
- ✅ **NFR-002:** Achieve ≥ 80% test coverage
- ✅ **NFR-003:** Zero external dependencies (Python stdlib only)
- ✅ **NFR-004:** Comprehensive type hints throughout
- ✅ **NFR-005:** Clear error messages and logging

### Quality Gates
- ✅ All unit tests passing (pytest)
- ✅ Integration tests passing (end-to-end)
- ✅ Coverage ≥ 80% (pytest-cov)
- ✅ Performance benchmarks met (< 30s)
- ✅ No code smells (pylint score > 8.0)

---

## 14. Next Steps (Phase 3: Implementation)

After design approval, proceed to implementation in this order:

1. **Phase 1: Foundation** (4-6 hours)
   - Create data models in `task_breakdown.py`
   - Write unit tests
   - Integrate with complexity modules

2. **Phase 2: Strategies** (8-12 hours)
   - Implement 4 breakdown strategies
   - Write comprehensive strategy tests
   - Validate against examples

3. **Phase 3: Duplicate Detection** (4-6 hours)
   - Implement similarity algorithms
   - Test edge cases
   - Tune threshold

4. **Phase 4: Visualization** (4-6 hours)
   - Implement terminal formatting
   - Test color output
   - Create ASCII trees

5. **Phase 5: Integration** (6-8 hours)
   - Create main feature_generator.py
   - End-to-end integration tests
   - Shell script integration

6. **Phase 6: Testing & Documentation** (4-6 hours)
   - Achieve coverage targets
   - Performance testing
   - Update documentation

**Total Estimated Duration:** 30-44 hours (4-6 working days)

---

## Appendix A: File Size Estimates

| File | LOC | Test LOC | Complexity |
|------|-----|----------|------------|
| task_breakdown.py | 400-500 | 300-400 | Medium |
| breakdown_strategies.py | 500-600 | 400-500 | High |
| duplicate_detector.py | 150-200 | 200-250 | Medium |
| visualization.py | 200-250 | 150-200 | Low |
| feature_generator.py | 300-400 | 300-400 | High |
| **TOTAL** | **1,550-1,950** | **1,350-1,750** | - |

**Grand Total:** ~3,200-3,700 LOC (code + tests)

---

## Appendix B: Dependencies Graph

```
feature_generator.py
├── task_breakdown.py
│   ├── complexity_calculator.py (REUSE)
│   ├── complexity_models.py (REUSE)
│   └── breakdown_strategies.py
│       ├── NoBreakdownStrategy
│       ├── LogicalUnitsStrategy
│       ├── FileBasedStrategy
│       └── PhaseBasedStrategy
├── duplicate_detector.py
│   └── (standard library only)
└── visualization.py
    └── (standard library only)

complexity_calculator.py (EXISTING - NO MODIFICATION)
├── complexity_factors.py (EXISTING - NO MODIFICATION)
└── complexity_models.py (EXISTING - NO MODIFICATION)
```

---

**END OF IMPLEMENTATION DESIGN DOCUMENT**
