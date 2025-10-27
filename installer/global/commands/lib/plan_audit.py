"""
Plan Audit Module - Compare actual implementation against original plan (Hubbard's Step 6).

Part of TASK-025: Implement Phase 5.5 Plan Audit.

This module implements John Hubbard's Step 6 (Audit) from his proven 6-step workflow.
It verifies that actual implementation matches the approved architectural plan by:
- Comparing files created vs planned
- Comparing dependencies added vs planned
- Comparing LOC (lines of code) vs estimates
- Comparing duration vs estimates

Research support:
- John Hubbard's 6-step workflow (Step 6: Audit)
- ThoughtWorks: "Agents frequently don't follow all instructions"
- Closes critical gap identified in SDD vs AI-Engineer analysis

Author: Claude (Anthropic)
Created: 2025-10-18
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Literal, Optional, Set
from pathlib import Path
from datetime import datetime
import json
import re


@dataclass
class Discrepancy:
    """Represents a single discrepancy between planned and actual implementation."""
    category: str  # "files", "dependencies", "loc", "duration"
    severity: Literal["low", "medium", "high"]
    message: str
    planned: Any
    actual: Any
    variance: float  # Percentage variance (e.g., 55.0 for 55%)


@dataclass
class PlanAuditReport:
    """Complete audit report with all discrepancies and recommendations."""
    task_id: str
    plan_summary: Dict[str, Any]
    actual_summary: Dict[str, Any]
    discrepancies: List[Discrepancy]
    severity: Literal["low", "medium", "high"]
    recommendations: List[str]
    timestamp: str
    plan_path: str
    audit_duration_seconds: float


class PlanAuditor:
    """Main auditor class that compares planned vs actual implementation."""

    def __init__(self, workspace_root: Path = Path(".")):
        """
        Initialize plan auditor.

        Args:
            workspace_root: Root directory of the workspace (default: current directory)
        """
        self.workspace_root = workspace_root

    def audit_implementation(self, task_id: str) -> PlanAuditReport:
        """
        Main entry point: Audit implementation against saved plan.

        Compares actual implementation (files, LOC, dependencies, duration) against
        the original implementation plan saved during Phase 2.7.

        Args:
            task_id: Task identifier (e.g., "TASK-025")

        Returns:
            Complete audit report with discrepancies and severity

        Raises:
            PlanAuditError: If plan doesn't exist or audit fails

        Example:
            >>> auditor = PlanAuditor()
            >>> report = auditor.audit_implementation("TASK-025")
            >>> print(report.severity)
            'low'
        """
        start_time = datetime.now()

        # Load implementation plan
        plan = self._load_plan(task_id)
        if not plan:
            raise PlanAuditError(f"No implementation plan found for {task_id}")

        # Analyze actual implementation
        actual = self._analyze_implementation(task_id, plan)

        # Compare and detect discrepancies
        discrepancies = self._compare(plan, actual)

        # Calculate overall severity
        severity = self._calculate_severity(discrepancies)

        # Generate actionable recommendations
        recommendations = self._generate_recommendations(discrepancies, severity)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return PlanAuditReport(
            task_id=task_id,
            plan_summary=self._extract_plan_summary(plan),
            actual_summary=actual,
            discrepancies=discrepancies,
            severity=severity,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            plan_path=f"docs/state/{task_id}/implementation_plan.md",
            audit_duration_seconds=duration
        )

    def _load_plan(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Load saved implementation plan from disk."""
        try:
            from .plan_persistence import load_plan
            return load_plan(task_id)
        except ImportError:
            # Fallback for testing
            plan_path = self.workspace_root / "docs" / "state" / task_id / "implementation_plan.md"
            if plan_path.exists():
                # Simplified loading for tests
                return {"plan": {}}
            return None

    def _analyze_implementation(
        self,
        task_id: str,
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze actual implementation: files created, LOC, dependencies, duration.

        Args:
            task_id: Task identifier
            plan: Loaded implementation plan

        Returns:
            Dictionary with actual implementation metrics
        """
        return {
            "files_created": self._scan_created_files(plan),
            "files_modified": self._scan_modified_files(plan),
            "total_loc": self._count_lines_of_code(plan),
            "dependencies": self._extract_dependencies(),
            "duration_hours": self._calculate_duration(task_id)
        }

    def _scan_created_files(self, plan: Dict[str, Any]) -> List[str]:
        """
        Scan for files created (compare against planned files).

        Args:
            plan: Implementation plan

        Returns:
            List of actual file paths created
        """
        planned_files = set(plan.get("plan", {}).get("files_to_create", []))
        actual_files = []

        # Scan common source directories
        patterns = [
            "src/**/*.py",
            "src/**/*.ts",
            "src/**/*.tsx",
            "src/**/*.js",
            "src/**/*.jsx",
            "src/**/*.cs",
            "lib/**/*.py",
            "installer/**/*.py"
        ]

        for pattern in patterns:
            for file_path in self.workspace_root.glob(pattern):
                if file_path.is_file() and not self._is_excluded(file_path):
                    rel_path = str(file_path.relative_to(self.workspace_root))
                    actual_files.append(rel_path)

        return actual_files

    def _scan_modified_files(self, plan: Dict[str, Any]) -> List[str]:
        """
        Scan for files modified (compare against planned modifications).

        Note: Simplified implementation - actual version would use git diff.

        Args:
            plan: Implementation plan

        Returns:
            List of modified file paths
        """
        # Simplified for MVP - actual implementation would use git
        return []

    def _count_lines_of_code(self, plan: Dict[str, Any]) -> int:
        """
        Count actual lines of code in created/modified files.

        Args:
            plan: Implementation plan

        Returns:
            Total non-empty, non-comment lines
        """
        total_loc = 0
        plan_data = plan.get("plan", {})
        planned_files = (
            plan_data.get("files_to_create", []) +
            plan_data.get("files_to_modify", [])
        )

        for file_path_str in planned_files:
            file_path = self.workspace_root / file_path_str
            if file_path.exists():
                total_loc += self._count_file_loc(file_path)

        return total_loc

    def _count_file_loc(self, file_path: Path) -> int:
        """
        Count non-empty, non-comment lines in a file.

        Simple LOC counter that excludes:
        - Blank lines
        - Single-line comments (#, //, /*)
        - Lines with only whitespace

        Args:
            file_path: Path to file

        Returns:
            Number of lines of code
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            loc = 0
            for line in lines:
                stripped = line.strip()
                # Skip blank lines and common comment patterns
                if stripped and not stripped.startswith(('#', '//', '/*', '*', '"""', "'''")):
                    loc += 1

            return loc
        except Exception:
            return 0

    def _extract_dependencies(self) -> List[str]:
        """
        Extract dependencies from package files.

        Supports:
        - Python: requirements.txt, pyproject.toml
        - JavaScript/TypeScript: package.json
        - .NET: *.csproj

        Returns:
            List of dependency names
        """
        deps: Set[str] = set()

        # Python: requirements.txt
        req_file = self.workspace_root / "requirements.txt"
        if req_file.exists():
            deps.update(self._parse_requirements_txt(req_file))

        # Python: pyproject.toml
        pyproject_file = self.workspace_root / "pyproject.toml"
        if pyproject_file.exists():
            deps.update(self._parse_pyproject_toml(pyproject_file))

        # JavaScript/TypeScript: package.json
        pkg_file = self.workspace_root / "package.json"
        if pkg_file.exists():
            deps.update(self._parse_package_json(pkg_file))

        # .NET: *.csproj
        for csproj in self.workspace_root.glob("**/*.csproj"):
            deps.update(self._parse_csproj(csproj))

        return sorted(list(deps))

    def _parse_requirements_txt(self, file_path: Path) -> Set[str]:
        """Parse Python requirements.txt."""
        deps = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name (before ==, >=, ~=, etc.)
                        pkg = re.split(r'[=<>~!]', line)[0].strip()
                        if pkg:
                            deps.add(pkg)
        except Exception:
            pass
        return deps

    def _parse_pyproject_toml(self, file_path: Path) -> Set[str]:
        """Parse Python pyproject.toml (simplified - no TOML parser)."""
        deps = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple regex to extract dependencies
                matches = re.findall(r'"([a-zA-Z0-9_-]+)\s*[=<>~]', content)
                deps.update(matches)
        except Exception:
            pass
        return deps

    def _parse_package_json(self, file_path: Path) -> Set[str]:
        """Parse JavaScript/TypeScript package.json."""
        deps = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            deps.update(data.get("dependencies", {}).keys())
            deps.update(data.get("devDependencies", {}).keys())
        except Exception:
            pass
        return deps

    def _parse_csproj(self, file_path: Path) -> Set[str]:
        """Parse .NET .csproj file (simplified - no XML parser)."""
        deps = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple regex to extract PackageReference
                matches = re.findall(r'<PackageReference Include="([^"]+)"', content)
                deps.update(matches)
        except Exception:
            pass
        return deps

    def _calculate_duration(self, task_id: str) -> float:
        """
        Calculate actual implementation duration from task metadata or git commits.

        Simplified implementation - checks task metadata for timestamps.

        Args:
            task_id: Task identifier

        Returns:
            Duration in hours (0.0 if not available)
        """
        # Placeholder - actual implementation would:
        # 1. Check task metadata for start/end timestamps
        # 2. Use git commit history to calculate duration
        # For MVP, return 0.0 (duration tracking not yet implemented)
        return 0.0

    def _compare(
        self,
        plan: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> List[Discrepancy]:
        """
        Compare planned vs actual, return list of discrepancies.

        Args:
            plan: Implementation plan
            actual: Actual implementation metrics

        Returns:
            List of discrepancies found
        """
        discrepancies = []
        plan_data = plan.get("plan", {})

        # Compare files
        discrepancies.extend(self._compare_files(plan_data, actual))

        # Compare dependencies
        discrepancies.extend(self._compare_dependencies(plan_data, actual))

        # Compare LOC
        discrepancies.extend(self._compare_loc(plan_data, actual))

        # Compare duration (if available)
        discrepancies.extend(self._compare_duration(plan_data, actual))

        return discrepancies

    def _compare_files(
        self,
        plan_data: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> List[Discrepancy]:
        """Compare files: detect extra/missing files."""
        discrepancies = []

        planned_files = set(plan_data.get("files_to_create", []))
        actual_files = set(actual.get("files_created", []))

        extra_files = actual_files - planned_files
        missing_files = planned_files - actual_files

        if extra_files:
            severity = "medium" if len(extra_files) <= 2 else "high"
            variance = (len(extra_files) / max(len(planned_files), 1)) * 100

            discrepancies.append(Discrepancy(
                category="files",
                severity=severity,
                message=f"{len(extra_files)} extra file(s) not in plan",
                planned=sorted(list(planned_files)),
                actual=sorted(list(extra_files)),
                variance=variance
            ))

        if missing_files:
            variance = (len(missing_files) / max(len(planned_files), 1)) * 100

            discrepancies.append(Discrepancy(
                category="files",
                severity="high",
                message=f"{len(missing_files)} planned file(s) not created",
                planned=sorted(list(missing_files)),
                actual=sorted(list(actual_files)),
                variance=variance
            ))

        return discrepancies

    def _compare_dependencies(
        self,
        plan_data: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> List[Discrepancy]:
        """Compare dependencies: detect extra/missing deps."""
        discrepancies = []

        planned_deps = set(plan_data.get("external_dependencies", []))
        actual_deps = set(actual.get("dependencies", []))

        extra_deps = actual_deps - planned_deps
        missing_deps = planned_deps - actual_deps

        if extra_deps:
            severity = "medium" if len(extra_deps) <= 1 else "high"
            variance = (len(extra_deps) / max(len(planned_deps), 1)) * 100

            discrepancies.append(Discrepancy(
                category="dependencies",
                severity=severity,
                message=f"{len(extra_deps)} extra dependenc(ies) not in plan",
                planned=sorted(list(planned_deps)),
                actual=sorted(list(extra_deps)),
                variance=variance
            ))

        if missing_deps:
            variance = (len(missing_deps) / max(len(planned_deps), 1)) * 100

            discrepancies.append(Discrepancy(
                category="dependencies",
                severity="medium",
                message=f"{len(missing_deps)} planned dependenc(ies) not added",
                planned=sorted(list(missing_deps)),
                actual=sorted(list(actual_deps)),
                variance=variance
            ))

        return discrepancies

    def _compare_loc(
        self,
        plan_data: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> List[Discrepancy]:
        """Compare lines of code: calculate variance %."""
        discrepancies = []

        planned_loc = plan_data.get("estimated_loc", 0)
        actual_loc = actual.get("total_loc", 0)

        if planned_loc > 0 and actual_loc > 0:
            variance = ((actual_loc - planned_loc) / planned_loc) * 100

            if abs(variance) > 10:  # More than 10% variance
                if abs(variance) < 30:
                    severity = "low"
                elif abs(variance) < 50:
                    severity = "medium"
                else:
                    severity = "high"

                discrepancies.append(Discrepancy(
                    category="loc",
                    severity=severity,
                    message=f"LOC variance: {variance:+.1f}% ({planned_loc} → {actual_loc} lines)",
                    planned=planned_loc,
                    actual=actual_loc,
                    variance=abs(variance)
                ))

        return discrepancies

    def _compare_duration(
        self,
        plan_data: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> List[Discrepancy]:
        """Compare duration: calculate variance %."""
        discrepancies = []

        planned_duration_str = plan_data.get("estimated_duration", "0 hours")
        planned_duration = self._parse_duration(planned_duration_str)
        actual_duration = actual.get("duration_hours", 0.0)

        if planned_duration > 0 and actual_duration > 0:
            variance = ((actual_duration - planned_duration) / planned_duration) * 100

            if abs(variance) > 10:  # More than 10% variance
                if abs(variance) < 30:
                    severity = "low"
                elif abs(variance) < 50:
                    severity = "medium"
                else:
                    severity = "high"

                discrepancies.append(Discrepancy(
                    category="duration",
                    severity=severity,
                    message=f"Duration variance: {variance:+.1f}% ({planned_duration:.1f}h → {actual_duration:.1f}h)",
                    planned=planned_duration,
                    actual=actual_duration,
                    variance=abs(variance)
                ))

        return discrepancies

    def _parse_duration(self, duration_str: str) -> float:
        """
        Parse duration string to hours (e.g., '4 hours' -> 4.0).

        Args:
            duration_str: Duration string like "4 hours", "2.5h", "3 days"

        Returns:
            Duration in hours
        """
        if not duration_str:
            return 0.0

        try:
            duration_str = duration_str.lower()

            # Try to extract number
            match = re.search(r'(\d+\.?\d*)', duration_str)
            if not match:
                return 0.0

            value = float(match.group(1))

            # Convert to hours based on unit
            if 'day' in duration_str:
                return value * 8  # Assume 8-hour workday
            elif 'min' in duration_str:
                return value / 60
            else:  # Default to hours
                return value

        except Exception:
            return 0.0

    def _calculate_severity(self, discrepancies: List[Discrepancy]) -> Literal["low", "medium", "high"]:
        """
        Calculate overall severity based on all discrepancies.

        Rules:
        - 2+ high severity → high
        - 1 high OR 3+ medium → high
        - 1+ medium → medium
        - Otherwise → low

        Args:
            discrepancies: List of discrepancies

        Returns:
            Overall severity level
        """
        if not discrepancies:
            return "low"

        # Count by severity
        high_count = sum(1 for d in discrepancies if d.severity == "high")
        medium_count = sum(1 for d in discrepancies if d.severity == "medium")

        if high_count >= 2:
            return "high"
        elif high_count == 1 or medium_count >= 3:
            return "high"
        elif medium_count >= 1:
            return "medium"
        else:
            return "low"

    def _generate_recommendations(
        self,
        discrepancies: List[Discrepancy],
        severity: str
    ) -> List[str]:
        """
        Generate actionable recommendations based on discrepancies.

        Args:
            discrepancies: List of discrepancies
            severity: Overall severity level

        Returns:
            List of recommendation strings
        """
        recommendations = []

        for disc in discrepancies:
            if disc.category == "files" and "extra" in disc.message:
                files_preview = ', '.join(disc.actual[:3])
                if len(disc.actual) > 3:
                    files_preview += f", ... and {len(disc.actual) - 3} more"
                recommendations.append(
                    f"Review extra files for scope creep: {files_preview}"
                )

            elif disc.category == "files" and "missing" in disc.message:
                files_preview = ', '.join(disc.planned[:3])
                if len(disc.planned) > 3:
                    files_preview += f", ... and {len(disc.planned) - 3} more"
                recommendations.append(
                    f"Verify planned files were created: {files_preview}"
                )

            elif disc.category == "dependencies" and "extra" in disc.message:
                deps_preview = ', '.join(disc.actual[:3])
                if len(disc.actual) > 3:
                    deps_preview += f", ... and {len(disc.actual) - 3} more"
                recommendations.append(
                    f"Justify extra dependencies: {deps_preview}"
                )

            elif disc.category == "loc" and disc.variance > 50:
                recommendations.append(
                    f"Understand why LOC exceeded estimate by {disc.variance:.0f}%"
                )

            elif disc.category == "duration" and disc.variance > 50:
                recommendations.append(
                    f"Analyze duration overrun ({disc.variance:.0f}%) for future estimates"
                )

        if not recommendations:
            recommendations.append("No major concerns - implementation closely matches plan")

        return recommendations

    def _extract_plan_summary(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Extract summary from plan for report."""
        plan_data = plan.get("plan", {})
        return {
            "files": len(plan_data.get("files_to_create", [])),
            "files_to_modify": len(plan_data.get("files_to_modify", [])),
            "dependencies": len(plan_data.get("external_dependencies", [])),
            "estimated_loc": plan_data.get("estimated_loc", 0),
            "estimated_duration": plan_data.get("estimated_duration", "N/A")
        }

    def _is_excluded(self, file_path: Path) -> bool:
        """
        Check if file should be excluded from audit.

        Excludes:
        - Test files
        - Migration files
        - Generated files
        - Cache directories

        Args:
            file_path: Path to check

        Returns:
            True if should be excluded
        """
        excluded_patterns = [
            "**/test_*.py",
            "**/*_test.py",
            "**/*.test.ts",
            "**/*.test.tsx",
            "**/*.spec.ts",
            "**/*.spec.tsx",
            "**/tests/**",
            "**/migrations/**",
            "**/__pycache__/**",
            "**/node_modules/**",
            "**/.pytest_cache/**",
            "**/coverage/**",
            "**/*.pyc",
            "**/*.pyo"
        ]

        file_str = str(file_path)

        for pattern in excluded_patterns:
            if file_path.match(pattern):
                return True

        return False


class PlanAuditError(Exception):
    """Raised when plan audit operations fail."""
    pass


def format_audit_report(report: PlanAuditReport) -> str:
    """
    Format audit report as human-readable summary.

    Args:
        report: Audit report to format

    Returns:
        Formatted report string
    """
    severity_emoji = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴"
    }

    output = []
    output.append("=" * 70)
    output.append(f"PLAN AUDIT - {report.task_id}")
    output.append("=" * 70)
    output.append("")

    # Planned implementation
    output.append("PLANNED IMPLEMENTATION:")
    plan = report.plan_summary
    output.append(f"  Files: {plan['files']} files ({plan['estimated_loc']} lines)")
    output.append(f"  Dependencies: {plan['dependencies']}")
    output.append(f"  Duration: {plan['estimated_duration']}")
    output.append("")

    # Actual implementation
    output.append("ACTUAL IMPLEMENTATION:")
    actual = report.actual_summary
    output.append(f"  Files: {len(actual.get('files_created', []))} files ({actual.get('total_loc', 0)} lines)")
    output.append(f"  Dependencies: {len(actual.get('dependencies', []))}")
    output.append(f"  Duration: {actual.get('duration_hours', 0):.1f} hours")
    output.append("")

    # Discrepancies
    if report.discrepancies:
        output.append("DISCREPANCIES:")
        for disc in report.discrepancies:
            emoji = severity_emoji.get(disc.severity, "⚠️")
            output.append(f"  {emoji} {disc.message}")

            # Show details for file/dependency discrepancies
            if disc.category in ["files", "dependencies"] and isinstance(disc.actual, list):
                for item in disc.actual[:5]:  # Show first 5
                    output.append(f"      - {item}")
                if len(disc.actual) > 5:
                    output.append(f"      ... and {len(disc.actual) - 5} more")

        output.append("")
    else:
        output.append("DISCREPANCIES: None")
        output.append("")

    # Severity
    severity_emoji_overall = severity_emoji.get(report.severity, "⚠️")
    output.append(f"SEVERITY: {severity_emoji_overall} {report.severity.upper()}")
    output.append("")

    # Recommendations
    output.append("RECOMMENDATIONS:")
    for i, rec in enumerate(report.recommendations, 1):
        output.append(f"  {i}. {rec}")
    output.append("")

    # Options
    output.append("OPTIONS:")
    output.append("  [A]pprove - Accept implementation as-is, update plan retroactively")
    output.append("  [R]evise - Request removal of scope creep items")
    output.append("  [E]scalate - Mark as complex, create follow-up task")
    output.append("  [C]ancel - Block task completion")
    output.append("")

    return "\n".join(output)


# Module exports
__all__ = [
    "PlanAuditor",
    "PlanAuditReport",
    "Discrepancy",
    "PlanAuditError",
    "format_audit_report"
]
