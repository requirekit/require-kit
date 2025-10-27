#!/usr/bin/env python3
"""Test script to verify all imports work correctly."""
import sys
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent / 'installer' / 'global' / 'lib'
sys.path.insert(0, str(lib_path))

def test_utilities():
    """Test utilities module imports."""
    print('Testing utilities module...')
    from utils import JsonSerializer, FileOperations, PathResolver
    print('✓ Utilities module imports successfully')
    return True

def test_configuration():
    """Test configuration module imports."""
    print('\nTesting configuration module...')
    try:
        from config import PlanReviewConfig, ConfigSchema, ThresholdConfig, MetricsConfig, DEFAULT_CONFIG
        print('✓ Configuration module imports successfully')
        return True
    except ImportError as e:
        print(f'⚠ Configuration module requires pydantic: {e}')
        print('  Install with: pip install pydantic')
        return False

def test_metrics():
    """Test metrics module imports."""
    print('\nTesting metrics module...')
    try:
        from metrics import PlanReviewMetrics, PlanReviewDashboard
        print('✓ Metrics module imports successfully')
        return True
    except ImportError as e:
        print(f'⚠ Metrics module requires dependencies: {e}')
        return False

def test_configuration_functionality():
    """Test configuration initialization."""
    print('\nTesting configuration initialization...')
    try:
        from config import PlanReviewConfig
        from utils import PathResolver

        config = PlanReviewConfig()
        print(f'  Enabled: {config.is_enabled()}')
        print(f'  Mode: {config.get_mode()}')
        print(f'  Metrics enabled: {config.is_metrics_enabled()}')
        print('✓ Configuration initialized successfully')

        # Test path resolution
        print('\nTesting path resolution...')
        settings_path = PathResolver.get_settings_path()
        metrics_dir = PathResolver.get_metrics_dir()
        print(f'  Settings path: {settings_path}')
        print(f'  Metrics dir: {metrics_dir}')
        print('✓ Path resolution working')

        return True
    except Exception as e:
        print(f'⚠ Configuration functionality test failed: {e}')
        return False

if __name__ == '__main__':
    print('=' * 80)
    print('TASK-003D Import Verification Test')
    print('=' * 80)

    results = []
    results.append(('Utilities', test_utilities()))
    results.append(('Configuration', test_configuration()))
    results.append(('Metrics', test_metrics()))

    # Only test functionality if imports succeeded
    if results[1][1]:  # If configuration imports succeeded
        results.append(('Configuration Functionality', test_configuration_functionality()))

    print('\n' + '=' * 80)
    print('Test Results Summary')
    print('=' * 80)

    for name, success in results:
        status = '✅' if success else '⚠'
        print(f'{status} {name}')

    all_critical_passed = all(success for name, success in results if name in ['Utilities', 'Configuration', 'Metrics'])

    if all_critical_passed:
        print('\n✅ All critical imports verified successfully!')
    else:
        print('\n⚠ Some imports require dependencies (pydantic)')
        print('   Install with: pip install pydantic')
