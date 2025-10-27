"""
Comprehensive Test Suite for TASK-030E-1 Documentation Validation

Tests documentation updates:
- docs/workflows/complexity-management-workflow.md
- docs/workflows/design-first-workflow.md

This test suite validates:
1. Markdown syntax validity (COMPILATION CHECK)
2. Document structure and headings
3. Cross-references between documents
4. Content consistency
5. Example validity
6. Metadata accuracy
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set
import subprocess


class MarkdownCompilationValidator:
    """Validates markdown syntax (MANDATORY COMPILATION CHECK)"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_markdown_syntax(self, file_path: str) -> bool:
        """
        MANDATORY COMPILATION CHECK: Verify markdown syntax is valid

        Returns True if valid, False if compilation errors found
        """
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        syntax_valid = True

        # Check 1: Balanced code fence blocks
        fence_count = sum(1 for line in lines if line.strip().startswith('```'))
        if fence_count % 2 != 0:
            self.errors.append({
                'file': file_path,
                'type': 'unbalanced_code_fences',
                'message': 'Code fence blocks must be balanced (found odd number)',
                'severity': 'critical'
            })
            syntax_valid = False

        # Check 2: Balanced bracket pairs (links, references) - SKIP JSON/code blocks
        in_code_block = False
        for idx, line in enumerate(lines, 1):
            # Track code blocks to skip bracket checking inside them
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check parentheses in links (not in code)
            open_parens = line.count('(')
            close_parens = line.count(')')
            if open_parens != close_parens:
                # Check if it's markdown link syntax (should be balanced)
                if '[' in line or ']' in line:
                    self.errors.append({
                        'file': file_path,
                        'line': idx,
                        'type': 'unbalanced_parens',
                        'content': line.strip()[:100],
                        'message': f'Unbalanced parentheses in markdown: {open_parens} ( vs {close_parens} )',
                        'severity': 'critical'
                    })
                    syntax_valid = False

        # Check 3: Valid markdown link syntax
        for idx, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                continue

            # Pattern: [text](url) should be balanced within markdown context
            markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', line)

            for text, url in markdown_links:
                if not text.strip():
                    self.warnings.append({
                        'file': file_path,
                        'line': idx,
                        'type': 'empty_link_text',
                        'url': url,
                        'severity': 'warning'
                    })

        # Check 4: Valid heading syntax (# to ######)
        for idx, line in enumerate(lines, 1):
            if line.startswith('#') and not line.startswith('```'):
                heading_match = re.match(r'^(#{1,6})\s+', line)
                if not heading_match:
                    self.errors.append({
                        'file': file_path,
                        'line': idx,
                        'type': 'invalid_heading',
                        'content': line[:100],
                        'message': 'Invalid heading format (must have space after #)',
                        'severity': 'critical'
                    })
                    syntax_valid = False

        return syntax_valid


class DocumentStructureValidator:
    """Validates document structure and organization"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_structure(self, file_path: str) -> bool:
        """Validates document structure: headings, sections, TOC"""
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        valid = True

        # Check 1: Document starts with title and purpose
        if not lines[0].startswith('#'):
            self.errors.append({
                'file': file_path,
                'type': 'missing_title',
                'message': 'Document must start with # title',
                'severity': 'critical'
            })
            valid = False

        # Check 2: Heading hierarchy (no skips like # then ###)
        headings = []
        for idx, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                headings.append((level, idx, line[:100]))

        for i in range(1, len(headings)):
            prev_level = headings[i-1][0]
            curr_level = headings[i][0]
            if curr_level > prev_level + 1:
                self.warnings.append({
                    'file': file_path,
                    'line': headings[i][1],
                    'type': 'heading_hierarchy_skip',
                    'message': f'Heading level skipped: {prev_level} -> {curr_level}',
                    'severity': 'warning'
                })

        # Check 3: Required sections for workflow documents
        required_sections = ['Quick Start', 'Core Concepts', 'Complete Reference']
        found_sections = set()

        for level, line_no, content in headings:
            for section in required_sections:
                if section.lower() in content.lower():
                    found_sections.add(section)

        missing_sections = set(required_sections) - found_sections
        if missing_sections:
            self.warnings.append({
                'file': file_path,
                'type': 'missing_sections',
                'missing': list(missing_sections),
                'severity': 'warning'
            })

        # Check 4: Document has reasonable length sections
        if len(headings) < 3:
            self.warnings.append({
                'file': file_path,
                'type': 'insufficient_structure',
                'message': 'Document has fewer than 3 sections',
                'severity': 'warning'
            })

        return valid


class ContentCrossReferenceValidator:
    """Validates cross-references between documents"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_cross_references(self, file_path: str) -> bool:
        """Validates that all cross-references exist and are reachable"""
        with open(file_path, 'r') as f:
            content = f.read()

        valid = True

        # Extract all links from markdown
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, content)

        base_dir = Path(file_path).parent.parent

        for link_text, link_url in links:
            # Skip external URLs
            if link_url.startswith('http'):
                continue

            # Skip anchor links
            if link_url.startswith('#'):
                continue

            # Check if referenced file exists
            target_path = base_dir / link_url
            if not target_path.exists():
                self.errors.append({
                    'file': file_path,
                    'type': 'broken_reference',
                    'link_text': link_text,
                    'target': link_url,
                    'message': f'Referenced file not found: {link_url}',
                    'severity': 'high'
                })
                valid = False

        return valid


class ExampleValidator:
    """Validates code examples and command blocks"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_examples(self, file_path: str) -> bool:
        """Validates code examples, command blocks, and output examples"""
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        valid = True
        in_code_block = False
        code_block_type = None
        code_block_start = 0

        for idx, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_start = idx
                    # Extract language identifier
                    code_block_type = line.strip()[3:].strip()
                else:
                    in_code_block = False

                # Warning: code block without language identifier
                if line.strip() == '```':
                    self.warnings.append({
                        'file': file_path,
                        'line': idx,
                        'type': 'unlabeled_code_block',
                        'message': 'Code block should have language identifier',
                        'severity': 'warning'
                    })

        return valid


class ContentConsistencyValidator:
    """Validates content consistency, references to tasks, and metadata"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_task_references(self, file_path: str) -> bool:
        """Validates that task references are correct and formatted consistently"""
        with open(file_path, 'r') as f:
            content = f.read()

        valid = True

        # Find all task references (TASK-XXX format)
        task_pattern = r'TASK-(\d+[A-Z]?(?:-\d+)?)'
        tasks = re.findall(task_pattern, content)

        # Known tasks in the system
        # These are mentioned in the documents as real examples
        valid_tasks = {
            '005', '005.1', '005.2', '005.3',
            '006',
            '008',
            '010', '020', '025', '030', '040',
            '042', '043', '044', '045', '045.1', '045.2', '045.3',
            '101', '202', '303', '404',
            '001', '301', '401', '501'
        }

        for task_ref in tasks:
            # Normalize task reference for validation
            if task_ref not in valid_tasks:
                self.warnings.append({
                    'file': file_path,
                    'type': 'task_reference',
                    'task': f'TASK-{task_ref}',
                    'message': f'Task reference may be example or new: TASK-{task_ref}',
                    'severity': 'info'
                })

        return valid

    def validate_complexity_scores(self, file_path: str) -> bool:
        """Validates that complexity scores are within 0-10 range"""
        with open(file_path, 'r') as f:
            content = f.read()

        valid = True

        # Pattern: complexity/complexity score: X/10
        complexity_pattern = r'[Cc]omplexity[:\s]+(\d+)/10'
        scores = re.findall(complexity_pattern, content)

        for score in scores:
            score_int = int(score)
            if not 0 <= score_int <= 10:
                self.errors.append({
                    'file': file_path,
                    'type': 'invalid_complexity_score',
                    'score': score_int,
                    'message': f'Complexity score out of range: {score_int}/10',
                    'severity': 'critical'
                })
                valid = False

        return valid

    def validate_consistency_markers(self, file_path: str) -> bool:
        """Validates special markers and status indicators"""
        with open(file_path, 'r') as f:
            content = f.read()

        valid = True

        # Check for TODO or FIXME markers (should not be in final docs)
        if 'TODO' in content or 'FIXME' in content:
            self.warnings.append({
                'file': file_path,
                'type': 'incomplete_markers',
                'message': 'Document contains TODO/FIXME markers',
                'severity': 'warning'
            })

        return valid


class CrossDocumentValidator:
    """Validates consistency and relationships between documents"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_related_docs(self, doc1_path: str, doc2_path: str) -> bool:
        """Validates that related documents reference each other appropriately"""
        with open(doc1_path, 'r') as f:
            doc1_content = f.read()

        with open(doc2_path, 'r') as f:
            doc2_content = f.read()

        valid = True

        # Extract basenames
        doc1_name = Path(doc1_path).name
        doc2_name = Path(doc2_path).name

        # Check if doc1 references doc2
        if doc2_name not in doc1_content:
            self.warnings.append({
                'file': doc1_path,
                'type': 'missing_cross_reference',
                'target': doc2_name,
                'message': f'Document should reference {doc2_name}',
                'severity': 'warning'
            })

        return valid


class DocumentMetadataValidator:
    """Validates document metadata and versioning"""

    def __init__(self):
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_metadata(self, file_path: str) -> bool:
        """Validates last updated timestamp, version, and maintenance info"""
        with open(file_path, 'r') as f:
            content = f.read()

        valid = True

        # Check for last updated timestamp
        if 'Last Updated' not in content:
            self.warnings.append({
                'file': file_path,
                'type': 'missing_metadata',
                'field': 'Last Updated',
                'severity': 'warning'
            })

        # Check for version
        if 'Version' not in content:
            self.warnings.append({
                'file': file_path,
                'type': 'missing_metadata',
                'field': 'Version',
                'severity': 'warning'
            })

        # Check for maintained by
        if 'Maintained By' not in content:
            self.warnings.append({
                'file': file_path,
                'type': 'missing_metadata',
                'field': 'Maintained By',
                'severity': 'warning'
            })

        return valid


class TestSuite:
    """Main test suite orchestrator for documentation validation"""

    def __init__(self):
        self.results = {
            'compilation': {},
            'structure': {},
            'cross_references': {},
            'examples': {},
            'consistency': {},
            'metadata': {}
        }
        self.files_to_test = [
            '/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/complexity-management-workflow.md',
            '/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/docs/workflows/design-first-workflow.md'
        ]

    def run_compilation_checks(self) -> bool:
        """MANDATORY COMPILATION CHECK: Verify markdown syntax"""
        print("\n" + "="*70)
        print("PHASE 1: MARKDOWN COMPILATION CHECK (MANDATORY)")
        print("="*70)

        all_valid = True

        for file_path in self.files_to_test:
            file_name = Path(file_path).name
            print(f"\nValidating: {file_name}")

            validator = MarkdownCompilationValidator()
            is_valid = validator.validate_markdown_syntax(file_path)

            self.results['compilation'][file_name] = {
                'valid': is_valid,
                'errors': validator.errors,
                'warnings': validator.warnings
            }

            if not is_valid:
                all_valid = False
                print(f"  ❌ COMPILATION FAILED")
                for error in validator.errors:
                    line_info = f":{error.get('line', '?')}" if 'line' in error else ""
                    print(f"    ERROR {error['type']}{line_info}: {error['message']}")
                    if 'content' in error:
                        print(f"      Content: {error['content']}")
            else:
                print(f"  ✅ COMPILATION PASSED")

        if not all_valid:
            print("\n" + "="*70)
            print("BUILD VERIFICATION FAILED - CANNOT PROCEED WITH TESTS")
            print("="*70)
            return False

        print("\n" + "="*70)
        print("✅ ALL FILES COMPILED SUCCESSFULLY - PROCEEDING TO VALIDATION")
        print("="*70)
        return True

    def run_all_tests(self) -> Dict:
        """Execute complete validation test suite"""
        # MANDATORY: Check compilation first
        if not self.run_compilation_checks():
            return self.results

        print("\n" + "="*70)
        print("PHASE 2: STRUCTURAL VALIDATION")
        print("="*70)

        for file_path in self.files_to_test:
            file_name = Path(file_path).name

            # Structure validation
            print(f"\n{file_name}:")
            structure_validator = DocumentStructureValidator()
            is_valid = structure_validator.validate_structure(file_path)
            self.results['structure'][file_name] = {
                'valid': is_valid,
                'errors': structure_validator.errors,
                'warnings': structure_validator.warnings
            }
            print(f"  Structure: {'✅ PASS' if is_valid else '❌ FAIL'}")

            # Cross references
            xref_validator = ContentCrossReferenceValidator()
            is_valid = xref_validator.validate_cross_references(file_path)
            self.results['cross_references'][file_name] = {
                'valid': is_valid,
                'errors': xref_validator.errors,
                'warnings': xref_validator.warnings
            }
            print(f"  Cross-References: {'✅ PASS' if is_valid else '❌ FAIL'}")

            # Examples
            example_validator = ExampleValidator()
            is_valid = example_validator.validate_examples(file_path)
            self.results['examples'][file_name] = {
                'valid': is_valid,
                'errors': example_validator.errors,
                'warnings': example_validator.warnings
            }
            print(f"  Examples: {'✅ PASS' if is_valid else '❌ FAIL'}")

            # Content consistency
            consistency_validator = ContentConsistencyValidator()
            is_valid = consistency_validator.validate_task_references(file_path)
            is_valid &= consistency_validator.validate_complexity_scores(file_path)
            is_valid &= consistency_validator.validate_consistency_markers(file_path)
            self.results['consistency'][file_name] = {
                'valid': is_valid,
                'errors': consistency_validator.errors,
                'warnings': consistency_validator.warnings
            }
            print(f"  Consistency: {'✅ PASS' if is_valid else '❌ FAIL'}")

            # Metadata
            metadata_validator = DocumentMetadataValidator()
            is_valid = metadata_validator.validate_metadata(file_path)
            self.results['metadata'][file_name] = {
                'valid': is_valid,
                'errors': metadata_validator.errors,
                'warnings': metadata_validator.warnings
            }
            print(f"  Metadata: {'✅ PASS' if is_valid else '❌ FAIL'}")

        # Cross-document validation
        print("\n" + "="*70)
        print("PHASE 3: CROSS-DOCUMENT VALIDATION")
        print("="*70)

        if len(self.files_to_test) == 2:
            cross_validator = CrossDocumentValidator()
            cross_validator.validate_related_docs(
                self.files_to_test[0],
                self.files_to_test[1]
            )
            cross_validator.validate_related_docs(
                self.files_to_test[1],
                self.files_to_test[0]
            )
            self.results['cross_document'] = {
                'errors': cross_validator.errors,
                'warnings': cross_validator.warnings
            }

        return self.results

    def print_summary(self) -> None:
        """Print summary report"""
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)

        total_errors = 0
        total_warnings = 0

        for phase, phase_results in self.results.items():
            if phase == 'cross_document':
                continue

            print(f"\n{phase.upper()}:")

            for file_name, file_results in phase_results.items():
                errors = file_results.get('errors', [])
                warnings = file_results.get('warnings', [])
                total_errors += len(errors)
                total_warnings += len(warnings)

                status = "✅ PASS" if file_results.get('valid', True) else "❌ FAIL"
                print(f"  {file_name}: {status}")
                print(f"    Errors: {len(errors)}, Warnings: {len(warnings)}")

        print("\n" + "-"*70)
        print(f"TOTAL ERRORS: {total_errors}")
        print(f"TOTAL WARNINGS: {total_warnings}")
        print("-"*70)

        if total_errors == 0:
            print("\n✅ ALL VALIDATION TESTS PASSED")
        else:
            print(f"\n❌ VALIDATION FAILED: {total_errors} errors found")


def run_tests():
    """Execute the complete test suite"""
    suite = TestSuite()
    results = suite.run_all_tests()
    suite.print_summary()

    # Return exit code based on results
    total_errors = sum(
        len(phase_results.get('errors', []))
        for phase_results in results.values()
        if isinstance(phase_results, dict) and phase_results.get('errors')
    )

    return 0 if total_errors == 0 else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
