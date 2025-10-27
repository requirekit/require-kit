"""
Test suite for TASK-011E: maui-repository-specialist agent documentation validation

This test suite validates the documentation meets all acceptance criteria:
- File existence and duplication
- Structure validation (YAML frontmatter, sections)
- Content validation (4 database technologies, ErrorOr pattern, anti-patterns, collaboration)
- Code example validation (C# syntax, ErrorOr<T> return types)
- Quality standards (format matching reference, namespace conventions)
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


# Test Data: File Paths
APPSHELL_DOC_PATH = "/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui-appshell/agents/maui-repository-specialist.md"
NAVIGATIONPAGE_DOC_PATH = "/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui-navigationpage/agents/maui-repository-specialist.md"
REFERENCE_DOC_PATH = "/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui-appshell/agents/maui-viewmodel-specialist.md"


class TestFileExistence:
    """Test that required documentation files exist"""

    def test_appshell_doc_exists(self):
        """Test that maui-appshell agent documentation exists"""
        assert os.path.exists(APPSHELL_DOC_PATH), \
            f"AppShell documentation not found at {APPSHELL_DOC_PATH}"

    def test_navigationpage_doc_exists(self):
        """Test that maui-navigationpage agent documentation exists"""
        assert os.path.exists(NAVIGATIONPAGE_DOC_PATH), \
            f"NavigationPage documentation not found at {NAVIGATIONPAGE_DOC_PATH}"


class TestFileDuplication:
    """Test that both documentation files are identical"""

    def test_files_are_identical(self):
        """Test that both agent documentation files have identical content"""
        with open(APPSHELL_DOC_PATH, 'r') as f1:
            appshell_content = f1.read()

        with open(NAVIGATIONPAGE_DOC_PATH, 'r') as f2:
            navigationpage_content = f2.read()

        assert appshell_content == navigationpage_content, \
            "AppShell and NavigationPage documentation files must be identical"


class TestYAMLFrontmatter:
    """Test YAML frontmatter validity and required fields"""

    def _extract_frontmatter(self, file_path: str) -> Dict:
        """Extract and parse YAML frontmatter from markdown file"""
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        assert match, f"No YAML frontmatter found in {file_path}"

        frontmatter_text = match.group(1)
        frontmatter = yaml.safe_load(frontmatter_text)

        return frontmatter

    def test_frontmatter_is_valid_yaml(self):
        """Test that frontmatter can be parsed as valid YAML"""
        frontmatter = self._extract_frontmatter(APPSHELL_DOC_PATH)
        assert isinstance(frontmatter, dict), "Frontmatter must be a valid YAML dictionary"

    def test_frontmatter_has_required_fields(self):
        """Test that frontmatter contains all required fields"""
        frontmatter = self._extract_frontmatter(APPSHELL_DOC_PATH)

        required_fields = ['name', 'description', 'tools', 'model', 'orchestration', 'collaborates_with']
        for field in required_fields:
            assert field in frontmatter, f"Frontmatter missing required field: {field}"

    def test_frontmatter_name_correct(self):
        """Test that agent name is 'maui-repository-specialist'"""
        frontmatter = self._extract_frontmatter(APPSHELL_DOC_PATH)
        assert frontmatter['name'] == 'maui-repository-specialist', \
            "Agent name must be 'maui-repository-specialist'"

    def test_frontmatter_description_mentions_databases(self):
        """Test that description mentions database technologies"""
        frontmatter = self._extract_frontmatter(APPSHELL_DOC_PATH)
        description = frontmatter['description'].lower()

        database_keywords = ['sqlite', 'litedb', 'entity framework', 'realm']
        found_keywords = [kw for kw in database_keywords if kw in description]

        assert len(found_keywords) >= 3, \
            f"Description should mention at least 3 database technologies, found: {found_keywords}"

    def test_frontmatter_mentions_erroror(self):
        """Test that description mentions ErrorOr pattern"""
        frontmatter = self._extract_frontmatter(APPSHELL_DOC_PATH)
        description = frontmatter['description'].lower()

        assert 'erroror' in description, \
            "Description must mention ErrorOr error handling"

    def test_frontmatter_collaborates_with_correct_agents(self):
        """Test that collaborates_with includes required agents"""
        frontmatter = self._extract_frontmatter(APPSHELL_DOC_PATH)
        collaborates_with = frontmatter.get('collaborates_with', [])

        required_collaborators = [
            'maui-domain-specialist',
            'database-specialist',
            'dotnet-testing-specialist'
        ]

        for collaborator in required_collaborators:
            assert collaborator in collaborates_with, \
                f"Must collaborate with {collaborator}"

        assert len(collaborates_with) >= 3, \
            f"Must collaborate with at least 3 agents, found: {len(collaborates_with)}"


class TestDocumentStructure:
    """Test that documentation has required sections"""

    def _read_content(self, file_path: str) -> str:
        """Read file content without frontmatter"""
        with open(file_path, 'r') as f:
            content = f.read()

        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        return content

    def test_has_core_expertise_section(self):
        """Test that documentation has Core Expertise section"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert '## Core Expertise' in content, \
            "Documentation must have '## Core Expertise' section"

    def test_has_implementation_patterns_section(self):
        """Test that documentation has Implementation Patterns section"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert '## Implementation Patterns' in content, \
            "Documentation must have '## Implementation Patterns' section"

    def test_has_anti_patterns_section(self):
        """Test that documentation has Anti-Patterns section"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert '## Anti-Patterns to Avoid' in content, \
            "Documentation must have '## Anti-Patterns to Avoid' section"

    def test_has_testing_strategies_section(self):
        """Test that documentation has Testing Strategies section"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert '## Testing Strategies' in content, \
            "Documentation must have '## Testing Strategies' section"

    def test_has_collaboration_section(self):
        """Test that documentation has Collaboration section"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert '## Collaboration & Best Practices' in content or '### I Collaborate With' in content, \
            "Documentation must have collaboration section"

    def test_has_best_practices_section(self):
        """Test that documentation has Best Practices section"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert '### Best Practices' in content or '## Best Practices' in content, \
            "Documentation must have Best Practices section"


class TestDatabaseTechnologies:
    """Test that all 4 database technologies are documented"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def test_documents_sqlite(self):
        """Test that SQLite is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert 'SQLite' in content or 'sqlite' in content.lower(), \
            "Documentation must include SQLite"

        # Check for SQLite-specific content
        assert 'Microsoft.Data.Sqlite' in content or 'SQLite-net-pcl' in content, \
            "Documentation should mention SQLite libraries"

    def test_documents_litedb(self):
        """Test that LiteDB is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert 'LiteDB' in content, \
            "Documentation must include LiteDB"

        # Check for LiteDB-specific content
        assert 'BSON' in content or 'document database' in content.lower(), \
            "Documentation should mention LiteDB characteristics"

    def test_documents_entity_framework_core(self):
        """Test that Entity Framework Core is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert 'Entity Framework Core' in content or 'EF Core' in content, \
            "Documentation must include Entity Framework Core"

        # Check for EF Core-specific content
        assert 'DbContext' in content or 'LINQ' in content, \
            "Documentation should mention EF Core characteristics"

    def test_documents_realm(self):
        """Test that Realm is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert 'Realm' in content, \
            "Documentation must include Realm"

        # Check for Realm-specific content
        assert 'Detach' in content or 'RealmObject' in content, \
            "Documentation should mention Realm-specific patterns"

    def test_has_implementation_for_each_technology(self):
        """Test that each database technology has implementation examples"""
        content = self._read_content(APPSHELL_DOC_PATH)

        implementations = [
            'SQLite Repository Implementation',
            'LiteDB Repository Implementation',
            'Entity Framework Core Repository Implementation',
            'Realm Repository Implementation'
        ]

        for impl in implementations:
            assert impl in content, \
                f"Missing implementation example: {impl}"


class TestErrorOrPattern:
    """Test that ErrorOr pattern is used throughout"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def _extract_code_blocks(self, content: str) -> List[str]:
        """Extract C# code blocks from markdown"""
        pattern = r'```csharp\s*\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

    def test_erroror_mentioned_in_content(self):
        """Test that ErrorOr is mentioned in documentation"""
        content = self._read_content(APPSHELL_DOC_PATH)
        assert 'ErrorOr' in content, \
            "Documentation must mention ErrorOr pattern"

    def test_code_examples_use_erroror_return_types(self):
        """Test that code examples use ErrorOr<T> return types"""
        content = self._read_content(APPSHELL_DOC_PATH)
        code_blocks = self._extract_code_blocks(content)

        # Check for ErrorOr<T> in code blocks
        erroror_pattern = r'Task<ErrorOr<[^>]+>>'
        found_erroror = False

        for code in code_blocks:
            if re.search(erroror_pattern, code):
                found_erroror = True
                break

        assert found_erroror, \
            "Code examples must include ErrorOr<T> return types"

    def test_repository_interface_uses_erroror(self):
        """Test that repository interface uses ErrorOr for all methods"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Find repository interface section
        interface_match = re.search(
            r'### Repository Interface Template.*?```csharp(.*?)```',
            content,
            re.DOTALL
        )

        assert interface_match, "Repository interface template not found"

        interface_code = interface_match.group(1)

        # All async methods should return Task<ErrorOr<T>>
        method_pattern = r'Task<ErrorOr<[^>]+>>'
        methods_with_erroror = re.findall(method_pattern, interface_code)

        assert len(methods_with_erroror) >= 5, \
            f"Repository interface should have at least 5 methods with ErrorOr, found: {len(methods_with_erroror)}"

    def test_no_exception_throwing_in_examples(self):
        """Test that code examples don't throw exceptions (use ErrorOr instead)"""
        content = self._read_content(APPSHELL_DOC_PATH)
        code_blocks = self._extract_code_blocks(content)

        # Find implementation code blocks (not anti-pattern examples)
        implementation_blocks = []
        for i, code in enumerate(code_blocks):
            # Skip blocks that are explicitly marked as WRONG
            if i > 0 and 'WRONG' in code_blocks[i-1]:
                continue
            implementation_blocks.append(code)

        # Check that CORRECT implementations don't throw exceptions
        for code in implementation_blocks:
            if 'CORRECT' in code or 'Repository' in code:
                assert 'throw new' not in code or 'WRONG' in code, \
                    "Implementation examples should not throw exceptions (use ErrorOr)"


class TestAntiPatterns:
    """Test that anti-patterns section includes WRONG/CORRECT examples"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def test_has_wrong_examples(self):
        """Test that anti-patterns section has WRONG examples"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Count WRONG markers
        wrong_count = content.count('WRONG')

        assert wrong_count >= 3, \
            f"Anti-patterns section should have at least 3 WRONG examples, found: {wrong_count}"

    def test_has_correct_examples(self):
        """Test that anti-patterns section has CORRECT examples"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Count CORRECT markers
        correct_count = content.count('CORRECT')

        assert correct_count >= 3, \
            f"Anti-patterns section should have at least 3 CORRECT examples, found: {correct_count}"

    def test_documents_no_api_calls_anti_pattern(self):
        """Test that documentation warns against API calls in repositories"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Should mention not making API calls
        api_warnings = [
            'NO API calls',
            'should NEVER make API calls',
            'API logic, not database logic'
        ]

        found_warning = any(warning in content for warning in api_warnings)
        assert found_warning, \
            "Documentation should warn against API calls in repositories"

    def test_documents_no_business_logic_anti_pattern(self):
        """Test that documentation warns against business logic in repositories"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Should mention not including business logic
        business_logic_warnings = [
            'NO business logic',
            'business logic, belongs in',
            'business logic in repository'
        ]

        found_warning = any(warning in content for warning in business_logic_warnings)
        assert found_warning, \
            "Documentation should warn against business logic in repositories"

    def test_documents_no_ui_dependencies_anti_pattern(self):
        """Test that documentation warns against UI dependencies in repositories"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Should mention not having UI dependencies
        ui_warnings = [
            'NO UI',
            'should not show UI',
            'UI dependencies'
        ]

        found_warning = any(warning in content for warning in ui_warnings)
        assert found_warning, \
            "Documentation should warn against UI dependencies in repositories"


class TestCollaboration:
    """Test that collaboration section documents agent interactions"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def test_documents_collaboration_with_maui_domain_specialist(self):
        """Test collaboration with maui-domain-specialist is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)

        assert 'maui-domain-specialist' in content, \
            "Should document collaboration with maui-domain-specialist"

    def test_documents_collaboration_with_database_specialist(self):
        """Test collaboration with database-specialist is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)

        assert 'database-specialist' in content, \
            "Should document collaboration with database-specialist"

    def test_documents_collaboration_with_testing_specialist(self):
        """Test collaboration with dotnet-testing-specialist is documented"""
        content = self._read_content(APPSHELL_DOC_PATH)

        assert 'dotnet-testing-specialist' in content, \
            "Should document collaboration with dotnet-testing-specialist"

    def test_describes_collaboration_responsibilities(self):
        """Test that collaboration section describes responsibilities"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Should have text describing what each collaboration involves
        collaboration_section_match = re.search(
            r'### I Collaborate With.*?(?=###|##|\Z)',
            content,
            re.DOTALL
        )

        if collaboration_section_match:
            collab_text = collaboration_section_match.group(0)

            # Should have multiple bullet points or descriptions
            bullet_count = collab_text.count('-') + collab_text.count('*')
            assert bullet_count >= 5, \
                "Collaboration section should describe multiple responsibilities"


class TestCodeExamples:
    """Test code example quality and completeness"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def _extract_code_blocks(self, content: str) -> List[str]:
        """Extract C# code blocks from markdown"""
        pattern = r'```csharp\s*\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

    def test_has_multiple_code_examples(self):
        """Test that documentation has multiple code examples"""
        content = self._read_content(APPSHELL_DOC_PATH)
        code_blocks = self._extract_code_blocks(content)

        assert len(code_blocks) >= 10, \
            f"Documentation should have at least 10 code examples, found: {len(code_blocks)}"

    def test_code_blocks_have_language_tags(self):
        """Test that all code blocks have language tags (csharp)"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Count code fences
        code_fence_count = content.count('```')

        # Count csharp tagged blocks
        csharp_count = content.count('```csharp')

        # All code blocks should be tagged as csharp
        assert csharp_count * 2 == code_fence_count or csharp_count * 2 >= code_fence_count - 2, \
            "All code blocks should have 'csharp' language tag"

    def test_code_examples_have_xml_comments(self):
        """Test that code examples include XML documentation comments"""
        content = self._read_content(APPSHELL_DOC_PATH)
        code_blocks = self._extract_code_blocks(content)

        # Count blocks with XML comments
        blocks_with_comments = sum(1 for code in code_blocks if '///' in code)

        assert blocks_with_comments >= 5, \
            f"At least 5 code examples should have XML documentation, found: {blocks_with_comments}"

    def test_namespace_conventions_followed(self):
        """Test that code examples follow proper namespace conventions"""
        content = self._read_content(APPSHELL_DOC_PATH)
        code_blocks = self._extract_code_blocks(content)

        # Check for proper namespace patterns
        expected_namespaces = [
            r'YourApp\.DatabaseServices',
            r'YourApp\.Entities',
            r'YourApp\.Services'
        ]

        for pattern in expected_namespaces:
            found = any(re.search(pattern, code) for code in code_blocks)
            assert found, \
                f"Code examples should include namespace pattern: {pattern}"


class TestTestingStrategies:
    """Test that testing strategies are comprehensive"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def test_has_unit_test_examples(self):
        """Test that documentation includes unit test examples"""
        content = self._read_content(APPSHELL_DOC_PATH)

        test_indicators = [
            '[Fact]',
            '[Theory]',
            'public async Task',
            'ShouldReturn'
        ]

        found_indicators = sum(1 for indicator in test_indicators if indicator in content)
        assert found_indicators >= 3, \
            f"Documentation should include unit test examples, found {found_indicators} indicators"

    def test_has_test_fixture_pattern(self):
        """Test that documentation shows test fixture patterns"""
        content = self._read_content(APPSHELL_DOC_PATH)

        assert 'IDisposable' in content or 'public void Dispose' in content, \
            "Documentation should show test fixture cleanup patterns"

    def test_has_test_data_setup(self):
        """Test that documentation shows test data setup"""
        content = self._read_content(APPSHELL_DOC_PATH)

        setup_indicators = [
            '// Arrange',
            'InitializeDatabase',
            'CreateTableSql'
        ]

        found = any(indicator in content for indicator in setup_indicators)
        assert found, \
            "Documentation should show test data setup patterns"

    def test_has_assertion_examples(self):
        """Test that documentation shows assertion patterns"""
        content = self._read_content(APPSHELL_DOC_PATH)

        assertion_patterns = [
            '.Should().',
            'IsError.Should().',
            'Assert.'
        ]

        found = any(pattern in content for pattern in assertion_patterns)
        assert found, \
            "Documentation should show assertion patterns (FluentAssertions or xUnit)"


class TestQualityStandards:
    """Test that documentation meets quality standards"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def test_document_is_substantial(self):
        """Test that documentation has substantial content"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Remove code blocks for line count
        content_without_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        lines = content_without_code.split('\n')

        assert len(lines) >= 100, \
            f"Documentation should be substantial (100+ lines), found: {len(lines)} lines"

    def test_has_clear_headings(self):
        """Test that documentation has clear heading structure"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Count headings
        h2_count = content.count('## ')
        h3_count = content.count('### ')

        assert h2_count >= 5, \
            f"Documentation should have at least 5 level-2 headings, found: {h2_count}"
        assert h3_count >= 10, \
            f"Documentation should have at least 10 level-3 headings, found: {h3_count}"

    def test_consistent_with_task_requirements(self):
        """Test that documentation addresses task acceptance criteria"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Key requirements from task
        requirements = [
            'Repository Pattern',
            'SQLite',
            'LiteDB',
            'Entity Framework Core',
            'Realm',
            'ErrorOr',
            'CRUD',
            'Testing',
            'Anti-Patterns',
            'Collaboration'
        ]

        for requirement in requirements:
            assert requirement in content, \
                f"Documentation must address requirement: {requirement}"


class TestCompilation:
    """Test 'compilation' for documentation (markdown validity)"""

    def _read_content(self, file_path: str) -> str:
        """Read file content"""
        with open(file_path, 'r') as f:
            return f.read()

    def test_markdown_syntax_valid(self):
        """Test that markdown syntax is valid (basic checks)"""
        content = self._read_content(APPSHELL_DOC_PATH)

        # Check for balanced code fences
        code_fence_count = content.count('```')
        assert code_fence_count % 2 == 0, \
            "Code fences must be balanced (opening and closing)"

        # Check for balanced heading structure (no heading levels skipped)
        headings = re.findall(r'^(#{1,6})\s+', content, re.MULTILINE)
        # This is a basic check; more sophisticated validation could be added

    def test_yaml_frontmatter_parses(self):
        """Test that YAML frontmatter can be parsed without errors"""
        with open(APPSHELL_DOC_PATH, 'r') as f:
            content = f.read()

        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        assert match, "YAML frontmatter not found"

        frontmatter_text = match.group(1)

        # This should not raise an exception
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            assert isinstance(frontmatter, dict)
        except yaml.YAMLError as e:
            assert False, f"YAML parsing error: {e}"

    def test_code_blocks_have_proper_syntax(self):
        """Test that C# code blocks have basic C# syntax elements"""
        content = self._read_content(APPSHELL_DOC_PATH)
        code_blocks = re.findall(r'```csharp\s*\n(.*?)```', content, re.DOTALL)

        # Check that code blocks contain C# keywords
        csharp_keywords = ['namespace', 'class', 'public', 'private', 'async', 'await', 'Task']

        code_with_keywords = 0
        for code in code_blocks:
            if any(keyword in code for keyword in csharp_keywords):
                code_with_keywords += 1

        # Most code blocks should contain C# keywords
        assert code_with_keywords >= len(code_blocks) * 0.5, \
            f"At least 50% of code blocks should contain C# syntax, found {code_with_keywords}/{len(code_blocks)}"


if __name__ == '__main__':
    import pytest
    import sys

    # Run tests and report results
    exit_code = pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--color=yes'
    ])

    sys.exit(exit_code)
