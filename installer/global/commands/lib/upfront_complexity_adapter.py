"""
Adapter for evaluating complexity from requirements text.

This module adapts requirements-based input to the ImplementationPlan format
used by TASK-003A's complexity calculator, enabling complexity evaluation
before implementation planning begins.

Key Responsibilities:
- Parse requirements text to estimate file count
- Detect patterns from requirement keywords
- Identify risk indicators from requirements
- Build ImplementationPlan for TASK-003A calculator
"""

import logging
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Handle imports for both direct execution and import as module
try:
    from .complexity_calculator import ComplexityCalculator
    from .complexity_models import (
        ComplexityScore,
        ImplementationPlan,
        EvaluationContext
    )
except ImportError:
    # Add lib directory to path if not already there
    lib_dir = Path(__file__).parent
    if str(lib_dir) not in sys.path:
        sys.path.insert(0, str(lib_dir))

    from complexity_calculator import ComplexityCalculator
    from complexity_models import (
        ComplexityScore,
        ImplementationPlan,
        EvaluationContext
    )


logger = logging.getLogger(__name__)


class UpfrontComplexityAdapter:
    """Adapts requirements text to implementation plan format for complexity evaluation.

    This adapter bridges the gap between upfront requirements analysis and
    TASK-003A's complexity calculator by estimating implementation details
    from requirements text using heuristics.

    Attributes:
        calculator: TASK-003A ComplexityCalculator instance (reused)
        config: Configuration for pattern/risk detection
    """

    # Default configuration for pattern and risk detection
    DEFAULT_CONFIG = {
        "patterns": {
            "entity_keywords": ["user", "order", "product", "customer", "account", "profile"],
            "api_keywords": ["endpoint", "route", "api", "rest", "graphql", "service"],
            "ui_keywords": ["form", "dashboard", "component", "view", "page", "interface"],
            "database_keywords": ["migration", "schema", "table", "database", "query"]
        },
        "risks": {
            "security_keywords": ["auth", "password", "token", "encryption", "permission", "security"],
            "data_keywords": ["migration", "schema", "database", "transaction", "consistency"],
            "external_keywords": ["api", "integration", "third-party", "webhook", "external"]
        },
        "file_estimation": {
            "files_per_entity": 2,  # model + service
            "files_per_api": 2,  # controller + tests
            "files_per_ui": 1,  # component
            "files_per_database": 1  # migration
        }
    }

    # Pattern detection mappings
    PATTERN_KEYWORDS = {
        "strategy": ["authentication", "payment", "provider", "algorithm"],
        "observer": ["notification", "event", "subscriber", "listener", "webhook"],
        "decorator": ["caching", "logging", "validation", "middleware"],
        "factory": ["create", "builder", "instantiate", "generate"],
        "singleton": ["connection", "pool", "manager", "registry"],
        "repository": ["data access", "query", "persistence", "storage"],
        "adapter": ["integration", "wrapper", "bridge", "interface"]
    }

    def __init__(self, calculator: ComplexityCalculator, config: Optional[Dict[str, Any]] = None):
        """Initialize adapter with TASK-003A calculator.

        Args:
            calculator: ComplexityCalculator instance from TASK-003A
            config: Optional configuration for pattern/risk detection
        """
        self.calculator = calculator
        self.config = config or self.DEFAULT_CONFIG
        logger.info("UpfrontComplexityAdapter initialized")

    def evaluate_requirements(
        self,
        requirements_text: str,
        task_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplexityScore:
        """Evaluate complexity from requirements text.

        Main entry point for upfront complexity evaluation. Converts requirements
        to ImplementationPlan format and delegates to TASK-003A calculator.

        Args:
            requirements_text: Requirements in EARS, BDD, or plain text format
            task_id: Task identifier (e.g., TASK-005)
            metadata: Optional task metadata (priority, tags, etc.)

        Returns:
            ComplexityScore from TASK-003A calculator

        Raises:
            Never raises - errors handled by calculator's fail-safe logic
        """
        logger.info(f"Evaluating upfront complexity for {task_id}")

        try:
            # Step 1: Estimate files from requirements
            estimated_files = self._estimate_files_from_requirements(requirements_text)
            logger.debug(f"Estimated {len(estimated_files)} files from requirements")

            # Step 2: Detect patterns from requirements
            detected_patterns = self._detect_patterns_from_requirements(requirements_text)
            logger.debug(f"Detected patterns: {detected_patterns}")

            # Step 3: Identify risk indicators
            risk_indicators = self._detect_risk_indicators(requirements_text)
            logger.debug(f"Risk indicators: {risk_indicators}")

            # Step 4: Estimate external dependencies
            dependencies = self._detect_external_dependencies(requirements_text)
            logger.debug(f"External dependencies: {dependencies}")

            # Step 5: Build ImplementationPlan (TASK-003A model)
            implementation_plan = ImplementationPlan(
                task_id=task_id,
                files_to_create=estimated_files,
                patterns_used=detected_patterns,
                external_dependencies=dependencies,
                estimated_loc=self._estimate_loc(estimated_files),
                risk_indicators=risk_indicators,
                raw_plan=requirements_text
            )

            # Step 6: Build EvaluationContext
            context = EvaluationContext(
                task_id=task_id,
                technology_stack=metadata.get("technology_stack", "unknown") if metadata else "unknown",
                implementation_plan=implementation_plan,
                task_metadata=metadata or {},
                user_flags={}
            )

            # Step 7: Delegate to TASK-003A calculator (100% reuse)
            complexity_score = self.calculator.calculate(context)

            logger.info(
                f"Upfront complexity calculated: score={complexity_score.total_score}, "
                f"mode={complexity_score.review_mode.value}"
            )

            return complexity_score

        except Exception as e:
            logger.error(f"Error in upfront complexity evaluation: {e}", exc_info=True)
            # Let calculator's fail-safe logic handle errors
            raise

    def _estimate_files_from_requirements(self, text: str) -> List[str]:
        """Estimate files to be created based on requirements text.

        Uses heuristics to predict file structure from requirements:
        - Entities mentioned → model files
        - API endpoints → controller/service files
        - UI components → view/component files
        - Database mentions → migration files

        Args:
            text: Requirements text

        Returns:
            List of estimated file paths
        """
        files = []
        text_lower = text.lower()

        # Extract configuration
        patterns = self.config.get("patterns", self.DEFAULT_CONFIG["patterns"])
        file_est = self.config.get("file_estimation", self.DEFAULT_CONFIG["file_estimation"])

        # Count entities (User, Order, Product, etc.)
        entity_keywords = patterns.get("entity_keywords", [])
        entity_count = sum(1 for keyword in entity_keywords if keyword in text_lower)
        if entity_count > 0:
            files.extend([f"models/{keyword}.py" for keyword in entity_keywords if keyword in text_lower])
            files.extend([f"services/{keyword}_service.py" for keyword in entity_keywords if keyword in text_lower])

        # Count API endpoints
        api_keywords = patterns.get("api_keywords", [])
        api_count = sum(1 for keyword in api_keywords if keyword in text_lower)
        if api_count > 0:
            files.append("api/endpoints.py")
            files.append("api/routes.py")

        # Count UI components
        ui_keywords = patterns.get("ui_keywords", [])
        ui_count = sum(1 for keyword in ui_keywords if keyword in text_lower)
        if ui_count > 0:
            for keyword in ui_keywords:
                if keyword in text_lower:
                    files.append(f"components/{keyword}.tsx")

        # Count database operations
        db_keywords = patterns.get("database_keywords", [])
        db_count = sum(1 for keyword in db_keywords if keyword in text_lower)
        if db_count > 0:
            files.append("migrations/001_initial.sql")

        # If no specific indicators, estimate minimal structure
        if not files:
            files = ["main.py", "tests/test_main.py"]

        logger.debug(f"File estimation: {len(files)} files from requirements")
        return files

    def _detect_patterns_from_requirements(self, text: str) -> List[str]:
        """Detect design patterns likely needed from requirements keywords.

        Maps requirement keywords to appropriate design patterns:
        - "authentication" → Strategy pattern (multiple auth providers)
        - "notification" → Observer pattern (event handlers)
        - "caching" → Decorator pattern
        - "create X" → Factory pattern

        Args:
            text: Requirements text

        Returns:
            List of detected pattern names
        """
        detected = []
        text_lower = text.lower()

        for pattern, keywords in self.PATTERN_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(pattern)
                logger.debug(f"Pattern detected: {pattern} (keywords: {keywords})")

        return detected

    def _detect_risk_indicators(self, text: str) -> List[str]:
        """Detect risk indicators from requirements.

        Identifies high-risk functionality mentioned in requirements:
        - Security: authentication, encryption, permissions
        - Data integrity: migrations, transactions, schema changes
        - External dependencies: API integrations, third-party services

        Args:
            text: Requirements text

        Returns:
            List of risk indicator keywords found
        """
        risks = []
        text_lower = text.lower()

        risk_config = self.config.get("risks", self.DEFAULT_CONFIG["risks"])

        # Check security risks
        security_keywords = risk_config.get("security_keywords", [])
        for keyword in security_keywords:
            if keyword in text_lower:
                risks.append(f"security:{keyword}")

        # Check data risks
        data_keywords = risk_config.get("data_keywords", [])
        for keyword in data_keywords:
            if keyword in text_lower:
                risks.append(f"data:{keyword}")

        # Check external integration risks
        external_keywords = risk_config.get("external_keywords", [])
        for keyword in external_keywords:
            if keyword in text_lower:
                risks.append(f"external:{keyword}")

        logger.debug(f"Risk indicators detected: {risks}")
        return risks

    def _detect_external_dependencies(self, text: str) -> List[str]:
        """Detect external dependencies from requirements.

        Identifies external systems, APIs, or services mentioned:
        - Database systems (PostgreSQL, MongoDB)
        - External APIs (payment gateways, email services)
        - Third-party libraries

        Args:
            text: Requirements text

        Returns:
            List of external dependency names
        """
        dependencies = []
        text_lower = text.lower()

        # Common external systems
        external_systems = [
            "database", "postgresql", "mysql", "mongodb", "redis",
            "payment", "stripe", "paypal",
            "email", "sendgrid", "mailgun",
            "storage", "s3", "azure blob",
            "authentication", "oauth", "saml"
        ]

        for system in external_systems:
            if system in text_lower:
                dependencies.append(system)

        logger.debug(f"External dependencies detected: {dependencies}")
        return dependencies

    def _estimate_loc(self, files: List[str]) -> Optional[int]:
        """Estimate lines of code from file count.

        Simple heuristic: ~100 LOC per file on average.

        Args:
            files: List of estimated files

        Returns:
            Estimated total LOC
        """
        if not files:
            return None

        # Average 100 LOC per file (conservative estimate)
        estimated = len(files) * 100
        logger.debug(f"Estimated LOC: {estimated} ({len(files)} files × 100 LOC/file)")
        return estimated
