"""
Test data fixtures for complexity-based plan review testing.

This module provides reusable test data fixtures representing various
task complexity levels and scenarios. Separated from mock fixtures to
maintain single responsibility.

Architecture:
    - Simple task data: Low complexity (score 1-3)
    - Medium task data: Medium complexity (score 4-6)
    - Complex task data: High complexity (score 7-10)
    - Edge case data: Boundary conditions and special scenarios

Usage:
    >>> from tests.fixtures.data_fixtures import simple_task_data
    >>> task = create_task_from_data(simple_task_data())
"""

import pytest
from datetime import datetime
from typing import Dict, Any, List


@pytest.fixture
def simple_task_data() -> Dict[str, Any]:
    """
    Low complexity task data (expected score: 2-3).

    Characteristics:
        - Single file modification
        - Familiar patterns (standard CRUD)
        - No external dependencies
        - Low business criticality
        - Estimated 1-2 hours

    Example:
        >>> data = simple_task_data()
        >>> assert len(data['files_to_create']) == 1
        >>> assert data['business_criticality'] == 'low'
    """
    return {
        'task_id': 'TASK-SIMPLE-001',
        'title': 'Fix validation error in user form',
        'requirements': ['REQ-001', 'REQ-002'],
        'files_to_create': [
            'src/validators/user_validator.py'
        ],
        'patterns_detected': ['validation', 'error_handling'],
        'external_dependencies': [],
        'technology_stack': ['Python'],
        'business_criticality': 'low',
        'estimated_hours': 2,
        'estimated_loc': 50,
        'risk_indicators': [],
        'has_security_keywords': False,
        'has_schema_changes': False,
        'is_hotfix': False,
    }


@pytest.fixture
def medium_task_data() -> Dict[str, Any]:
    """
    Medium complexity task data (expected score: 4-6).

    Characteristics:
        - 3-4 files to create/modify
        - Mix of familiar and new patterns
        - 1-2 external dependencies
        - Medium business criticality
        - Estimated 4-8 hours

    Example:
        >>> data = medium_task_data()
        >>> assert 3 <= len(data['files_to_create']) <= 4
        >>> assert data['business_criticality'] == 'medium'
    """
    return {
        'task_id': 'TASK-MEDIUM-001',
        'title': 'Add password reset functionality',
        'requirements': ['REQ-010', 'REQ-011', 'REQ-012', 'REQ-013'],
        'files_to_create': [
            'src/auth/password_reset_handler.py',
            'src/email/password_reset_email.py',
            'src/api/endpoints/auth/password_reset.py',
            'tests/test_password_reset.py'
        ],
        'patterns_detected': ['authentication', 'email_service', 'api_endpoint'],
        'external_dependencies': ['smtp', 'redis'],
        'technology_stack': ['Python', 'FastAPI', 'Redis'],
        'business_criticality': 'medium',
        'estimated_hours': 6,
        'estimated_loc': 300,
        'risk_indicators': ['external_email_service'],
        'has_security_keywords': True,  # 'password' keyword
        'has_schema_changes': False,
        'is_hotfix': False,
    }


@pytest.fixture
def complex_task_data() -> Dict[str, Any]:
    """
    High complexity task data (expected score: 7-10).

    Characteristics:
        - 6+ files to create/modify
        - New/unfamiliar patterns
        - Multiple external dependencies
        - High business criticality
        - Estimated 16+ hours

    Example:
        >>> data = complex_task_data()
        >>> assert len(data['files_to_create']) >= 6
        >>> assert data['business_criticality'] == 'critical'
    """
    return {
        'task_id': 'TASK-COMPLEX-001',
        'title': 'Implement event sourcing for order management',
        'requirements': [
            'REQ-050', 'REQ-051', 'REQ-052', 'REQ-053',
            'REQ-054', 'REQ-055', 'REQ-056', 'REQ-057'
        ],
        'files_to_create': [
            'src/domain/events/order_events.py',
            'src/domain/aggregates/order_aggregate.py',
            'src/infrastructure/event_store.py',
            'src/infrastructure/projections/order_projection.py',
            'src/api/commands/order_commands.py',
            'src/api/queries/order_queries.py',
            'tests/domain/test_order_aggregate.py',
            'tests/infrastructure/test_event_store.py'
        ],
        'patterns_detected': ['event_sourcing', 'cqrs', 'ddd', 'projections'],
        'external_dependencies': ['postgresql', 'kafka', 'redis'],
        'technology_stack': ['Python', 'FastAPI', 'PostgreSQL', 'Kafka'],
        'business_criticality': 'critical',
        'estimated_hours': 40,
        'estimated_loc': 1200,
        'risk_indicators': [
            'new_architecture_pattern',
            'data_consistency',
            'eventual_consistency',
            'high_business_impact'
        ],
        'has_security_keywords': False,
        'has_schema_changes': True,
        'is_hotfix': False,
    }


@pytest.fixture
def boundary_low_to_medium_data() -> Dict[str, Any]:
    """
    Boundary case: Exactly at score 3-4 threshold.

    Tests boundary between auto-proceed and quick review modes.
    """
    return {
        'task_id': 'TASK-BOUNDARY-LM-001',
        'title': 'Add logging to authentication module',
        'requirements': ['REQ-020', 'REQ-021'],
        'files_to_create': [
            'src/auth/logging_config.py',
            'tests/test_auth_logging.py'
        ],
        'patterns_detected': ['logging', 'configuration'],
        'external_dependencies': [],
        'technology_stack': ['Python'],
        'business_criticality': 'low',
        'estimated_hours': 3,
        'estimated_loc': 100,
        'risk_indicators': [],
        'has_security_keywords': False,
        'has_schema_changes': False,
        'is_hotfix': False,
    }


@pytest.fixture
def boundary_medium_to_high_data() -> Dict[str, Any]:
    """
    Boundary case: Exactly at score 6-7 threshold.

    Tests boundary between quick review and full review modes.
    """
    return {
        'task_id': 'TASK-BOUNDARY-MH-001',
        'title': 'Refactor database connection pool',
        'requirements': ['REQ-030', 'REQ-031', 'REQ-032', 'REQ-033'],
        'files_to_create': [
            'src/infrastructure/db_pool.py',
            'src/infrastructure/db_config.py',
            'src/infrastructure/db_health_check.py',
            'tests/infrastructure/test_db_pool.py',
            'tests/infrastructure/test_db_health.py'
        ],
        'patterns_detected': ['connection_pooling', 'resource_management'],
        'external_dependencies': ['postgresql', 'asyncpg'],
        'technology_stack': ['Python', 'PostgreSQL'],
        'business_criticality': 'high',
        'estimated_hours': 12,
        'estimated_loc': 500,
        'risk_indicators': ['performance_impact', 'resource_leaks'],
        'has_security_keywords': False,
        'has_schema_changes': False,
        'is_hotfix': False,
    }


@pytest.fixture
def force_trigger_security_data() -> Dict[str, Any]:
    """
    Force trigger scenario: Security-sensitive task.

    Should trigger full review regardless of low complexity score.
    """
    return {
        'task_id': 'TASK-SECURITY-001',
        'title': 'Update JWT token expiration',
        'requirements': ['REQ-040'],
        'files_to_create': [
            'src/auth/jwt_handler.py'
        ],
        'patterns_detected': ['authentication', 'jwt'],
        'external_dependencies': [],
        'technology_stack': ['Python'],
        'business_criticality': 'high',
        'estimated_hours': 2,
        'estimated_loc': 50,
        'risk_indicators': ['security_change'],
        'has_security_keywords': True,  # Force trigger
        'has_schema_changes': False,
        'is_hotfix': False,
    }


@pytest.fixture
def force_trigger_schema_data() -> Dict[str, Any]:
    """
    Force trigger scenario: Database schema changes.

    Should trigger full review regardless of complexity score.
    """
    return {
        'task_id': 'TASK-SCHEMA-001',
        'title': 'Add user_roles table',
        'requirements': ['REQ-045', 'REQ-046'],
        'files_to_create': [
            'migrations/001_add_user_roles_table.sql',
            'src/models/user_role.py'
        ],
        'patterns_detected': ['database_migration', 'schema_change'],
        'external_dependencies': ['alembic'],
        'technology_stack': ['Python', 'PostgreSQL'],
        'business_criticality': 'medium',
        'estimated_hours': 4,
        'estimated_loc': 150,
        'risk_indicators': ['data_migration', 'backward_compatibility'],
        'has_security_keywords': False,
        'has_schema_changes': True,  # Force trigger
        'is_hotfix': False,
    }


@pytest.fixture
def force_trigger_hotfix_data() -> Dict[str, Any]:
    """
    Force trigger scenario: Production hotfix.

    Should trigger full review regardless of complexity score.
    """
    return {
        'task_id': 'TASK-HOTFIX-001',
        'title': 'Fix critical payment processing bug',
        'requirements': ['REQ-099'],
        'files_to_create': [
            'src/payments/payment_processor.py'
        ],
        'patterns_detected': ['payment', 'bug_fix'],
        'external_dependencies': [],
        'technology_stack': ['Python'],
        'business_criticality': 'critical',
        'estimated_hours': 1,
        'estimated_loc': 20,
        'risk_indicators': ['production_impact', 'revenue_impact'],
        'has_security_keywords': False,
        'has_schema_changes': False,
        'is_hotfix': True,  # Force trigger
    }


@pytest.fixture
def edge_case_zero_files_data() -> Dict[str, Any]:
    """
    Edge case: Task with no files to create.

    Tests handling of unusual but valid edge case.
    """
    return {
        'task_id': 'TASK-EDGE-ZERO-001',
        'title': 'Research authentication strategies',
        'requirements': ['REQ-RESEARCH-001'],
        'files_to_create': [],  # Edge case
        'patterns_detected': [],
        'external_dependencies': [],
        'technology_stack': [],
        'business_criticality': 'low',
        'estimated_hours': 4,
        'estimated_loc': 0,
        'risk_indicators': [],
        'has_security_keywords': False,
        'has_schema_changes': False,
        'is_hotfix': False,
    }


@pytest.fixture
def edge_case_many_files_data() -> Dict[str, Any]:
    """
    Edge case: Task with very many files (50+).

    Tests handling of extreme complexity scenarios.
    """
    return {
        'task_id': 'TASK-EDGE-MANY-001',
        'title': 'Implement complete microservice',
        'requirements': [f'REQ-{i:03d}' for i in range(1, 21)],
        'files_to_create': [
            f'src/module_{i}/component_{j}.py'
            for i in range(1, 11)
            for j in range(1, 6)
        ],  # 50 files
        'patterns_detected': ['microservice', 'ddd', 'cqrs', 'event_sourcing'],
        'external_dependencies': [
            'postgresql', 'redis', 'kafka', 'rabbitmq',
            'elasticsearch', 'prometheus', 'grafana'
        ],
        'technology_stack': ['Python', 'FastAPI', 'PostgreSQL'],
        'business_criticality': 'critical',
        'estimated_hours': 200,
        'estimated_loc': 5000,
        'risk_indicators': [
            'very_high_complexity',
            'scope_creep_risk',
            'integration_risk'
        ],
        'has_security_keywords': False,
        'has_schema_changes': True,
        'is_hotfix': False,
    }


@pytest.fixture
def edge_case_missing_metadata_data() -> Dict[str, Any]:
    """
    Edge case: Task with missing metadata fields.

    Tests graceful degradation and default value handling.
    """
    return {
        'task_id': 'TASK-EDGE-MISSING-001',
        'title': 'Minimal task definition',
        'requirements': ['REQ-MIN-001'],
        'files_to_create': [
            'src/minimal.py'
        ],
        # Missing many optional fields
        'patterns_detected': [],
        'external_dependencies': [],
        'technology_stack': [],
        # Missing: business_criticality, estimated_hours, estimated_loc
        'risk_indicators': [],
        'has_security_keywords': False,
        'has_schema_changes': False,
        'is_hotfix': False,
    }


# Collection fixtures for parametrized tests
@pytest.fixture
def all_task_data(
    simple_task_data,
    medium_task_data,
    complex_task_data
) -> List[Dict[str, Any]]:
    """
    Collection of all standard task complexity levels.

    Useful for parametrized tests across complexity spectrum.
    """
    return [
        simple_task_data,
        medium_task_data,
        complex_task_data
    ]


@pytest.fixture
def all_boundary_data(
    boundary_low_to_medium_data,
    boundary_medium_to_high_data
) -> List[Dict[str, Any]]:
    """
    Collection of all boundary condition test data.

    Useful for testing threshold behavior.
    """
    return [
        boundary_low_to_medium_data,
        boundary_medium_to_high_data
    ]


@pytest.fixture
def all_force_trigger_data(
    force_trigger_security_data,
    force_trigger_schema_data,
    force_trigger_hotfix_data
) -> List[Dict[str, Any]]:
    """
    Collection of all force-review trigger scenarios.

    Useful for testing trigger detection and override logic.
    """
    return [
        force_trigger_security_data,
        force_trigger_schema_data,
        force_trigger_hotfix_data
    ]


@pytest.fixture
def all_edge_case_data(
    edge_case_zero_files_data,
    edge_case_many_files_data,
    edge_case_missing_metadata_data
) -> List[Dict[str, Any]]:
    """
    Collection of all edge case scenarios.

    Useful for testing robustness and error handling.
    """
    return [
        edge_case_zero_files_data,
        edge_case_many_files_data,
        edge_case_missing_metadata_data
    ]
