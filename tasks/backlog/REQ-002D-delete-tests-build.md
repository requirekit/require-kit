---
id: REQ-002D
title: "Delete Tests and Build Artifacts"
created: 2025-10-27
status: backlog
priority: high
complexity: 3
parent_task: REQ-002
subtasks: []
estimated_hours: 0.5
---

# REQ-002D: Delete Tests and Build Artifacts

## Description

Delete all test files, coverage reports, and build configuration files that are specific to task execution testing.

## Files/Directories to DELETE

### Test Directory

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/

# Delete entire tests directory
rm -rf tests/
```

### Coverage Files

```bash
# Delete coverage directory
rm -rf coverage/

# Delete coverage JSON files
rm -f coverage*.json
rm -f coverage-*.json
rm -f .coverage
```

### Build Configuration Files

```bash
# Node.js / TypeScript
rm -f package.json
rm -f package-lock.json
rm -f tsconfig.json
rm -f vitest.config.ts

# .NET
rm -f ai-engineer.sln
rm -f *.csproj

# Python testing
rm -f pytest.ini
```

### Test Scripts

```bash
# Delete test scripts
rm -f test_*.py
rm -f test-*.sh
rm -f validate-*.py
rm -f verify_*.py
rm -f test_*.txt
rm -f test-results.xml
rm -f test_output.txt
```

### Build/Development Artifacts

```bash
# Delete development files
rm -rf DEVELOPMENT/

# Delete example files (if task-focused)
rm -rf examples/

# Delete migration files (if task-focused)
rm -rf migrations/
```

## Files to KEEP

```bash
# Keep core files
✅ .gitignore
✅ README.md
✅ CLAUDE.md
✅ requirements.txt (minimal Python dependencies)
```

## Implementation

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/

# Delete tests
rm -rf tests/

# Delete coverage
rm -rf coverage/
rm -f coverage*.json .coverage

# Delete build configs
rm -f package.json package-lock.json tsconfig.json vitest.config.ts
rm -f ai-engineer.sln pytest.ini

# Delete test scripts
rm -f test_*.py test-*.sh validate-*.py verify_*.py
rm -f test_*.txt test-results.xml test_output.txt test-*.xml

# Delete development artifacts
rm -rf DEVELOPMENT/ examples/ migrations/

# List remaining files
echo "Remaining root files:"
ls -la | grep -v "^d" | grep -v "^\."
```

## Verification

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/require-kit/

# Verify tests deleted
[ ! -d "tests" ] && echo "✓ tests/ deleted" || echo "✗ tests/ still exists"

# Verify coverage deleted
[ ! -d "coverage" ] && echo "✓ coverage/ deleted" || echo "✗ coverage/ still exists"
! ls coverage*.json 2>/dev/null && echo "✓ coverage files deleted" || echo "✗ coverage files remain"

# Verify build configs deleted
! ls package.json tsconfig.json pytest.ini 2>/dev/null && echo "✓ build configs deleted" || echo "✗ build configs remain"

# Verify test scripts deleted
! ls test_*.py test-*.sh 2>/dev/null && echo "✓ test scripts deleted" || echo "✗ test scripts remain"
```

## Acceptance Criteria

- [ ] tests/ directory deleted
- [ ] coverage/ directory deleted
- [ ] All coverage*.json files deleted
- [ ] package.json, tsconfig.json, vitest.config.ts deleted
- [ ] ai-engineer.sln deleted
- [ ] pytest.ini deleted
- [ ] All test_*.py files deleted
- [ ] All test-*.sh files deleted
- [ ] DEVELOPMENT/, examples/, migrations/ deleted
- [ ] Only core files remain
- [ ] Verification tests pass

## Estimated Time

0.5 hours

## Notes

- This is a clean sweep of all testing/build artifacts
- We'll rebuild minimal testing later for requirements features
- Keep .gitignore and requirements.txt
- Commit after verification
