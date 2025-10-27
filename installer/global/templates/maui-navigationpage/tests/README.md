# MAUI NavigationPage Template - Test Suite

## Quick Start

Run the complete validation suite:

```bash
cd installer/global/templates/maui-navigationpage
./tests/validate-template.sh
```

## Test Coverage

The validation suite checks:

### 1. Directory Structure (11 checks)
- All required directories present
- Proper template hierarchy

### 2. File Existence (18 checks)
- Agent files (8)
- Navigation components (3)
- Configuration files (3)
- Documentation files (3)
- Test files (1)

### 3. JSON Validation (11 checks)
- Valid JSON syntax
- Required fields present
- Proper structure

### 4. Documentation Completeness (15 checks)
- CLAUDE.md sections
- README.md sections
- MIGRATION.md sections

### 5. Source Attribution (8 checks)
- All agent files properly attributed

## Test Reports

Test execution generates reports in `tests/reports/`:
- `test-execution-report-YYYYMMDD.md` - Detailed test results
- `test-coverage-summary-YYYYMMDD.txt` - Coverage metrics

## Quality Gates

| Gate | Threshold | Description |
|------|-----------|-------------|
| Directory Structure | 100% | All directories must exist |
| File Existence | 100% | All required files must exist |
| JSON Validation | 100% | All JSON must be valid |
| Documentation | ≥90% | Documentation must be comprehensive |
| Source Attribution | 100% | All copied files must be attributed |

## Latest Test Results

**Date:** 2025-10-13
**Status:** ✅ PASSED
**Coverage:** 98.4% (62/63 checks)
**Warnings:** 1 (non-blocking)

## Manual Validation

For manual verification:

```bash
# Validate JSON files
jq empty config/manifest.json
jq empty config/settings.json

# Check bash script syntax
bash -n tests/validate-template.sh

# Verify template placeholders
grep -r "{{ProjectName}}" templates/

# Count files
find . -type f | wc -l
```

## CI/CD Integration

To integrate with CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Validate Template
  run: |
    cd installer/global/templates/maui-navigationpage
    ./tests/validate-template.sh
```

## Requirements

- `bash` 4.0+
- `jq` (for JSON validation)
- `dotnet` SDK (optional, for compilation testing)

## Troubleshooting

**Issue:** Script not executable
**Solution:** `chmod +x tests/validate-template.sh`

**Issue:** jq not found
**Solution:** Install jq: `brew install jq` (macOS) or `apt-get install jq` (Linux)

## Related Files

- `/installer/global/agents/test-orchestrator.md` - Test orchestration rules
- `/installer/global/agents/test-verifier.md` - Test verification standards
- `CLAUDE.md` - Template usage documentation
- `README.md` - Template overview

## Version History

- **v1.0** (2025-10-13) - Initial test suite with 63 validation checks
