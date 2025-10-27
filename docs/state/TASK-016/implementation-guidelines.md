# TASK-016: Implementation Guidelines and Best Practices

## Quick Reference

### Command Cheat Sheet

```bash
# Development workflow
./migrate-completed-tasks.sh                    # Dry-run preview
./migrate-completed-tasks.sh --execute -i       # Interactive execution
./migrate-completed-tasks.sh --validate-only    # Check existing state
./migrate-completed-tasks.sh --rollback FILE    # Restore from backup

# Testing workflow
bats tests/unit/*.bats                          # Run unit tests
bats tests/integration/*.bats                   # Run integration tests
shellcheck lib/*.sh migrate-completed-tasks.sh  # Static analysis
bashcov -- bats tests/**/*.bats                 # Coverage report
```

---

## Implementation Priority Matrix

### Critical Path (Must Complete First)

```
Priority 1: Foundation
┌────────────────────────────────┐
│ Phase A: CLI + Infrastructure  │ ← Start here
│ - Logging framework            │
│ - Error handling               │
│ - Lock mechanism               │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ Phase C: Backup Manager        │ ← Required for safety
│ - Backup creation              │
│ - Rollback capability          │
└────────────────────────────────┘
```

### Secondary Path (Core Functionality)

```
Priority 2: Discovery & Migration
┌────────────────────────────────┐
│ Phase B: File Discovery        │ ← Parallel with Phase D
│ - Task ID extraction           │
│ - File grouping                │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ Phase D: Git Operations        │ ← Parallel with Phase B
│ - Git mv wrapper               │
│ - History preservation         │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ Phase F: Name Standardization  │ ← Quick implementation
│ - Filename normalization       │
└────────────────────────────────┘
```

### Tertiary Path (Quality & Polish)

```
Priority 3: Quality Assurance
┌────────────────────────────────┐
│ Phase E: Link Management       │ ← After migration works
│ - Link detection               │
│ - Path adjustment              │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ Phase G: Validation            │ ← Final polish
│ - Post-migration checks        │
│ - Report generation            │
└────────────────────────────────┘
```

---

## Development Workflow

### Day 1: Foundation (6 hours)

**Morning Session (3 hours): Phase A**
```bash
# Create main script structure
cat > migrate-completed-tasks.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

readonly VERSION="1.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LIB_DIR="${SCRIPT_DIR}/lib"

source "${LIB_DIR}/core.sh"

main() {
  log INFO "Starting migration..."
}

main "$@"
EOF

chmod +x migrate-completed-tasks.sh

# Create core utilities
mkdir -p lib
touch lib/core.sh

# Implement logging and error handling
# Write unit tests
bats tests/unit/test_cli_parsing.bats
```

**Afternoon Session (3 hours): Phase C**
```bash
# Implement backup manager
touch lib/backup_manager.sh

# Test backup creation
./migrate-completed-tasks.sh --backup

# Verify backup integrity
tar -tzf .migration-backups/backup-*.tar.gz | head

# Test rollback
./migrate-completed-tasks.sh --rollback .migration-backups/backup-*.tar.gz
```

**End of Day 1 Checkpoint:**
- ✅ CLI framework working
- ✅ Logging with colors
- ✅ Backup/rollback tested
- ✅ Error handling in place

---

### Day 2: Discovery & Migration (7 hours)

**Morning Session (4 hours): Phases B & D**
```bash
# Implement file discovery
touch lib/project_detection.sh
touch lib/file_discovery.sh
touch lib/task_id_parser.sh

# Test task ID extraction
echo "Testing task ID extraction:"
extract_task_id "TASK-003-SUMMARY.md"           # → TASK-003
extract_task_id "TASK-003B-4-COMPLEXITY.md"     # → TASK-003B-4
extract_task_id "TASK_DUPLICATION_ANALYSIS.md"  # → (empty)

# Implement git operations
touch lib/git_operations.sh

# Test git mv on sample files
git_move_file "test.md" "tasks/completed/TASK-001/test.md"
git log --follow tasks/completed/TASK-001/test.md  # Verify history
```

**Afternoon Session (3 hours): Phase F**
```bash
# Implement name standardization
touch lib/name_standardizer.sh

# Test standardization rules
standardize_filename "TASK-003B-4-IMPLEMENTATION-SUMMARY.md" "TASK-003B-4"
# → implementation-summary.md

standardize_coverage_filename "coverage-task006.json"
# → task-006-coverage.json

# Run unit tests
bats tests/unit/test_task_id_parser.bats
bats tests/unit/test_name_standardizer.bats
```

**End of Day 2 Checkpoint:**
- ✅ File discovery working
- ✅ Task ID extraction handles edge cases
- ✅ Git mv preserves history
- ✅ Name standardization complete

---

### Day 3: Quality & Integration (8 hours)

**Morning Session (4 hours): Phase E**
```bash
# Implement link updater
touch lib/link_updater.sh

# Test link detection
cat > test-links.md <<'EOF'
[Guide](../docs/guide.md)
[API](../../api/reference.md)
[Image](../images/diagram.png)
EOF

detect_relative_links test-links.md

# Test link update
update_markdown_links test-links.md 1
# Should prepend ../ to all relative links

# Validate updated links
validate_links test-links.md
```

**Afternoon Session (4 hours): Phase G + Integration**
```bash
# Implement validator
touch lib/validator.sh

# Run integration tests
bats tests/integration/test_migration_flow.bats
bats tests/integration/test_idempotency.bats

# Test on sample repository
cd test-repo
../migrate-completed-tasks.sh --execute

# Verify results
../migrate-completed-tasks.sh --validate-only

# Check coverage
bashcov -- bats ../tests/**/*.bats
```

**End of Day 3 Checkpoint:**
- ✅ Link updating working
- ✅ Validation comprehensive
- ✅ Integration tests passing
- ✅ 80%+ test coverage achieved

---

### Day 4: Testing & Deployment (6 hours)

**Morning Session (3 hours): Edge Cases**
```bash
# Test edge cases
bats tests/integration/test_edge_cases.bats

# Test with real data (dry-run)
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer
./migrate-completed-tasks.sh  # Preview only

# Review output, verify expectations

# Test idempotency
./migrate-completed-tasks.sh --execute
./migrate-completed-tasks.sh --execute  # Should skip all
```

**Afternoon Session (3 hours): Deployment**
```bash
# Deploy to ai-engineer
./migrate-completed-tasks.sh --execute --interactive

# Verify results
find . -maxdepth 1 -name "TASK-*.md" | wc -l  # Should be 0
find tasks/completed -mindepth 1 -maxdepth 1 -type d | wc -l  # Should be 54

# Commit changes
git add -A
git commit -m "feat: Reorganize completed task files (TASK-016)"
git push

# Deploy to MyDrive (repeat process)
```

**End of Day 4 Checkpoint:**
- ✅ All edge cases handled
- ✅ Deployed to ai-engineer
- ✅ Deployed to MyDrive
- ✅ Documentation complete

---

## Code Style Guidelines

### Bash Best Practices

**1. Use Strict Mode**
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'        # Safe word splitting
```

**2. Function Documentation**
```bash
# Extract task ID from filename
# Arguments:
#   $1 - Filename (e.g., "TASK-003B-4-COMPLEXITY.md")
# Returns:
#   Task ID string (e.g., "TASK-003B-4")
#   Empty string if no match
# Exit codes:
#   0 - Success (task ID found)
#   1 - No match (not a task file)
extract_task_id() {
  local filename=$1
  # Implementation...
}
```

**3. Error Handling**
```bash
# Good: Explicit error handling
if ! git mv "$source" "$dest"; then
  log ERROR "Failed to move: $source"
  return 1
fi

# Bad: Silent failures
git mv "$source" "$dest" 2>/dev/null || true
```

**4. Variable Naming**
```bash
# Good: Descriptive, lowercase with underscores
local task_id="TASK-003"
local source_file="path/to/file.md"
readonly MAX_RETRIES=3

# Bad: Unclear, uppercase (reserved for env vars)
local TID="TASK-003"
local f="path/to/file.md"
```

**5. Quoting**
```bash
# Good: Always quote variables
local file="$1"
if [[ -f "$file" ]]; then
  echo "Found: $file"
fi

# Bad: Unquoted (breaks with spaces)
local file=$1
if [[ -f $file ]]; then
  echo "Found: $file"
fi
```

---

## Testing Best Practices

### Unit Test Structure

```bash
# tests/unit/test_task_id_parser.bats

setup() {
  # Load functions to test
  source lib/task_id_parser.sh
}

@test "extract_task_id: simple numeric format" {
  result=$(extract_task_id "TASK-003-SUMMARY.md")
  [ "$result" = "TASK-003" ]
}

@test "extract_task_id: with letter suffix" {
  result=$(extract_task_id "TASK-003B-IMPLEMENTATION.md")
  [ "$result" = "TASK-003B" ]
}

@test "extract_task_id: complex format with number" {
  result=$(extract_task_id "TASK-003B-4-COMPLEXITY.md")
  [ "$result" = "TASK-003B-4" ]
}

@test "extract_task_id: invalid format returns empty" {
  result=$(extract_task_id "NOT-A-TASK.md")
  [ -z "$result" ]
}

@test "extract_task_id: analysis file returns empty" {
  result=$(extract_task_id "TASK_DUPLICATION_ANALYSIS.md")
  [ -z "$result" ]
}
```

### Integration Test Structure

```bash
# tests/integration/test_migration_flow.bats

setup() {
  # Create temporary test repository
  export TEST_DIR=$(mktemp -d)
  cd "$TEST_DIR"
  git init
  git config user.email "test@example.com"
  git config user.name "Test User"

  # Create sample files
  mkdir -p tasks/completed
  echo "# Task 003" > tasks/completed/TASK-003.md
  echo "# Implementation" > TASK-003-IMPLEMENTATION-SUMMARY.md
  echo "# Completion" > TASK-003-COMPLETION-REPORT.md

  git add .
  git commit -m "Initial commit"

  # Copy migration script to test directory
  cp -r "$BATS_TEST_DIRNAME/../../migrate-completed-tasks.sh" .
  cp -r "$BATS_TEST_DIRNAME/../../lib" .
}

teardown() {
  # Cleanup
  cd /
  rm -rf "$TEST_DIR"
}

@test "end-to-end migration creates task subfolder" {
  run ./migrate-completed-tasks.sh --execute
  [ "$status" -eq 0 ]

  # Verify subfolder created
  [ -d "tasks/completed/TASK-003" ]
}

@test "end-to-end migration moves all related files" {
  ./migrate-completed-tasks.sh --execute

  # Verify files moved
  [ -f "tasks/completed/TASK-003/TASK-003.md" ]
  [ -f "tasks/completed/TASK-003/implementation-summary.md" ]
  [ -f "tasks/completed/TASK-003/completion-report.md" ]

  # Verify files removed from original locations
  [ ! -f "TASK-003-IMPLEMENTATION-SUMMARY.md" ]
  [ ! -f "TASK-003-COMPLETION-REPORT.md" ]
}

@test "end-to-end migration preserves git history" {
  ./migrate-completed-tasks.sh --execute

  # Check git log for moved file
  run git log --follow --oneline tasks/completed/TASK-003/TASK-003.md
  [ "$status" -eq 0 ]
  [[ "$output" =~ "Initial commit" ]]
}

@test "idempotency: second run makes no changes" {
  ./migrate-completed-tasks.sh --execute

  # Capture git status after first run
  local first_status=$(git status --porcelain)

  # Run again
  ./migrate-completed-tasks.sh --execute

  # Verify no additional changes
  local second_status=$(git status --porcelain)
  [ "$first_status" = "$second_status" ]
}
```

---

## Debugging Strategies

### Enable Debug Mode

```bash
# Add to migrate-completed-tasks.sh
if [[ "${DEBUG:-false}" == true ]]; then
  set -x  # Enable command tracing
  PS4='+ ${BASH_SOURCE}:${LINENO}: '  # Show file:line in trace
fi

# Run with debugging
DEBUG=true ./migrate-completed-tasks.sh --execute
```

### Logging Levels

```bash
# Implement logging levels in lib/core.sh
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

log() {
  local level=$1
  shift
  local message="$*"

  # Check if should log based on level
  case "$LOG_LEVEL" in
    ERROR) [[ "$level" == "ERROR" ]] || return ;;
    WARN)  [[ "$level" =~ ^(ERROR|WARN)$ ]] || return ;;
    INFO)  [[ "$level" =~ ^(ERROR|WARN|INFO)$ ]] || return ;;
    DEBUG) ;;  # Log everything
  esac

  # Rest of logging implementation...
}

# Usage
LOG_LEVEL=DEBUG ./migrate-completed-tasks.sh --execute
```

### Dry-Run Tracing

```bash
# Implement in migration functions
migrate_task_files() {
  local dry_run=${DRY_RUN:-false}

  for task_id in "${task_ids[@]}"; do
    if [[ "$dry_run" == true ]]; then
      log INFO "[DRY-RUN] Would migrate: $task_id"
    else
      log INFO "Migrating: $task_id"
      # Actual migration logic
    fi
  done
}
```

---

## Performance Optimization Tips

### 1. Batch Operations

```bash
# Bad: Serial processing (slow)
for file in "${files[@]}"; do
  git_move_file "$file" "$dest"
done

# Good: Batch git operations
git mv file1 file2 file3 dest/

# Better: Parallel processing (if safe)
printf '%s\n' "${files[@]}" | \
  xargs -P 4 -I {} bash -c 'git_move_file {} dest/'
```

### 2. Cache Expensive Operations

```bash
# Bad: Repeated git root detection
for file in "${files[@]}"; do
  local git_root=$(git rev-parse --show-toplevel)
  # Use git_root...
done

# Good: Cache once
readonly GIT_ROOT=$(git rev-parse --show-toplevel)
for file in "${files[@]}"; do
  # Use GIT_ROOT...
done
```

### 3. Optimize Regex Patterns

```bash
# Bad: Multiple regex matches
if [[ "$file" =~ TASK-[0-9]+ ]]; then
  task_num="${BASH_REMATCH[0]}"
fi
if [[ "$file" =~ TASK-[0-9]+[A-Z] ]]; then
  task_id="${BASH_REMATCH[0]}"
fi

# Good: Single comprehensive regex
if [[ "$file" =~ ^(TASK-[0-9]+([A-Z](-[0-9]+)?)?) ]]; then
  task_id="${BASH_REMATCH[1]}"
fi
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Word Splitting

```bash
# Problem: Filenames with spaces break
for file in $(find . -name "*.md"); do  # DON'T DO THIS
  echo "$file"
done

# Solution: Use while read with null delimiter
while IFS= read -r -d '' file; do
  echo "$file"
done < <(find . -name "*.md" -print0)

# Or: Array with proper quoting
mapfile -t files < <(find . -name "*.md")
for file in "${files[@]}"; do
  echo "$file"
done
```

### Pitfall 2: Unquoted Variables

```bash
# Problem: Variables with spaces or special chars
file="my file.md"
if [ -f $file ]; then  # Breaks: expands to multiple args
  echo "Found"
fi

# Solution: Always quote
if [[ -f "$file" ]]; then
  echo "Found"
fi
```

### Pitfall 3: Ignoring Exit Codes

```bash
# Problem: Silent failures
git mv source dest
process_next_file  # Runs even if git mv failed

# Solution: Check exit codes
if git mv source dest; then
  process_next_file
else
  log ERROR "Failed to move file"
  return 1
fi
```

### Pitfall 4: Platform-Specific Commands

```bash
# Problem: macOS vs Linux differences
sed -i 's/old/new/' file  # Works on Linux, fails on macOS

# Solution: Platform detection
if [[ "$(uname -s)" == "Darwin" ]]; then
  sed -i '' 's/old/new/' file  # macOS syntax
else
  sed -i 's/old/new/' file     # Linux syntax
fi
```

---

## Quality Gates Checklist

### Pre-Commit Checklist

- [ ] All unit tests passing (`bats tests/unit/*.bats`)
- [ ] All integration tests passing (`bats tests/integration/*.bats`)
- [ ] Shellcheck clean (`shellcheck lib/*.sh migrate-completed-tasks.sh`)
- [ ] Test coverage ≥80% (`bashcov`)
- [ ] Manual testing on sample repository
- [ ] Documentation updated

### Pre-Deployment Checklist

- [ ] Code review completed
- [ ] Dry-run tested on both projects
- [ ] Backup/rollback tested
- [ ] Edge cases verified (spaces, unicode, etc.)
- [ ] Performance acceptable (<2 min for 62 files)
- [ ] No broken links after migration
- [ ] Git history preserved for all files

### Post-Deployment Validation

- [ ] No task files in root directory
- [ ] All task subfolders have ≥1 file
- [ ] Coverage files organized correctly
- [ ] Analysis files archived
- [ ] `.gitignore` updated
- [ ] Migration report generated
- [ ] Rollback capability verified

---

## Quick Troubleshooting

### Issue: "Lock file exists"

```bash
# Check if process is running
ps aux | grep migrate-completed-tasks.sh

# If not running, remove stale lock
rm -f .migration-lock

# If running, wait or kill process
kill $(cat .migration-lock)
```

### Issue: "Git mv failed"

```bash
# Check git status
git status

# Ensure clean working tree
git add -A
git commit -m "WIP: Before migration"

# Check file exists
ls -la path/to/source/file

# Check permissions
ls -ld path/to/dest/directory

# Verify destination directory exists
mkdir -p path/to/dest/directory
```

### Issue: "Broken links detected"

```bash
# Find broken links
find tasks/completed -name "*.md" -exec markdown-link-check {} \;

# Manual fix
# Edit file and update link paths

# Re-validate
./migrate-completed-tasks.sh --validate-only
```

### Issue: "Backup creation failed"

```bash
# Check disk space
df -h

# Check permissions
ls -ld .migration-backups

# Try manual backup
tar -czf backup-manual.tar.gz tasks/ docs/ TASK*.md coverage*.json

# Verify backup integrity
tar -tzf backup-manual.tar.gz | head
```

---

## Next Steps After Implementation

### 1. Update `/task-complete` Command

Modify the task completion workflow to automatically create subfolders:

```bash
# In installer/global/commands/task-complete.md
# Add logic to create subfolder structure

TASK_ID="TASK-042"
COMPLETED_DIR="tasks/completed/${TASK_ID}"

mkdir -p "$COMPLETED_DIR"
git mv "tasks/in_progress/${TASK_ID}.md" "$COMPLETED_DIR/"

# Move any related files
find . -name "${TASK_ID}-*.md" -exec git mv {} "$COMPLETED_DIR/" \;
```

### 2. Update `.gitignore` Patterns

```gitignore
# Coverage reports (prevent root pollution)
coverage.json
coverage_*.json
coverage-*.json

# Coverage directory (allow .gitkeep)
coverage/
!coverage/.gitkeep
```

### 3. Update Testing Configuration

```toml
# pyproject.toml (if using pytest)
[tool.coverage.run]
data_file = "coverage/reports/.coverage"

[tool.coverage.html]
directory = "coverage/reports/html"

[tool.coverage.json]
output = "coverage/reports/coverage.json"
```

### 4. Documentation Updates

- [ ] Update project README with new structure
- [ ] Add migration guide to docs/
- [ ] Update task workflow documentation
- [ ] Create runbook for future migrations

---

## Maintenance and Future Enhancements

### Potential Enhancements (Future Tasks)

1. **Automated Link Fixing**
   - Use `markdown-link-check` API to auto-fix broken links
   - Generate link fix report with suggested changes

2. **Web UI for Migration**
   - Create simple web interface for migration preview
   - Interactive file selection and customization

3. **Incremental Migration**
   - Migrate tasks as they complete (via `/task-complete`)
   - No need for batch migration script

4. **Smart Duplicate Detection**
   - Detect duplicate files before migration
   - Prompt for merge or separate strategies

5. **Coverage Integration**
   - Automatically move coverage files on test runs
   - Hook into pytest to write to correct directory

---

## Success Metrics Dashboard

**Track these metrics post-deployment:**

```
┌─────────────────────────────────────────────────────────┐
│              TASK-016 Success Metrics                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Files Migrated:          62 / 62        (100%)  ✅     │
│  Root Files Remaining:     0 / 62        (0%)    ✅     │
│  Broken Links:             0             (0%)    ✅     │
│  Git History Preserved:   62 / 62        (100%)  ✅     │
│  Migration Time:          1m 45s         (<2min) ✅     │
│  Test Coverage:           85%            (>80%)  ✅     │
│  Edge Cases Handled:      10 / 10        (100%)  ✅     │
│                                                          │
│  Overall Status:  🎉 SUCCESS                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Contact and Support

**For issues or questions:**
- Review this document first
- Check troubleshooting section
- Examine test cases for examples
- Consult technical design document

**Rollback procedure:**
```bash
# If anything goes wrong
./migrate-completed-tasks.sh --rollback .migration-backups/backup-YYYYMMDD-HHMMSS.tar.gz
```

---

**Document Version:** 1.0
**Companion to:** technical-design.md
**Last Updated:** 2025-10-17
