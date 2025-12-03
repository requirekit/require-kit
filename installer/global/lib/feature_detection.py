"""
Feature Detection Library

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  SHARED FILE - KEEP IN SYNC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This file is duplicated across multiple repositories:
  • guardkit/installer/global/lib/feature_detection.py
  • require-kit/installer/global/lib/feature_detection.py

When making changes:
  1. Update both copies to maintain consistency
  2. Test in both contexts (guardkit-only and require-kit-only)
  3. Changes should be rare (only when adding new packages or features)

Why duplicated?
  • Simple: No dependency management, each repo is self-contained
  • Stable: Infrequent changes (only when package ecosystem evolves)
  • Small: ~270 lines, stdlib-only, easy to keep in sync

If this grows beyond 1000 lines or 3+ repos need it, consider creating
a shared agentecflow-common package. Until then, duplication is the
pragmatic choice.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Provides utilities to detect which Agentecflow packages are installed
and enable graceful degradation of features.

**Bidirectional Optional Integration Model:**
- guardkit works standalone (task execution + quality gates)
- require-kit works standalone (requirements management + EARS/BDD)
- Both packages detect each other via marker files
- Enhanced features available when both installed
- No hard dependencies either way

This enables guardkit and require-kit to coexist in ~/.agentecflow
with conditional feature availability based on installed marker files.

Core Capabilities:
  • Detect installed packages (guardkit, require-kit)
  • Query feature availability (requirements, epics, BDD, etc.)
  • Check package compatibility
  • Provide user-friendly status messages

Usage:
    from lib.feature_detection import supports_requirements

    if supports_requirements():
        # Load EARS requirements
        requirements = load_requirements()
    else:
        # Gracefully skip requirements features
        requirements = []
"""

from pathlib import Path
from typing import Dict, List, Optional
import json


class FeatureDetector:
    """Detects installed Agentecflow packages and available features."""

    def __init__(self, agentecflow_home: Optional[Path] = None):
        """
        Initialize feature detector.

        Args:
            agentecflow_home: Path to .agentecflow directory.
                            Defaults to ~/.agentecflow
        """
        self.agentecflow_home = agentecflow_home or Path.home() / ".agentecflow"

    def is_guardkit_installed(self) -> bool:
        """Check if guardkit is installed."""
        marker = self.agentecflow_home / "guardkit.marker.json"
        return marker.exists()

    def is_require_kit_installed(self) -> bool:
        """Check if require-kit is installed."""
        marker = self.agentecflow_home / "require-kit.marker.json"
        return marker.exists()

    def supports_requirements(self) -> bool:
        """
        Check if requirements management features are available.

        Returns:
            True if require-kit is installed, False otherwise
        """
        return self.is_require_kit_installed()

    def supports_epics(self) -> bool:
        """
        Check if epic management features are available.

        Returns:
            True if require-kit is installed, False otherwise
        """
        return self.is_require_kit_installed()

    def supports_features(self) -> bool:
        """
        Check if feature management is available.

        Returns:
            True if require-kit is installed, False otherwise
        """
        return self.is_require_kit_installed()

    def supports_bdd(self) -> bool:
        """
        Check if BDD/Gherkin scenario generation is available.

        Returns:
            True if require-kit is installed, False otherwise
        """
        return self.is_require_kit_installed()

    def get_installed_packages(self) -> List[str]:
        """
        Get list of installed Agentecflow packages.

        Returns:
            List of package names (e.g., ['guardkit', 'require-kit'])
        """
        packages = []
        if self.is_guardkit_installed():
            packages.append("guardkit")
        if self.is_require_kit_installed():
            packages.append("require-kit")
        return packages

    def get_package_info(self, package_name: str) -> Optional[Dict]:
        """
        Get information about an installed package.

        Args:
            package_name: Name of the package (e.g., 'guardkit')

        Returns:
            Package manifest dict or None if not installed
        """
        manifest_path = self.agentecflow_home / f"{package_name}.manifest.json"
        if not manifest_path.exists():
            return None

        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def get_available_features(self) -> Dict[str, bool]:
        """
        Get dictionary of all features and their availability.

        Returns:
            Dict mapping feature names to availability (True/False)
        """
        return {
            "task_management": self.is_guardkit_installed(),
            "quality_gates": self.is_guardkit_installed(),
            "architectural_review": self.is_guardkit_installed(),
            "test_enforcement": self.is_guardkit_installed(),
            "requirements_engineering": self.supports_requirements(),
            "bdd_generation": self.supports_bdd(),
            "epic_management": self.supports_epics(),
            "feature_management": self.supports_features(),
        }

    def check_compatibility(self) -> Dict[str, any]:
        """
        Check compatibility between installed packages.

        Returns:
            Dict with compatibility status and any warnings
        """
        result = {
            "compatible": True,
            "warnings": [],
            "errors": []
        }

        # Bidirectional optional integration - no hard dependencies
        # Both packages work standalone, enhanced features when both present
        if self.is_require_kit_installed() and not self.is_guardkit_installed():
            result["warnings"].append(
                "require-kit installed without guardkit - requirements management available, "
                "install guardkit for full integration (task execution)"
            )

        if self.is_guardkit_installed() and not self.is_require_kit_installed():
            result["warnings"].append(
                "guardkit installed without require-kit - task execution available, "
                "install require-kit for full integration (requirements management)"
            )

        return result

    def get_feature_status_message(self) -> str:
        """
        Get a human-readable message about feature availability.

        Returns:
            Status message string
        """
        packages = self.get_installed_packages()

        if not packages:
            return "No Agentecflow packages installed"

        if len(packages) == 1:
            if packages[0] == "guardkit":
                return "guardkit installed (task execution only, install require-kit for requirements management)"
            elif packages[0] == "require-kit":
                return "require-kit installed (requirements management only, install guardkit for task execution)"

        if "guardkit" in packages and "require-kit" in packages:
            return "Full Agentecflow (guardkit + require-kit with bidirectional integration)"

        return f"Installed: {', '.join(packages)}"


# Global instance for convenience
_detector = FeatureDetector()


def is_require_kit_installed() -> bool:
    """
    Check if require-kit is installed.

    Returns:
        True if require-kit is available, False otherwise
    """
    return _detector.is_require_kit_installed()


def supports_requirements() -> bool:
    """
    Check if requirements features are available.

    Returns:
        True if requirements management is available, False otherwise
    """
    return _detector.supports_requirements()


def supports_epics() -> bool:
    """
    Check if epic management is available.

    Returns:
        True if epic management is available, False otherwise
    """
    return _detector.supports_epics()


def supports_features() -> bool:
    """
    Check if feature management is available.

    Returns:
        True if feature management is available, False otherwise
    """
    return _detector.supports_features()


def supports_bdd() -> bool:
    """
    Check if BDD/Gherkin generation is available.

    Returns:
        True if BDD generation is available, False otherwise
    """
    return _detector.supports_bdd()


def get_available_features() -> Dict[str, bool]:
    """
    Get all available features.

    Returns:
        Dict mapping feature names to availability
    """
    return _detector.get_available_features()


def check_feature_or_warn(feature_name: str, command_name: str) -> bool:
    """
    Check if a feature is available, print warning if not.

    Args:
        feature_name: Name of the feature to check
        command_name: Name of the command requiring the feature

    Returns:
        True if available, False otherwise (with warning printed)
    """
    features = get_available_features()

    if feature_name not in features:
        print(f"Warning: Unknown feature '{feature_name}'")
        return False

    if not features[feature_name]:
        print(f"Warning: {command_name} requires '{feature_name}' feature")
        print(f"Install require-kit to enable this feature:")
        print(f"  cd require-kit && ./installer/scripts/install.sh")
        return False

    return True
