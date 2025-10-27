"""
Complexity scoring factors using Strategy pattern.

This module implements individual complexity factors as strategies that can be
evaluated independently and aggregated. Each factor follows the Protocol pattern
for type safety and extensibility.

Factors:
- FileComplexityFactor: Scores based on number of files (0-3 points)
- PatternFamiliarityFactor: Scores based on pattern complexity (0-2 points)
- RiskLevelFactor: Scores based on risk indicators (0-3 points)

Future extension (deferred):
- DependencyComplexityFactor: External dependencies (0-2 points)
"""

from typing import Protocol, List
try:
    from .complexity_models import FactorScore, ImplementationPlan, EvaluationContext
except ImportError:
    from complexity_models import FactorScore, ImplementationPlan, EvaluationContext


class ComplexityFactor(Protocol):
    """Protocol for complexity scoring factors.

    Each factor evaluates one aspect of implementation complexity and returns
    a FactorScore with justification.
    """

    def evaluate(self, context: EvaluationContext) -> FactorScore:
        """Evaluate this factor and return a score.

        Args:
            context: Evaluation context with task and plan details

        Returns:
            FactorScore with numeric score and justification
        """
        ...


class FileComplexityFactor:
    """Evaluates complexity based on number of files to create/modify.

    Scoring:
    - 0-2 files: 0 points (simple, single-file change)
    - 3-5 files: 1 point (moderate, multi-file change)
    - 6-8 files: 2 points (complex, multiple components)
    - 9+ files: 3 points (very complex, cross-cutting change)

    Max Score: 3 points
    """

    FACTOR_NAME = "file_complexity"
    MAX_SCORE = 3

    def evaluate(self, context: EvaluationContext) -> FactorScore:
        """Evaluate file complexity based on file count."""
        plan = context.implementation_plan
        file_count = plan.file_count

        # Calculate score
        if file_count <= 2:
            score = 0
            justification = f"Simple change ({file_count} files) - minimal complexity"
        elif file_count <= 5:
            score = 1
            justification = f"Moderate change ({file_count} files) - multi-file coordination"
        elif file_count <= 8:
            score = 2
            justification = f"Complex change ({file_count} files) - multiple components"
        else:
            score = 3
            justification = f"Very complex change ({file_count} files) - cross-cutting concerns"

        return FactorScore(
            factor_name=self.FACTOR_NAME,
            score=score,
            max_score=self.MAX_SCORE,
            justification=justification,
            details={
                "file_count": file_count,
                "files": plan.files_to_create[:5]  # Include first 5 files
            }
        )


class PatternFamiliarityFactor:
    """Evaluates complexity based on design pattern sophistication.

    Scoring:
    - No patterns or simple patterns: 0 points (straightforward)
    - Moderate patterns (Strategy, Factory, Repository): 1 point (familiar)
    - Advanced patterns (Saga, CQRS, Event Sourcing): 2 points (complex)

    Max Score: 2 points
    """

    FACTOR_NAME = "pattern_familiarity"
    MAX_SCORE = 2

    # Pattern complexity mapping
    SIMPLE_PATTERNS = ["repository", "factory", "singleton", "adapter"]
    MODERATE_PATTERNS = ["strategy", "observer", "decorator", "command", "chain"]
    ADVANCED_PATTERNS = ["saga", "cqrs", "event sourcing", "mediator", "specification"]

    def evaluate(self, context: EvaluationContext) -> FactorScore:
        """Evaluate pattern complexity based on patterns mentioned in plan."""
        plan = context.implementation_plan
        patterns = [p.lower() for p in plan.patterns_used]

        # Check for advanced patterns
        advanced_found = [p for p in patterns if any(adv in p for adv in self.ADVANCED_PATTERNS)]
        if advanced_found:
            score = 2
            justification = f"Advanced patterns detected: {', '.join(advanced_found)} - high complexity"
            pattern_category = "advanced"
        # Check for moderate patterns
        elif patterns:
            moderate_found = [p for p in patterns if any(mod in p for mod in self.MODERATE_PATTERNS)]
            if moderate_found:
                score = 1
                justification = f"Moderate patterns: {', '.join(moderate_found)} - familiar complexity"
                pattern_category = "moderate"
            else:
                score = 0
                justification = f"Simple patterns: {', '.join(patterns)} - low complexity"
                pattern_category = "simple"
        else:
            score = 0
            justification = "No specific patterns mentioned - straightforward implementation"
            pattern_category = "none"

        return FactorScore(
            factor_name=self.FACTOR_NAME,
            score=score,
            max_score=self.MAX_SCORE,
            justification=justification,
            details={
                "patterns_count": len(patterns),
                "patterns": patterns,
                "pattern_category": pattern_category
            }
        )


class RiskLevelFactor:
    """Evaluates complexity based on risk indicators in implementation.

    Risk indicators:
    - Security-related (auth, encryption, permissions)
    - Data integrity (schema changes, migrations)
    - External integrations (APIs, third-party services)
    - Performance-critical (high traffic, real-time)

    Scoring:
    - No risk indicators: 0 points (low risk)
    - 1-2 risk indicators: 1 point (moderate risk)
    - 3-4 risk indicators: 2 points (high risk)
    - 5+ risk indicators: 3 points (critical risk)

    Max Score: 3 points
    """

    FACTOR_NAME = "risk_level"
    MAX_SCORE = 3

    # Risk indicator categories
    SECURITY_KEYWORDS = [
        "authentication", "authorization", "auth", "security", "permission",
        "password", "token", "jwt", "oauth", "encryption", "crypto", "signing"
    ]

    DATA_INTEGRITY_KEYWORDS = [
        "migration", "schema", "alter table", "create table", "drop table",
        "database", "transaction", "acid", "consistency"
    ]

    EXTERNAL_INTEGRATION_KEYWORDS = [
        "api", "external", "third-party", "integration", "webhook",
        "http client", "rest", "graphql", "grpc"
    ]

    PERFORMANCE_KEYWORDS = [
        "performance", "optimization", "caching", "scaling", "load",
        "throughput", "latency", "real-time", "streaming"
    ]

    def evaluate(self, context: EvaluationContext) -> FactorScore:
        """Evaluate risk level based on keywords and indicators."""
        plan = context.implementation_plan
        plan_lower = plan.raw_plan.lower()

        # Detect risk indicators
        security_risks = self._count_keywords(plan_lower, self.SECURITY_KEYWORDS)
        data_risks = self._count_keywords(plan_lower, self.DATA_INTEGRITY_KEYWORDS)
        external_risks = self._count_keywords(plan_lower, self.EXTERNAL_INTEGRATION_KEYWORDS)
        performance_risks = self._count_keywords(plan_lower, self.PERFORMANCE_KEYWORDS)

        # Calculate total unique risk categories
        risk_count = sum([
            1 if security_risks > 0 else 0,
            1 if data_risks > 0 else 0,
            1 if external_risks > 0 else 0,
            1 if performance_risks > 0 else 0
        ])

        # Calculate score
        if risk_count == 0:
            score = 0
            justification = "No significant risk indicators - low risk"
            risk_level = "low"
        elif risk_count <= 2:
            score = 1
            justification = f"Moderate risk ({risk_count} risk categories) - standard caution"
            risk_level = "moderate"
        elif risk_count <= 4:
            score = 2
            justification = f"High risk ({risk_count} risk categories) - careful review needed"
            risk_level = "high"
        else:
            score = 3
            justification = f"Critical risk ({risk_count}+ risk categories) - comprehensive review required"
            risk_level = "critical"

        # Build risk detail summary
        risk_categories = []
        if security_risks > 0:
            risk_categories.append(f"security ({security_risks} indicators)")
        if data_risks > 0:
            risk_categories.append(f"data_integrity ({data_risks} indicators)")
        if external_risks > 0:
            risk_categories.append(f"external_integration ({external_risks} indicators)")
        if performance_risks > 0:
            risk_categories.append(f"performance ({performance_risks} indicators)")

        return FactorScore(
            factor_name=self.FACTOR_NAME,
            score=score,
            max_score=self.MAX_SCORE,
            justification=justification,
            details={
                "risk_level": risk_level,
                "risk_count": risk_count,
                "risk_categories": risk_categories,
                "security_indicators": security_risks,
                "data_integrity_indicators": data_risks,
                "external_integration_indicators": external_risks,
                "performance_indicators": performance_risks
            }
        )

    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        """Count unique keyword matches in text."""
        matches = sum(1 for keyword in keywords if keyword in text)
        return min(matches, 10)  # Cap at 10 to avoid skewing


# Default factor set for MVP (3 core factors)
DEFAULT_FACTORS: List[ComplexityFactor] = [
    FileComplexityFactor(),
    PatternFamiliarityFactor(),
    RiskLevelFactor()
]
