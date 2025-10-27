# TASK-016 Quick Start Guide

## For Implementers: Get Started in 5 Minutes

### What Are We Building?

A bash script that migrates **62 scattered task files** from the ai-engineer repo root into organized subfolders:

**Before:**
```
/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/
├── TASK-002-COMPLETION-REPORT.md         # 54 files like this in root
├── TASK-003B-4-COMPLEXITY-ANALYSIS.md
├── coverage-task006.json                  # 6 coverage files in root
└── TASK_DUPLICATION_ANALYSIS.md           # 2 analysis files in root
```

**After:**
```
/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/
├── tasks/completed/
│   ├── TASK-002/
│   │   └── completion-report.md
│   ├── TASK-003B-4/
│   │   ├── complexity-analysis.md
│   │   ├── design-summary.md
│   │   └── implementation-plan.md
│   └── ... (54 task folders)
├── coverage/reports/
│   ├── task-006-coverage.json
│   └── ... (6 coverage files)
└── docs/archive/
    └── task-duplication-analysis.md
```

### Key Features

✅ **Automatic Discovery** - Finds all TASK-XXX files
✅ **Git History Preserved** - Uses `git mv` for all moves
✅ **Backup/Rollback** - Creates backup before migration
✅ **Link Updates** - Fixes relative links in markdown
✅ **Idempotent** - Safe to run multiple times
✅ **80% Test Coverage** - 100 test cases (unit + integration)

---

## Setup (2 minutes)

### 1. Install Dependencies

```bash
# Check bash version (need 4.0+)
bash --version

# Install BATS testing framework
brew install bats-core  # macOS
# OR
sudo apt install bats   # Linux

# Install shellcheck (optional, for linting)
brew install shellcheck  # macOS
# OR
sudo apt install shellcheck  # Linux
```

### 2. Create Project Structure

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer

# Create directories
mkdir -p lib tests/unit tests/integration

# Create main script
touch migrate-completed-tasks.sh
chmod +x migrate-completed-tasks.sh
```

### 3. Verify Setup

```bash
# Check tools available
which bash git find grep sed awk tar bats shellcheck

# Should show paths for all commands
```

---

## Implementation Order (4 days)

### Day 1: Foundation (6 hours)

**Morning (3 hours): Phase A - CLI + Infrastructure**

```bash
# 1. Create main script skeleton
cat > migrate-completed-tasks.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

readonly VERSION="1.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LIB_DIR="${SCRIPT_DIR}/lib"
readonly LOCK_FILE=".migration-lock"

source "${LIB_DIR}/core.sh"

main() {
  parse_arguments "$@"
  validate_prerequisites
  create_lock_file
  trap cleanup_on_exit EXIT

  log INFO "Migration complete!"
}

main "$@"
EOF

# 2. Create core utilities
cat > lib/core.sh <<'EOF'
#!/usr/bin/env bash

log() {
  local level=$1
  shift
  local message="$*"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

  case "$level" in
    INFO)    color="\033[0;36m" ;;
    WARN)    color="\033[0;33m" ;;
    ERROR)   color="\033[0;31m" ;;
    SUCCESS) color="\033[0;32m" ;;
  esac

  echo -e "${color}[${timestamp}] [${level}] ${message}\033[0m"
}

die() {
  log ERROR "$1"
  exit "${2:-1}"
}
EOF

# 3. Test it works
./migrate-completed-tasks.sh --help
```

**Expected Output:**
```
Usage: migrate-completed-tasks.sh [OPTIONS]
...
```

**Afternoon (3 hours): Phase C - Backup Manager**

```bash
# Create backup manager
cat > lib/backup_manager.sh <<'EOF'
#!/usr/bin/env bash

create_backup() {
  local timestamp=$(date '+%Y%m%d-%H%M%S')
  local backup_file=".migration-backups/backup-${timestamp}.tar.gz"

  mkdir -p .migration-backups

  log INFO "Creating backup: $backup_file"

  tar -czf "$backup_file" \
    tasks/completed \
    TASK*.md \
    coverage*.json \
    2>/dev/null || true

  echo "$backup_file"
}
EOF

# Test backup
source lib/core.sh lib/backup_manager.sh
create_backup
ls -lh .migration-backups/
```

**End of Day 1 Checkpoint:**
- ✅ Script runs without errors
- ✅ Logging works with colors
- ✅ Backup creates .tar.gz file

---

### Day 2: Discovery & Migration (7 hours)

**Morning (4 hours): Phases B & D**

```bash
# 1. Project detection
cat > lib/project_detection.sh <<'EOF'
#!/usr/bin/env bash

detect_project_type() {
  if [[ -f "installer/global/manifest.json" ]]; then
    echo "ai-engineer"
  elif [[ -f "DeCUK.Mobile.MyDrive.sln" ]]; then
    echo "mydrive"
  else
    echo ""
  fi
}
EOF

# 2. Task ID extraction
cat > lib/task_id_parser.sh <<'EOF'
#!/usr/bin/env bash

extract_task_id() {
  local filename=$1
  local basename=$(basename "$filename" .md)

  # TASK-003B-4-COMPLEXITY.md → TASK-003B-4
  if [[ "$basename" =~ ^(TASK-[0-9]+([A-Z](-[0-9]+)?)?) ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi

  echo ""
  return 1
}
EOF

# 3. Test task ID extraction
source lib/task_id_parser.sh

extract_task_id "TASK-003-SUMMARY.md"           # → TASK-003
extract_task_id "TASK-003B-IMPLEMENTATION.md"   # → TASK-003B
extract_task_id "TASK-003B-4-COMPLEXITY.md"     # → TASK-003B-4

# 4. Git operations
cat > lib/git_operations.sh <<'EOF'
#!/usr/bin/env bash

git_move_file() {
  local source=$1
  local dest=$2

  mkdir -p "$(dirname "$dest")"

  if git mv "$source" "$dest" 2>/dev/null; then
    log INFO "Moved: $source → $dest"
    return 0
  else
    log ERROR "Failed to move: $source"
    return 1
  fi
}
EOF
```

**Test Task ID Extraction:**
```bash
# Create test file
echo "# Test" > TASK-003B-4-TEST.md

# Extract task ID
source lib/task_id_parser.sh
task_id=$(extract_task_id "TASK-003B-4-TEST.md")
echo "Extracted: $task_id"  # Should show: TASK-003B-4

# Cleanup
rm TASK-003B-4-TEST.md
```

**Afternoon (3 hours): Phase F - Name Standardization**

```bash
cat > lib/name_standardizer.sh <<'EOF'
#!/usr/bin/env bash

standardize_filename() {
  local original=$1
  local task_id=$2
  local basename=$(basename "$original" .md)

  # Remove task ID prefix
  local without_prefix="${basename#${task_id}-}"

  # Convert to lowercase and replace underscores
  local normalized=$(echo "$without_prefix" | tr '[:upper:]' '[:lower:]' | tr '_' '-')

  # Apply naming rules
  case "$normalized" in
    *implementation*) echo "implementation-summary.md" ;;
    *completion*)     echo "completion-summary.md" ;;
    *complexity*)     echo "complexity-evaluation.md" ;;
    *)                echo "${normalized}.md" ;;
  esac
}
EOF

# Test standardization
source lib/name_standardizer.sh

standardize_filename "TASK-003B-4-IMPLEMENTATION-SUMMARY.md" "TASK-003B-4"
# → implementation-summary.md

standardize_filename "TASK-003B-4-COMPLEXITY-ANALYSIS.md" "TASK-003B-4"
# → complexity-evaluation.md
```

**End of Day 2 Checkpoint:**
- ✅ Task ID extraction works for all formats
- ✅ Name standardization follows rules
- ✅ Git operations ready

---

### Day 3: Links & Integration (8 hours)

**Morning (4 hours): Phase E - Link Management**

```bash
cat > lib/link_updater.sh <<'EOF'
#!/usr/bin/env bash

update_markdown_links() {
  local file=$1
  local depth_change=${2:-1}

  # Calculate prefix (../ for each level)
  local prefix=""
  for ((i=0; i<depth_change; i++)); do
    prefix="../${prefix}"
  done

  # Backup original
  cp "$file" "${file}.bak"

  # Update links (simple version)
  sed "s|\](\.\.\/|\](${prefix}../|g" "$file" > "${file}.tmp"
  mv "${file}.tmp" "$file"

  rm "${file}.bak"
  log SUCCESS "Updated links in: $file"
}
EOF

# Test link updating
cat > test-links.md <<'EOF'
# Test
[Guide](../docs/guide.md)
[API](../../api/reference.md)
EOF

source lib/core.sh lib/link_updater.sh
update_markdown_links "test-links.md" 1

cat test-links.md
# Should show: [Guide](../../docs/guide.md)

rm test-links.md
```

**Afternoon (4 hours): Integration Testing**

```bash
# Create integration test
cat > tests/integration/test_migration_flow.bats <<'EOF'
#!/usr/bin/env bats

setup() {
  export TEST_DIR=$(mktemp -d)
  cd "$TEST_DIR"
  git init
  git config user.email "test@test.com"
  git config user.name "Test"

  mkdir -p tasks/completed
  echo "# Task" > tasks/completed/TASK-003.md
  echo "# Summary" > TASK-003-IMPLEMENTATION-SUMMARY.md

  git add .
  git commit -m "Initial"
}

teardown() {
  rm -rf "$TEST_DIR"
}

@test "migration creates subfolder" {
  # Copy script to test dir
  cp -r "$BATS_TEST_DIRNAME/../../migrate-completed-tasks.sh" .
  cp -r "$BATS_TEST_DIRNAME/../../lib" .

  run ./migrate-completed-tasks.sh --execute
  [ "$status" -eq 0 ]
  [ -d "tasks/completed/TASK-003" ]
}
EOF

# Run integration test
bats tests/integration/test_migration_flow.bats
```

**End of Day 3 Checkpoint:**
- ✅ Link updating works
- ✅ Integration test passes
- ✅ End-to-end flow verified

---

### Day 4: Testing & Deployment (6 hours)

**Morning (3 hours): Final Testing**

```bash
# Run all tests
bats tests/unit/*.bats
bats tests/integration/*.bats

# Check code quality
shellcheck lib/*.sh migrate-completed-tasks.sh

# Test on real data (dry-run)
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer
./migrate-completed-tasks.sh  # Preview only
```

**Afternoon (3 hours): Deployment**

```bash
# Execute migration
./migrate-completed-tasks.sh --execute --interactive

# Verify results
find . -maxdepth 1 -name "TASK-*.md" | wc -l  # Should be 0
find tasks/completed -mindepth 1 -maxdepth 1 -type d | wc -l  # Should be 54

# Commit
git add -A
git commit -m "feat: Reorganize completed task files (TASK-016)"
git push
```

**End of Day 4 Checkpoint:**
- ✅ All tests passing
- ✅ Deployed to ai-engineer
- ✅ All files organized
- ✅ Git history preserved

---

## Quick Reference

### Most Important Files

```
1. technical-design.md        # Complete architecture and specs
2. implementation-guidelines.md  # Day-by-day workflow and examples
3. design-phase-summary.md    # High-level overview
4. QUICKSTART.md              # This file
```

### Key Commands

```bash
# Development
./migrate-completed-tasks.sh                    # Dry-run preview
./migrate-completed-tasks.sh --execute -i       # Interactive execution
./migrate-completed-tasks.sh --validate-only    # Check state

# Testing
bats tests/unit/*.bats                          # Unit tests
bats tests/integration/*.bats                   # Integration tests
shellcheck lib/*.sh migrate-completed-tasks.sh  # Linting

# Rollback
./migrate-completed-tasks.sh --rollback FILE    # Restore backup
```

### Testing Your Work

After each phase, verify:

```bash
# Phase A: CLI works
./migrate-completed-tasks.sh --help
./migrate-completed-tasks.sh --version

# Phase B: Discovery works
source lib/file_discovery.sh
discover_task_files "ai-engineer"

# Phase C: Backup works
source lib/backup_manager.sh
create_backup
ls -lh .migration-backups/

# Phase D: Git mv works
echo "test" > test.md
git add test.md
git commit -m "Test"
source lib/git_operations.sh
git_move_file "test.md" "tasks/completed/test.md"
git log --follow tasks/completed/test.md  # Should show history

# Phase E: Link update works
echo "[link](../doc.md)" > test.md
source lib/link_updater.sh
update_markdown_links "test.md" 1
cat test.md  # Should show ../../doc.md

# Phase F: Name standardization works
source lib/name_standardizer.sh
standardize_filename "TASK-003-IMPLEMENTATION-SUMMARY.md" "TASK-003"
# → implementation-summary.md
```

---

## Troubleshooting

### "bash: command not found: bats"
```bash
brew install bats-core  # macOS
sudo apt install bats   # Linux
```

### "Permission denied: ./migrate-completed-tasks.sh"
```bash
chmod +x migrate-completed-tasks.sh
```

### "Lock file exists"
```bash
rm -f .migration-lock
```

### "Git mv failed"
```bash
# Ensure clean working tree
git status
git add -A
git commit -m "WIP: Before migration"
```

---

## Success Checklist

### After Implementation
- [ ] Script runs without errors
- [ ] All unit tests passing (71 tests)
- [ ] All integration tests passing (29 tests)
- [ ] Shellcheck clean (no warnings)
- [ ] Dry-run tested on both projects
- [ ] Backup/rollback tested

### After Deployment
- [ ] No task files in root (should be 0)
- [ ] 54 task folders in tasks/completed/
- [ ] Coverage files in coverage/reports/
- [ ] Analysis files in docs/archive/
- [ ] No broken links detected
- [ ] Git history preserved for all files

---

## Need Help?

1. **Read technical design** (`technical-design.md`) for detailed specs
2. **Check implementation guidelines** (`implementation-guidelines.md`) for examples
3. **Review test cases** in `tests/` directories for expected behavior
4. **Test incrementally** - verify each phase before proceeding

---

## Time Estimates

- **Setup:** 30 minutes
- **Day 1 (Foundation):** 6 hours
- **Day 2 (Discovery/Migration):** 7 hours
- **Day 3 (Links/Integration):** 8 hours
- **Day 4 (Testing/Deployment):** 6 hours
- **Total:** 27.5 hours (~4 days)

**With contingency (25%):** 34 hours (~5 days)

---

## Final Notes

**Remember:**
- ✅ Always use `git mv` (preserves history)
- ✅ Create backup before migration
- ✅ Test with dry-run first
- ✅ Validate links after migration
- ✅ Run incrementally (phase by phase)

**Success means:**
- 62 files migrated from root
- Organized into task subfolders
- Git history preserved
- No broken links
- Idempotent (safe to re-run)

**You've got this!** 🚀

---

**Quick Start Version:** 1.0
**Created:** 2025-10-17
**For Task:** TASK-016
**Estimated Completion:** 4-5 days
