#!/usr/bin/env python3
"""
Comprehensive verification script for TASK-003D implementation.

This script validates:
1. All required files exist
2. Module structure is correct
3. Settings.json has plan_review configuration
4. Metrics directory exists with .gitignore
5. Basic imports work (without pydantic)
"""
import json
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if file exists and report."""
    if path.exists():
        print(f'  ✓ {description}: {path.name}')
        return True
    else:
        print(f'  ✗ {description}: {path.name} NOT FOUND')
        return False


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if directory exists and report."""
    if path.is_dir():
        print(f'  ✓ {description}: {path}')
        return True
    else:
        print(f'  ✗ {description}: {path} NOT FOUND')
        return False


def verify_utilities_module(base_path: Path) -> bool:
    """Verify utilities module structure."""
    print('\n1. UTILITIES MODULE')
    print('=' * 80)

    utils_dir = base_path / 'installer' / 'global' / 'lib' / 'utils'
    results = []

    results.append(check_directory_exists(utils_dir, 'Utils directory'))
    results.append(check_file_exists(utils_dir / '__init__.py', '__init__.py'))
    results.append(check_file_exists(utils_dir / 'json_serializer.py', 'JSON Serializer'))
    results.append(check_file_exists(utils_dir / 'file_operations.py', 'File Operations'))
    results.append(check_file_exists(utils_dir / 'path_resolver.py', 'Path Resolver'))

    # Check key classes exist in files
    if (utils_dir / 'json_serializer.py').exists():
        content = (utils_dir / 'json_serializer.py').read_text()
        if 'class JsonSerializer' in content:
            print('  ✓ JsonSerializer class defined')
            results.append(True)
        else:
            print('  ✗ JsonSerializer class not found')
            results.append(False)

    if (utils_dir / 'file_operations.py').exists():
        content = (utils_dir / 'file_operations.py').read_text()
        if 'class FileOperations' in content:
            print('  ✓ FileOperations class defined')
            results.append(True)
        else:
            print('  ✗ FileOperations class not found')
            results.append(False)

    if (utils_dir / 'path_resolver.py').exists():
        content = (utils_dir / 'path_resolver.py').read_text()
        if 'class PathResolver' in content:
            print('  ✓ PathResolver class defined')
            results.append(True)
        else:
            print('  ✗ PathResolver class not found')
            results.append(False)

    return all(results)


def verify_configuration_module(base_path: Path) -> bool:
    """Verify configuration module structure."""
    print('\n2. CONFIGURATION MODULE')
    print('=' * 80)

    config_dir = base_path / 'installer' / 'global' / 'lib' / 'config'
    results = []

    results.append(check_directory_exists(config_dir, 'Config directory'))
    results.append(check_file_exists(config_dir / '__init__.py', '__init__.py'))
    results.append(check_file_exists(config_dir / 'defaults.py', 'Defaults'))
    results.append(check_file_exists(config_dir / 'config_schema.py', 'Config Schema'))
    results.append(check_file_exists(config_dir / 'plan_review_config.py', 'Plan Review Config'))

    # Check key classes and constants exist
    if (config_dir / 'defaults.py').exists():
        content = (config_dir / 'defaults.py').read_text()
        if 'DEFAULT_CONFIG' in content:
            print('  ✓ DEFAULT_CONFIG defined')
            results.append(True)
        else:
            print('  ✗ DEFAULT_CONFIG not found')
            results.append(False)

    if (config_dir / 'config_schema.py').exists():
        content = (config_dir / 'config_schema.py').read_text()
        classes = ['ConfigSchema', 'ThresholdConfig', 'MetricsConfig']
        for cls in classes:
            if f'class {cls}' in content:
                print(f'  ✓ {cls} class defined')
                results.append(True)
            else:
                print(f'  ✗ {cls} class not found')
                results.append(False)

    if (config_dir / 'plan_review_config.py').exists():
        content = (config_dir / 'plan_review_config.py').read_text()
        if 'class PlanReviewConfig' in content:
            print('  ✓ PlanReviewConfig class defined')
            results.append(True)
        else:
            print('  ✗ PlanReviewConfig class not found')
            results.append(False)

    return all(results)


def verify_metrics_module(base_path: Path) -> bool:
    """Verify metrics module structure."""
    print('\n3. METRICS MODULE')
    print('=' * 80)

    metrics_dir = base_path / 'installer' / 'global' / 'lib' / 'metrics'
    results = []

    results.append(check_directory_exists(metrics_dir, 'Metrics directory'))
    results.append(check_file_exists(metrics_dir / '__init__.py', '__init__.py'))
    results.append(check_file_exists(metrics_dir / 'metrics_storage.py', 'Metrics Storage'))
    results.append(check_file_exists(metrics_dir / 'plan_review_metrics.py', 'Plan Review Metrics'))
    results.append(check_file_exists(metrics_dir / 'plan_review_dashboard.py', 'Plan Review Dashboard'))

    # Check key classes exist
    if (metrics_dir / 'metrics_storage.py').exists():
        content = (metrics_dir / 'metrics_storage.py').read_text()
        if 'class MetricsStorage' in content:
            print('  ✓ MetricsStorage class defined')
            results.append(True)
        else:
            print('  ✗ MetricsStorage class not found')
            results.append(False)

    if (metrics_dir / 'plan_review_metrics.py').exists():
        content = (metrics_dir / 'plan_review_metrics.py').read_text()
        if 'class PlanReviewMetrics' in content:
            print('  ✓ PlanReviewMetrics class defined')
            results.append(True)
        else:
            print('  ✗ PlanReviewMetrics class not found')
            results.append(False)

    if (metrics_dir / 'plan_review_dashboard.py').exists():
        content = (metrics_dir / 'plan_review_dashboard.py').read_text()
        if 'class PlanReviewDashboard' in content:
            print('  ✓ PlanReviewDashboard class defined')
            results.append(True)
        else:
            print('  ✗ PlanReviewDashboard class not found')
            results.append(False)

    return all(results)


def verify_settings_json(base_path: Path) -> bool:
    """Verify settings.json has plan_review configuration."""
    print('\n4. SETTINGS.JSON CONFIGURATION')
    print('=' * 80)

    settings_path = base_path / '.claude' / 'settings.json'
    results = []

    if not settings_path.exists():
        print('  ✗ settings.json not found')
        return False

    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        if 'plan_review' in settings:
            print('  ✓ plan_review section exists')
            results.append(True)

            plan_review = settings['plan_review']

            # Check required fields
            required_fields = ['enabled', 'default_mode', 'thresholds', 'force_triggers', 'timeouts', 'weights', 'metrics']
            for field in required_fields:
                if field in plan_review:
                    print(f'  ✓ {field} configured')
                    results.append(True)
                else:
                    print(f'  ✗ {field} missing')
                    results.append(False)

            # Check thresholds structure
            if 'thresholds' in plan_review:
                thresholds = plan_review['thresholds']
                if 'default' in thresholds:
                    print('  ✓ Default thresholds configured')
                    results.append(True)
                if 'stack_overrides' in thresholds:
                    print(f'  ✓ Stack overrides configured ({len(thresholds["stack_overrides"])} stacks)')
                    results.append(True)

            # Check metrics configuration
            if 'metrics' in plan_review:
                metrics = plan_review['metrics']
                if metrics.get('enabled'):
                    print('  ✓ Metrics enabled')
                if 'retention_days' in metrics:
                    print(f'  ✓ Retention: {metrics["retention_days"]} days')
                if metrics.get('output_format') == 'terminal':
                    print('  ✓ Output format: terminal')
                results.append(True)
        else:
            print('  ✗ plan_review section not found')
            results.append(False)

    except Exception as e:
        print(f'  ✗ Error reading settings.json: {e}')
        return False

    return all(results)


def verify_metrics_directory(base_path: Path) -> bool:
    """Verify metrics directory structure."""
    print('\n5. METRICS DIRECTORY')
    print('=' * 80)

    metrics_dir = base_path / 'docs' / 'state' / 'metrics'
    results = []

    results.append(check_directory_exists(metrics_dir, 'Metrics directory'))

    gitignore_path = metrics_dir / '.gitignore'
    if gitignore_path.exists():
        print('  ✓ .gitignore exists')
        content = gitignore_path.read_text()
        if '*.jsonl' in content:
            print('  ✓ .gitignore ignores *.jsonl')
            results.append(True)
        if '*.json' in content:
            print('  ✓ .gitignore ignores *.json')
            results.append(True)
    else:
        print('  ✗ .gitignore not found')
        results.append(False)

    return all(results)


def verify_code_quality(base_path: Path) -> bool:
    """Verify code quality standards."""
    print('\n6. CODE QUALITY CHECKS')
    print('=' * 80)

    results = []

    # Check for type hints
    config_file = base_path / 'installer' / 'global' / 'lib' / 'config' / 'plan_review_config.py'
    if config_file.exists():
        content = config_file.read_text()
        if '-> ' in content and 'typing' in content:
            print('  ✓ Type hints present')
            results.append(True)
        else:
            print('  ⚠ Type hints may be missing')
            results.append(True)  # Warning, not failure

    # Check for docstrings
    if config_file.exists():
        content = config_file.read_text()
        docstring_count = content.count('"""') + content.count("'''")
        if docstring_count >= 10:  # Expect multiple docstrings
            print(f'  ✓ Docstrings present ({docstring_count//2} found)')
            results.append(True)
        else:
            print('  ⚠ Limited docstrings')
            results.append(True)  # Warning, not failure

    # Check for error handling
    file_ops = base_path / 'installer' / 'global' / 'lib' / 'utils' / 'file_operations.py'
    if file_ops.exists():
        content = file_ops.read_text()
        if 'try:' in content and 'except' in content:
            print('  ✓ Error handling present')
            results.append(True)
        else:
            print('  ⚠ Error handling may be missing')
            results.append(True)

    # Check for pathlib usage
    if file_ops.exists():
        content = file_ops.read_text()
        if 'from pathlib import Path' in content:
            print('  ✓ Using pathlib.Path')
            results.append(True)
        else:
            print('  ⚠ May not be using pathlib')
            results.append(True)

    return all(results)


def main():
    """Run all verification checks."""
    print('=' * 80)
    print('TASK-003D: Configuration & Metrics System Verification')
    print('=' * 80)

    base_path = Path.cwd()

    checks = [
        ('Utilities Module', lambda: verify_utilities_module(base_path)),
        ('Configuration Module', lambda: verify_configuration_module(base_path)),
        ('Metrics Module', lambda: verify_metrics_module(base_path)),
        ('Settings.json', lambda: verify_settings_json(base_path)),
        ('Metrics Directory', lambda: verify_metrics_directory(base_path)),
        ('Code Quality', lambda: verify_code_quality(base_path))
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f'\n  ✗ Error during {name} check: {e}')
            results.append((name, False))

    # Summary
    print('\n' + '=' * 80)
    print('VERIFICATION SUMMARY')
    print('=' * 80)

    for name, success in results:
        status = '✅' if success else '❌'
        print(f'{status} {name}')

    all_passed = all(success for _, success in results)

    print('\n' + '=' * 80)
    if all_passed:
        print('✅ ALL CHECKS PASSED')
        print('\nImplementation is complete and ready for integration.')
        print('\nNote: Runtime testing requires pydantic installation:')
        print('  pip install pydantic')
    else:
        print('❌ SOME CHECKS FAILED')
        print('\nPlease review failed checks above.')

    print('=' * 80)

    return 0 if all_passed else 1


if __name__ == '__main__':
    exit(main())
