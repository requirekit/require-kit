"""
Duplicate task detection module.

This module provides fuzzy matching to detect duplicate or similar tasks
across all task directories to prevent duplicate work and maintain task
uniqueness.

Key Features:
- Fuzzy title matching using string similarity
- Cross-directory search (backlog, in_progress, in_review, blocked, completed)
- Configurable similarity threshold
- Detailed duplicate reports with similarity scores

Usage:
    from duplicate_detector import DuplicateDetector

    detector = DuplicateDetector()
    duplicates = detector.find_duplicates(task_data)
"""

import logging
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import re

logger = logging.getLogger(__name__)


@dataclass
class DuplicateMatch:
    """Represents a potential duplicate task match.

    Attributes:
        task_id: ID of the existing task
        title: Title of the existing task
        similarity_score: Similarity score (0.0-1.0)
        file_path: Path to the existing task file
        status: Current status of the duplicate (backlog, in_progress, etc.)
    """
    task_id: str
    title: str
    similarity_score: float
    file_path: str
    status: str

    @property
    def is_exact_match(self) -> bool:
        """Check if this is an exact title match."""
        return self.similarity_score >= 0.95

    @property
    def is_likely_duplicate(self) -> bool:
        """Check if this is likely a duplicate (>= 80% similar)."""
        return self.similarity_score >= 0.80


class DuplicateDetector:
    """Detects duplicate or similar tasks across all task directories.

    This detector uses fuzzy string matching to identify potential duplicates,
    helping prevent redundant work and maintain task uniqueness.
    """

    # Default similarity threshold (80%)
    DEFAULT_THRESHOLD = 0.80

    # Task directories to search
    TASK_DIRECTORIES = [
        "tasks/backlog",
        "tasks/in_progress",
        "tasks/in_review",
        "tasks/blocked",
        "tasks/completed"
    ]

    def __init__(
        self,
        threshold: float = DEFAULT_THRESHOLD,
        project_root: Optional[str] = None
    ):
        """Initialize duplicate detector.

        Args:
            threshold: Minimum similarity score to consider as duplicate (0.0-1.0)
            project_root: Project root directory (default: current directory)
        """
        self.threshold = threshold
        self.project_root = Path(project_root or os.getcwd())
        logger.info(f"DuplicateDetector initialized with threshold={threshold}")

    def find_duplicates(
        self,
        task_data: Dict[str, Any],
        threshold_override: Optional[float] = None
    ) -> List[DuplicateMatch]:
        """Find duplicate or similar tasks.

        Args:
            task_data: Task data dictionary with title and id
            threshold_override: Optional custom threshold for this search

        Returns:
            List of DuplicateMatch objects (sorted by similarity, descending)
        """
        threshold = threshold_override or self.threshold
        title = task_data.get("title", "")

        if not title:
            logger.warning("Task title is empty, cannot check for duplicates")
            return []

        logger.info(f"Searching for duplicates of: '{title}'")

        # Search all task directories
        all_matches = []
        for directory in self.TASK_DIRECTORIES:
            dir_path = self.project_root / directory

            if not dir_path.exists():
                continue

            matches = self._search_directory(dir_path, title, threshold)
            all_matches.extend(matches)

        # Sort by similarity score (descending)
        all_matches.sort(key=lambda m: m.similarity_score, reverse=True)

        if all_matches:
            logger.info(
                f"Found {len(all_matches)} potential duplicates "
                f"(threshold={threshold:.2f})"
            )
        else:
            logger.info("No duplicates found")

        return all_matches

    def _search_directory(
        self,
        directory: Path,
        title: str,
        threshold: float
    ) -> List[DuplicateMatch]:
        """Search a single directory for similar tasks.

        Args:
            directory: Directory path to search
            title: Task title to match against
            threshold: Similarity threshold

        Returns:
            List of matches from this directory
        """
        matches = []
        status = directory.name  # backlog, in_progress, etc.

        try:
            # Search for .md files
            for file_path in directory.glob("*.md"):
                # Extract task ID and title from filename
                task_info = self._parse_task_filename(file_path.name)

                if not task_info:
                    continue

                existing_id, existing_title = task_info

                # Calculate similarity
                similarity = self._calculate_similarity(title, existing_title)

                # Add if above threshold
                if similarity >= threshold:
                    match = DuplicateMatch(
                        task_id=existing_id,
                        title=existing_title,
                        similarity_score=similarity,
                        file_path=str(file_path),
                        status=status
                    )
                    matches.append(match)

        except Exception as e:
            logger.error(f"Error searching directory {directory}: {e}", exc_info=True)

        return matches

    def _parse_task_filename(self, filename: str) -> Optional[Tuple[str, str]]:
        """Parse task ID and title from filename.

        Expected format: TASK-XXX-title-with-dashes.md

        Args:
            filename: Task filename

        Returns:
            Tuple of (task_id, title) or None if invalid format
        """
        # Match pattern: TASK-XXX-title.md
        pattern = r"^(TASK-[\d.]+)-(.*?)\.md$"
        match = re.match(pattern, filename)

        if not match:
            return None

        task_id = match.group(1)
        title_slug = match.group(2)

        # Convert slug back to title (replace dashes with spaces, capitalize)
        title = title_slug.replace("-", " ").title()

        return (task_id, title)

    def _calculate_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity score between two titles.

        Uses a simple token-based similarity algorithm:
        1. Tokenize titles into words
        2. Calculate Jaccard similarity (intersection / union)
        3. Adjust for exact matches

        Args:
            title1: First title
            title2: Second title

        Returns:
            Similarity score (0.0-1.0)
        """
        # Normalize titles (lowercase, remove punctuation)
        normalized1 = self._normalize_title(title1)
        normalized2 = self._normalize_title(title2)

        # Exact match
        if normalized1 == normalized2:
            return 1.0

        # Tokenize
        tokens1 = set(normalized1.split())
        tokens2 = set(normalized2.split())

        # Calculate Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))

        if union == 0:
            return 0.0

        jaccard_score = intersection / union

        # Adjust for partial substring matches
        substring_bonus = 0.0
        if normalized1 in normalized2 or normalized2 in normalized1:
            substring_bonus = 0.1

        # Final score (capped at 1.0)
        final_score = min(jaccard_score + substring_bonus, 1.0)

        return round(final_score, 2)

    def _normalize_title(self, title: str) -> str:
        """Normalize title for comparison.

        Args:
            title: Raw title string

        Returns:
            Normalized title (lowercase, no punctuation, single spaces)
        """
        # Lowercase
        normalized = title.lower()

        # Remove punctuation
        normalized = re.sub(r"[^\w\s]", "", normalized)

        # Collapse multiple spaces
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return normalized

    def check_exact_duplicate(self, task_id: str) -> bool:
        """Check if a task ID already exists.

        Args:
            task_id: Task ID to check (e.g., TASK-001.2.05)

        Returns:
            True if task ID exists, False otherwise
        """
        logger.info(f"Checking for exact duplicate: {task_id}")

        for directory in self.TASK_DIRECTORIES:
            dir_path = self.project_root / directory

            if not dir_path.exists():
                continue

            # Search for files starting with task ID
            pattern = f"{task_id}-*.md"
            matches = list(dir_path.glob(pattern))

            if matches:
                logger.warning(
                    f"Exact duplicate found: {task_id} in {directory}/"
                )
                return True

        return False

    def get_duplicate_summary(
        self,
        matches: List[DuplicateMatch]
    ) -> Dict[str, Any]:
        """Generate summary statistics for duplicate matches.

        Args:
            matches: List of duplicate matches

        Returns:
            Summary dictionary with counts and statistics
        """
        if not matches:
            return {
                "total_matches": 0,
                "exact_matches": 0,
                "likely_duplicates": 0,
                "possible_duplicates": 0
            }

        exact = sum(1 for m in matches if m.is_exact_match)
        likely = sum(1 for m in matches if m.is_likely_duplicate and not m.is_exact_match)
        possible = len(matches) - exact - likely

        # Status distribution
        status_counts = {}
        for match in matches:
            status_counts[match.status] = status_counts.get(match.status, 0) + 1

        return {
            "total_matches": len(matches),
            "exact_matches": exact,
            "likely_duplicates": likely,
            "possible_duplicates": possible,
            "status_distribution": status_counts,
            "highest_similarity": matches[0].similarity_score if matches else 0.0
        }
