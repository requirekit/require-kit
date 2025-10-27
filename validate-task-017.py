#!/usr/bin/env python3
"""
TASK-017 Validation Script
Validates agent model configuration implementation
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []

    def add_error(self, msg):
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_success(self, msg):
        self.successes.append(msg)

    def is_valid(self):
        return len(self.errors) == 0

    def print_summary(self):
        print(f"\n{'='*80}")
        print(f"{BLUE}VALIDATION SUMMARY{RESET}")
        print(f"{'='*80}\n")

        if self.successes:
            print(f"{GREEN}✓ SUCCESSES ({len(self.successes)}):{RESET}")
            for success in self.successes:
                print(f"  {GREEN}✓{RESET} {success}")
            print()

        if self.warnings:
            print(f"{YELLOW}⚠ WARNINGS ({len(self.warnings)}):{RESET}")
            for warning in self.warnings:
                print(f"  {YELLOW}⚠{RESET} {warning}")
            print()

        if self.errors:
            print(f"{RED}✗ ERRORS ({len(self.errors)}):{RESET}")
            for error in self.errors:
                print(f"  {RED}✗{RESET} {error}")
            print()

        print(f"{'='*80}")
        if self.is_valid():
            print(f"{GREEN}VALIDATION PASSED{RESET}")
        else:
            print(f"{RED}VALIDATION FAILED{RESET}")
        print(f"{'='*80}\n")

        return 0 if self.is_valid() else 1

def extract_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from markdown content"""
    pattern = r'^---\s*\n(.*?\n)---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, content

    frontmatter_str = match.group(1)
    body = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter, body
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in frontmatter: {e}")

def validate_agent_file(file_path: Path, result: ValidationResult):
    """Validate a single agent file"""
    agent_name = file_path.stem

    print(f"\n{BLUE}Validating:{RESET} {agent_name}")

    try:
        content = file_path.read_text()

        # Extract frontmatter
        try:
            frontmatter, body = extract_frontmatter(content)
        except ValueError as e:
            result.add_error(f"{agent_name}: {e}")
            return

        if frontmatter is None:
            result.add_error(f"{agent_name}: No frontmatter found")
            return

        # Validate required fields
        if 'model' not in frontmatter:
            result.add_error(f"{agent_name}: Missing 'model' field")
            return

        if 'model_rationale' not in frontmatter:
            result.add_error(f"{agent_name}: Missing 'model_rationale' field")
            return

        # Validate model value
        model = frontmatter['model']
        if model not in ['haiku', 'sonnet']:
            result.add_error(f"{agent_name}: Invalid model '{model}' (must be 'haiku' or 'sonnet')")
            return

        # Validate rationale is not placeholder
        rationale = frontmatter['model_rationale']
        if not rationale or len(rationale.strip()) < 20:
            result.add_warning(f"{agent_name}: Model rationale seems too short or empty")

        placeholder_phrases = [
            'TODO', 'PLACEHOLDER', 'TBD', 'to be determined',
            'needs configuration', 'update this'
        ]
        if any(phrase.lower() in rationale.lower() for phrase in placeholder_phrases):
            result.add_warning(f"{agent_name}: Model rationale appears to be a placeholder")

        # Validate other expected fields
        expected_fields = ['agent_type', 'domain', 'purpose', 'capabilities', 'dependencies']
        for field in expected_fields:
            if field not in frontmatter:
                result.add_warning(f"{agent_name}: Missing optional field '{field}'")

        result.add_success(f"{agent_name}: Valid (model={model})")
        return model

    except Exception as e:
        result.add_error(f"{agent_name}: Unexpected error - {e}")
        return None

def validate_documentation(result: ValidationResult):
    """Validate required documentation files"""
    base_path = Path("/Users/richardwoollcott/Projects/appmilla_github/ai-engineer")

    docs_to_check = [
        ("docs/guides/model-optimization-guide.md", "Model Optimization Guide"),
        ("docs/MODEL-ASSIGNMENT-MATRIX.md", "Model Assignment Matrix"),
        ("docs/TASK-017-VERIFICATION-REPORT.md", "Verification Report"),
        ("TASK-017-IMPLEMENTATION-SUMMARY.md", "Implementation Summary")
    ]

    print(f"\n{BLUE}Validating Documentation:{RESET}")

    for file_path, doc_name in docs_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            if size > 100:  # At least 100 bytes
                result.add_success(f"{doc_name}: Exists and has content ({size} bytes)")
            else:
                result.add_warning(f"{doc_name}: Exists but seems empty ({size} bytes)")
        else:
            result.add_error(f"{doc_name}: Missing at {file_path}")

def main():
    print(f"{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TASK-017 IMPLEMENTATION VALIDATION{RESET}")
    print(f"{BLUE}Optimize Agent Model Configuration{RESET}")
    print(f"{BLUE}{'='*80}{RESET}")

    result = ValidationResult()

    # Find all agent files
    agents_dir = Path("/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/agents")
    agent_files = sorted(agents_dir.glob("*.md"))

    print(f"\nFound {len(agent_files)} agent files to validate")

    # Track model distribution
    model_distribution = {'haiku': [], 'sonnet': []}

    # Validate each agent file
    for agent_file in agent_files:
        model = validate_agent_file(agent_file, result)
        if model:
            model_distribution[model].append(agent_file.stem)

    # Print model distribution
    print(f"\n{BLUE}Model Distribution:{RESET}")
    print(f"  Haiku agents: {len(model_distribution['haiku'])}")
    for agent in model_distribution['haiku']:
        print(f"    - {agent}")
    print(f"  Sonnet agents: {len(model_distribution['sonnet'])}")
    for agent in model_distribution['sonnet']:
        print(f"    - {agent}")

    # Validate expected distribution
    if len(model_distribution['haiku']) < 3:
        result.add_warning(f"Only {len(model_distribution['haiku'])} Haiku agents (expected 5-6)")
    if len(model_distribution['sonnet']) < 8:
        result.add_warning(f"Only {len(model_distribution['sonnet'])} Sonnet agents (expected 11)")

    # Validate documentation
    validate_documentation(result)

    # Print summary and exit with appropriate code
    return result.print_summary()

if __name__ == "__main__":
    sys.exit(main())
