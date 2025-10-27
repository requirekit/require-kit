"""
Single source of truth for test coverage configuration.

This module centralizes all coverage thresholds, exclusions, and
reporting settings to avoid configuration drift across multiple files.

Architecture Philosophy:
    - DRY: Single definition for all coverage rules
    - Graduated thresholds: Different targets for different test types
    - Stack-specific overrides: Technology-appropriate standards
    - Progressive improvement: Ratchet up requirements over time

Usage:
    >>> from tests.coverage_config import COVERAGE_TARGETS
    >>> unit_target = COVERAGE_TARGETS['unit']['line']
    >>> assert unit_target == 90.0
"""

from typing import Dict, List, Any


# --- Core Coverage Targets ---

COVERAGE_TARGETS: Dict[str, Dict[str, float]] = {
    'unit': {
        'line': 90.0,       # Line coverage: ≥90%
        'branch': 85.0,     # Branch coverage: ≥85%
        'function': 95.0,   # Function coverage: ≥95%
    },
    'integration': {
        'line': 80.0,       # Line coverage: ≥80%
        'branch': 75.0,     # Branch coverage: ≥75%
        'function': 85.0,   # Function coverage: ≥85%
    },
    'e2e': {
        'line': 70.0,       # Line coverage: ≥70%
        'branch': 65.0,     # Branch coverage: ≥65%
        'function': 75.0,   # Function coverage: ≥75%
    },
    'edge_cases': {
        'line': 100.0,      # Edge cases must cover all paths
        'branch': 100.0,
        'function': 100.0,
    }
}

# Overall minimum threshold (fail build if below)
MINIMUM_TOTAL_COVERAGE = 85.0  # Global minimum: 85%


# --- Module-Specific Targets ---

MODULE_SPECIFIC_TARGETS: Dict[str, Dict[str, float]] = {
    'installer/global/commands/lib/complexity_calculator.py': {
        'line': 95.0,       # Core logic requires higher coverage
        'branch': 90.0,
    },
    'installer/global/commands/lib/review_modes.py': {
        'line': 92.0,
        'branch': 88.0,
    },
    'installer/global/commands/lib/complexity_factors.py': {
        'line': 93.0,
        'branch': 88.0,
    },
    'installer/global/commands/lib/review_router.py': {
        'line': 90.0,
        'branch': 85.0,
    },
}


# --- Coverage Exclusions ---

COVERAGE_EXCLUSIONS: List[str] = [
    # Test files themselves
    '*/tests/*',
    '*/test_*.py',
    '*_test.py',

    # Configuration and setup
    '*/conftest.py',
    '*/setup.py',
    '*/config.py',

    # Database migrations
    '*/migrations/*',
    '*/alembic/*',

    # Type stubs
    '*.pyi',

    # Development tools
    '*/scripts/*',
    '*/tools/*',

    # Examples and demos
    '*/examples/*',
    '*/demos/*',

    # Documentation
    '*/docs/*',

    # Generated code
    '*/__pycache__/*',
    '*.pyc',
    '*_pb2.py',  # Protocol buffers
    '*_pb2_grpc.py',
]


# --- Exclusion Pragmas ---
# Patterns to exclude specific lines from coverage

PRAGMA_EXCLUSIONS: List[str] = [
    'pragma: no cover',
    'pragma: nocover',
    'coverage: ignore',

    # Defensive programming
    'raise NotImplementedError',
    'raise AssertionError',
    'assert False',

    # Type checking only
    'if TYPE_CHECKING:',
    'if typing.TYPE_CHECKING:',

    # Abstract methods
    '@abstractmethod',
    '@abc.abstractmethod',

    # Debug code
    'if __name__ == "__main__":',
    'if DEBUG:',

    # Platform-specific code
    'if sys.platform',
    'if platform.system',
]


# --- Report Configuration ---

COVERAGE_REPORT_CONFIG: Dict[str, Any] = {
    'precision': 2,              # Show 2 decimal places
    'show_missing': True,        # Show missing line numbers
    'skip_covered': False,       # Show all files, not just incomplete
    'skip_empty': True,          # Skip empty files
    'sort': '-cover',            # Sort by coverage (lowest first)

    # Report formats
    'formats': [
        'term-missing',          # Terminal output with missing lines
        'html',                  # HTML report in htmlcov/
        'json',                  # JSON report for CI/CD
        'xml',                   # XML report for tools like Codecov
    ],

    # Output paths
    'html_dir': 'htmlcov',
    'json_file': 'coverage.json',
    'xml_file': 'coverage.xml',
}


# --- CI/CD Integration ---

CI_COVERAGE_CONFIG: Dict[str, Any] = {
    'fail_under': MINIMUM_TOTAL_COVERAGE,
    'skip_covered': False,
    'skip_empty': True,

    # CI-specific behavior
    'no_color': True,            # No ANSI colors in CI logs
    'quiet': False,              # Show full output
    'verbose': True,             # Detailed reporting

    # Coverage trends
    'compare_branch': 'main',    # Compare against main branch
    'fail_on_decrease': True,    # Fail if coverage decreases
    'max_decrease': 1.0,         # Allow max 1% decrease
}


# --- Stack-Specific Overrides ---

STACK_OVERRIDES: Dict[str, Dict[str, float]] = {
    'python': {
        'line': 90.0,
        'branch': 85.0,
    },
    'typescript': {
        'line': 85.0,
        'branch': 80.0,
    },
    'javascript': {
        'line': 80.0,
        'branch': 75.0,
    },
    'csharp': {
        'line': 85.0,
        'branch': 80.0,
    },
    'java': {
        'line': 85.0,
        'branch': 80.0,
    },
}


# --- Progressive Improvement Schedule ---
# Ratchet up coverage requirements over time

PROGRESSIVE_TARGETS: Dict[str, Dict[str, float]] = {
    'phase_1_current': {  # Current (MVP)
        'line': 85.0,
        'branch': 80.0,
    },
    'phase_2_q1_2025': {  # Q1 2025
        'line': 88.0,
        'branch': 83.0,
    },
    'phase_3_q2_2025': {  # Q2 2025
        'line': 90.0,
        'branch': 85.0,
    },
    'phase_4_mature': {   # Mature (goal)
        'line': 92.0,
        'branch': 88.0,
    },
}


# --- Helper Functions ---

def get_target_for_test_type(test_type: str, metric: str = 'line') -> float:
    """
    Get coverage target for specific test type.

    Args:
        test_type: Test type ('unit', 'integration', 'e2e', 'edge_cases')
        metric: Coverage metric ('line', 'branch', 'function')

    Returns:
        Target coverage percentage

    Example:
        >>> target = get_target_for_test_type('unit', 'line')
        >>> assert target == 90.0
    """
    return COVERAGE_TARGETS.get(test_type, {}).get(metric, MINIMUM_TOTAL_COVERAGE)


def get_module_target(module_path: str, metric: str = 'line') -> float:
    """
    Get coverage target for specific module.

    Falls back to overall minimum if no module-specific target.

    Args:
        module_path: Path to module
        metric: Coverage metric ('line', 'branch')

    Returns:
        Target coverage percentage

    Example:
        >>> target = get_module_target('complexity_calculator.py', 'line')
        >>> assert target >= 90.0
    """
    return MODULE_SPECIFIC_TARGETS.get(module_path, {}).get(metric, MINIMUM_TOTAL_COVERAGE)


def should_exclude_path(path: str) -> bool:
    """
    Check if path should be excluded from coverage.

    Args:
        path: File path to check

    Returns:
        True if should be excluded

    Example:
        >>> assert should_exclude_path('tests/test_foo.py') == True
        >>> assert should_exclude_path('src/main.py') == False
    """
    import fnmatch
    return any(fnmatch.fnmatch(path, pattern) for pattern in COVERAGE_EXCLUSIONS)


def get_stack_target(stack: str, metric: str = 'line') -> float:
    """
    Get coverage target for specific technology stack.

    Args:
        stack: Technology stack name
        metric: Coverage metric

    Returns:
        Target coverage percentage

    Example:
        >>> target = get_stack_target('python', 'line')
        >>> assert target == 90.0
    """
    return STACK_OVERRIDES.get(stack.lower(), {}).get(metric, MINIMUM_TOTAL_COVERAGE)


def format_coverage_report(coverage_data: Dict[str, float]) -> str:
    """
    Format coverage data for human-readable display.

    Args:
        coverage_data: Dictionary of coverage metrics

    Returns:
        Formatted report string

    Example:
        >>> data = {'line': 92.5, 'branch': 88.3}
        >>> report = format_coverage_report(data)
        >>> assert 'Line: 92.50%' in report
    """
    lines = []
    lines.append("Coverage Report:")
    lines.append("-" * 40)

    for metric, value in coverage_data.items():
        target = get_target_for_test_type('unit', metric)
        status = "✓" if value >= target else "✗"
        lines.append(f"  {status} {metric.capitalize()}: {value:.2f}% (target: {target:.2f}%)")

    return "\n".join(lines)


# --- Validation ---

def validate_coverage(coverage_data: Dict[str, float], test_type: str = 'unit') -> bool:
    """
    Validate coverage data meets targets.

    Args:
        coverage_data: Dictionary of coverage metrics
        test_type: Type of tests ('unit', 'integration', 'e2e')

    Returns:
        True if all targets met

    Example:
        >>> data = {'line': 92.0, 'branch': 87.0}
        >>> assert validate_coverage(data, 'unit') == True
    """
    targets = COVERAGE_TARGETS.get(test_type, {})

    for metric, target in targets.items():
        actual = coverage_data.get(metric, 0.0)
        if actual < target:
            return False

    return True


# --- pytest Configuration Generator ---

def generate_pytest_ini() -> str:
    """
    Generate pytest.ini configuration from coverage config.

    Returns:
        pytest.ini file content

    Example:
        >>> ini_content = generate_pytest_ini()
        >>> assert '--cov=' in ini_content
    """
    exclusions = " ".join(f"--cov-omit={pattern}" for pattern in COVERAGE_EXCLUSIONS[:5])

    return f"""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Coverage settings
addopts =
    --cov=installer/global/commands/lib
    --cov=tests
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=json:coverage.json
    --cov-fail-under={MINIMUM_TOTAL_COVERAGE}
    --strict-markers
    --tb=short
    -v
    {exclusions}

# Markers
markers =
    unit: Unit tests (deselect with '-m "not unit"')
    integration: Integration tests
    e2e: End-to-end tests
    edge_case: Edge case tests
    slow: Slow-running tests (deselect with '-m "not slow"')
    requires_network: Tests requiring network access

# Coverage exclude patterns
[coverage:report]
precision = {COVERAGE_REPORT_CONFIG['precision']}
show_missing = {COVERAGE_REPORT_CONFIG['show_missing']}
skip_covered = {COVERAGE_REPORT_CONFIG['skip_covered']}
skip_empty = {COVERAGE_REPORT_CONFIG['skip_empty']}

[coverage:run]
branch = True
source = installer/global/commands/lib/
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */conftest.py

fail_under = {MINIMUM_TOTAL_COVERAGE}
"""


if __name__ == '__main__':
    # Print configuration summary
    print("Coverage Configuration Summary")
    print("=" * 60)
    print(f"\nMinimum Total Coverage: {MINIMUM_TOTAL_COVERAGE}%")
    print("\nTest Type Targets:")
    for test_type, targets in COVERAGE_TARGETS.items():
        print(f"  {test_type}:")
        for metric, value in targets.items():
            print(f"    - {metric}: {value}%")

    print(f"\nExcluding {len(COVERAGE_EXCLUSIONS)} patterns")
    print(f"Using {len(PRAGMA_EXCLUSIONS)} pragma exclusions")
    print(f"Configured {len(MODULE_SPECIFIC_TARGETS)} module-specific targets")

    print("\n" + "=" * 60)
