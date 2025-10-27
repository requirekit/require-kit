"""
Spec Drift Detector - Prevents AI hallucination and scope creep

This module analyzes implementation against requirements to detect:
1. Requirements coverage (are all requirements implemented?)
2. Scope creep (are there unspecified features?)
3. Compliance scoring (how well does implementation match spec?)

Part of Phase 5 Code Review workflow.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Set
import re
import yaml


@dataclass
class Requirement:
    """Represents a single EARS requirement."""
    id: str
    text: str
    type: str  # ubiquitous, event, state, unwanted, optional
    implemented: bool = False
    implementation_files: List[str] = None

    def __post_init__(self):
        if self.implementation_files is None:
            self.implementation_files = []


@dataclass
class ScopeCreepItem:
    """Represents code not linked to any requirement."""
    file_path: str
    line_number: int
    description: str
    code_snippet: str
    severity: str  # low, medium, high


@dataclass
class DriftReport:
    """Complete drift analysis report."""
    requirements_coverage: Dict[str, Requirement]
    scope_creep_items: List[ScopeCreepItem]
    compliance_score: int
    requirements_implemented_percent: float
    scope_creep_percent: float

    def has_issues(self) -> bool:
        """Check if there are any compliance issues."""
        return self.scope_creep_percent > 0 or self.requirements_implemented_percent < 100


class SpecDriftDetector:
    """Analyzes spec drift between requirements and implementation."""

    def __init__(self, workspace_root: Path = None):
        """
        Initialize drift detector.

        Args:
            workspace_root: Root directory of the workspace. Defaults to current directory.
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.requirements_dir = self.workspace_root / "docs" / "requirements"
        self.tasks_dir = self.workspace_root / "tasks"

    def analyze_drift(self, task_id: str) -> DriftReport:
        """
        Analyze spec drift for a task.

        Args:
            task_id: Task identifier (e.g., "TASK-042")

        Returns:
            DriftReport with coverage and scope creep analysis
        """
        # Load task metadata
        task_data = self._load_task(task_id)

        # Load requirements
        requirements = self._load_requirements(task_data)

        # Get implementation files
        implementation_files = self._get_implementation_files(task_data)

        # Calculate requirements coverage
        coverage = self._calculate_coverage(requirements, implementation_files)

        # Detect scope creep
        scope_creep = self._detect_scope_creep(requirements, implementation_files)

        # Calculate compliance score
        compliance = self._calculate_compliance(coverage, scope_creep)

        # Calculate percentages
        req_percent = self._calculate_requirements_percent(coverage)
        creep_percent = self._calculate_scope_creep_percent(
            scope_creep, implementation_files
        )

        return DriftReport(
            requirements_coverage=coverage,
            scope_creep_items=scope_creep,
            compliance_score=compliance,
            requirements_implemented_percent=req_percent,
            scope_creep_percent=creep_percent
        )

    def _load_task(self, task_id: str) -> Dict:
        """Load task metadata from markdown file."""
        # Search in all task folders
        task_folders = [
            "backlog", "in_progress", "in_review", "blocked", "completed"
        ]

        for folder in task_folders:
            task_path = self.tasks_dir / folder
            if task_path.exists():
                for file in task_path.glob(f"{task_id}*.md"):
                    return self._parse_task_file(file)

        raise FileNotFoundError(f"Task {task_id} not found in any task folder")

    def _parse_task_file(self, file_path: Path) -> Dict:
        """Parse task markdown file and extract frontmatter."""
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return {}

        frontmatter = yaml.safe_load(frontmatter_match.group(1))

        # Extract implementation files from content
        impl_section = re.search(
            r'## Implementation Files\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL
        )

        if impl_section:
            # Extract file paths from markdown list
            files = re.findall(r'- `([^`]+)`', impl_section.group(1))
            frontmatter['implementation_files'] = files

        return frontmatter

    def _load_requirements(self, task_data: Dict) -> List[Requirement]:
        """Load requirements linked to the task."""
        requirements = []
        req_ids = task_data.get('requirements', [])

        if isinstance(req_ids, str):
            req_ids = [req_ids]

        for req_id in req_ids:
            req = self._load_requirement(req_id)
            if req:
                requirements.append(req)

        return requirements

    def _load_requirement(self, req_id: str) -> Optional[Requirement]:
        """Load a single requirement from the requirements directory."""
        # Search in all requirement folders
        req_folders = ["draft", "approved", "implemented"]

        for folder in req_folders:
            req_path = self.requirements_dir / folder
            if req_path.exists():
                for file in req_path.glob(f"{req_id}*.md"):
                    return self._parse_requirement_file(file, req_id)

        return None

    def _parse_requirement_file(self, file_path: Path, req_id: str) -> Requirement:
        """Parse requirement file and extract EARS notation."""
        with open(file_path, 'r') as f:
            content = f.read()

        # Determine requirement type from EARS pattern
        req_type = "ubiquitous"  # default
        if re.search(r'\bWhen\b.*\bshall\b', content):
            req_type = "event"
        elif re.search(r'\bWhile\b.*\bshall\b', content):
            req_type = "state"
        elif re.search(r'\bIf\b.*\bthen\b.*\bshall\b', content):
            req_type = "unwanted"
        elif re.search(r'\bWhere\b.*\bshall\b', content):
            req_type = "optional"

        # Extract the requirement text
        req_text_match = re.search(r'## Requirement\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        req_text = req_text_match.group(1).strip() if req_text_match else ""

        return Requirement(
            id=req_id,
            text=req_text,
            type=req_type
        )

    def _get_implementation_files(self, task_data: Dict) -> List[Path]:
        """Get list of implementation files for the task."""
        file_paths = task_data.get('implementation_files', [])

        # Convert to Path objects and make absolute
        return [
            self.workspace_root / file_path
            for file_path in file_paths
            if file_path
        ]

    def _calculate_coverage(
        self,
        requirements: List[Requirement],
        implementation_files: List[Path]
    ) -> Dict[str, Requirement]:
        """
        Calculate which requirements are implemented in the code.

        Uses keyword matching and semantic patterns to trace requirements.
        """
        coverage = {}

        for req in requirements:
            # Extract keywords from requirement text
            keywords = self._extract_keywords(req.text)

            # Search implementation files for traces
            implemented = False
            impl_files = []

            for file_path in implementation_files:
                if self._file_implements_requirement(file_path, keywords):
                    implemented = True
                    impl_files.append(str(file_path.relative_to(self.workspace_root)))

            req.implemented = implemented
            req.implementation_files = impl_files
            coverage[req.id] = req

        return coverage

    def _extract_keywords(self, requirement_text: str) -> Set[str]:
        """Extract significant keywords from requirement text."""
        # Remove common words
        stop_words = {
            'the', 'shall', 'system', 'when', 'while', 'if', 'then',
            'where', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'as'
        }

        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b\w+\b', requirement_text.lower())

        # Filter out stop words and short words
        keywords = {
            word for word in words
            if word not in stop_words and len(word) > 3
        }

        return keywords

    def _file_implements_requirement(
        self,
        file_path: Path,
        keywords: Set[str]
    ) -> bool:
        """Check if a file implements a requirement based on keywords."""
        if not file_path.exists():
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except (UnicodeDecodeError, PermissionError):
            return False

        # Check if at least 50% of keywords appear in the file
        matches = sum(1 for keyword in keywords if keyword in content)
        threshold = max(1, len(keywords) * 0.5)

        return matches >= threshold

    def _detect_scope_creep(
        self,
        requirements: List[Requirement],
        implementation_files: List[Path]
    ) -> List[ScopeCreepItem]:
        """
        Detect code that doesn't trace to any requirement.

        This is a simplified version that looks for common scope creep patterns.
        """
        scope_creep = []

        # Build set of all requirement keywords
        all_req_keywords = set()
        for req in requirements:
            all_req_keywords.update(self._extract_keywords(req.text))

        # Common scope creep patterns
        creep_patterns = [
            (r'class.*Refresh', 'Token refresh mechanism'),
            (r'class.*RateLimit', 'Rate limiting'),
            (r'class.*Cache', 'Caching layer'),
            (r'class.*Logger', 'Custom logging'),
            (r'class.*Metrics', 'Metrics collection'),
            (r'class.*Monitor', 'Monitoring'),
            (r'class.*Retry', 'Retry logic'),
            (r'class.*Circuit', 'Circuit breaker'),
            (r'class.*Validator.*Extra', 'Extra validation'),
        ]

        for file_path in implementation_files:
            if not file_path.exists():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except (UnicodeDecodeError, PermissionError):
                continue

            for line_num, line in enumerate(lines, start=1):
                for pattern, description in creep_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Check if this relates to any requirement
                        line_keywords = self._extract_keywords(line)
                        if not line_keywords.intersection(all_req_keywords):
                            scope_creep.append(ScopeCreepItem(
                                file_path=str(file_path.relative_to(self.workspace_root)),
                                line_number=line_num,
                                description=description,
                                code_snippet=line.strip(),
                                severity='medium'
                            ))

        return scope_creep

    def _calculate_compliance(
        self,
        coverage: Dict[str, Requirement],
        scope_creep: List[ScopeCreepItem]
    ) -> int:
        """
        Calculate overall compliance score (0-100).

        Formula:
        - Start at 100
        - -10 points for each unimplemented requirement
        - -5 points for each scope creep item (medium)
        - Minimum score: 0
        """
        score = 100

        # Deduct for unimplemented requirements
        unimplemented = sum(1 for req in coverage.values() if not req.implemented)
        score -= unimplemented * 10

        # Deduct for scope creep
        score -= len(scope_creep) * 5

        return max(0, score)

    def _calculate_requirements_percent(
        self,
        coverage: Dict[str, Requirement]
    ) -> float:
        """Calculate percentage of requirements implemented."""
        if not coverage:
            return 100.0

        implemented = sum(1 for req in coverage.values() if req.implemented)
        total = len(coverage)

        return round((implemented / total) * 100, 1)

    def _calculate_scope_creep_percent(
        self,
        scope_creep: List[ScopeCreepItem],
        implementation_files: List[Path]
    ) -> float:
        """Calculate scope creep as percentage of total implementation."""
        if not implementation_files:
            return 0.0

        # Count total lines of code
        total_lines = 0
        for file_path in implementation_files:
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except (UnicodeDecodeError, PermissionError):
                    continue

        if total_lines == 0:
            return 0.0

        # Each scope creep item counts as ~10 lines (heuristic)
        creep_lines = len(scope_creep) * 10

        return round((creep_lines / total_lines) * 100, 1)


def format_drift_report(report: DriftReport, task_id: str) -> str:
    """
    Format drift report for display.

    Args:
        report: DriftReport to format
        task_id: Task identifier

    Returns:
        Formatted report string
    """
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"Spec Drift Detection Report - {task_id}")
    lines.append(f"{'='*70}\n")

    # Requirements Coverage
    lines.append("📋 REQUIREMENTS COVERAGE")
    lines.append("-" * 70)

    for req_id, req in sorted(report.requirements_coverage.items()):
        status = "✅" if req.implemented else "❌"
        lines.append(f"{status} {req_id}: {req.text[:60]}...")

        if req.implemented and req.implementation_files:
            for file in req.implementation_files:
                lines.append(f"    └─ {file}")
        elif not req.implemented:
            lines.append(f"    └─ NOT IMPLEMENTED")

    lines.append("")

    # Scope Creep
    if report.scope_creep_items:
        lines.append("⚠️  SCOPE CREEP DETECTED")
        lines.append("-" * 70)

        for item in report.scope_creep_items:
            lines.append(f"❌ {item.description}")
            lines.append(f"   File: {item.file_path}:{item.line_number}")
            lines.append(f"   Code: {item.code_snippet}")
            lines.append(f"   Severity: {item.severity}")
            lines.append("")
    else:
        lines.append("✅ NO SCOPE CREEP DETECTED")
        lines.append("-" * 70)
        lines.append("")

    # Compliance Scorecard
    lines.append("📊 COMPLIANCE SCORECARD")
    lines.append("-" * 70)
    lines.append(f"Requirements Implemented: {report.requirements_implemented_percent}%")
    lines.append(f"Scope Creep: {report.scope_creep_percent}%")
    lines.append(f"Overall Compliance: {report.compliance_score}/100")

    # Overall status
    if report.compliance_score >= 90:
        lines.append("\n✅ EXCELLENT - Ready for review")
    elif report.compliance_score >= 80:
        lines.append("\n⚠️  GOOD - Minor issues to address")
    elif report.compliance_score >= 70:
        lines.append("\n⚠️  ACCEPTABLE - Several issues to address")
    else:
        lines.append("\n❌ POOR - Major compliance issues")

    lines.append(f"\n{'='*70}\n")

    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    detector = SpecDriftDetector()
    report = detector.analyze_drift("TASK-042")
    print(format_drift_report(report, "TASK-042"))
