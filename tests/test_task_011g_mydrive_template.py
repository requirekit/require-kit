#!/usr/bin/env python3
"""
Comprehensive Test Suite for TASK-011G: Create MyDrive Local Template

This test suite validates that the MyDrive template implementation is correct:
1. File System Validation - All required files exist
2. Manifest Validation - manifest.json is valid and correct
3. Engine Pattern Validation - Templates contain Engine suffix
4. Documentation Validation - Required docs present
5. Settings Validation - MyDrive settings.json updated
6. Validation Script Execution - Run the template's own validation

Stack: Default (technology-agnostic file system operations)
No compilation required - this is a template configuration task
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class TemplateTestSuite:
    """Test suite for MyDrive template validation"""

    def __init__(self):
        self.template_root = Path("/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive/.claude/templates/maui-mydrive")
        self.settings_file = Path("/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive/.claude/settings.json")
        self.results: List[Tuple[str, bool, str]] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def log_result(self, test_name: str, passed: bool, message: str):
        """Log a test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"

        self.results.append((test_name, passed, message))
        print(f"{status}: {test_name}")
        if message:
            print(f"  {message}")

    def test_template_directory_exists(self):
        """Test 1: Template directory exists"""
        exists = self.template_root.exists() and self.template_root.is_dir()
        self.log_result(
            "Template directory exists",
            exists,
            f"Path: {self.template_root}"
        )

    def test_required_directories_exist(self):
        """Test 2: All required subdirectories exist"""
        required_dirs = [
            "agents",
            "src",
            "tests",
            "docs"
        ]

        all_exist = True
        missing = []

        for dir_name in required_dirs:
            dir_path = self.template_root / dir_name
            if not dir_path.exists():
                all_exist = False
                missing.append(dir_name)

        message = f"Required directories: {', '.join(required_dirs)}"
        if missing:
            message += f" | Missing: {', '.join(missing)}"

        self.log_result(
            "Required directories exist",
            all_exist,
            message
        )

    def test_manifest_file_exists(self):
        """Test 3: manifest.json exists"""
        manifest_path = self.template_root / "manifest.json"
        exists = manifest_path.exists()
        self.log_result(
            "manifest.json exists",
            exists,
            f"Path: {manifest_path}"
        )
        return exists

    def test_manifest_valid_json(self):
        """Test 4: manifest.json is valid JSON"""
        manifest_path = self.template_root / "manifest.json"

        try:
            with open(manifest_path, 'r') as f:
                data = json.load(f)
            self.log_result(
                "manifest.json is valid JSON",
                True,
                f"Parsed successfully: {len(data)} top-level keys"
            )
            return data
        except json.JSONDecodeError as e:
            self.log_result(
                "manifest.json is valid JSON",
                False,
                f"JSON parse error: {e}"
            )
            return None
        except Exception as e:
            self.log_result(
                "manifest.json is valid JSON",
                False,
                f"Error reading file: {e}"
            )
            return None

    def test_manifest_schema(self, manifest_data: Dict):
        """Test 5: manifest.json has required schema fields"""
        if manifest_data is None:
            self.log_result(
                "manifest.json schema validation",
                False,
                "Manifest data not available"
            )
            return

        required_fields = [
            "name",
            "version",
            "description",
            "scope",
            "stack",
            "extends",
            "metadata",
            "patterns",
            "templates",
            "agents",
            "quality_gates",
            "conventions",
            "validation",
            "documentation"
        ]

        missing_fields = [field for field in required_fields if field not in manifest_data]

        all_present = len(missing_fields) == 0
        message = f"Required fields: {len(required_fields)}"
        if missing_fields:
            message += f" | Missing: {', '.join(missing_fields)}"

        self.log_result(
            "manifest.json schema validation",
            all_present,
            message
        )

    def test_manifest_scope_local(self, manifest_data: Dict):
        """Test 6: manifest.json has scope='local'"""
        if manifest_data is None:
            self.log_result(
                "manifest.json scope is 'local'",
                False,
                "Manifest data not available"
            )
            return

        scope = manifest_data.get("scope")
        is_local = scope == "local"

        self.log_result(
            "manifest.json scope is 'local'",
            is_local,
            f"Found scope: '{scope}'"
        )

    def test_manifest_stack_mydrive(self, manifest_data: Dict):
        """Test 7: manifest.json has stack='maui-mydrive'"""
        if manifest_data is None:
            self.log_result(
                "manifest.json stack is 'maui-mydrive'",
                False,
                "Manifest data not available"
            )
            return

        stack = manifest_data.get("stack")
        is_correct = stack == "maui-mydrive"

        self.log_result(
            "manifest.json stack is 'maui-mydrive'",
            is_correct,
            f"Found stack: '{stack}'"
        )

    def test_manifest_namespace(self, manifest_data: Dict):
        """Test 8: manifest.json has correct namespace"""
        if manifest_data is None:
            self.log_result(
                "manifest.json namespace configuration",
                False,
                "Manifest data not available"
            )
            return

        metadata = manifest_data.get("metadata", {})
        namespace = metadata.get("namespace")

        is_correct = namespace == "DeCUK.Mobile.MyDrive"

        self.log_result(
            "manifest.json namespace configuration",
            is_correct,
            f"Found namespace: '{namespace}'"
        )

    def test_source_templates_exist(self):
        """Test 9: All source template files exist"""
        expected_files = [
            "src/BaseEngine.cs",
            "src/FeatureEngine.cs",
            "src/IFeatureEngine.cs",
            "src/FeatureViewModelEngine.cs"
        ]

        all_exist = True
        missing = []
        existing = []

        for file_path in expected_files:
            full_path = self.template_root / file_path
            if full_path.exists():
                existing.append(file_path)
            else:
                all_exist = False
                missing.append(file_path)

        message = f"Found {len(existing)}/{len(expected_files)} template files"
        if missing:
            message += f" | Missing: {', '.join(missing)}"

        self.log_result(
            "Source template files exist",
            all_exist,
            message
        )

    def test_test_templates_exist(self):
        """Test 10: All test template files exist"""
        expected_files = [
            "tests/FeatureEngineTests.cs",
            "tests/FeatureViewModelEngineTests.cs",
            "tests/validate-mydrive-template.sh"
        ]

        all_exist = True
        missing = []
        existing = []

        for file_path in expected_files:
            full_path = self.template_root / file_path
            if full_path.exists():
                existing.append(file_path)
            else:
                all_exist = False
                missing.append(file_path)

        message = f"Found {len(existing)}/{len(expected_files)} test files"
        if missing:
            message += f" | Missing: {', '.join(missing)}"

        self.log_result(
            "Test template files exist",
            all_exist,
            message
        )

    def test_documentation_files_exist(self):
        """Test 11: All documentation files exist"""
        expected_files = [
            "docs/README.md",
            "docs/engine-patterns.md",
            "docs/namespace-conventions.md",
            "docs/migration-guide.md"
        ]

        all_exist = True
        missing = []
        existing = []

        for file_path in expected_files:
            full_path = self.template_root / file_path
            if full_path.exists():
                existing.append(file_path)
            else:
                all_exist = False
                missing.append(file_path)

        message = f"Found {len(existing)}/{len(expected_files)} documentation files"
        if missing:
            message += f" | Missing: {', '.join(missing)}"

        self.log_result(
            "Documentation files exist",
            all_exist,
            message
        )

    def test_agent_files_exist(self):
        """Test 12: All agent files exist"""
        expected_files = [
            "agents/engine-pattern-specialist.md",
            "agents/mydrive-architect.md",
            "agents/maui-mydrive-generator.md"
        ]

        all_exist = True
        missing = []
        existing = []

        for file_path in expected_files:
            full_path = self.template_root / file_path
            if full_path.exists():
                existing.append(file_path)
            else:
                all_exist = False
                missing.append(file_path)

        message = f"Found {len(existing)}/{len(expected_files)} agent files"
        if missing:
            message += f" | Missing: {', '.join(missing)}"

        self.log_result(
            "Agent files exist",
            all_exist,
            message
        )

    def test_engine_suffix_in_templates(self):
        """Test 13: Engine templates contain 'Engine' suffix"""
        templates_to_check = [
            ("src/FeatureEngine.cs", "FeatureEngine"),
            ("src/IFeatureEngine.cs", "IFeatureEngine"),
            ("src/FeatureViewModelEngine.cs", "FeatureViewModelEngine")
        ]

        all_correct = True
        issues = []

        for file_path, expected_pattern in templates_to_check:
            full_path = self.template_root / file_path
            if not full_path.exists():
                all_correct = False
                issues.append(f"{file_path} does not exist")
                continue

            try:
                with open(full_path, 'r') as f:
                    content = f.read()

                if "Engine" not in content:
                    all_correct = False
                    issues.append(f"{file_path} missing 'Engine' pattern")
            except Exception as e:
                all_correct = False
                issues.append(f"{file_path} read error: {e}")

        message = f"Checked {len(templates_to_check)} templates"
        if issues:
            message += f" | Issues: {'; '.join(issues)}"

        self.log_result(
            "Engine suffix in templates",
            all_correct,
            message
        )

    def test_namespace_in_templates(self):
        """Test 14: Templates contain DeCUK.Mobile.MyDrive namespace"""
        cs_files = list(self.template_root.glob("**/*.cs"))

        all_correct = True
        missing_namespace = []
        checked = []

        for file_path in cs_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                relative_path = file_path.relative_to(self.template_root)

                if "DeCUK.Mobile.MyDrive" in content:
                    checked.append(str(relative_path))
                else:
                    all_correct = False
                    missing_namespace.append(str(relative_path))
            except Exception as e:
                all_correct = False
                missing_namespace.append(f"{relative_path} (error: {e})")

        message = f"Checked {len(checked)} C# files"
        if missing_namespace:
            message += f" | Missing namespace: {', '.join(missing_namespace)}"

        self.log_result(
            "Namespace in templates",
            all_correct,
            message
        )

    def test_base_engine_inheritance(self):
        """Test 15: Engine templates inherit from BaseEngine"""
        engine_files = [
            "src/FeatureEngine.cs"
        ]

        all_correct = True
        issues = []

        for file_path in engine_files:
            full_path = self.template_root / file_path
            if not full_path.exists():
                all_correct = False
                issues.append(f"{file_path} does not exist")
                continue

            try:
                with open(full_path, 'r') as f:
                    content = f.read()

                if ": BaseEngine" not in content:
                    all_correct = False
                    issues.append(f"{file_path} does not inherit from BaseEngine")
            except Exception as e:
                all_correct = False
                issues.append(f"{file_path} read error: {e}")

        message = f"Checked {len(engine_files)} engine templates"
        if issues:
            message += f" | Issues: {'; '.join(issues)}"

        self.log_result(
            "BaseEngine inheritance in templates",
            all_correct,
            message
        )

    def test_erroror_return_types(self):
        """Test 16: Engine templates use ErrorOr return types"""
        engine_files = [
            "src/FeatureEngine.cs",
            "src/IFeatureEngine.cs"
        ]

        all_correct = True
        issues = []

        for file_path in engine_files:
            full_path = self.template_root / file_path
            if not full_path.exists():
                all_correct = False
                issues.append(f"{file_path} does not exist")
                continue

            try:
                with open(full_path, 'r') as f:
                    content = f.read()

                if "ErrorOr<" not in content:
                    all_correct = False
                    issues.append(f"{file_path} missing ErrorOr<T> return type")
            except Exception as e:
                all_correct = False
                issues.append(f"{file_path} read error: {e}")

        message = f"Checked {len(engine_files)} engine templates"
        if issues:
            message += f" | Issues: {'; '.join(issues)}"

        self.log_result(
            "ErrorOr return types in templates",
            all_correct,
            message
        )

    def test_settings_json_exists(self):
        """Test 17: MyDrive settings.json exists"""
        exists = self.settings_file.exists()
        self.log_result(
            "MyDrive settings.json exists",
            exists,
            f"Path: {self.settings_file}"
        )
        return exists

    def test_settings_json_valid(self):
        """Test 18: MyDrive settings.json is valid JSON"""
        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
            self.log_result(
                "MyDrive settings.json is valid JSON",
                True,
                f"Parsed successfully: {len(data)} top-level keys"
            )
            return data
        except json.JSONDecodeError as e:
            self.log_result(
                "MyDrive settings.json is valid JSON",
                False,
                f"JSON parse error: {e}"
            )
            return None
        except Exception as e:
            self.log_result(
                "MyDrive settings.json is valid JSON",
                False,
                f"Error reading file: {e}"
            )
            return None

    def test_settings_local_template_configured(self, settings_data: Dict):
        """Test 19: settings.json has local_template configured"""
        if settings_data is None:
            self.log_result(
                "settings.json local_template configured",
                False,
                "Settings data not available"
            )
            return

        local_template = settings_data.get("local_template")
        is_configured = local_template == ".claude/templates/maui-mydrive"

        message = f"Found local_template: '{local_template}'"

        self.log_result(
            "settings.json local_template configured",
            is_configured,
            message
        )

    def test_settings_template_maui_mydrive(self, settings_data: Dict):
        """Test 20: settings.json project template is 'maui-mydrive'"""
        if settings_data is None:
            self.log_result(
                "settings.json template is 'maui-mydrive'",
                False,
                "Settings data not available"
            )
            return

        project = settings_data.get("project", {})
        template = project.get("template")
        is_correct = template == "maui-mydrive"

        message = f"Found template: '{template}'"

        self.log_result(
            "settings.json template is 'maui-mydrive'",
            is_correct,
            message
        )

    def test_validation_script_exists(self):
        """Test 21: Validation script exists and is executable"""
        script_path = self.template_root / "tests" / "validate-mydrive-template.sh"

        exists = script_path.exists()
        is_executable = os.access(script_path, os.X_OK) if exists else False

        passed = exists and is_executable

        message = f"Path: {script_path}"
        if exists and not is_executable:
            message += " | File exists but is not executable"
        elif not exists:
            message += " | File does not exist"

        self.log_result(
            "Validation script exists and is executable",
            passed,
            message
        )

        return passed

    def test_run_validation_script(self):
        """Test 22: Execute the template's validation script"""
        script_path = self.template_root / "tests" / "validate-mydrive-template.sh"

        if not script_path.exists():
            self.log_result(
                "Run validation script",
                False,
                "Script does not exist"
            )
            return

        try:
            # Run the validation script
            result = subprocess.run(
                ['bash', str(script_path)],
                capture_output=True,
                text=True,
                timeout=30
            )

            passed = result.returncode == 0

            # Capture key output lines
            output_lines = result.stdout.split('\n')
            summary_lines = [line for line in output_lines if '✅' in line or '❌' in line or 'passed' in line.lower()]

            message = f"Exit code: {result.returncode}"
            if summary_lines:
                message += f" | Summary: {len([l for l in summary_lines if '✅' in l])} checks passed"

            self.log_result(
                "Run validation script",
                passed,
                message
            )

            # Print full validation output
            print("\n" + "="*60)
            print("VALIDATION SCRIPT OUTPUT:")
            print("="*60)
            print(result.stdout)
            if result.stderr:
                print("\nSTDERR:")
                print(result.stderr)
            print("="*60 + "\n")

        except subprocess.TimeoutExpired:
            self.log_result(
                "Run validation script",
                False,
                "Script execution timeout (>30s)"
            )
        except Exception as e:
            self.log_result(
                "Run validation script",
                False,
                f"Error executing script: {e}"
            )

    def test_file_count_correct(self):
        """Test 23: Verify total file count matches expectations"""
        # Count all files in the template
        all_files = list(self.template_root.glob("**/*"))
        file_count = len([f for f in all_files if f.is_file()])

        # Expected: 15 files based on task description
        # manifest.json + 4 src templates + 3 test files + 4 docs + 3 agents = 15
        expected_min = 15

        passed = file_count >= expected_min

        message = f"Found {file_count} files (expected at least {expected_min})"

        self.log_result(
            "File count correct",
            passed,
            message
        )

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("="*70)
        print("TASK-011G: MyDrive Template Test Suite")
        print("="*70)
        print(f"Template Root: {self.template_root}")
        print(f"Settings File: {self.settings_file}")
        print("="*70)
        print()

        # Phase 1: File System Validation
        print("📁 PHASE 1: FILE SYSTEM VALIDATION")
        print("-"*70)
        self.test_template_directory_exists()
        self.test_required_directories_exist()
        self.test_file_count_correct()
        print()

        # Phase 2: Manifest Validation
        print("📄 PHASE 2: MANIFEST VALIDATION")
        print("-"*70)
        manifest_exists = self.test_manifest_file_exists()
        manifest_data = None
        if manifest_exists:
            manifest_data = self.test_manifest_valid_json()
            if manifest_data:
                self.test_manifest_schema(manifest_data)
                self.test_manifest_scope_local(manifest_data)
                self.test_manifest_stack_mydrive(manifest_data)
                self.test_manifest_namespace(manifest_data)
        print()

        # Phase 3: Template Files Validation
        print("📝 PHASE 3: TEMPLATE FILES VALIDATION")
        print("-"*70)
        self.test_source_templates_exist()
        self.test_test_templates_exist()
        self.test_documentation_files_exist()
        self.test_agent_files_exist()
        print()

        # Phase 4: Engine Pattern Validation
        print("⚙️  PHASE 4: ENGINE PATTERN VALIDATION")
        print("-"*70)
        self.test_engine_suffix_in_templates()
        self.test_namespace_in_templates()
        self.test_base_engine_inheritance()
        self.test_erroror_return_types()
        print()

        # Phase 5: Settings Validation
        print("⚙️  PHASE 5: SETTINGS VALIDATION")
        print("-"*70)
        settings_exists = self.test_settings_json_exists()
        settings_data = None
        if settings_exists:
            settings_data = self.test_settings_json_valid()
            if settings_data:
                self.test_settings_local_template_configured(settings_data)
                self.test_settings_template_maui_mydrive(settings_data)
        print()

        # Phase 6: Validation Script Execution
        print("🔧 PHASE 6: VALIDATION SCRIPT EXECUTION")
        print("-"*70)
        script_exists = self.test_validation_script_exists()
        if script_exists:
            self.test_run_validation_script()
        print()

        # Final Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests:  {self.total_tests}")
        print(f"Passed:       {self.passed_tests} ✅")
        print(f"Failed:       {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print("="*70)

        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            print("-"*70)
            for test_name, passed, message in self.results:
                if not passed:
                    print(f"  • {test_name}")
                    if message:
                        print(f"    {message}")
            print()

        # Final verdict
        if self.failed_tests == 0:
            print("✅ ALL TESTS PASSED - Template is ready for use!")
            return 0
        else:
            print(f"❌ {self.failed_tests} TEST(S) FAILED - Please review issues above")
            return 1


def main():
    """Main entry point"""
    suite = TemplateTestSuite()
    exit_code = suite.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
