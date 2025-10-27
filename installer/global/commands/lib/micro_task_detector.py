"""
Micro-Task Detection System for /task-work Command

This module provides heuristic-based detection to identify micro-tasks that qualify
for streamlined workflow execution. Micro-tasks are trivial changes (typo fixes,
doc updates, cosmetic changes) that don't require full architectural review.

Key Responsibilities:
- Analyze task metadata to determine micro-task eligibility
- Detect high-risk keywords that block micro-task mode
- Provide actionable suggestions for micro-task mode usage
- Validate user-provided --micro flag against task characteristics

Design Principles:
- Conservative blocking (false negative better than false positive)
- Zero external dependencies
- Dataclass-based structured results
- Compiled regex patterns for performance
"""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MicroTaskAnalysis:
    """Structured result of micro-task detection analysis.

    Attributes:
        is_micro_task: Whether task qualifies for micro-task mode
        blocking_reasons: List of reasons preventing micro-task mode
        confidence_score: Confidence level (0.0-1.0)
        suggested_flags: Recommended command-line flags
        metadata: Additional analysis details
    """
    is_micro_task: bool
    blocking_reasons: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    suggested_flags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def can_use_micro_mode(self) -> bool:
        """Check if micro-task mode is allowed."""
        return self.is_micro_task and len(self.blocking_reasons) == 0

    @property
    def should_escalate(self) -> bool:
        """Check if task should escalate to full workflow."""
        return not self.is_micro_task or len(self.blocking_reasons) > 0


class MicroTaskDetector:
    """Detects micro-tasks eligible for streamlined workflow.

    Uses heuristic-based analysis to identify trivial tasks that can skip
    expensive workflow phases (architectural review, complexity evaluation).

    Micro-Task Criteria (ALL must be true):
    - Single file modification (or docs-only)
    - Estimated effort <1 hour
    - Low complexity indicators
    - No high-risk keywords (security, schema, breaking changes)

    Attributes:
        config: Configuration for thresholds and patterns
        _risk_patterns: Compiled regex patterns for risk detection
    """

    # High-risk keywords that block micro-task mode
    HIGH_RISK_KEYWORDS = {
        'security': ['security', 'auth', 'authentication', 'authorization', 'password',
                     'token', 'jwt', 'oauth', 'saml', 'encryption', 'crypto', 'permission'],
        'data': ['database', 'migration', 'schema', 'sql', 'table', 'column',
                 'alter table', 'drop', 'truncate', 'transaction'],
        'api': ['breaking', 'breaking change', 'api change', 'public api',
                'interface change', 'contract change'],
        'external': ['integration', 'third-party', 'external api', 'webhook',
                     'payment', 'billing'],
    }

    # Documentation file extensions (low risk)
    DOC_EXTENSIONS = {'.md', '.txt', '.rst', '.adoc', '.pdf', '.docx'}

    # Default configuration
    DEFAULT_CONFIG = {
        'max_files': 1,
        'max_hours': 1.0,
        'max_complexity': 1,
        'confidence_threshold': 0.8,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize detector with configuration.

        Args:
            config: Optional configuration overrides
        """
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}

        # Compile regex patterns for performance
        self._risk_patterns = self._compile_risk_patterns()

        logger.info("MicroTaskDetector initialized with config: %s", self.config)

    def _compile_risk_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for risk keyword detection.

        Returns:
            Dictionary of compiled regex patterns by category
        """
        patterns = {}
        for category, keywords in self.HIGH_RISK_KEYWORDS.items():
            # Create case-insensitive pattern with word boundaries
            pattern = r'\b(?:' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'
            patterns[category] = re.compile(pattern, re.IGNORECASE)
            logger.debug(f"Compiled risk pattern for {category}: {len(keywords)} keywords")
        return patterns

    def analyze(self, task_metadata: Dict[str, Any]) -> MicroTaskAnalysis:
        """Analyze task to determine micro-task eligibility.

        Main entry point for micro-task detection. Performs comprehensive
        analysis of task metadata to determine if streamlined workflow is safe.

        Args:
            task_metadata: Task metadata including title, description, files, etc.

        Returns:
            MicroTaskAnalysis with detection results and reasoning
        """
        logger.info(f"Analyzing task {task_metadata.get('id', 'unknown')} for micro-task eligibility")

        blocking_reasons = []
        metadata = {}

        # Check 1: File count
        file_count = self._estimate_file_count(task_metadata)
        metadata['estimated_file_count'] = file_count

        if file_count > self.config['max_files']:
            blocking_reasons.append(
                f"Multiple files affected ({file_count} files, threshold: {self.config['max_files']})"
            )
            logger.debug(f"Blocked: file_count={file_count} > max_files={self.config['max_files']}")

        # Check 2: Estimated effort
        hours = self._parse_estimated_hours(task_metadata.get('estimated_effort'))
        metadata['estimated_hours'] = hours

        if hours and hours >= self.config['max_hours']:
            blocking_reasons.append(
                f"Estimated effort too high ({hours} hours, threshold: <{self.config['max_hours']} hour)"
            )
            logger.debug(f"Blocked: estimated_hours={hours} >= max_hours={self.config['max_hours']}")

        # Check 3: Complexity estimate
        complexity = task_metadata.get('complexity_estimate', 0)
        metadata['complexity_estimate'] = complexity

        if complexity > self.config['max_complexity']:
            blocking_reasons.append(
                f"Complexity too high ({complexity}/10, threshold: {self.config['max_complexity']}/10)"
            )
            logger.debug(f"Blocked: complexity={complexity} > max_complexity={self.config['max_complexity']}")

        # Check 4: High-risk keywords
        risk_results = self._detect_high_risk(task_metadata)
        metadata['risk_analysis'] = risk_results

        if risk_results['has_risks']:
            for category, keywords in risk_results['found_keywords'].items():
                blocking_reasons.append(
                    f"High-risk {category} keywords detected: {', '.join(keywords)}"
                )
                logger.debug(f"Blocked: risk category '{category}' with keywords: {keywords}")

        # Check 5: Documentation-only exception
        is_doc_only = self._is_documentation_only(task_metadata)
        metadata['is_doc_only'] = is_doc_only

        if is_doc_only:
            # Documentation-only changes are always safe for micro-task mode
            logger.info("Documentation-only task detected, allowing micro-task mode")
            blocking_reasons = []

        # Calculate confidence score
        confidence = self._calculate_confidence(
            file_count=file_count,
            hours=hours,
            complexity=complexity,
            has_risks=risk_results['has_risks'],
            is_doc_only=is_doc_only
        )
        metadata['confidence_calculation'] = confidence

        # Determine micro-task eligibility
        is_micro_task = len(blocking_reasons) == 0 and confidence >= self.config['confidence_threshold']

        # Generate suggested flags
        suggested_flags = []
        if is_micro_task:
            suggested_flags.append('--micro')

        analysis = MicroTaskAnalysis(
            is_micro_task=is_micro_task,
            blocking_reasons=blocking_reasons,
            confidence_score=confidence,
            suggested_flags=suggested_flags,
            metadata=metadata
        )

        logger.info(
            f"Analysis complete: is_micro_task={is_micro_task}, "
            f"confidence={confidence:.2f}, blocks={len(blocking_reasons)}"
        )

        return analysis

    def validate_micro_mode(self, task_metadata: Dict[str, Any]) -> bool:
        """Validate if --micro flag can be used for this task.

        Called when user explicitly provides --micro flag. Returns True if safe,
        False if task should escalate to full workflow.

        Args:
            task_metadata: Task metadata

        Returns:
            True if micro-mode is valid, False otherwise
        """
        analysis = self.analyze(task_metadata)

        if not analysis.can_use_micro_mode:
            logger.warning(
                f"User requested --micro but task doesn't qualify: {analysis.blocking_reasons}"
            )

        return analysis.can_use_micro_mode

    def suggest_micro_mode(self, task_metadata: Dict[str, Any]) -> Optional[str]:
        """Generate suggestion message for micro-task mode.

        Called during task-work to suggest --micro flag if applicable.

        Args:
            task_metadata: Task metadata

        Returns:
            Suggestion message if micro-task detected, None otherwise
        """
        analysis = self.analyze(task_metadata)

        if analysis.is_micro_task and analysis.confidence_score >= 0.9:
            task_id = task_metadata.get('id', 'TASK-XXX')
            return (
                f"\n💡 This task appears to be trivial (confidence: {analysis.confidence_score:.0%}).\n"
                f"   Consider using: /task-work {task_id} --micro\n"
                f"   Saves ~12 minutes by skipping optional phases.\n"
            )

        return None

    def _estimate_file_count(self, task_metadata: Dict[str, Any]) -> int:
        """Estimate number of files affected by task.

        Uses heuristics to estimate file count from task metadata:
        - Explicit 'files' or 'files_to_modify' metadata
        - Count file extensions in description
        - Count file paths in description
        - Default to 1 if unclear

        Args:
            task_metadata: Task metadata

        Returns:
            Estimated file count
        """
        # Check explicit file list
        if 'files' in task_metadata:
            return len(task_metadata['files'])

        if 'files_to_modify' in task_metadata:
            return len(task_metadata['files_to_modify'])

        # Analyze description for file mentions
        description = task_metadata.get('description', '')
        title = task_metadata.get('title', '')
        text = f"{title} {description}".lower()

        # Count file extension mentions (.py, .cs, .md, etc.)
        file_pattern = re.compile(r'\.\w{2,4}\b')
        file_mentions = file_pattern.findall(text)

        # Count explicit file path mentions
        path_pattern = re.compile(r'[\w/]+\.\w+')
        path_mentions = path_pattern.findall(text)

        # Use max of mentions (deduplicated)
        estimated = max(len(set(file_mentions)), len(set(path_mentions)), 1)

        logger.debug(f"Estimated file count: {estimated} (mentions: {len(file_mentions)}, paths: {len(path_mentions)})")

        return min(estimated, 10)  # Cap at 10 to avoid outliers

    def _parse_estimated_hours(self, effort_str: Optional[str]) -> Optional[float]:
        """Parse estimated effort string to hours.

        Supports formats:
        - "1 hour", "2 hours"
        - "30 minutes", "45 mins"
        - "1-2 hours"
        - "15m", "1h", "2.5h"

        Args:
            effort_str: Estimated effort string

        Returns:
            Estimated hours as float, or None if unparseable
        """
        if not effort_str:
            return None

        effort_lower = effort_str.lower().strip()

        # Handle range formats (take maximum)
        if '-' in effort_lower:
            parts = effort_lower.split('-')
            if len(parts) == 2:
                effort_lower = parts[1].strip()

        # Extract numeric value
        number_match = re.search(r'(\d+(?:\.\d+)?)', effort_lower)
        if not number_match:
            return None

        value = float(number_match.group(1))

        # Determine unit (hours or minutes)
        if 'min' in effort_lower or 'm' in effort_lower:
            hours = value / 60.0
        elif 'hour' in effort_lower or 'h' in effort_lower or 'hr' in effort_lower:
            hours = value
        else:
            # Assume hours if no unit specified
            hours = value

        logger.debug(f"Parsed effort '{effort_str}' as {hours:.2f} hours")

        return hours

    def _detect_high_risk(self, task_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Detect high-risk keywords in task metadata.

        Scans title, description, and labels for risk indicators.

        Args:
            task_metadata: Task metadata

        Returns:
            Dictionary with risk analysis results
        """
        title = task_metadata.get('title', '')
        description = task_metadata.get('description', '')
        labels = task_metadata.get('labels', [])

        # Combine all text for analysis
        text = f"{title} {description} {' '.join(labels)}"

        found_keywords = {}
        for category, pattern in self._risk_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # Deduplicate and lowercase
                unique_matches = list(set(m.lower() for m in matches))
                found_keywords[category] = unique_matches

        has_risks = len(found_keywords) > 0

        return {
            'has_risks': has_risks,
            'found_keywords': found_keywords,
            'categories': list(found_keywords.keys())
        }

    def _is_documentation_only(self, task_metadata: Dict[str, Any]) -> bool:
        """Check if task only affects documentation files.

        Documentation-only tasks are always safe for micro-task mode,
        even if they affect multiple files.

        Args:
            task_metadata: Task metadata

        Returns:
            True if task only affects documentation files
        """
        # Check explicit file list
        files = task_metadata.get('files', [])
        if files:
            # All files must have doc extensions
            return all(
                Path(f).suffix.lower() in self.DOC_EXTENSIONS
                for f in files
            )

        # Heuristic: check for doc-related keywords
        title = task_metadata.get('title', '').lower()
        description = task_metadata.get('description', '').lower()

        doc_keywords = ['documentation', 'readme', 'docs', 'comment', 'typo']
        text = f"{title} {description}"

        has_doc_keywords = any(keyword in text for keyword in doc_keywords)

        # Check for non-doc file extensions in text
        code_extensions = ['.py', '.cs', '.js', '.ts', '.java', '.go', '.rs']
        has_code_mentions = any(ext in text for ext in code_extensions)

        is_doc_only = has_doc_keywords and not has_code_mentions

        logger.debug(f"Documentation-only check: {is_doc_only} (doc_kw={has_doc_keywords}, code={has_code_mentions})")

        return is_doc_only

    def _calculate_confidence(
        self,
        file_count: int,
        hours: Optional[float],
        complexity: int,
        has_risks: bool,
        is_doc_only: bool
    ) -> float:
        """Calculate confidence score for micro-task classification.

        Combines multiple signals into single confidence score (0.0-1.0).

        Args:
            file_count: Estimated file count
            hours: Estimated hours (or None)
            complexity: Complexity estimate (0-10)
            has_risks: Whether high-risk keywords detected
            is_doc_only: Whether documentation-only task

        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 1.0

        # File count penalty (exponential)
        if file_count > 1:
            confidence *= 0.5 ** (file_count - 1)

        # Effort penalty
        if hours:
            if hours < 0.5:
                confidence *= 1.0  # Very quick task
            elif hours < 1.0:
                confidence *= 0.8
            else:
                confidence *= 0.3

        # Complexity penalty
        if complexity > 1:
            confidence *= 0.4
        elif complexity == 1:
            confidence *= 0.9
        else:
            confidence *= 1.0  # Complexity 0 or unset

        # Risk penalty (severe)
        if has_risks:
            confidence *= 0.1  # Almost always disqualifies

        # Documentation-only bonus
        if is_doc_only:
            confidence = max(confidence, 0.95)  # Override other penalties

        return min(max(confidence, 0.0), 1.0)  # Clamp to [0.0, 1.0]


# Public API functions for convenience
def analyze_micro_task(task_metadata: Dict[str, Any]) -> MicroTaskAnalysis:
    """Convenience function to analyze micro-task eligibility.

    Args:
        task_metadata: Task metadata dictionary

    Returns:
        MicroTaskAnalysis result
    """
    detector = MicroTaskDetector()
    return detector.analyze(task_metadata)


def validate_micro_mode(task_metadata: Dict[str, Any]) -> bool:
    """Convenience function to validate --micro flag usage.

    Args:
        task_metadata: Task metadata dictionary

    Returns:
        True if micro-mode is valid
    """
    detector = MicroTaskDetector()
    return detector.validate_micro_mode(task_metadata)


def suggest_micro_mode(task_metadata: Dict[str, Any]) -> Optional[str]:
    """Convenience function to generate micro-mode suggestion.

    Args:
        task_metadata: Task metadata dictionary

    Returns:
        Suggestion message or None
    """
    detector = MicroTaskDetector()
    return detector.suggest_micro_mode(task_metadata)
